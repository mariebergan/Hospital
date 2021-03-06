startDay = 0
runDays = 60
nSeedNodes = 1

# Set base probabilities
baseP = {}

# Infection probabilities
p = 0.001
baseP['inf'] = {'ADM': {'ADM': p, 'MED': p, 'NUR': p, 'PAT': p},
                'MED': {'ADM': p, 'MED': p, 'NUR': p, 'PAT': p},
                'NUR': {'ADM': p, 'MED': p, 'NUR': p, 'PAT': p},
                'PAT': {'ADM': p, 'MED': p, 'NUR': p, 'PAT': p}}


baseP['rec'] = 0.1

# Legg in asymptomatic
baseP['inc'] = 1

# Chance to develop symptoms
baseP['S'] = {0: 0.5, 10: 0.5, 20: 0.5, 30:0.5, 40:0.5, 50: 0.5, 60: 0.5, 70: 0.5, 80: 0.5} 

# Chance to hospitalize
baseP['H'] = {'B': 0.0001, 'A1': 0.02, 'A2':0.08, 'E1':0.15, 'E2': 0.184}

# Chance to die once hospitalized
baseP['D'] = {'B': 0.1, 'A1': 0.05, 'A2':0.15, 'E1':0.3, 'E2': 0.40 }
baseP['ICU'] = 0.3
baseP['NI'] = 0

baseP['infRatio'] = {'B': 0.25, 'A1': 1, 'A2': 1, 'E1': 1, 'E2': 1}

# Hospitalization by age bracket
baseP['Hage'] = {0: 0.0001, 10: 0.00048, 20: 0.0104, 30: 0.0343, 40: 0.0425, 50: 0.0816, 60: 0.118, 70: 0.166, 80: 0.184}

# Hospitalization corrected for asymptomatic cases
baseP['HRage'] = {}
for ageGrp in baseP['Hage']:
    baseP['HRage'][ageGrp] = baseP['Hage'][ageGrp]/baseP['S'][ageGrp]

# ICU per hospitalization by age bracket
baseP['ICUage'] = {0: 0.3, 10: 0.3, 20: 0.3, 30: 0.3, 40: 0.3, 50: 0.3, 60: 0.3, 70: 0.3, 80: 0.3}

# Death per case by age bracket
baseP['Dage'] = {0: 1.61*pow(10, -5), 10: 6.95*pow(10, -5), 20: 3.09*pow(10, -4), 30: 8.44*pow(10, -4), 40: 1.61*pow(10, -3), 50: 5.95*pow(10, -3), 60: 0.0193, 70: 0.0428, 80: 0.078}

# Death rate by age group
baseP['DRage'] = {}
for ageGrp in baseP['Hage']:
    baseP['DRage'][ageGrp] = baseP['Dage'][ageGrp]/(baseP['Hage'][ageGrp])
  
# State change duration
dur = {}
dur['I-E'] = 5
dur['PS-I'] = 2
dur['I-R'] = 5
dur['I-H'] = 6
dur['AS-R'] = 8
dur['H-R'] = 8
dur['H-ICU'] = 4
dur['ICU-R'] = 12
dur['ICU-D'] = dur['ICU-R']
dur['H-D'] = dur['H-ICU']+.5*dur['ICU-D']
dur['I-D'] = dur['I-H']+dur['H-D']