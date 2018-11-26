import sys

from iVerb.Tables import VictorinaTable, SimpleTable



print("hello")

sys.exit()

victorina = Victorina()
score = 0
for verb in iter(IrregularVerbs()):
	riddle_verb = copy.deepcopy(verb)
	# ["infinitive", "past_simple", "past_participle"]
	expected_answer = riddle_verb["past_simple"]["verb"]
	lenght = max([len(riddle_verb["past_simple"]["verb"]), len(riddle_verb["past_simple"]["ipa"])])
	riddle_placeholder = " "*int((lenght - 1)/2) + '?' + " "*int((lenght - 1)/2)
	riddle_verb["past_simple"] = {"verb": riddle_placeholder, "ipa": riddle_placeholder}
	score = victorina.draw(verb, riddle_verb, expected_answer, score)

#stable = SimpleTable()
#for verb in iter(IrregularVerbs()):
#	stable.draw(verb)
#	GetLine.await_for_enter({" ": {"break": 1}, "\x1b[C": {"break": 1}})

sys.exit()
data = [
	['Row one column one', 'Row one column two', 'eeee'],
	['Row two column one', 'Row two column two', 'fooop'],
]
table = VerbAsciiTable(data)
table.replace_draw()

print("Score: 0")
print("What: ", end='', flush=True)
answer = GetLine.await_for_enter()
answer = answer.strip().lower()
if answer == "foobar":
	table.replace_draw(1)
	print("Score: 10")
	print("What: FOOBAR", end='', flush=True)
	GetLine.await_for_enter({" ": {"break": 1}})
else:
	table.replace_draw(1)
	print("Score: -10")
	
	print("What: "+answer[0:-1]+" X", end='', flush=True)
	GetLine.await_for_enter({" ": {"break": 1}})

data[0][0]="FFFFF"
table.replace_draw(1)
GetLine.await_for_enter({" ": {"break": 1}})	
