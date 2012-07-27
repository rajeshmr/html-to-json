import bs4
from bs4 import BeautifulSoup
import json
from collections import defaultdict

class HtmlTree:
	output = open("output.json","w")
	tree=[]
	path=[]
	depth=0
	
	def recFunction(self,inp,i):
		self.actFunction(inp,i)
		if type(inp) is bs4.element.Tag:
			i+=1
			for a in inp.children:
				self.recFunction(a,i)

	def actFunction(self,inp,i):
		if type(inp) is bs4.element.Tag:
			p = '~'.join(self.getPath(inp)[::-1])
			self.buildTree(p,self.tree,inp)
			print len(self.path)
			self.path[:]=[]

	def getPath(self,inp):
		if inp.parent is None:
			return self.path
		else:
			self.path.append(inp.parent.name)
			self.getPath(inp.parent)
			return self.path

	def buildTree(self,p,dic,inp):
		if len(self.path)<=1:
			self.tree.append({"name":"[document]","children":[{"name":inp.name,"children":[]}]})
		else:
			if '~' in p:
				k,rk = p.split('~',1)
				item = (itm for itm in dic if itm['name'] == k).next()
				self.buildTree(rk,item['children'],inp)
			else:
				item = (itm for itm in dic if itm['name'] == p).next()
				item['children'].append({"name":inp.name,
										"children":[],
										"text":inp.find(text=True).strip() if (inp.find(text=True) != None) else None,
										"attrs":dict(inp.__dict__['attrs']),
										})

	def getTree(self):
		return self.tree[0]

	def writeOutput(self):
		self.output.write(json.dumps(h.getTree(),  indent=4))

if __name__ == '__main__':
	h = HtmlTree()
	soup = BeautifulSoup(open('flip.html'))
	for a in soup.children:
		h.recFunction(a,1)
	h.writeOutput()
	print "end"
