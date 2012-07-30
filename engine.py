import json,re

class Engine:

	def getText(self,keyword):
		pass

	def searchDict(self,tree):
		for item in tree['children']:
			self.searchDictRec(item['children'])

	def searchDictRec(self,child):
		self.searchDictAct(child)
		if isinstance(child,list):
			for item in child:
				self.searchDictRec(item['children'])

	def searchDictAct(self,child,keyword="price"):
		for item in child:
			if item['text']:
				if(re.search(keyword,item['text'])):
					print item['text']

if __name__ == '__main__':
	tree=json.loads(open('output.json').read())
	e = Engine()
	e.searchDict(tree)
