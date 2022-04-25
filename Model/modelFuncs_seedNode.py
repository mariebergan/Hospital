import numpy as np
import random
from InitializeParams import *

stateList = ['S', 'E', 'Ia', 'Ip', 'Is', 'R', 'H', 'ICU', 'D']

#Initialize full model
def initModel(contactsArray, baseP, seedNode):
    attrs = readModel(contactsArray)
    
    seedState(attrs, seedNode)


    return attrs

# Builds attrs from daily contacts array
def readModel(contactsArray):
    attrs = {}
    for ID in range(75):
        attrs[ID] = {}
        attrs[ID]['present'] = True 
        attrs[ID]['state'] = 'S'
        attrs[ID]['sick'] = False 

        if ID < 8:
            attrs[ID]['status'] = 'ADM'
            attrs[ID]['age'] = random.randint(22, 67)
        elif ID < 19:
            attrs[ID]['status'] = 'MED'
            attrs[ID]['age'] = random.randint(25, 67)

        elif ID < 46:
            attrs[ID]['status'] = 'NUR'
            attrs[ID]['age'] = random.randint(22, 67)
        else:
            attrs[ID]['status'] = 'PAT'  
            attrs[ID]['age'] = random.randint(1, 100)
        attrs[ID]['decade'] = min(attrs[ID]['age']-attrs[ID]['age']%10, 80)

        if attrs[ID]['age'] < 19:
            attrs[ID]['ageGroup'] = 'B'
        elif attrs[ID]['age'] < 55:
            attrs[ID]['ageGroup'] = 'A1'
        elif attrs[ID]['age'] < 65:
            attrs[ID]['ageGroup'] = 'A2'
        elif attrs[ID]['age'] < 80:
            attrs[ID]['ageGroup'] = 'E1'
        else:
            attrs[ID]['ageGroup'] = 'E2'
    
    return attrs 
     
def infectNode(attrs, node, day):
    attrs[node]['state'] = 'E'
    attrs[node]['lastDay'] = day
    attrs[node]['nextDay'] = day+1+np.random.poisson(dur['I-E'])  

def infectDay(contactsArray, attrs, p, day):    
    infNodes = []  
    susIDs = []
    sickIDs = []
    for i in range(75):
        if attrs[i]['state'] == 'S':
            susIDs.append(i)
        if attrs[i]['sick']:
            sickIDs.append(i)

    for i in sickIDs:
        for j in susIDs:
            if attrs[i]['present'] and attrs[j]['present']:
                n = contactsArray[i][j]
                p1 = p['inf'][attrs[i]['status']][attrs[j]['status']] 
                infP = 1-((1-p1)**(n*attrs[i]['relInfectivity'])) # gange n med relInf
                if random.random() < infP:
                    if attrs[i]['state'] == 'S':
                        infectNode(attrs, i, day)
                        infNodes.append(i) 
                    else:
                        infectNode(attrs, j, day)
                        infNodes.append(j) 

    return infNodes


# Daily state progress check and branching functions
def incubate(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        if random.random() < p['S'][attrs[node]['decade']]: 
            turnPresymp(node, attrs, p, day)
        else:
            turnAsymp(node, attrs, p, day)
    
def asymptomatic(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        recover(node, attrs, p, day)

def preSymptomatic(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        activateSymptoms(node, attrs, p, day)
        
def symptomatic(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        if attrs[node]['nextState'] == 'D':
            die(node, attrs, p, day)
        elif attrs[node]['nextState'] == 'H':
            hospitalize(node, attrs, p, day)
        else:
            recover(node, attrs, p, day)

def hospital(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        if attrs[node]['nextState'] == 'ICU':
            enterICU(node, attrs, p, day)
        elif attrs[node]['nextState'] == 'R':
            recover(node, attrs, p, day)
        elif attrs[node]['nextState'] == 'D':
            die(node, attrs, p, day)

def ICU(node, attrs, p, day):
    if day == attrs[node]['nextDay']:
        if attrs[node]['nextState'] == 'D':
            die(node, attrs, p, day)
        elif attrs[node]['nextState'] == 'R':
            recover(node, attrs, p, day)

            
# State change functions
def recover(node, attrs, p, day):
    attrs[node]['state'] = 'R'
    attrs[node]['lastDay'] = day
    attrs[node]['sick'] = False
    attrs[node]['present'] = True   

def turnAsymp(node, attrs, p, day):
    attrs[node]['state'] = 'Ia'
    attrs[node]['nextState'] = 'R'
    attrs[node]['nextDay'] = day+1+np.random.poisson(dur['AS-R'])
    attrs[node]['sick'] = True
    attrs[node]['relInfectivity'] = 0.3 
    
def turnPresymp(node, attrs, p, day):
    attrs[node]['state'] = 'Ip'
    attrs[node]['nextState'] = 'Is'
    attrs[node]['nextDay'] = day+1+np.random.poisson(dur['PS-I'])
    attrs[node]['sick'] = True
    attrs[node]['relInfectivity'] = 3.0
    if attrs[node]['age'] < 13: 
        attrs[node]['relInfectivity'] = 0.3
    
def activateSymptoms(node, attrs, p, day):
    attrs[node]['state'] = 'Is'
    attrs[node]['lastDay'] = day
    attrs[node]['present'] = False                 
    if random.random() < p['HRage'][attrs[node]['decade']]: 
        attrs[node]['nextState'] = 'H'
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['I-H'])
    else:
        attrs[node]['nextState'] = 'R'
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['I-R'])
    attrs[node]['relInfectivity'] = 1
    if attrs[node]['age'] < 13: 
        attrs[node]['relInfectivity'] = 0.3
   
def hospitalize(node, attrs, p, day):
    attrs[node]['state'] = 'H'
    attrs[node]['lastDay'] = day
    if random.random() < p['ICUage'][attrs[node]['decade']]:
        attrs[node]['nextState'] = 'ICU'
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['H-ICU'])
        
    elif random.random() < p['DRage'][attrs[node]['decade']]:
        attrs[node]['nextState'] = 'D'    
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['H-D'])
    else:
        attrs[node]['nextState'] = 'R'
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['H-R'])

