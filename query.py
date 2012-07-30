import re

class Query:
	def __init__(self):
#		self.tree=tree
		self.selectors={
			"a":	['link'],
			"div":	['area','region'],
			"embed":['video','movie'],
			"img":	['image','photo','picture'],
			"li":	['list-item'],
			"p":	['paragraph','line'],
			"td":	['column',"element"],
			"tr":	['row']
			}
		self.howMany = re.compile("([0-9]+)(?:st|nd|rd|th)?")
		self.direction = {
			"up":['above','up','before'],
			"down":['below','down','after']
		}
		self.reference = re.compile('\"(.+?)\"')
		self.trans ={}

	def buildQuery(self,query):
		self.trans ={}
		qTokens=query.split(' ')
		print qTokens
		for token in qTokens:
			for tag,pos in self.selectors.iteritems():
				if token in pos:
					self.trans.update({'tag':tag})
			if self.howMany.match(token):
				g = self.howMany.match(token)
				self.trans.update({"howMany":g.group(1)})
			for d,p in self.direction.iteritems():
				if token in p:
					self.trans.update({"direction":d})
			if self.reference.match(token):
				a=self.reference.match(token)
				self.trans.update({"reference":a.group(1)})

	def getTrans(self):
		return self.trans

	def extract(self,tag,direction,howMany,reference):
		pass

if __name__ == '__main__':
	test =[
	'"obama"'
	'3rd "obama"',
	'3 "obama"',
	'4 "tetris" link',
	'"list price" row',
	'2nd column in "leaderboard"',
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

	q=Query()
	for item in test:
		q.buildQuery(item)
		print q.getTrans()