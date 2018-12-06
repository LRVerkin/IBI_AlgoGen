


import re
import rstr

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







