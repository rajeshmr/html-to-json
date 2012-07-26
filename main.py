import bs4
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from dotdictify import dotdictify

tree={}
#tree = dotdictify()
soup = BeautifulSoup(open('test.html'))
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
		print ' '*i,"|"
		print ' '*i,"+-"+inp.name,p
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
	if '.' in p:
		k, rk = p.split('.',1)
		try:
			buildTree(rk,dic[k],inp)
		except:
			for item in dic['children']:
				if item['name'] == rk:
					item['children'].append({"name":inp.name,"children":[]})
			#dic['children'].append({"name":inp.name,"children":[]})
	else:
		if len(path)<=1:
			dic[p]={"name":inp.name,"children":[]}
		else:
			dic['children'].append({"name":inp.name,"children":[]})



	
for a in soup.children:
	recFunction(a,1)

print json.dumps(tree,  indent=4)