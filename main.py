from flask import Flask, render_template, request, make_response, url_for, session
import requests
import json
import threading
import ast


# information about the wcl client that is required for the program to work
clientIdd = '9b48dcbb-f98f-463e-b687-0c75e79a2e93'
clientSecrets = 'ozrRbdHOM6QeFgx5Wfv3YWLEHOmojaXL5G7tnMze'

# keep the dungeon name, id, and image in the same order
encounterName = ["Algeth'ar Academy", "Brackenhide Hollow", "Halls of Infusion", "Neltharus", "Ruby Life Pools", "Azure Vault", "Nokhud Offensive", "Uldaman"]
encounterId = [62526, 62520, 62527, 62519, 62521, 62515, 62516, 62451]

# html names
loadingHtml = 'loadingV2.6.html'
mainHtml = 'mainV3.5.html'
displayHtml = 'displayV3.html'
errorHtml = 'errorV2.3.html'


# used to create an encounter object for easier management
class Encounter():
    def __init__(self, name, Id):
        self.name = name    # name of the encounter
        self.id = Id        # the ID of the encounter
        self.amount = '0'   # dps/hps
        self.parse = '0'    # parse number
        self.rAmount = '0'  # rounded amount
        self.rParse = '0'   # rounded parse
        self.spec = ''      # spec name of the logs being used
        self.numberOfFights  = 0 # the number of logs that include the encounter

# funciton to get OAuth 2.0 token for Warcraft logs API 2.0 calls
def getNewToken():
    authServerUrl = 'https://www.warcraftlogs.com/oauth/token' 
    clientId = clientIdd
    clientSecret = clientSecrets

    tokenReqPayload = {'grant_type': 'client_credentials'}

    token_response = requests.post(authServerUrl, data = tokenReqPayload, verify = False, allow_redirects = True, auth = ( clientId, clientSecret))
    if token_response.status_code != 200:
        return 'Status Code 200'
    tokens = json.loads(token_response.text)
    return tokens['access_token']

# function that does the API call for data
def apiCall(query, vars, authToken):
    apiUrl = 'https://www.warcraftlogs.com/api/v2/client'
    apiCallHeaders = {'Authorization': 'Bearer ' + authToken}
    apiCallResponse = requests.post(apiUrl, json = {"query": query, 'variables': vars}, headers=apiCallHeaders, verify = True)
    return apiCallResponse.json()
    
# query that returns the json that we will be parsing
def getPlayerPerformanceFromEncounter(playerName, authToken, boss_ID, spec_Name, server_Name, metricType):
    vars = {'bossID': boss_ID, 'playerName': playerName, 'specName': spec_Name, 'serverName': server_Name, 'metricType': metricType}
    query = """query characterRank($playerName: String!, $bossID: Int!, $specName: String!, $serverName: String!, $metricType: CharacterRankingMetricType!){
	                characterData{
		                character(name: $playerName, serverSlug: $serverName, serverRegion: "US"){
			                encounterRankings(byBracket: true, compare: Rankings, metric: $metricType, encounterID: $bossID, specName: $specName)
		                }
	                }   
                }"""
    return apiCall(query, vars, authToken)

# function that runs the program, triggered by a button
def RunLogle(encounter, specList, playerName, serverName, specName, metricType, keyLevelCutoff, authToken, i):
    
    global avgPar
    
	# grabs all fights for the player based on encounter id
    logs = getPlayerPerformanceFromEncounter(playerName, authToken, encounter[i].id, specName, serverName, metricType.lower())


	# gets the relevant data fron the json text
    try:
        allFights = logs["data"]["characterData"]["character"]["encounterRankings"]["ranks"]
	# if the information is incorrect, exit the function and do not continue
    except:
        avgPar = "Error"
        return 0
    
    # iterates through all the fights of the selected encounter to analyze amount/parse
    for fight in allFights:
        
            
        if fight['bracketData'] >= int(keyLevelCutoff) and fight['medal'] != 'none' and fight['historicalPercent'] > float(encounter[i].parse):
            if specName == '':  # if the specName was left blank
                encounter[i].parse = str(fight['historicalPercent'])
                encounter[i].amount = str(fight['amount'])
                encounter[i].spec = ' - ' + fight['spec']
            elif specName == fight['spec']:  # if the specName was specified and the log has a matching specName
                encounter[i].parse = str(fight['historicalPercent'])
                encounter[i].amount = str(fight['amount'])

        if fight['bracketData'] >= int(keyLevelCutoff) and fight['medal'] != 'none':    # adds to the total num of fights if the key is eligible
            encounter[i].numberOfFights += 1
            specList.append(fight['spec'])
                
            ####################################################
            ''' code = fight['report']['code']
            fightId = fight['report']['fightID']
            specTemp = fight['spec']
            charId = getCharacterId(playerName, specTemp, code, fightId, authToken)
                    
            testing = reportInfo(code, fightId, charId, authToken)
            print('\n' + str(code))
            allTests = testing['data']['reportData']['report']['events']['data']
            for x in allTests:
                try:
                    print(x['killingAbilityGameID'])
                except:
                    print('Unknown Ability') '''
            ####################################################
           
    # rounds the parse and amount if the log exists
    if encounter[i].amount != '0':
        encounter[i].rAmount = "{:,.0f}".format(round(float(encounter[i].amount), 0))
        encounter[i].rParse = "{:.0f}".format(round(float(encounter[i].parse), 0))


