import re
import rstr
import random as rd
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
from scipy.stats import rankdata


class Individu:
	'''
	un individu est un MDP potentiel
	de 12 caractères dans 0-9A-Z_

	'''
	def __init__(self,proba_mut):
		self.genotype = []
		self.lengthPW = 12
		self.possibilities = []
		self.proba_mut = proba_mut


	def setGenotype(self,genotype):
		self.genotype = genotype

	def setRandomGenotype(self):
		self.genotype = list(rstr.xeger(r'[0-9A-Z_]{12}'))



	##### CHANGE INDIVIDUAL #######

	def mutate(self):
		for i in range(self.lengthPW):
			if rd.random()<self.proba_mut:
				self.genotype[i] = rstr.xeger(r'[0-9A-Z_]')

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
		indices = np.random.randint(0,self.lengthPW-1,size=2)
		i_min,i_max = (min(indices),max(indices))
		insertion_self = partner.genotype[i_min:min(i_max+1,self.lengthPW)]
		insertion_partner = self.genotype[i_min:min(i_max+1,self.lengthPW)]
		futureSelf = self.genotype[:max(0,i_min)]+insertion_self+self.genotype[min(self.lengthPW,i_max+1):]
		futurePartner = partner.genotype[:max(0,i_min)]+insertion_partner+partner.genotype[min(self.lengthPW,i_max+1):]
		self.setGenotype(futureSelf)
		partner.setGenotype(futurePartner)


	#######################

	# def GenoToPheno(self):

	# def PhenoToGeno(self):



class AlgoGen:
	
	def __init__(self, Nind,proba_crossover,proba_mut):
		
		self.N = Nind
		self.proba_crossover = proba_crossover
		self.proba_mut = proba_mut
		self.pop = np.array([Individu(proba_mut) for n in range(self.N)])
		for individu in self.pop:
			individu.setRandomGenotype()
		

	def show(self):
		for ind in self.pop:
			print("genome is ",''.join(ind.genotype))


	def getFitnessPop(self):
		if self.N <=100:
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
		else:
			fitnessesAll = []
			nbBash = int(self.N /100)
			#print('nbBash à faire : ', nbBash)
			for b in range(nbBash+1):
				maxi = (b+1)*100
				if self.N-1 < maxi :
					maxi = self.N-1
				#print(' De ', b*100+1, ' à ', (b+1)*100)
				
				bashCommand = (os.name=='nt')*"ibi_2018-2019_fitness_windows.exe 14"+(os.name!='nt')*"./ibi_2018-2019_fitness_linux 1"
				for ind in self.pop[b*100:(b+1)*100]:
					bashCommand += ' '+''.join(ind.genotype)
				process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
				output, error = process.communicate()
				chars = output.decode("utf-8").split('\n')
				chars = chars[0:len(chars)-1]
				fitnesses = []
				for c in chars:
					fitnesses.append(float(c.split('\t')[-1].split('\r')[0]))
				fitnessesAll += fitnesses
			#print(fitnessesAll)
			self.fitnesses = fitnessesAll
			return(fitnessesAll)
			
					

		self.fitnesses = fitnesses
		return fitnesses
		



	#### DIFFERENT SELECTIONS ####

	def rouletteSelection(self):
		'''returns two individuals that will reproduce
		'''
		
		probs = [f / sum(self.fitnesses) for f in self.fitnesses]
		p1, p2 = np.random.choice(self.pop, 2, p = probs)
		return p1,p2

	def rankSelection(self):
		#fitnesses = self.getFitnessPop()
		rank_fitnesses = rankdata(self.fitnesses)
		probs = [f / sum(rank_fitnesses) for f in rank_fitnesses]
		p1, p2 = np.random.choice(self.pop, 2, p = probs)
		return p1, p2

	#################################


	def reproduction(self):
		'''
		change population to a new generation
		'''
		nb_children = 0
		new_gen = []
		self.fitnesses = self.getFitnessPop()
		while (nb_children<len(self.pop)):

			parent1,parent2 = self.rouletteSelection()
			child1 = Individu(self.proba_mut)
			child1.setGenotype(parent1.genotype)
			child2 = Individu(self.proba_mut)
			child2.setGenotype(parent2.genotype)

			if (rd.random()<self.proba_crossover):
				child1.crossover(child2)

			child1.mutate()
			child2.mutate()
			new_gen.append(child1)
			new_gen.append(child2)
			#new_gen.append(parent1)
			#new_gen.append(parent2)
			nb_children += 2


		self.pop = list(new_gen)
		
	def evolution(self, T):
		t = 0
		mean_fitnesses = []
		max_fitnesses = []
		while t < T:
			print('Generation ',t)
			self.reproduction()
			mean_fitnesses.append(np.mean(self.fitnesses))
			max_fitnesses.append(max(self.fitnesses))
			if max(self.fitnesses) == 1:
				#print('Solution found : ' ''.join(self.pop[self.fitnesses.index(max(self.fitnesses)].genotype)))
				break
			t+= 1
		plt.figure()
		plt.plot(range(T), mean_fitnesses)
		plt.plot(range(T), max_fitnesses)
		plt.show()
		print('Individu avec les meilleur score : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].genotype))



#TESTS
p_mut = 0.001
p_co = 0.2


a= AlgoGen(208,p_co,p_mut)
a.evolution(200)


