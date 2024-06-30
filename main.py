from flask import Flask, render_template, request, make_response, url_for, session, redirect
from urllib.parse import unquote
import ast

from loglePy import avoidableDeaths as avDs
from loglePy import wowAPI as api
from loglePy import display as dis
from loglePy import utility as util
from loglePy import encounter as enc

# disables the https warning #
import urllib3
urllib3.disable_warnings()
# remove this and fix in future update #


# html names
loadingHtml = 'loadingV4.html'
mainHtml = 'mainV5.html'
displayHtml = 'displayV5.html'
errorHtml = 'errorV4.html'
avoidableDeathsHtml = 'avoidableDeathsV2.html'
testHtml = 'avoidableDeathsV2.html'



app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():

    if request.method == 'GET':

        userInfo = util.checkSetCookie(request.cookies.get('userInfo'))
        
        return render_template(mainHtml, 
            charName = userInfo['name'],
            servName = userInfo['server'],
            specName = userInfo['spec'],
            metric = userInfo['metric'],
            keyLvlCo = userInfo['keyLvlCO'],
            specTog = userInfo['specTog'],
            rioInput = userInfo['rio'],
            rioTog = userInfo['rioTog'],
            pasteRioTog = userInfo['pasteRioTog'],
            avoidableDeathsTog = userInfo['avoidableDeathsTog']
            )

    elif request.method == 'POST':
        # create response and set cookies based on user input
        resp = make_response(render_template(loadingHtml))
        
        # check the status of all toggle options
        if request.form.get('specToggle') == 'on': specTogStatus = 'true';
        else: specTogStatus = 'false';
        if request.form.get('rioToggle') == 'on': rioTogStatus = 'true';
        else: rioTogStatus = 'false';
        if request.form.get('pasteRioToggle') == 'on': pasteRioTogStatus = 'true';
        else: pasteRioTogStatus = 'false';
        if request.form.get('avoidableDeathsToggle') == 'on': avoidableDeathsStatus = 'true';
        else: avoidableDeathsStatus = 'false';
        
        # update userInfo accordingly
        userInfo = {
            'name': request.form.get('charName').replace(' ', ''),
            'server': request.form.get('servName').replace(' ', ''),
            'spec': request.form.get('specName').replace(' ', ''),
            'metric': request.form.get('metricSelected'),
            'keyLvlCO': request.form.get('minKeyLvlSelected'),
            'rio': request.form.get('rioInput').replace(' ', ''),
            'specTog': specTogStatus,
            'rioTog': rioTogStatus,
            'pasteRioTog': pasteRioTogStatus,
            'avoidableDeathsTog': avoidableDeathsStatus,
            'specList': [],
            'avgPar': ''
            }
        
        resp.set_cookie('userInfo', str(userInfo))
        
        return resp

# currently only used for the specChoice option on the summary page
@app.route('/loading', methods = ['GET', 'POST'])
def loading():

    if request.method == 'GET': return render_template(loadingHtml);
    
    elif request.method == 'POST':
    
        # get userInfo from cookie and covert to dict
        userInfo = ast.literal_eval(request.cookies.get('userInfo'))
        
        
        # error check for empty fields so we don't make a bad url
        if (userInfo['name'] == '' or userInfo['server'] == '') and userInfo['rio'] == '': return error();
        
        
        # change spec so it will work with url input
        if userInfo['spec'] == '': userInfo['spec'] = '_';
        
        
        # if they entered raider io, convert the url to usable data
        if userInfo['rio'] != '':
            try:
                xSplit = userInfo['rio'].split('/')
                ySplit = xSplit[6].split('?')
                if userInfo['name'] != ySplit[0]:
                    userInfo['specList'] = ''
                    userInfo['name'] = ySplit[0]
                if userInfo['server'] != xSplit[5]:
                    userInfo['server'] = xSplit[5]
            except: return error(); # if this happens the url wasn't valid
        
        
        # redirect to avoidable deaths
        if userInfo['avoidableDeathsTog'] == 'true': return redirect(userInfo['name'] + '/' + userInfo['server'] + '/avoidable_deaths');
        
        return redirect(userInfo['name'] + '/' + userInfo['server'] + '/' + userInfo['spec'] + '/' + userInfo['metric'] + '/' + userInfo['keyLvlCO'])

