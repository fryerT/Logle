import requests
import json

# information about the wcl client that is required for the program to work
clientIdd = '9b48dcbb-f98f-463e-b687-0c75e79a2e93'
clientSecrets = 'ozrRbdHOM6QeFgx5Wfv3YWLEHOmojaXL5G7tnMze'


# funciton to get OAuth 2.0 token for Warcraft logs API 2.0 calls
def getNewToken():
    authServerUrl = 'https://www.warcraftlogs.com/oauth/token' 
    clientId = clientIdd
    clientSecret = clientSecrets

    tokenReqPayload = {'grant_type': 'client_credentials'}

    token_response = requests.post(authServerUrl, data = tokenReqPayload, verify = False, allow_redirects = True, auth = ( clientId, clientSecret))
    if token_response.status_code != 200:
        return 'Not Status Code 200'
    tokens = json.loads(token_response.text)
    return tokens['access_token']

# function that does the API call for data
def apiCall(query, vars, authToken):
    apiUrl = 'https://www.warcraftlogs.com/api/v2/client'
    apiCallHeaders = {'Authorization': 'Bearer ' + authToken}
    apiCallResponse = requests.post(apiUrl, json = {"query": query, 'variables': vars}, headers=apiCallHeaders, verify = True)
    return apiCallResponse.json()
    
# query that returns the json that we will be parsing
def getPlayerPerformanceFromEncounter(playerName, authToken, boss_ID, spec_Name, server_Name, metricType, bracket):
    vars = {'bossID': boss_ID, 'playerName': playerName, 'specName': spec_Name, 'serverName': server_Name, 'metricType': metricType, 'bracket': bracket}
    query = """query characterRank($playerName: String!, $bossID: Int!, $specName: String!, $serverName: String!, $metricType: CharacterRankingMetricType!, $bracket: Boolean!){
	                characterData{
		                character(name: $playerName, serverSlug: $serverName, serverRegion: "US"){
			                encounterRankings(byBracket: $bracket, compare: Rankings, metric: $metricType, encounterID: $bossID, specName: $specName)
		                }
	                }   
                }"""
    return apiCall(query, vars, authToken)

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

# grabs a specific fight from a report and returns the characterId for the matching characterName
# this is done because the characterId is needed to use reportInfo on players since the sourceId == characterId
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

