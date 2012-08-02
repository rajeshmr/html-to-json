import re
import shlex
import nltk
from pprint import pprint

class Query:
	def __init__(self):
#		self.tree=tree
		self.selectors={
			"a":	['link','links'],
			"div":	['area','region'],
			"embed":['video','movie'],
			"img":	['image','photo','picture','images','photos','pictures'],
			"li":	['list-item','list-items'],
			"p":	['paragraph','line','paragraphs','lines'],
			"td":	['column',"element",'columns',"elements"],
			"tr":	['row','rows']
			}
		self.whichOne = re.compile("([0-9]+)[st|nd|rd|th]")
		self.howMany = re.compile("([0-9]+)$")
		self.direction = {
			"up":['above','up','before'],
			"down":['below','down','after'],
			"contain":['in','inside','containing']
		}
		self.reference = re.compile('.*\"(.+?)\".*')
		self.trans ={}
		self.parent = None
		self.dirs = [item for sublist in self.direction.values() for item in sublist]
		print self.dirs

	def buildQuery(self,query):
		"""
			CC  coordinating conjunction
			RB Adverb
			IN Preposition
			NN Noun
			JJ Adjective
			VB Verb
		"""

		self.trans ={}
		qTokens=nltk.pos_tag(shlex.split(query))
		for token in qTokens:
			if token in self.dirs:
				self.parent = token
				self.trans.update({token:{}})
			if self.parent is not None:
				self.trans.update(self.typeIdentifier(token))
			else:
				self.trans[self.parent].update(self.typeIdentifier(token))

	def typeIdentifier(self,token):
		for tag,pos in self.selectors.iteritems():
			if token in pos:
				return {'tag':tag}
		if self.howMany.match(token):
			g = self.howMany.match(token)
			return {"howMany":g.group(1)}
		if self.whichOne.match(token):
			w=self.whichOne.match(token)
			return {"whichOne":w.group(1)}
		for d,p in self.direction.iteritems():
			if token in p:
				return {"direction":d}
		if self.reference.match(token):
			a=self.reference.match(token)
			return {"reference":a.group(1)}
		

	def getTrans(self):
		return self.trans

	def extract(self,tag,direction,howMany,reference):
		pass

if __name__ == '__main__':
	test =[
		'"obama"',#
		'3rd "obama"',#
		'3 "obama"',#
		'4 "tetris" link',#
		'"list price" row',#
		'2nd column in "leaderboard"',#
		'"best score" column in "leaderboard"',
		'2nd column in "list price" row',
		'links before 1st "research" link',
		'links after 1st "crunchbase" link',
		'1st 10 links after "latest news"',
		'area containing "all entertainment"',
		'links in "just in" area',
		'links inside area containing "all entertainment"',
		'1st 4 links after "video" in area containing "all entertainment"'
	]
	"""
	{
		"whichOne":1,
		"howMany":4,
		"tag":"a",
		"after":{
			"tag":"embed",
			"in":{
				"tag":"div",
				"direction":"contain",
				"keyword":"all entertainment"
			}
		}
	}

	"""

	q=Query()
	for item in test:
		q.buildQuery(item)
		print item
		print pprint(q.getTrans())
