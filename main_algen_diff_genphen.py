import re
import rstr
import random as rd
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
from scipy.stats import rankdata
import string
import sys
import math

class Individu:
	'''
	un individu est un MDP potentiel
	de 12 caractères dans 0-9A-Z_

	'''
	def __init__(self,proba_mut):
		self.genotype = []
		self.phenotype = []
		self.lengthPW = 12
		self.possibilities = list(string.ascii_uppercase)+[str(i) for i in range(10)]+['_']
		self.proba_mut = proba_mut



	def setPhenotype(self,phenotype):
		self.phenotype = list(phenotype)
		self.PhenoToGeno()


	def setRandomPhenotype(self):
		self.phenotype = list(rstr.xeger(r'[0-9A-Z_]{12}'))
		self.PhenoToGeno()

	def setGenotype(self,genotype):
		self.genotype = list(genotype)
		self.GenoToPheno()



	##### CHANGE GENOTYPE OF INDIVIDUAL #######

	def mutate(self):

		if rd.random()<self.proba_mut:
			i1,i2 = np.random.randint(0,self.lengthPW-1,size=2)
			self.genotype[i1],self.genotype[i2] = self.genotype[i2],self.genotype[i1]
			self.GenoToPheno()
		for i in range(len(self.genotype)):
			if rd.random()<self.proba_mut:
				self.genotype[i] = int((i+np.random.normal(loc=0,scale=12))%len(self.possibilities))
		


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

	def GenoToPheno(self):
		self.phenotype = []
		for elem in self.genotype:
			#print(math.floor(elem))
			self.phenotype.append(self.possibilities[elem])


	def PhenoToGeno(self):
		self.genotype = []
		for elem in self.phenotype:
			self.genotype.append(self.possibilities.index(elem))


class AlgoGen:
	
	def __init__(self, Nind, M, proba_crossover,proba_mut):
		
		self.N = Nind
		self.M = M
		self.proba_crossover = proba_crossover
		self.proba_mut = proba_mut
		self.pop = np.array([Individu(proba_mut) for n in range(self.N)])
		for individu in self.pop:
			individu.setRandomPhenotype()
		

	def show(self):
		for ind in self.pop:
			print("genome is ",''.join(ind.phenotype))


	def getFitnessPop(self):
		if self.N <=100:
			bashCommand = (os.name=='nt')*"ibi_2018-2019_fitness_windows.exe 14"+(os.name!='nt')*"./ibi_2018-2019_fitness_linux 1"
			for ind in self.pop:
				ind.PhenoToGeno()
				bashCommand += ' '+''.join(ind.phenotype)
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
						ind.PhenoToGeno()
						bashCommand += ' '+''.join(ind.phenotype)
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
			
					

		self.fitnesses = fitnesses
		return fitnesses
		



	#### DIFFERENT SELECTIONS ####

	def rouletteSelection(self, n_parents):
		'''returns two individuals that will reproduce
		'''
		parents = []
		probs = [f / sum(self.fitnesses) for f in self.fitnesses]
		parents_index = np.random.choice(list(range(len(self.pop))), n_parents, p = probs)
		#print(parents_index)
		return parents_index
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
		
		self.fitnesses = self.getFitnessPop()
		parents_index = self.rouletteSelection(100)
		parents = [self.pop[i] for i in parents_index]
		parents_fitnesses = [self.fitnesses[i] for i in parents_index]
		print("mean fitness of parents is ",np.mean(parents_fitnesses)," while mean fitness is ",np.mean(self.fitnesses))
		#parents = self.rankSelection(100)
		new_gen = []
		#best = parents[0].genotype
		while (nb_children<self.N):
			
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
		#new_gen[0].genotype = best
		self.pop = list(new_gen)
		
	def evolution(self, T):
		t = 0
		mean_fitnesses = []
		max_fitnesses = []
		std_fitnesses = []
		self.getFitnessPop()
		mean_fitnesses.append(np.mean(self.fitnesses))
		max_fitnesses.append(max(self.fitnesses))
		std_fitnesses.append(np.std(self.fitnesses))
		f = open("best_mdp.txt", "w")
		while t < T-1:
			print('Generation ',t)
			print(''.join(self.pop[np.argmax(self.fitnesses)].phenotype), max(self.fitnesses), np.argmax(self.fitnesses))
			if max(self.fitnesses) == 1:
				print('Solution found : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype))
				f.write('The one : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype)+'\n')
				return ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype)
				break
			if max(self.fitnesses) > 0.7:
				print('presque !!!!!!!!!!!!!!!!!!!!!!!!!!!', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype))
				f.write(''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype)+'\n')
			
			self.reproduction()
			
			mean_fitnesses.append(np.mean(self.fitnesses))
			max_fitnesses.append(max(self.fitnesses))
			std_fitnesses.append(np.std(self.fitnesses))
			t+= 1
		plt.figure()
		plt.plot(range(T), mean_fitnesses)
		plt.plot(range(T), max_fitnesses)
		plt.plot(range(T), std_fitnesses)
		plt.show()
		f.close()
		print('Individu avec le meilleur score : ', ''.join(self.pop[self.fitnesses.index(max(self.fitnesses))].phenotype))



#TESTS

p_mut = 0.1
p_co = 0.25

a= AlgoGen(int(sys.argv[1]),100, p_co,p_mut)
a.evolution(int(sys.argv[2]))

#a= AlgoGen(300,p_co,p_mut)
#a.evolution(400)