def avgParse(encounter):
    global avgPar  
    
    # calculates average parse and updates information
    avg = 0
    numOfEnc = len(encounter)
    for i in range(len(encounter)):
            if float(encounter[i].amount) == 0: # decrement numOfEnc and update encounter if no logs exist
                numOfEnc -= 1
                encounter[i].rAmount = "N/A"
                encounter[i].rParse = "..."
            elif float(encounter[i].amount) != 0:   # add the amount to the total if logs exist
                avg += float(encounter[i].parse)

    # after we know how many encounters with logs exist
    if numOfEnc != 0:   # if any logs exist divide the total by the amount of encounters with logs
            avg /= numOfEnc
            avgPar = "{:.0f}".format(avg)
    if numOfEnc == 0:   # if no logs exist, reflect that in avgPar
            avgPar = "None"





# to be scrapped if it can't be optimized further
def reportInfo(reportId, fightId, sourceId, authToken):
    vars = {'reportId': reportId, 'fightId': fightId, 'sourceId': sourceId}
    query = """query reportInfo($reportId: String!, $fightId: [Int]!, $sourceId: Int!) {
                reportData {
                    report(code: $reportId) {
                        events(fightIDs: $fightId, sourceID: $sourceId, dataType: Deaths) {
                            data
                        }
                    }
                }
            }"""
    return apiCall(query, vars, authToken)

# to be scrapped if it can't be optimized further
def getCharacterId(characterName, specName, reportId, fightId, authToken):
    vars = {"reportId": reportId, "fightId": fightId}
    query = """query reportingData($reportId: String!, $fightId: [Int]!){
        reportData{
            report(code: $reportId){
                playerDetails(fightIDs: $fightId)
            }
        }
    }"""
    log = apiCall(query, vars, authToken)
    # makes sure the log exists and returns an error if it doesn't
    if log["data"]["reportData"]["report"] == None:
        print("getCharacterId() function has failed to find the log requested, please check inputs", file=sys.stderr)
        sys.exit(1)
    # applies the role based on the spec name
    if specName == "Discipline" or specName == "Holy" or specName == "Mistweaver" or specName == "Restoration" or specName == "Preservation":
        role = "healers"
    elif specName == "Protection" or specName == "Vengence" or specName == "Brewmaster" or specName == "Blood" or specName == "Guardian":
        role = "tanks"
    else:
        role = "dps"
    allCharacters = log["data"]["reportData"]["report"]["playerDetails"]["data"]["playerDetails"][role]
    for character in allCharacters:
        # looks for a character in the log and returns it if it finds the one requested
        if character["name"] == characterName:
            return character["id"]
    # if the character could not be found in the log
    return "Character ID not found..."


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():

    if request.method == 'GET':
        # checks if cookies are stored, if not defaults and goes to homepage
        userInfo = ast.literal_eval(request.cookies.get('userInfo'))
        if userInfo is None:
             userInfo = {
                'name': '',
                'server': '',
                'spec': '',
                'metric': 'DPS',
                'keyLvlCO': '2',
                'rio': '',
                'specTog': 'false',
                'rioTog': 'false',
                'pasteRioTog': 'false'
            }
        
        return render_template(mainHtml, charName = userInfo['name'], servName = userInfo['server'], specName = userInfo['spec'], metric = userInfo['metric'],
            keyLvlCo = userInfo['keyLvlCO'], specTog = userInfo['specTog'], rioInput = userInfo['rio'], rioTog = userInfo['rioTog'],
            pasteRioTog = userInfo['pasteRioTog'])

    elif request.method == 'POST':
        # create response and set cookies based on user input
        resp = make_response(render_template(loadingHtml))
        
        if request.form.get('specToggle') == 'on':
            specTogStatus = 'true'
        else:
            specTogStatus = 'false'
        
        if request.form.get('rioToggle') == 'on':
            rioTogStatus = 'true'
        else:
            rioTogStatus = 'false'
        
        if request.form.get('pasteRioToggle') == 'on':
            pasteRioTogStatus = 'true'
        else:
            pasteRioTogStatus = 'false'
        
        userInfo = {
            'name': request.form.get('charName').replace(' ', ''),
            'server': request.form.get('servName').replace(' ', ''),
            'spec': request.form.get('specName').replace(' ', ''),
            'metric': request.form.get('metricSelected'),
            'keyLvlCO': request.form.get('minKeyLvlSelected'),
            'rio': request.form.get('rioInput').replace(' ', ''),
            'specTog': specTogStatus,
            'rioTog': rioTogStatus,
            'pasteRioTog': pasteRioTogStatus
        }
        resp.set_cookie('userInfo', str(userInfo))
        
        return resp

