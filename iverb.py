import sys
import copy
from random import uniform

from iVerb.Tables import IrregularVerbs, VictorinaTable, SimpleTable
from iVerb.Term import GetLine, HorizontalOptions

def weighted_choice(choices):
	total = sum(w for c, w in choices.items())
	r = uniform(0, total)
	upto = 0
	for c, w in choices.items():
		if upto + w >= r:
			return c
		upto += w

choice = HorizontalOptions(["study", "game"]).choice()
if choice == 0:
	stable = SimpleTable()
	for verb in iter(IrregularVerbs()):
		stable.draw(verb)
		GetLine.await_for_enter({" ": {"break": 1}, "\x1b[C": {"break": 1}})
else:
	victorina = VictorinaTable()
	score = 0
	for verb in iter(IrregularVerbs()):
		riddle_verb = copy.deepcopy(verb)
		riddle_target = weighted_choice({"infinitive": 10, "past_simple": 40, "past_participle": 25})
		expected_answer = riddle_verb.get(riddle_target).get("verb")
		lenght = max([len(riddle_verb.get(riddle_target).get("verb")), len(riddle_verb.get(riddle_target).get("ipa"))])
		riddle_placeholder = " "*int((lenght - 1)/2) + '?' + " "*int((lenght - 1)/2)
		riddle_verb["past_simple"] = {"verb": riddle_placeholder, "ipa": riddle_placeholder}
		score = victorina.draw(verb, riddle_verb, expected_answer, score)

sys.exit()
