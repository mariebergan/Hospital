import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

class Person:
    def __init__(self, ID, status):
        self.ID = ID
        self.status = status
        self.contacts = [] # list of tuples with contact data for the given Person object

    def create_contacts(self, sizes, hours): # sizes = [8, 11, 27, 29]
        self.people = {}
        self.people['ADM'] = range(max(0, self.ID), sizes[0]) 
        self.people['MED'] = range(sizes[0], sizes[0]+sizes[1])
        self.people['NUR'] = range(sizes[0]+sizes[1], sizes[0]+sizes[1]+sizes[2])
        self.people['PAT'] = range(sizes[0]+sizes[1]+sizes[2], sum(sizes))

        for h in range(hours): # goes through every hour in hours
            for group in self.people:
                for x in self.people[group]:
                    n = np.random.poisson()
                    if n > 0:
                        self.contacts.append((x, h, n)) # x = target node ID, h = hour of contact, n = number of contacts with x within h
                        #Hospital.self.contacts.append(self.ID, h, n) 
    

class Hospital:
    def __init__(self, sizes, hours): # sizes = [8, 11, 27, 29]
        self.sizes = sizes

        self.objs = {} 
        self.objs['ADM'] = []
        self.objs['MED'] = []
        self.objs['NUR'] = []
        self.objs['PAT'] = []

        # create Person objects for each group and store them in objs dict
        for i in range(sizes[0]):
            obj = Person(i, 'ADM')
            obj.create_contacts(self.sizes, hours)
            self.objs['ADM'].append(obj)
        
        for i in range(sizes[1]):
            obj = Person(sizes[0]+i, 'MED')
            obj.create_contacts(self.sizes, hours)
            self.objs['MED'].append(obj)
        
        for i in range(sizes[2]):
            obj = Person(sizes[0]+sizes[1]+i, 'NUR')
            obj.create_contacts(self.sizes, hours)
            self.objs['NUR'].append(obj)
        
        for i in range(sizes[3]):
            obj = Person(sizes[0]+sizes[1]+sizes[2]+i, 'PAT')
            obj.create_contacts(self.sizes, hours)
            self.objs['PAT'].append(obj)
        
        #print(self.objs)

    
    def create_array(self):
        
        self.hosp_array = np.zeros((sum(self.sizes), sum(self.sizes)), dtype = int)
     
        # iterate over the objects in each group list and create an array of contacts
        for group in self.objs:
            for obj in self.objs[group]:
                for contact in obj.contacts:
                    i = obj.ID
                    j = contact[0]
                    Wij = contact[2]
                    if (self.hosp_array[i, j] == 0) & (i != j):
                        self.hosp_array[i, j] = Wij
                        self.hosp_array[j, i] = Wij
                    else:
                        self.hosp_array[i, j] = self.hosp_array[i, j] + Wij
                        self.hosp_array[j, i] = self.hosp_array[j, i] + Wij
                    
        self.hosp_array = np.log(self.hosp_array) 

        print(self.hosp_array)
    
    def create_heatmap(self):
        hosp_hm = sns.heatmap(self.hosp_array, vmin = 0, vmax = 6)
        hosp_hm.axhline(self.sizes[0], linewidth = 1, color = 'w')
        hosp_hm.axhline(self.sizes[0]+self.sizes[1], linewidth = 1, color = 'w')
        hosp_hm.axhline(self.sizes[0]+self.sizes[1]+self.sizes[2], linewidth = 1, color = 'w')
        hosp_hm.axvline(self.sizes[0], linewidth = 1, color = 'w')
        hosp_hm.axvline(self.sizes[0]+self.sizes[1], linewidth = 1, color = 'w')
        hosp_hm.axvline(self.sizes[0]+self.sizes[1]+self.sizes[2], linewidth = 1, color = 'w')
        plt.show()

# p1 = Person(0, 'ADM')
# p1.create_contacts([8, 11, 27, 29], 24)

hosp = Hospital([8, 11, 27, 29], 24)
hosp.create_array()
hosp.create_heatmap()