# currently only used for the specChoice option on the summary page
@app.route('/loading')
def loading():
    return render_template(loadingHtml)

@app.route('/summary', methods = ['GET', 'POST'])
def summary():
    if request.method == 'GET':
        # retrieve info from cookies
        userInfo = ast.literal_eval(request.cookies.get('userInfo'))
        player = userInfo['name']
        serv = userInfo['server']
        spec = userInfo['spec']
        metric = userInfo['metric']
        keyLevelCutoff = userInfo['keyLvlCO']
        rio = userInfo['rio']
        
        if rio != '':
            try:
                xSplit = rio.split('/')
                ySplit = xSplit[6].split('?')
                player = ySplit[0]
                serv = xSplit[5]
            except:
                return render_template(errorHtml)

        global avgPar
        avgPar = ''
        specList = []
        
        authToken = getNewToken()
        
        if authToken == 'Status Code 200':
            return render_template(errorHtml)
        
        # inilialize encounter class objects
        encounter = []
        for i in range(len(encounterName)):
            encounter.append(Encounter(encounterName[i], encounterId[i]))

        # assigns each dungeon encounter to a thread
        t0 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 0,))
        t1 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 1,))
        t2 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 2,))
        t3 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 3,))
        t4 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 4,))
        t5 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 5,))
        t6 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 6,))
        t7 = threading.Thread(target = RunLogle, args = (encounter, specList, player, serv, spec, metric, keyLevelCutoff, authToken, 7,))
        
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
        
        # if there was an error with the query, go to the error page
        if avgPar == 'Error':
            return error()

        avgParse(encounter)
        specList = list(dict.fromkeys(specList))
        # used in case the specName isn't specified by user so it doesn't mess up the input on main['get']
        modSpec = spec


        # only do this if specialization was not specified
        if spec == '':
            specializationNames = []    # create a list to store spec names that have a top parse
            for i in range(len(encounter)):     # loop through each encounter
                if encounter[i].spec != '':
                    specializationNames.append(encounter[i].spec)   # add spec names to the list
            specializationNames = list(dict.fromkeys(specializationNames)) # remove any duplicates
            
            for i in range(len(specializationNames)):
                if i == 0:  # base case
                    modSpec = specializationNames[i][3:]
                    if len(specializationNames) == 1:   # if there is only one spec, listing these would be repetitive
                        for i in range(len(encounter)):
                            encounter[i].spec = ''
                else:
                    modSpec = modSpec + ' & ' + specializationNames[i][3:]
      
        # unique case for bm hunters sicne they have that damn _
        if modSpec == 'BeastMastery': modSpec = 'Beast Mastery';
        
        # calculates the total number of logs parsed by the program
        numRunsTotal = 0
        for i in range(len(encounter)):
            numRunsTotal += encounter[i].numberOfFights
        
        # return webpage with updated values
        return render_template(displayHtml, 
            name0 = encounter[0].name, amount0 = encounter[0].rAmount, parse0 = encounter[0].rParse, spec0 = encounter[0].spec[:7], numRuns0 = encounter[0].numberOfFights,
            name1 = encounter[1].name, amount1 = encounter[1].rAmount, parse1 = encounter[1].rParse, spec1 = encounter[1].spec[:7], numRuns1 = encounter[1].numberOfFights,
            name2 = encounter[2].name, amount2 = encounter[2].rAmount, parse2 = encounter[2].rParse, spec2 = encounter[2].spec[:7], numRuns2 = encounter[2].numberOfFights, 
            name3 = encounter[3].name, amount3 = encounter[3].rAmount, parse3 = encounter[3].rParse, spec3 = encounter[3].spec[:7], numRuns3 = encounter[3].numberOfFights, 
            name4 = encounter[4].name, amount4 = encounter[4].rAmount, parse4 = encounter[4].rParse, spec4 = encounter[4].spec[:7], numRuns4 = encounter[4].numberOfFights, 
            name5 = encounter[5].name, amount5 = encounter[5].rAmount, parse5 = encounter[5].rParse, spec5 = encounter[5].spec[:7], numRuns5 = encounter[5].numberOfFights, 
            name6 = encounter[6].name, amount6 = encounter[6].rAmount, parse6 = encounter[6].rParse, spec6 = encounter[6].spec[:7], numRuns6 = encounter[6].numberOfFights, 
            name7 = encounter[7].name, amount7 = encounter[7].rAmount, parse7 = encounter[7].rParse, spec7 = encounter[7].spec[:7], numRuns7 = encounter[7].numberOfFights, 
            avgParse = avgPar, spec = modSpec, name = player, numRunsTotal = numRunsTotal, specList = specList)

    elif request.method == 'POST':
        resp = make_response(render_template(loadingHtml))
        resp.set_cookie('specName', request.form.get('newSpec'))
        return resp

@app.route('/error')
def error():
    return render_template(errorHtml)

   

if __name__ == '__main__':
	app.run()