@app.route("/<name>/<server>/<specName>/<metricType>/<keyLevelCO>", methods = ['GET', 'POST'])
def summaryLink(name, server, specName, metricType, keyLevelCO):

    # unencrypt the url versions of the name, this lets it play nice with alt characters
    name = unquote(name)

    if request.method == 'GET':
        
        authToken = api.getNewToken()
        if authToken == 'Not Status Code 200': return error();

        if specName == '_': specName = '';
        
        # retrieve info from cookies as a dict
        characterData = util.checkSetCookie(request.cookies.get('userInfo'))
        
        
        
        # update values in case the url was entered and there is no cookie associated with the query
        characterData['name'] = name
        characterData['server'] = server
        characterData['spec'] = specName
        characterData['metric'] = metricType
        characterData['keyLvlCO'] = keyLevelCO
        
        # inilialize encounter class objects
        encounterObj = enc.newEncounterObj()

        # run the program with a process assigned to each dungeon
        dis.ThreadLogle(characterData, encounterObj, authToken)
        
        # if there was an error with the query, go to the error page
        if characterData['avgPar'] == 'Error': return error();

        # calculate the average parse of all dungeons
        dis.avgParse(characterData, encounterObj)
        
        # remove duplicates from the specialization list
        characterData['specList'] = list(dict.fromkeys(characterData['specList']))
        

        # only do this if specialization was not specified
        if characterData['spec'] == '': dis.getCorrectSpecName(characterData, encounterObj);

      
        # unique case for bm hunters sicne they have that damn _
        if characterData['spec'] == 'BeastMastery': characterData['spec'] = 'Beast Mastery';
        
        if characterData['spec'] == '': characterData['spec'] = ' ';
        
        # calculates the total number of logs parsed by the program
        numRunsTotal = 0
        for i in range(len(encounterObj)): numRunsTotal += encounterObj[i]['numberOfFights'];
        
        # create the response to return
        resp = make_response(render_template(displayHtml, 
            name0 = encounterObj[0]['name'], amount0 = encounterObj[0]['rAmount'], parse0 = encounterObj[0]['rParse'], spec0 = encounterObj[0]['spec'][:7], numRuns0 = encounterObj[0]['numberOfFights'],
            name1 = encounterObj[1]['name'], amount1 = encounterObj[1]['rAmount'], parse1 = encounterObj[1]['rParse'], spec1 = encounterObj[1]['spec'][:7], numRuns1 = encounterObj[1]['numberOfFights'],
            name2 = encounterObj[2]['name'], amount2 = encounterObj[2]['rAmount'], parse2 = encounterObj[2]['rParse'], spec2 = encounterObj[2]['spec'][:7], numRuns2 = encounterObj[2]['numberOfFights'], 
            name3 = encounterObj[3]['name'], amount3 = encounterObj[3]['rAmount'], parse3 = encounterObj[3]['rParse'], spec3 = encounterObj[3]['spec'][:7], numRuns3 = encounterObj[3]['numberOfFights'], 
            name4 = encounterObj[4]['name'], amount4 = encounterObj[4]['rAmount'], parse4 = encounterObj[4]['rParse'], spec4 = encounterObj[4]['spec'][:7], numRuns4 = encounterObj[4]['numberOfFights'], 
            name5 = encounterObj[5]['name'], amount5 = encounterObj[5]['rAmount'], parse5 = encounterObj[5]['rParse'], spec5 = encounterObj[5]['spec'][:7], numRuns5 = encounterObj[5]['numberOfFights'], 
            name6 = encounterObj[6]['name'], amount6 = encounterObj[6]['rAmount'], parse6 = encounterObj[6]['rParse'], spec6 = encounterObj[6]['spec'][:7], numRuns6 = encounterObj[6]['numberOfFights'], 
            name7 = encounterObj[7]['name'], amount7 = encounterObj[7]['rAmount'], parse7 = encounterObj[7]['rParse'], spec7 = encounterObj[7]['spec'][:7], numRuns7 = encounterObj[7]['numberOfFights'], 
            avgParse = characterData['avgPar'], spec = characterData['spec'], name = characterData['name'], numRunsTotal = numRunsTotal, specList = characterData['specList'],
            metric = characterData['metric'], keyLevelCO = characterData['keyLvlCO'], server = characterData['server'],
            queryData = str(list(characterData.values()))))
        resp.set_cookie('userInfo', str(characterData))
        return resp


    elif request.method == 'POST':
        resp = make_response(render_template(loadingHtml))
        oldUserInfo = util.checkSetCookie(request.cookies.get('userInfo'))
        
        if specName.find('&') != -1 or specName == ' ' or specName.find('%') != -1: specName = '';
        
        queryOption = request.form.get('newQueryOption')
        if queryOption != None:
            if queryOption.isdigit(): keyLevelCO = queryOption;
            else: metricType = queryOption;
        
        newSpecName = request.form.get('newSpec')
        if newSpecName != None: specName = newSpecName;
        
        userInfo = {
            'name': name,
            'server': server,
            'spec': specName,
            'metric': metricType,
            'keyLvlCO': keyLevelCO,
            'rio': '',
            'specTog': oldUserInfo['specTog'],
            'rioTog': oldUserInfo['rioTog'],
            'pasteRioTog': oldUserInfo['pasteRioTog'],
            'avoidableDeathsTog': oldUserInfo['avoidableDeathsTog'],
            'specList': oldUserInfo['specList'],
            'encounter': [],
            'avgPar': oldUserInfo['avgPar']
            }
            
        resp.set_cookie('userInfo', str(userInfo))

        return resp

