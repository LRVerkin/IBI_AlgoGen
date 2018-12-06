


import re
import rstr
import random as rd
import numpy as np
import subprocess


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
			bashCommand = "ibi_2018-2019_fitness_windows.exe 1"
			for ind in self.pop:
				bashCommand += ' '+''.join(ind.genotype)
			process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			chars = output.decode("utf-8").split('\n')
			chars = chars[0:len(chars)-1]
			fitnesses = []
			for c in chars:
				fitnesses.append(float(c.split('\t')[-1].split('\r')[0]))
		print(fitnesses)
		return fitnesses
		
	def rouletteSelection(self):
		fitnesses = self.getFitnessPop()
		probs = [f / sum(fitnesses) for f in fitnesses]
		p1, p2 = np.random.choice(self.pop, 2, p = probs)
		print(p1.genotype, p2.genotype)
		

a= AlgoGen(10)
a.show()
a.rouletteSelection()
#bashCommand = "ibi_2018-2019_fitness_windows.exe 1 "



#TESTS
'''indiv = Individu()
indiv.setRandomGenotype()
print(indiv.genotype)
indiv.mutate()
print(indiv.genotype)'''






		
		

#fitness = output.decode("utf-8").split('\n')[0].split('\t')[-1]	
#print(fitness)
