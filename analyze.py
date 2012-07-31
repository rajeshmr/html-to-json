
class Analyzer:
	def __init__(self,tree):
		self.tree = tree
		for item in tree['children']:
			self.recFunction(item)

	def recFunction(self,inp):
		self.actFunction(inp)
		if isinstance(inp['children'],list):
			for a in inp['children']:
				self.recFunction(a)
		
	
	def actFunction(self,inp): 
		inp.update({"childcount":len(inp['children'])})

		if len(inp['children']) > 1:
			try:
				print inp['name']+"#"+inp['attrs']['id']+'.'+'.'.join(inp['attrs']['class'])+ '-'*len(inp['children'])
			except:
				print inp['name']+'-'*len(inp['children'])
				

	def getResult(self):
		return self.tree


