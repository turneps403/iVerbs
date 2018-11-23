import os
from random import shuffle
import json
import copy

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

#"""
if __name__=='__main__':
	import sys
	print("hello")

	stable = SimpleTable()
	for verb in iter(IrregularVerbs()):
		stable.draw(verb)
		GetLine.await_for_enter({" ": {"break": 1}, "\x1b[C": {"break": 1}})
	
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
