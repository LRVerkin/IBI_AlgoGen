


import re
import rstr
import random as rd
import numpy

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


	def 
	# def GenoToPheno(self):

	# def PhenoToGeno(self):



#TESTS
indiv = Individu()
indiv.setRandomGenotype()
print(indiv.genotype)
indiv.mutate()
print(indiv.genotype)




