# TODO: mutation

# Jeremy Kendal
#  monogamy + polygeny (John Hartyg, paternity certainty)

import random, math, copy

pop_size = 20
parental_uncertainty = 0.05

# The population is represented as a dictionary of names (keys) and agents (values). 
#  To get an agent by name, use pop[name]

pop = {}


# Agent is a class to represent an individual agent
#  Agents have names (unique in history) to identify them
#  A gender (M or F)
#  genetic parents
#  cultural parents (which might differ from genetic parents
#  cultural children
#  Married to someone (up to one person)
#  genetics (list of 1s and 0s)
#  Various methods to get information

class Agent:

	
	def __init__(self, generation, gender, genetic_father, genetic_mother, cultural_father, cultural_mother, genes=None):
		
		global pop
		
		self.name = str(generation)+"_"+ str(len(pop))+ "_" + str(random.uniform(0,1000000))
			
		self.genetic_father =genetic_father
		self.genetic_mother = genetic_mother
		self.cultural_father = cultural_father
		self.cultural_mother = cultural_mother
		
		self.cultural_sons = []
		self.cultural_daughters = []
		
		self.married_to=""
		
		self.generation = generation
		self.gender = gender
		
		if(genes== -1):
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
		
####################
# Helper functions #
####################

# Given a female agent, pick a random cousin to marry
def getRandomNonSiblingMale(f):

	candidates = [k for k in pop.keys() if pop[k].getGender()=="M" and pop[k].getCulturalMotherName() != f.getCulturalMotherName()]
	
	if len(candidates)>0:
		return pop[random.choice(candidates)]
	
	return None
			

#  Marry cousins:
def marry_cousin(gen):
	keys = pop.keys()
	for k in keys:
		a = pop[k]
		if a.getGender()=="M" and a.getGeneration()==gen:

			w = a.getMarryableCousin()
			if w!=None:
				#print "MARRY", a.getName(), w.getName()
				a.marry(w.getName())
				w.marry(a.getName())
	return "marry_cousin"


# Marry whole population at random			
def marry_random(gen):
	px = [pop[k] for k in pop.keys() if pop[k].getGeneration()==gen]
	females = [a for a in px if a.getGender()=="F" and a.getHusband()==""]
	males = [a for a in px if a.getGender()=="M" and a.getWife()==""]
	# Marry in a random order
	random.shuffle(females)
	
	# In case there are different number of males and females, 
	#  marry as many as possible
	for i in range(min([len(females), len(males)])):
		females[i].marry(males[i].getName())
		males[i].marry(females[i].getName())
	return "marry_random"
	
# Reproduce, with the possibility of the father not being the husband
def reproduce(gen):
	# each female has two children, one son and one daughter
	
	keys = copy.deepcopy(pop.keys())
	
	childrenNotFromHusbands = 0
	
	for k in keys:
		
		a = pop[k]
		# Only married females in the current generation reproduce
		if a.gender=="F" and a.getGeneration()==gen:
			if  a.getHusband()!="":
				
				h = pop[a.getHusband()]			
				for gender in ["F","M"]:
					# By default, the father is the husband
					geneticFather = pop[a.getHusband()]
					# With a small probability, the father is a random non-sibling male
					#  (of the same generation, not a brother)
					if random.random() < parental_uncertainty:
						random_male = getRandomNonSiblingMale(a)
						if random_male !=None:
							geneticFather = random_male
				
					# New child
					
					child = Agent(	    a.getGeneration()+1,  # generation
										gender,  
										geneticFather.getName(),  # genetic father
										a.getName(),  # genetic mother
										h.getName(),  # cultural father is the husband
										a.getName(),  # cultural mother == genetic mother
										-1 )        # genes (assigned in Agent class)
					# Register the child
					#  as belonging to the cultural parents
					pop[child.getName()] = child
					a.addChild(child)
					h.addChild(child)
	return childrenNotFromHusbands

# Remove generations from the population
def death(currentGen):
	keys = pop.keys()
	for k in keys:
		if pop[k].getGeneration()<currentGen:
			del pop[k]
	
def getGeneDiversity(pop, gen):

	#genes = [pop[k].getGenes() for k in pop.keys() if pop[k].getGeneration()==gen]
	genes = [pop[k].getGenes() for k in pop.keys() if pop[k].getGeneration()==gen]
	
	alleles = {}

	for g in genes:
		#print len(genes),str(g)
		try:
			alleles[str(g)] +=1
		except:
			alleles[str(g)] =1
			
	return 1 - sum([math.pow(x/float(len(genes)),2) for x in alleles.values()])

def numberOfMarriedCouples(pop,gen):
	return(sum([v.getHusband!="" for v in pop.values() if v.getGeneration()==gen]))

###########################		


def run(runNumber, marriageRule, pops, pu):
	
	out = ""
	
	global pop_size
	pop_size = pops
	global parental_uncertainty
	parental_uncertainty = pu
	# initialise population
	global pop
	pop = {}
	for i in range(pop_size):
		# unique genes for each agent
		g = [0 for x in range(pop_size)]
		g[i] = 1
	
		gender = "F"
		if (i % 2)==0:
			gender = "M"
	
		# generation, gender, genetic_father, genetic_mother, cultural_father, cultural_mother, genes
		a = Agent( 0, gender , None, None, None, None, genes=g)
	
		# add to population
		pop[a.getName()] = a


	# The first two generations mate randomly
	marry_random(0)
	reproduce(0)

	out += ",".join([str(x) for x in[runNumber,"NA", 0,getGeneDiversity(pop, 0),0,pop_size, parental_uncertainty,numberOfMarriedCouples(pop,0)]]) + "\n"
	marry_random(1)
	reproduce(1)

	out += ",".join([str(x) for x in [runNumber,"NA", 0,getGeneDiversity(pop, 1),0,pop_size, parental_uncertainty,numberOfMarriedCouples(pop,1)]])+ "\n"


	#############

	# Run generations
	gen = 1
	geneDiversity = 1.0
	#while geneDiversity>0.5 and gen < 1000:
	for i in range(1000):
		gen += 1

		# Marry people
		ruleName = marriageRule(gen)
		# reproduce
		childrenNotFromHusbands = reproduce(gen)
		# Kill off older generations?
		if gen > 4:
			death(gen-4)
	
		geneDiversity = getGeneDiversity(pop, gen)
	
		out += ",".join([str(x) for x in [runNumber, ruleName,gen,geneDiversity,childrenNotFromHusbands,pop_size, parental_uncertainty,numberOfMarriedCouples(pop,gen)]])+ "\n"
	return out

out =  "run,marriageRule,gen,diversity,childrenNotFromHusbands,pop_size,parental_uncertainty,numberOfMarriedCouples\n"	

for pu in [0,0.01,0.05,0.1]:
	print "Uncertainty:",pu
	for r in range(10):
		print "run",r
		for rule in [marry_cousin,marry_random]:
			out += run(r, rule, 100, pu)
		
o = open("res.csv",'w')
o.write(out)
o.close()