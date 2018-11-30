"""Console game and trainer."""
import argparse
import copy
from random import uniform
import sys

from iVerb.Tables import IrregularVerbs, SimpleTable, VictorinaTable
from iVerb.Term import GetLine, HorizontalOptions

import contextlib # noqa
with contextlib.redirect_stdout(None):
    import pygame


parser = argparse.ArgumentParser()
parser.add_argument("--quiet", action='store_true', help="disable audio")
args = parser.parse_args()
audio_enable = False if args.quiet else True
if audio_enable:
    pygame.mixer.init(channels=1)


def weighted_choice(choices):
    """Sample of weight balanced."""
    total = sum(w for c, w in choices.items())
    r = uniform(0, total)
    upto = 0
    for c, w in choices.items():
        if upto + w >= r:
            return c
        upto += w


choice = HorizontalOptions(["study", "test"]).choice()
if audio_enable:
    print("tap \033[1mshift+a\033[0m to repeat pronounciation and \033[1mesc\033[0m to exit")
if choice == 0:
    stable = SimpleTable()
    audio_channel = None
    verbs = IrregularVerbs().as_list(True)
    i = 0
    while i < len(verbs):
        verb = verbs[i]
        stable.draw(verb)
        if audio_enable:
            if audio_channel is not None:
                audio_channel.stop()
            else:
                audio_channel = pygame.mixer.find_channel(True)
            audio_channel.play(pygame.mixer.Sound(verb["audio"]))
        index_addition = {}
        GetLine.await_for_enter({
            " ": {"break": 1}, 
            "\x1b[C": {"break": 1},
            "\x1b[D": {
                "action": lambda: (i > 0 and index_addition.setdefault("decrease", 1)),
                "break": lambda arg: (i > 0 and arg.setdefault("ret", 1)),
                "continue": lambda arg: (i <= 0 and arg.setdefault("ret", 1)),
            },
            "A": {
                "action": lambda: (
                    audio_enable and audio_channel.stop(),
                    audio_enable and audio_channel.play(pygame.mixer.Sound(verb["audio"]))
                ),
                "continue": lambda arg: (
                    audio_enable and arg.setdefault("ret", 1)
                )
            }
        })
        i += -1 if index_addition.get("decrease", None) else 1

else:
    victorina = VictorinaTable()
    score = 0
    audio_channel = None
    for verb in iter(IrregularVerbs()):
        riddle_verb = copy.deepcopy(verb)
        riddle_target = weighted_choice({"infinitive": 10, "past_simple": 40, "past_participle": 25})
        expected_answer = riddle_verb.get(riddle_target).get("verb")
        lenght = max([len(riddle_verb.get(riddle_target).get("verb")), len(riddle_verb.get(riddle_target).get("ipa"))])
        riddle_placeholder = " " * (lenght // 2) + "\033[1m?\033[0m" + " " * (lenght - 1 - (lenght // 2))
        riddle_verb[riddle_target] = {"verb": riddle_placeholder, "ipa": riddle_placeholder}
        if audio_enable:
            if audio_channel is not None:
                audio_channel.stop()
            else:
                audio_channel = pygame.mixer.find_channel(True)
            audio_channel.play(pygame.mixer.Sound(riddle_verb["audio"]))
        score = victorina.draw(verb, riddle_verb, expected_answer, score, 10, {
            "A": {
                "action": lambda: (
                    audio_enable and audio_channel.stop(),
                    audio_enable and audio_channel.play(pygame.mixer.Sound(riddle_verb["audio"]))
                ),
                "continue": lambda arg: (
                    audio_enable and arg.setdefault("ret", 1)
                )
            }
        })

sys.exit()