def enterICU(node, attrs, p, day):
    attrs[node]['state'] = 'ICU'
    attrs[node]['lastDay'] = day
    if random.random() < p['DRage'][attrs[node]['decade']]:
        attrs[node]['nextState'] = 'D'
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['ICU-D'])   
    else:
        attrs[node]['nextState'] = 'R' 
        attrs[node]['nextDay'] = day+1+np.random.poisson(dur['ICU-R'])
       
def die(node, attrs, p, day):
    attrs[node]['diedFrom'] = attrs[node]['state']
    attrs[node]['state'] = 'D'
    attrs[node]['lastDay'] = day
    attrs[node]['nextDay'] = -1
    attrs[node]['nextState'] = ''
    attrs[node]['sick'] = False
 

def stateFunction(state):
    funcs = {
        'E': incubate,
        'Ia': asymptomatic,
        'Ip': preSymptomatic,
        'Is': symptomatic,
        'H': hospital,
        'ICU': ICU
        }
    return funcs[state]

# Daily pulse
def systemDay(contactsArray, attrs, p, day, startDay):
    cont = 0
    dailyInfs = 0  
    infNodes = infectDay(contactsArray, attrs, p, day)
    dailyInfs += len(infNodes)
    ageCount = countAge(attrs)
      
    for node in attrs:
        if (attrs[node]['sick'] or (attrs[node]['state'] == 'E')):
            stateFunction(attrs[node]['state'])(node, attrs, p, day)
            cont = True
    return cont, dailyInfs, ageCount

def countState(attrs, stateList):
    stateCount = {}
    for s in stateList:
        stateCount[s] = 0
    for node in attrs:
        stateCount[attrs[node]['state']] += 1
    return stateCount
    

def countAge(attrs):
    ageCount = {}
    for node in attrs:
        if attrs[node]['state'] == 'E':
            if (attrs[node]['decade'] not in ageCount):
                ageCount[attrs[node]['decade']] = 1
            else:
                ageCount[attrs[node]['decade']] += 1
    return ageCount

def getInfIDs(attrs):
    infIDs = []
    for ID in attrs:
        if attrs[ID]['state'] != 'S':
            infIDs.append(ID)
    return infIDs

def timedRun(contactsArray, attrs, baseP, startDay, runDays):
    cont = 1
    day = startDay
    stateLog = []
    infLog = []
    ageLog = []
    endDay = startDay + runDays               
    
    while day < endDay: 
        day += 1
        
        dailyInfs = 0

        cont, dailyInfs, ageCount = systemDay(contactsArray[day%4], attrs, baseP, day, startDay) # contactsArray[day%4]
        
        stateLog.append(countState(attrs, stateList))
        infLog.append(dailyInfs)
        ageLog.append(ageCount)
    
    infIDs = getInfIDs(attrs)
    
    return stateLog, infLog, ageLog, day, infIDs

def seedState(attrs, node): 
    attrs[node]['state'] = 'Ip'
    attrs[node]['nextState'] = 'Is'
    attrs[node]['nextDay'] = 1+np.random.poisson(dur['PS-I'])
    attrs[node]['sick'] = True
    attrs[node]['relInfectivity'] = 3.0
    if attrs[node]['age'] < 13: 
        attrs[node]['relInfectivity'] = 0.3
