import random, math



class Agent:

	generation = 0
	gender = "F"

	genetic_father =""
	genetic_mother = ""
	cultural_father = ""
	cultural_mother = ""
	
	cultural_sons = []
	cultural_daughters = []
	
	married_to = ""
	
	genes = []
	
	name = ""
	
	def __init__(self, generation, gender, genetic_father, genetic_mother, cultural_father, cultural_mother, genes=None):
		
		global pop
		
		self.name = str(generation)+"_"+ str(len(pop))+ "_" + str(random.uniform(0,1000000))
			
		self.genetic_father =genetic_father
		self.genetic_mother = genetic_mother
		self.cultural_father = cultural_father
		self.cultural_mother = cultural_mother
		
		self.generation = generation
		self.gender = gender
	
		if(genes==None):
			self.genes = self.newGene(pop[self.genetic_father], pop[self.genetic_mother])
		else:
			self.genes = genes
	
	def newGene(self,a,b):
		ag = a.getGenes()
		bg = b.getGenes()
		c = [random.choice([0,1]) for x in ag]
		return [ [ag[i],bg[i]][c[i]] for i in range(len(ag))]
	
	def getGenes(self):
		return self.genes
		
	def getName(self):
		return self.name
		
	def getGeneration(self):
		return self.generation
		
	def getHusband(self):
		return self.married_to
		
	def getWife(self):
		return self.married_to
		
	def marry(self, name):
		self.married_to = name
	
	def getGender(self):
		return self.gender
		
	def getCulturalMotherName(self):
		return self.cultural_mother
	
	def addChild(self,c):
		if c.getGender()=="M":
			self.cultural_sons.append(c.getName())
		else:
			self.cultural_daughters.append(c.getName())
			
	def getCulturalSonsName(self):
		return self.cultural_sons
		
	def getCulturalDaughtersName(self):
		return self.cultural_daughters
		
		
	def getMarryableCousin(self):
		# marriage between man and his mother's brother's daughter (matrilineal)
		mother = pop[self.getCulturalMotherName()]
		grandmother = pop[mother.getCulturalMotherName()]
		mothers_brothers = [pop[k] for k in grandmother.getCulturalSonsName()]
		
		mothers_brothers_daughters = []
		for mb in mothers_brothers:
			mbd = mb.getCulturalDaughtersName()
			for x in mbd:
				if pop[x].getHusband()=="":
					mothers_brothers_daughters.append(x)

		# return agent
		if len(mothers_brothers_daughters)>0:
			return pop[random.choice(mothers_brothers_daughters)]
		else:
			return None
		
		

def getRandomNonSiblingMale(f):

	chosen = random.choice([k for k in pop.keys() if pop[k].getGender()=="M" and pop[k].getCulturalMotherName() != f.getCulturalMotherName()])
	
	return pop[chosen]
			


def marry(gen):
	keys = pop.keys()
	for k in keys:
		a = pop[k]
		if a.getGender()=="M" and a.getGeneration()==gen:

			w = a.getMarryableCousin()
			if w!=None:
				#print "MARRY", a.getName(), w.getName()
				a.marry(w.getName())
				w.marry(a.getName())
			
def marry_random(gen):
	px = [pop[k] for k in pop.keys() if pop[k].getGeneration()==gen]
	females = [a for a in px if a.getGender()=="F" and a.getHusband()==""]
	males = [a for a in px if a.getGender()=="M" and a.getWife()==""]
	
	random.shuffle(females)
	
	for i in range(min([len(females), len(males)])):
		females[i].marry(males[i].getName())
		males[i].marry(females[i].getName())
	
	
def reproduce(gen):
	# each female has two children, one son and one daughter
	keys = pop.keys()
	for k in keys:
		a = pop[k]
		if a.gender=="F" and a.getGeneration()==gen and a.getHusband()!="":
			h = pop[a.getHusband()]			
			for gender in ["F","M"]:
				geneticFather = pop[a.getHusband()]
				if random.random() < parental_uncertainty:
					geneticFather = getRandomNonSiblingMale(a)
			
				child = Agent(	a.getGeneration()+1, 
									gender, 
									geneticFather.getName(),
									a.getName(),
									h.getName(),
									a.getName(),
									None )
				pop[child.getName()] = child
				a.addChild(child)
				h.addChild(child)
				

def death(currentGen):
	keys = pop.keys()
	for k in keys:
		if pop[k].getGeneration<currentGen:
			del pop[k]
	
def getGeneDiversity(pop, gen):

	#genes = [pop[k].getGenes() for k in pop.keys() if pop[k].getGeneration()==gen]
	genes = [pop[k].getGenes() for k in pop.keys() if pop[k].getGeneration()==gen]
	
	alleles = {}

	for g in genes:
		print len(genes),str(g)
		try:
			alleles[str(g)] +=1
		except:
			alleles[str(g)] =1
			
	return 1 - sum([math.pow(x/float(len(genes)),2) for x in alleles.values()])