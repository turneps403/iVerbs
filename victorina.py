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
	def __init__(self, jdata):
		self.jdata = jdata

	def draw(self, row_after=0):
		data = [
			
		]
		table = VerbAsciiTable(self.jdata)
		table.replace_draw(row_after)

#"""
if __name__=='__main__':
	import sys
	print("hello")

	SimpleTable()

	sys.exit()
	for ee in iter(SimpleVerbTables()):
		print(ee["infinitive"]["verb"])
	
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
