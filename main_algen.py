import re
import rstr
import random as rd
import numpy as np
import subprocess
import os
from scipy.stats import rankdata


class Individu:
	'''
	un individu est un MDP potentiel
	de 12 caractères dans 0-9A-Z_

	'''
	def __init__(self):
		self.genotype = []
		self.lengthPW = 12
		self.possibilities = []


	def setGenotype(self,genotype):
		self.genotype = genotype

	def setRandomGenotype(self):
		self.genotype = list(rstr.xeger(r'[0-9A-Z_]{12}'))



	def mutate(self):
		self.genotype[rd.randint(0,self.lengthPW-1)] = rstr.xeger(r'[0-9A-Z_]')

	def crossover(self,partner):
		'''
		draw 2 indices between 0 and length i_min and i_max
		self will have genotype of:
		- self from 0 to i_min and i_max to length
		- partner from i_min to i_max
		partner will have genotype of :
		- partner from 0 to i_min and i_max to length
		- self from i_min to i_max
		Modifies genotypes of self and partner
		'''
		print(self.genotype)
		print(partner.genotype)
		print("becomes")
		indices = np.random.randint(0,self.lengthPW-1,size=2)
		print(indices)
		i_min,i_max = (min(indices),max(indices))
		insertion_self = partner.genotype[i_min:min(i_max+1,self.lengthPW)]
		insertion_partner = self.genotype[i_min:min(i_max+1,self.lengthPW)]
		futureSelf = self.genotype[:max(0,i_min)]+insertion_self+self.genotype[min(self.lengthPW,i_max+1):]
		futurePartner = partner.genotype[:max(0,i_min)]+insertion_partner+partner.genotype[min(self.lengthPW,i_max+1):]
		self.setGenotype(futureSelf)
		partner.setGenotype(futurePartner)
		print(self.genotype)
		print(partner.genotype)

	# def GenoToPheno(self):

	# def PhenoToGeno(self):



class AlgoGen:
	
	def __init__(self, Nind):
		
		self.N = Nind
		self.pop = np.array([Individu() for n in range(self.N)])
		for individu in self.pop:
			individu.setRandomGenotype()
		
	def show(self):
		for ind in self.pop:
			print("genome is ",ind.genotype)

	def getFitnessPop(self):
		if self.N <100:
			bashCommand = (os.name=='nt')*"ibi_2018-2019_fitness_windows.exe 14"+(os.name!='nt')*"./ibi_2018-2019_fitness_linux 1"
			for ind in self.pop:
				bashCommand += ' '+''.join(ind.genotype)
			process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			chars = output.decode("utf-8").split('\n')
			chars = chars[0:len(chars)-1]
			fitnesses = []
			for c in chars:
				fitnesses.append(float(c.split('\t')[-1].split('\r')[0]))
		print("fitnesses are ",fitnesses)
		return fitnesses
		
	def rouletteSelection(self):
		'''returns two individuals that will reproduce
		'''
		fitnesses = self.getFitnessPop()
		probs = [f / sum(fitnesses) for f in fitnesses]
		p1, p2 = np.random.choice(self.pop, 2, p = probs)
		print("genomes selected for repro ",p1.genotype, p2.genotype)
		return p1,p2

	def reproduction(self):
		'''
		add
		'''
		
		
	def rankSelection(self):
		fitnesses = self.getFitnessPop()
		rank_fitnesses = rankdata(fitnesses)
		probs = [f / sum(rank_fitnesses) for f in rank_fitnesses]
		p1, p2 = np.random.choice(self.pop, 2, p = probs)
		print(p1.genotype, p2.genotype)
		return p1, p2




#TESTS


## test mutation
# indiv2 = Individu()
# indiv2.setRandomGenotype()
# indiv2.mutate()
# print("genotype indiv2 ",indiv2.genotype)

## test crossover function
# indiv1 = Individu()
# indiv1.setRandomGenotype()
# indiv2 = Individu()
# indiv2.setRandomGenotype()

# indiv1.crossover(indiv2)


# a= AlgoGen(10)
# a.show()
# a.rouletteSelection()