@app.route("/<name>/<server>/avoidable_deaths")
def avoidableDeathsPage(name, server):

    # unencrypt the url versions of the name, this lets it play nice with alt characters
    name = unquote(name)
    
    # generate authentication token
    authToken = api.getNewToken()
    # make sure the token is valid
    if authToken == 'Not Status Code 200': return error();
    
    # retrieve info from cookies as a dict
    queryData = util.checkSetCookie(request.cookies.get('userInfo'))
    
    # update values in case the url was entered and there is no cookie associated with the query
    queryData['name'] = name
    queryData['server'] = server
    
    # inilialize encounter class objects
    encounterObj = enc.newEncounterObj()
    
    # create a dictionary of avoidable abilities
    avoidableDamage = avDs.avoidableDamageAsDict(enc.encounterId)
    
    ad = {
        0: { 'runs': 0, 'avoidableDeaths': 0 },
        1: { 'runs': 0, 'avoidableDeaths': 0 },
        2: { 'runs': 0, 'avoidableDeaths': 0 },
        3: { 'runs': 0, 'avoidableDeaths': 0 },
        4: { 'runs': 0, 'avoidableDeaths': 0 },
        5: { 'runs': 0, 'avoidableDeaths': 0 },
        6: { 'runs': 0, 'avoidableDeaths': 0 },
        7: { 'runs': 0, 'avoidableDeaths': 0 } 
        }
    
    # assign functions to processes
    avDs.threadAvoidableDeaths(queryData, avoidableDamage, authToken, ad, enc.encounterId)
    
    if queryData['avgPar'] == 'error': return error();
    

    x = avDs.printAvoidableDamage(avoidableDamage, enc.encounterName, enc.encounterId)
    
    x = avDs.sortAvoidableDamageDict(x)


    return render_template(avoidableDeathsHtml, name = name + ' (' + server + ')', server = 'Avoidable Deaths',
        encName0 = enc.encounterName[0], ad0 = ad[0]['avoidableDeaths'], runs0 = ad[0]['runs'], adpr0 = avDs.adprCalc(0, ad), encText0 = avDs.returnDeaths(x, 0, enc.encounterName),
        encName1 = enc.encounterName[1], ad1 = ad[1]['avoidableDeaths'], runs1 = ad[1]['runs'], adpr1 = avDs.adprCalc(1, ad), encText1 = avDs.returnDeaths(x, 1, enc.encounterName),
        encName2 = enc.encounterName[2], ad2 = ad[2]['avoidableDeaths'], runs2 = ad[2]['runs'], adpr2 = avDs.adprCalc(2, ad), encText2 = avDs.returnDeaths(x, 2, enc.encounterName),
        encName3 = enc.encounterName[3], ad3 = ad[3]['avoidableDeaths'], runs3 = ad[3]['runs'], adpr3 = avDs.adprCalc(3, ad), encText3 = avDs.returnDeaths(x, 3, enc.encounterName),
        encName4 = enc.encounterName[4], ad4 = ad[4]['avoidableDeaths'], runs4 = ad[4]['runs'], adpr4 = avDs.adprCalc(4, ad), encText4 = avDs.returnDeaths(x, 4, enc.encounterName),
        encName5 = enc.encounterName[5], ad5 = ad[5]['avoidableDeaths'], runs5 = ad[5]['runs'], adpr5 = avDs.adprCalc(5, ad), encText5 = avDs.returnDeaths(x, 5, enc.encounterName),
        encName6 = enc.encounterName[6], ad6 = ad[6]['avoidableDeaths'], runs6 = ad[6]['runs'], adpr6 = avDs.adprCalc(6, ad), encText6 = avDs.returnDeaths(x, 6, enc.encounterName),
        encName7 = enc.encounterName[7], ad7 = ad[7]['avoidableDeaths'], runs7 = ad[7]['runs'], adpr7 = avDs.adprCalc(7, ad), encText7 = avDs.returnDeaths(x, 7, enc.encounterName)
        )

# error page
@app.route('/error')
def error(): return render_template(errorHtml);

if __name__ == '__main__':
	app.run(debug = False)