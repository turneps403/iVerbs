import os
from random import shuffle
import json
import copy
import time
import re
from colorclass import Color

from AsciiTable import VerbAsciiTable
from Term import GetLine

#"""
class IrregularVerbs:
	def __init__(self, json_path=None):
		if json_path is None:
			json_path = os.path.join(os.path.dirname(__file__), 'data', 'iVerb.json')
		with open(json_path, 'r') as f:
			self._iverb = json.load(f)

	def iverb(self):
		return copy.deepcopy(self._iverb)

	def __iter__(self):
		iverb = self.iverb()
		shuffle(iverb)
		return iter(iverb) # my little trick

class SimpleTable:
	def __init__(self):
		self.ascii_table = VerbAsciiTable([])

	def draw(self, verb_dict, row_after=0):
		data = [
			list(map(lambda x: verb_dict.get(x).get("verb"), ["infinitive", "past_simple", "past_participle"])),
			list(map(lambda x: verb_dict.get(x).get("ipa"), ["infinitive", "past_simple", "past_participle"]))
		]
		self.ascii_table.table_data = data
		self.ascii_table.replace_draw(row_after)

class Victorina(SimpleTable):
	def __init__(self, *args, **kwargs):
		super(Victorina, self).__init__(*args, **kwargs)
		self.sleep_after_right_answer = kwargs.get("sleep_after_right_answer", 2)
		self.sleep_after_wrong_answer = kwargs.get("sleep_after_wrong_answer", 4)
		self._first_render = 1

	def draw(self, verb_dict_origin, verb_dict_for_ask, expected_answear, score=None, score_points=10):
		super(Victorina, self).draw(verb_dict_for_ask, 0 if self._first_render == 1 else 1)
		self._first_render = 0
		row_after = 0 
		if score is not None:
			print("socre: " + str(score))
			row_after += 1
		print("your answer: ", end='', flush=True)
		answer = GetLine.await_for_enter()
		answer = answer.strip().lower()
		super(Victorina, self).draw(verb_dict_origin, row_after)
		if answer == expected_answear:
			if score is not None:
				score += score_points
				print("socre: " + str(score))
			print("your answer: "+ Color('{autogreen}' + answer +'{/autogreen}'), end='', flush=True)
			if self.sleep_after_right_answer > 0:
				time.sleep(self.sleep_after_right_answer)
		else:
			if score is not None:
				print("socre: " + str(score))
			answer = re.sub('([0-9a-zA-Z])', lambda x: x.group(0) + '\u0336', answer)
			print("your answer: "+ Color('{autored}' + answer + '{/autored} ' + Color('{autogreen}' + expected_answear +'{/autogreen}')), end='', flush=True)
			if self.sleep_after_wrong_answer > 0:
				time.sleep(self.sleep_after_wrong_answer)
		return score

#"""
if __name__=='__main__':
	import sys
	print("hello")
	
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
