import bs4
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from dotdictify import dotdictify

tree=[]
#tree = dotdictify()
soup = BeautifulSoup(open('flip.html'))
path=[]
depth=0
def recFunction(inp,i):
	actFunction(inp,i)
	if type(inp) is bs4.element.Tag:
		i+=1
		for a in inp.children:
			recFunction(a,i)

def actFunction(inp,i):
	if type(inp) is bs4.element.Tag:
		p = '.'.join(getPath(inp)[::-1])
#		print ' '*i,"|"
#		print ' '*i,"+-"+inp.name,p
		buildTree(p,tree,inp)
		path[:]=[]

def getPath(inp):
	if inp.parent is None:
		return path
	else:
		path.append(inp.parent.name)
		getPath(inp.parent)
		return path

def buildTree(p,dic,inp):
	if len(path)<=1:
		tree.append({"name":"[document]","children":[{"name":inp.name,"children":[]}]})
	else:
		if '.' in p:
			k,rk = p.split('.',1)
			if isinstance(dic,list):
				for item in dic:
					if item['name'] == k:
						buildTree(rk,item['children'],inp)
		else:
			for item in dic:
				if item['name'] == p:
					item['children'].append({"name":inp.name,"children":[]})


for a in soup.children:
	recFunction(a,1)

f = open("output.json","w")
f.write(json.dumps(tree,  indent=4))
print "end"