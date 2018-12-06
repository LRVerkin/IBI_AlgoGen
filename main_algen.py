


import re
import rstr
import numpy as np

class Individu:
	'''
	un individu est un MDP potentiel
	de 12 caractères dans 0-9A-Z_

	'''
	def __init__(self):
		self.genotype = ""
		self.lengthPW = 12
		self.possibilities = []


	def setGenotype(self,genotype):
		self.genotype = genotype

	def setRandomGenotype(self):
		self.genotype = rstr.xeger(r'[0-9A-Z_]{12}')



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

a= AlgoGen(10)
a.show()
		
		
	

