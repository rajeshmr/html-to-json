import bs4
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from analyze import Analyzer

class HtmlTree:
	output = open("output.json","w")
	tree=[]
	path=[]
	depth=2
	ignore=['script','style']
	
	def recFunction(self,inp,i):
		self.actFunction(inp,i)
		if type(inp) is bs4.element.Tag:
			i+=1
			for a in inp.children:
				self.recFunction(a,i)

	def actFunction(self,inp,i):
		if type(inp) is bs4.element.Tag:
			p = '~'.join(self.getPath(inp)[::-1])
			self.buildTree(p,self.tree,inp,i)
			self.path[:]=[]

	def getPath(self,inp):
		if inp.parent is None:
			return self.path
		else:
			self.path.append(inp.parent.name)
			self.getPath(inp.parent)
			return self.path

	def buildTree(self,p,dic,inp,i):
		if len(self.path)<=1:
			self.tree.append({"name":"[document]","depth":1,"level":0,"children":[{"name":inp.name,"depth":2,"level":1,"children":[]}]})
		else:
			if '~' in p:
				k,rk = p.split('~',1)
				item = (itm for itm in dic if itm['name'] == k).next()
				self.buildTree(rk,item['children'],inp,i)
			else:
				if inp.name == 'td':
					item = (itm for itm in reversed(dic) if itm['name'] == p ).next()
				else:
					item = (itm for itm in dic if itm['name'] == p ).next()
				if inp.name not in self.ignore:
					self.depth+=1
					item['children'].append({ 
											"id":self.depth,
											"name":inp.name,
											"children":[],
											"text":inp.find(text=True).strip().lower() if (inp.find(text=True) != None) else None,
											"attrs":dict(inp.__dict__['attrs']),
											"depth":i,
											"path":' > '.join(self.path[::-1])
										})

	def getTree(self):
		return self.tree[0]

	def writeOutput(self):
		self.output.write(json.dumps(h.getTree(), indent=4))

if __name__ == '__main__':
	h = HtmlTree()
	soup = BeautifulSoup(open('inputs/test.html'))
	for a in soup.children:
		h.recFunction(a,1)
	h.writeOutput()
	tree = h.getTree()
	a = Analyzer(tree)
	#print a.getResult()
	print "end"
