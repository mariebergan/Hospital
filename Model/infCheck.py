def infectDay(contactsArray, attrs, p, day):    
    susIDs = []
    sickIDs = []
    for i in range(75):
        if attrs[i]['state'] == 'S':
            susIDs.append(i)
        if attrs[i]['sick']:
            sickIDs.append(i)

    for i in sickIDs:
        for j in susIDs:
            infNodes = infCheck(contactsArray, attrs, p, day, i, j)
            
def infCheck(contactsArray, attrs, p, day, i, j):    
    infNodes = []  
    if attrs[i]['present'] and attrs[j]['present']:
        n = contactsArray[i][j]
        p1 = p['inf'][attrs[i]['status']][attrs[j]['status']] 
        infP = 1-(1-p1)**n
        if random.random() < infP:
            if attrs[i]['state'] == 'S':
                infectNode(attrs, i, day)
                infNodes.append(i) 
            else:
                infectNode(attrs, j, day)
                infNodes.append(j) 

    return infNodes