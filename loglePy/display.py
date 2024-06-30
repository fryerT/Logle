import threading
import math
from . import wowAPI as api
from . import utility as util

# function that runs the program, triggered by a button
def RunLogle(queryData, encounterObj, authToken, i):
    
    # playerName, serverName, specName, metricType, keyLevelCutoff, 
    playerName = queryData['name']
    serverName = queryData['server']
    specName = queryData['spec']
    metricType = queryData['metric']
    keyLevelCutoff = queryData['keyLvlCO']
    keyPercentParse = True
    
	# grabs all fights for the player based on encounter id
    logs = api.getPlayerPerformanceFromEncounter(playerName, authToken, encounterObj[i]['id'], specName, serverName, metricType.lower(), keyPercentParse)


	# gets the relevant data fron the json text
    try: allFights = logs["data"]["characterData"]["character"]["encounterRankings"]["ranks"];
	# if the information is incorrect, exit the function and do not continue
    except:
        queryData['avgPar'] = "Error"
        return 0
        
    
    def parseFights(allFights, queryData, authToken, i):
    
        # iterates through all the fights of the selected encounter to analyze amount/parse
        for fight in allFights:
            
            if fight['bracketData'] >= int(keyLevelCutoff) and fight['medal'] != 'none' and fight['historicalPercent'] > float(encounterObj[i]['parse']):
                if specName == '':  # if the specName was left blank
                    encounterObj[i]['parse'] = str(fight['historicalPercent'])
                    encounterObj[i]['amount'] = str(fight['amount'])
                    encounterObj[i]['spec'] = ' - ' + fight['spec']
                elif specName == fight['spec']:  # if the specName was specified and the log has a matching specName
                    encounterObj[i]['parse'] = str(fight['historicalPercent'])
                    encounterObj[i]['amount'] = str(fight['amount'])
                
            if fight['bracketData'] >= int(keyLevelCutoff) and fight['medal'] != 'none':    # adds to the total num of fights if the key is eligible
                encounterObj[i]['numberOfFights'] += 1
                queryData['specList'].append(fight['spec'])
                
        return 0
    
    

    
    fightLists = util.splitList(allFights)
    
    t0 = threading.Thread(target = parseFights, args = (fightLists[0], queryData, authToken, i,))
    t1 = threading.Thread(target = parseFights, args = (fightLists[1], queryData, authToken, i,))
    t2 = threading.Thread(target = parseFights, args = (fightLists[2], queryData, authToken, i,))
    t3 = threading.Thread(target = parseFights, args = (fightLists[3], queryData, authToken, i,))
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t0.join()
    t1.join()
    t2.join()
    t3.join()    
        
   
    

           
    # rounds the parse and amount if the log exists
    if encounterObj[i]['amount'] != '0':
        encounterObj[i]['rAmount'] = "{:,.0f}".format(math.ceil(float(encounterObj[i]['amount'])), 0)
        encounterObj[i]['rParse'] = math.ceil(float(encounterObj[i]['parse']))



    return 0

def ThreadLogle(queryData, encounterObj, authToken):
    # assigns each dungeon encounter to a thread
    t0 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 0,))
    t1 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 1,))
    t2 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 2,))
    t3 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 3,))
    t4 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 4,))
    t5 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 5,))
    t6 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 6,))
    t7 = threading.Thread(target = RunLogle, args = (queryData, encounterObj, authToken, 7,))
    
    # start em up
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    
    # wow, so fast
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    
    return 0

def avgParse(queryData, encounterObj):  
    
    # calculates average parse and updates information
    avg = 0
    numOfEnc = len(encounterObj)
    for i in range(len(encounterObj)):
            if float(encounterObj[i]['amount']) == 0: # decrement numOfEnc and update encounter if no logs exist
                numOfEnc -= 1
                encounterObj[i]['rAmount'] = "N/A"
                encounterObj[i]['rParse'] = "..."
            elif float(encounterObj[i]['amount']) != 0:   # add the amount to the total if logs exist
                avg += float(encounterObj[i]['rParse'])

    # after we know how many encounters with logs exist
    if numOfEnc != 0:   # if any logs exist divide the total by the amount of encounters with logs
            avg /= numOfEnc
            queryData['avgPar'] = "{:.0f}".format(avg)
    if numOfEnc == 0:   # if no logs exist, reflect that in avgPar
            queryData['avgPar'] = "None"

    return 0



def getCorrectSpecName(queryData, encounterObj):
    specializationNames = []    # create a list to store spec names that have a top parse
    for i in range(len(encounterObj)):     # loop through each encounter
        if encounterObj[i]['spec'] != '':
            specializationNames.append(encounterObj[i]['spec'])   # add spec names to the list
    specializationNames = list(dict.fromkeys(specializationNames)) # remove any duplicates
    
    for i in range(len(specializationNames)):
        if i == 0:  # base case
            queryData['spec'] = specializationNames[i][3:]
            if len(specializationNames) == 1:   # if there is only one spec, listing these would be repetitive
                for i in range(len(encounterObj)): encounterObj[i]['spec'] = '';
        else:
            queryData['spec'] = queryData['spec'] + ' & ' + specializationNames[i][3:]