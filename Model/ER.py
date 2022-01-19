import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import random

def create_contacts(sizes, hours): # [8, 11, 27, 29], 24
	n = sum(sizes)
	contacts = np.zeros((n, n), dtype = int)

	p_ADM = 0.08
	p_MED = 0.18
	p_NUR = 0.15
	p_PAT = 0.01
	p_ADM_MED = 0.12
	p_ADM_NUR = 0.1
	p_ADM_PAT = 0.06
	p_MED_NUR = 0.15
	p_MED_PAT = 0.1
	p_NUR_PAT = 0.15

	# ADM-ADM
	for h in range(hours):
		for i in range(0, sizes[0]):
			for j in range(0, sizes[0]):
				rand_num = random.random()
				if (rand_num < p_ADM) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# MED-MED
	for h in range(hours):
		for i in range(sizes[0], sizes[0]+sizes[1]):
			for j in range(sizes[0], sizes[0]+sizes[1]):
				rand_num = random.random()
				if (rand_num < p_MED) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# NUR-NUR
	for h in range(hours):
		for i in range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2]):
			for j in range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2]):
				rand_num = random.random()
				if (rand_num < p_NUR) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# PAT-PAT
	for h in range(hours):
		for i in range(sizes[0]+sizes[1]+sizes[2], n):
			for j in range(sizes[0]+sizes[1]+sizes[2], n):
				rand_num = random.random()
				if (rand_num < p_PAT) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# ADM-MED
	for h in range(hours):
		for i in range(0, sizes[0]):
			for j in range(sizes[0], sizes[0]+sizes[1]):
				rand_num = random.random()
				if (rand_num < p_ADM_MED) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# ADM-NUR
	for h in range(hours):
		for i in range(0, sizes[0]):
			for j in range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2]):
				rand_num = random.random()
				if (rand_num < p_ADM_NUR) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1

	# ADM-PAT
	for h in range(hours):
		for i in range(0, sizes[0]):
			for j in range(sizes[0]+sizes[1]+sizes[2], sum(sizes)):
				rand_num = random.random()
				if (rand_num < p_ADM_PAT) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# MED-NUR
	for h in range(hours):
		for i in range(sizes[0], sizes[0]+sizes[1]):
			for j in range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2]):
				rand_num = random.random()
				if (rand_num < p_MED_NUR) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# MED-PAT
	for h in range(hours):
		for i in range(sizes[0], sizes[0]+sizes[1]):
			for j in range(sizes[0]+sizes[1]+sizes[2], sum(sizes)):
				rand_num = random.random()
				if (rand_num < p_MED_PAT) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
	
	# NUR-PAT
	for h in range(hours):
		for i in range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2]):
			for j in range(sizes[0]+sizes[1]+sizes[2], sum(sizes)):
				rand_num = random.random()
				if (rand_num < p_NUR_PAT) & (i != j):
					if contacts[i, j] == 0:
						contacts[i, j] = 1
						contacts[j, i] = 1
					else:
						contacts[i, j] += 1
						contacts[j, i] += 1
					
	
	contacts = np.log(contacts+1)

	hm = sns.heatmap(contacts, vmin = 1, vmax = 8)
	hm.axhline(8, linewidth = 1, color = 'w')
	hm.axhline(19, linewidth = 1, color = 'w')
	hm.axhline(46, linewidth = 1, color = 'w')
	hm.axvline(8, linewidth = 1, color = 'w')
	hm.axvline(19, linewidth = 1, color = 'w')
	hm.axvline(46, linewidth = 1, color = 'w')
	plt.show()


create_contacts([8, 11, 27, 29], 24)
