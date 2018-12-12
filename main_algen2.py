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
				if rd.random() < 0.1:
					self.genotype[i] = '_'
				else:
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
	
	def __init__(self, Nind,proba_crossover,proba_mut, M):
		
		self.N = Nind
		self.M = M
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
				#print('bash ', b,' de ', b*100, ' a ',(b+1)*100)
				maxi = (b+1)*100
				if self.N < maxi :
					maxi = self.N
				#print('maxi : ', maxi, b*100)
				if b*100 != maxi:
					bashCommand = (os.name=='nt')*"ibi_2018-2019_fitness_windows.exe 14"+(os.name!='nt')*"./ibi_2018-2019_fitness_linux 1"
					for ind in self.pop[b*100:maxi]:
						bashCommand += ' '+''.join(ind.genotype)
					process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
					output, error = process.communicate()
					chars = output.decode("utf-8").split('\n')
					chars = chars[0:len(chars)-1]
					fitnesses = []
					for c in chars:
						fitnesses.append(float(c.split('\t')[-1].split('\r')[0]))
					fitnessesAll += fitnesses
			self.fitnesses = fitnessesAll
			return(fitnessesAll)
		self.fitnesses = fitnesses
		return fitnesses
		



	#### DIFFERENT SELECTIONS ####

	def rouletteSelection(self, n_parents):
		'''returns two individuals that will reproduce
		'''
		parents = []
		probs = [f / sum(self.fitnesses) for f in self.fitnesses]
		parents = np.random.choice(self.pop, n_parents, p = probs)
		return parents
		#return p1,p2

	def rankSelection(self, n_parents):
		parents = []
		rank_fitnesses = rankdata(self.fitnesses)
		probs = [f / sum(rank_fitnesses) for f in rank_fitnesses]
		parents = np.random.choice(self.pop, n_parents, p = probs)
		#print parents
		return parents

	#################################


	def reproduction(self):
		'''
		change population to a new generation
		'''
		nb_children = 0
		new_gen = []
		self.fitnesses = self.getFitnessPop()
		parents = self.rouletteSelection(int(self.N/4))
		while (nb_children<self.M):
			parent1,parent2 = np.random.choice(parents, 2)
			child1 = Individu(self.proba_mut)
			child1.setGenotype(parent1.genotype)
			child2 = Individu(self.proba_mut)
			child2.setGenotype(parent2.genotype)

			if rd.random()<self.proba_crossover:
				child1.crossover(child2)

			child1.mutate()
			child2.mutate()
			new_gen.append(child1)
			new_gen.append(child2)
			#new_gen.append(parent1)
			#new_gen.append(parent2)
			nb_children += 2
		while len(new_gen) < len(self.pop):
			new_gen.append(np.random.choice(self.pop, 1)[0])
		self.pop = list(new_gen)
		
	def evolution(self, T):
		t = 0
		mean_fitnesses = []
		max_fitnesses = []
		std_fitnesses = []
		while t < T:
			print('Generation ',t)
			self.reproduction()
			mean_fitnesses.append(np.mean(self.fitnesses))
			max_fitnesses.append(max(self.fitnesses))
			std_fitnesses.append(np.std(self.fitnesses))
			print(''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].genotype))
			if max(self.fitnesses) == 1:
				print('Solution found : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].genotype))
				return ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].genotype)
				break
			t+= 1
		plt.figure()
		plt.plot(range(T), mean_fitnesses)
		plt.plot(range(T), max_fitnesses)
		plt.plot(range(T), std_fitnesses)
		plt.show()
		print('Individu avec le meilleur score : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].genotype))



#TESTS
p_mut = 0.01
p_co = 0.25


a= AlgoGen(200,p_co,p_mut, 200)
#a = AlgoGen(301, 0.001, 0.25,200)
mdp = a.evolution(400000)



