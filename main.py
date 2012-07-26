import bs4
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from dotdictify import dotdictify

#tree=defaultdict(list)
tree = dotdictify()
soup = BeautifulSoup(open('test.html'))
path=[]
def recFunction(inp,i):
	actFunction(inp,i)
	if type(inp) is bs4.element.Tag:
		i+=1
		for a in inp.children:
			recFunction(a,i)

def actFunction(inp,i):
	if type(inp) is bs4.element.Tag:
		print ' '*i,"|"
		print ' '*i,"+-"+inp.name
		p = '.'.join(getPath(inp)[::-1])+".children"
#		tree[p].append({inp.name:inp.string})
		print path
		try:
			tree[p].append([{"name":inp.name,"children":[],"text":inp.string}])
		except:
			tree[p] = [{"name":inp.name,"children":[],"text":inp.string}]
		path[:]=[]

def getPath(inp):
	if inp.parent is None:
		return path
	else:
		path.append(inp.parent.name)
		getPath(inp.parent)
		return path

def saveText(path,text):
	for a in path:
		tree[a]

for a in soup.children:
	recFunction(a,1)

print json.dumps(tree)