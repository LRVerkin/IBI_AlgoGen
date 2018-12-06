


import re
import rstr
import random as rd
import numpy as np
import subprocess
import os


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
		child will have genotype of:
		- self from 0 to i_min and i_max to length
		- partner from i_min to i_max
		'''

		child = Individu()
		indices = np.random.randint(0,self.lengthPW-1,size=2)
		i_min,i_max = (min(indices),max(indices))
		insertion = partner.genotype[i_min:min(i_max+1,self.lengthPW)]
		childGeno = self.genotype[:max(0,i_min)]+insertion+self.genotype[min(self.lengthPW,i_max+1):]
		child.setGenotype(childGeno)
		return child

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
			print(ind.genotype)

	def getFitnessPop(self):
		if self.N <100:
			bashCommand = (os.name=='nt')*"ibi_2018-2019_fitness_windows.exe 1"+(os.name!='nt')*"./ibi_2018-2019_fitness_linux 1"
			for ind in self.pop:
				bashCommand += ' '+''.join(ind.genotype)
			
			process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			
			chars = output.decode("utf-8").split('\n')
			chars = chars[0:len(chars)-1]
			fitnesses = []
			for c in chars:
				fitnesses.append(c.split('\t')[-1].split('\r')[0])
		return fitnesses
		


#TESTS
indiv1 = Individu()
indiv1.setRandomGenotype()
print("genotype indiv1 ",indiv1.genotype)

indiv2 = Individu()
indiv2.setRandomGenotype()
indiv2.mutate()
print("genotype indiv2 ",indiv2.genotype)

child = Individu()
child.setGenotype(indiv1.crossover(indiv2).genotype)
print("child is ",child.genotype)

			
		

a= AlgoGen(10)
a.show()
print(a.getFitnessPop())

#bashCommand = "ibi_2018-2019_fitness_windows.exe 1 "




		
		

#fitness = output.decode("utf-8").split('\n')[0].split('\t')[-1]	
#print(fitness)
