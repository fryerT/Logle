from . import wowAPI as api
from . import utility as util
import threading

# combines encounterName[] and encounterId[] into one dictionary
def encounterAsDict(encounterName, encounterId):

    encounterDict = {}
    
    for i in range(len(encounterName)): encounterDict[encounterId[i]] = encounterName[i];
    
    return encounterDict

# used to make a copy of the encounterAvoidableDamage dictionary
def avoidableDamageAsDict(encounterId):
    encounterAvoidableDamage = {
        
        encounterId[0]: {
            388884: {"name": "Arcane Rain (Spellbound Scepter)", "count": 0},
            388957: {"name": "Riftbreath (Arcane Ravager)", "count": 0},
            378011: {"name": "Deadly Winds (Guardian Sentry)", "count": 0},
            377516: {"name": "Dive Bomb (Territorial Eagle)", "count": 0},
            377524: {"name": "Dive Bomb (Alpha Eagle)", "count": 0},
            377383: {"name": "Gust (Alpha Eagle)", "count": 0},
            390918: {"name": "Seed Detonation (Vile Lasher)", "count": 0},
            387932: {"name": "Astral Whirlwind (Algeth'ar Echoknight)", "count": 0},
            385970: {"name": "Arcane Orb, Spawn (Vexamus)", "count": 0},
            386201: {"name": "Corrupted Mana (Vexamus)", "count": 0},
            388546: {"name": "Arcane Fissure, Swirly (Vexamus)", "count": 0},
            377034: {"name": "Overpowering Gust (Crawth)", "count": 0},
            376449: {"name": "Firestorm (Crawth)", "count": 0},
            393122: {"name": "Roving Cyclone (Crawth)", "count": 0},
            388799: {"name": "Germinate (Overgrown Ancient)", "count": 0},
            388625: {"name": "Branch Out (Overgrown Ancient)", "count": 0},
            388822: {"name": "Power Vacuum (Echo of Doragosa)", "count": 0},
            374361: {"name": "Astral Breath (Echo of Doragosa)", "count": 0},
            389007: {"name": "Arcane Rift / Wild Energy (Echo of Doragosa)", "count": 0},
            388996: {"name": "Energy Eruption (Echo of Doragosa)", "count": 0}
            },
        
        encounterId[1]: {
            368297: {"name": "Toxic Trap, Trigger (Bonebolt Hunter)", "count": 0},
            368299: {"name": "Toxic Trap, Area (Bonebolt Hunter)", "count": 0},
            382556: {"name": "Ragestorm (Bracken Warscourge)", "count": 0},
            384673: {"name": "Spreading Rot (Decay Ritual, Environment)", "count": 0},
            378055: {"name": "Burst (Decaying Slime)", "count": 0},
            378054: {"name": "Withering Away! (Decaying Slime)", "count": 0},
            374569: {"name": "Burst (Monstrous Decay)", "count": 0},
            373943: {"name": "Stomp (Wilted Oak)", "count": 0},
            385303: {"name": "Teeth Trap (Environment)", "count": 0},
            385524: {"name": "Sentry Fire (Environment)", "count": 0},
            385805: {"name": "Violent Whirlwind (Stinkbreath)", "count": 0},
            379425: {"name": "Rotting Creek (Environment)", "count": 0},
            383392: {"name": "Rotting Surge, Impact (Filth Caller)", "count": 0},
            383399: {"name": "Rotting Surge, periodic (Filth Caller)", "count": 0},
            377830: {"name": "Bladestorm (Rira Hackclaw)", "count": 0},
            384148: {"name": "Ensnaring Trap (Gutshot)", "count": 0},
            384558: {"name": "Bounding Leap (Rotfang Hyena, Gutshot)", "count": 0},
            376797: {"name": "Decay Spray (Treemouth)", "count": 0},
            373944: {"name": "Rotburst Totem, Spawn (Decatriarch Wratheye)", "count": 0},
            376170: {"name": "Choking Rotcloud, Frontal (Decatriarch Wratheye)", "count": 0},
            376149: {"name": "Choking Rotcloud, Area (Decatriarch Wratheye)", "count": 0},
            379425: {"name": "Decaying Fog (Environment, Decatriarch Wratheye)", "count": 0}
            },
        
        encounterId[2]: {
            374075: {"name": "Seismic Slam (Primalist Geomancer)", "count": 0},
            393444: {"name": "Spear Flurry / Gushing Wound (Refti Defender)", "count": 0},
            374045: {"name": "Expulse (Containment Apparatus)", "count": 0},
            375215: {"name": "Cave In (Curious Swoglet)", "count": 0},
            374563: {"name": "Dazzle (Dazzling Dragonfly)", "count": 0},
            374741: {"name": "Magma Crush (Flamecaller Aymi)", "count": 0},
            375080: {"name": "Whirling Fury (Squallbringer Cyraz)", "count": 0},
            385168: {"name": "Thunderstorm (Primalist Galesinger)", "count": 0},
            375384: {"name": "Rumbling Earth (Primalist Earthshaker)", "count": 0},
            383204: {"name": "Crashing Tsunami (Environment)", "count": 0},
            390290: {"name": "Flash Flood (Infuser Sariya)", "count": 0},
            383935: {"name": "Spark Volley (Watcher Irideus)", "count": 0},
            389446: {"name": "Nullifying Pulse (Nullification Device, Watcher Irideus)", "count": 0},
            385691: {"name": "Belly Slam (Gulping Goliath)", "count": 0},
            386757: {"name": "Hailstorm (Khajin the Unyielding)", "count": 0},
            386562: {"name": "Glacial Surge (Khajin the Unyielding)", "count": 0},
            386295: {"name": "Avalanche (Khajin the Unyielding)", "count": 0},
            390118: {"name": "Frost Cyclone (Khajin the Unyielding)", "count": 0},
            387474: {"name": "Infused Globule, Impact (Primal Tsunami)", "count": 0},
            387359: {"name": "Waterlogged (Primal Tsunami)", "count": 0},
            387363: {"name": "Infused Globule, Explosion (Primal Tsunami)", "count": 0},
            388786: {"name": "Rogue Waves (Primal Tsunami)", "count": 0}
            },
        
        encounterId[3]: {
            372459: {"name": "Burning (Environment)", "count": 0},
            382708: {"name": "Volcanic Guard (Qalashi Warden)", "count": 0},
            372583: {"name": "Binding Spear, Impact (Qalashi Hunter)", "count": 0},
            373540: {"name": "Binding Spear, periodic (Qalashi Hunter)", "count": 0},
            376186: {"name": "Eruptive Crush, Area (Overseer Lahar)", "count": 0},
            383928: {"name": "Eruptive Crush, Projectiles (Overseer Lahar)", "count": 0},
            395427: {"name": "Burning Roar (Overseer Lahar)", "count": 0},
            372372: {"name": "Magma Fist (Qalashi Trainee)", "count": 0},
            379410: {"name": "Throw Lava (Qalashi Lavabearer)", "count": 0},
            372208: {"name": "Djaradin Lava (Qalashi Lavabearer)", "count": 0},
            372203: {"name": "Scorching Breath (Qalashi Irontorch)", "count": 0},
            372293: {"name": "Conflagrant Battery (Irontorch Commander)", "count": 0},
            378831: {"name": "Explosive Concoction (Qalashi Plunderer)", "count": 0},
            373756: {"name": "Magma Wave (Chargath, Bane of Scales)", "count": 0},
            375397: {"name": "Lava Splash (Chargath, Bane of Scales)", "count": 0},
            375061: {"name": "Blazing Eruption (Forgemaster Gorek)", "count": 0},
            375241: {"name": "Forgestorm (Forgemaster Gorek)", "count": 0},
            374397: {"name": "Heated Swings, Jump (Forgemaster Gorek)", "count": 0},
            374517: {"name": "Heated Swings, Jump (Forgemaster Gorek)", "count": 0},
            381482: {"name": "Forgefire (Forgemaster Gorek)", "count": 0},
            375071: {"name": "Magma Lob (Magmatusk)", "count": 0},
            375204: {"name": "Liquid Hot Magma (Magmatusk)", "count": 0},
            375449: {"name": "Blazing Charge (Magmatusk)", "count": 0},
            375535: {"name": "Lava Wave (Magmatusk)", "count": 0},
            377204: {"name": "The Dragon's Kiln (Warlord Sargha)", "count": 0},
            377477: {"name": "Burning Ember (Warlord Sargha)", "count": 0},
            377542: {"name": "Burning Ground (Warlord Sargha)", "count": 0},
            391773: {"name": "The Dragon's Eruption (Warlord Sargha)", "count": 0}
            },
        
        encounterId[4]: {
            372696: {"name": "Excavating Blast (Primal Juggernaut)", "count": 0},
            372697: {"name": "Jagged Earth (Primal Juggernaut)", "count": 0},
            373458: {"name": "Stone Missile (Primal Terrasentry)", "count": 0},
            372088: {"name": "Blazing Rush, Hit (Defier Draghar)", "count": 0},
            372796: {"name": "Blazing Rush, DoT (Defier Draghar)", "count": 0},
            385292: {"name": "Molten Steel (Defier Draghar)", "count": 0},
            378968: {"name": "Flame Patch (Scorchling)", "count": 0},
            373973: {"name": "Blaze of Glory, AoE (Primalist Flamedancer)", "count": 0},
            373977: {"name": "Blaze of Glory, Projectile (Primalist Flamedancer)", "count": 0},
            391727: {"name": "Storm Breath (Thunderhead)", "count": 0},
            391724: {"name": "Flame Breath (Flamegullet)", "count": 0},
            373614: {"name": "Burnout (Blazebound Destroyer)", "count": 0},
            385311: {"name": "Thunderstorm (Primalist Shockcaster)", "count": 0},
            392406: {"name": "Thunderclap (Storm Warrior) probably not avoidable for melee?", "count": 0},
            392399: {"name": "Crackling Detonation (Primal Thundercloud)", "count": 0},
            384024: {"name": "Hailbombs, Projectiles (Melidrussa Chillworm)", "count": 0},
            372863: {"name": "Ritual of Blazebinding (Kokia Blazehoof)", "count": 0},
            372811: {"name": "Molten Boulder, Projectile (Kokia Blazehoof)", "count": 0},
            372819: {"name": "Molten Boulder, Explosion (Kokia Blazehoof)", "count": 0},
            372820: {"name": "Scorched Earth (Kokia Blazehoof)", "count": 0},
            373087: {"name": "Burnout (Blazebound Firestorm, Kokia Blazehoof)", "count": 0},
            381526: {"name": "Roaring Firebreath (Kyrakka)", "count": 0},
            384773: {"name": "Flaming Embers (Kyrakka)", "count": 0}
            },
        
        encounterId[5]: {
            370766: {"name": "Crystalline Rupture (Crystal Thrasher)", "count": 0},
            371021: {"name": "Splintering Shards, Aura (Crystal Thrasher)", "count": 0},
            375649: {"name": "Infused Ground (Arcane Tender)", "count": 0},
            375591: {"name": "Sappy Burst (Volatile Sapling / Bubbling Sapling)", "count": 0},
            371352: {"name": "Forbidden Knowledge (Unstable Curator)", "count": 0},
            387067: {"name": "Arcane Bash (Arcane Construct)", "count": 0},
            374868: {"name": "Unstable Power (Astral Attendant)", "count": 0},
            386536: {"name": "Null Stomp (Nullmagic Hornswog)", "count": 0},
            374523: {"name": "Stinging Sap (Leymor)", "count": 0},
            386660: {"name": "Erupting Fissure (Leymor)", "count": 0},
            374582: {"name": "Explosive Brand, Area (Leymor)", "count": 0},
            385579: {"name": "Ancient Orb (Azureblade)", "count": 0},
            390462: {"name": "Ancient Orb Fragment (Azureblade)", "count": 0},
            389855: {"name": "Unstable Magic (Draconic Image / Draconic Illusion, Azureblade)", "count": 0},
            387150: {"name": "Frozen Ground (Telash Greywing)", "count": 0},
            384699: {"name": "Crystalline Roar (Umbrelskul)", "count": 0},
            385078: {"name": "Arcane Eruption (Umbrelskul)", "count": 0},
            385267: {"name": "Crackling Vortex (Umbrelskul)", "count": 0}
            },
        
        encounterId[6]: {
            384868: {"name": "Multi-Shot (Nokhud Longbow)", "count": 0},
            384479: {"name": "Rain of Arrows (Nokhud Longbow)", "count": 0},
            384336: {"name": "War Stomp (Nokhud Plainstomper / Nokhud Lancemaster / Nokhud Defender)", "count": 0},
            386028: {"name": "Thunder Clap (Primalist Thunderbeast)", "count": 0},
            384882: {"name": "Stormsurge Lightning (Stormsurge Totem)", "count": 0},
            386694: {"name": "Stormsurge (Stormsurge Totem)", "count": 0},
            386912: {"name": "Stormsurge Cloud (Stormsurge Totem)", "count": 0},
            396376: {"name": "Chant of the Dead (Ukhel Deathspeaker)", "count": 0},
            387611: {"name": "Necrotic Eruption (Ukhel Corruptor)", "count": 0},
            387629: {"name": "Rotting Wind (Desecrated Ohuna)", "count": 0},
            388451: {"name": "Stormcaller's Fury (Environment)", "count": 0},
            382233: {"name": "Broad Stomp (Nokhud Defender / Batak)", "count": 0},
            382274: {"name": "Vehement Charge (Nokhud Defender / Balara)", "count": 0},
            374711: {"name": "Ravaging Spear (Nokhud Warspear / Balara)", "count": 0},
            385916: {"name": "Tectonic Stomp (Granyth)", "count": 0},
            386920: {"name": "Raging Lightning (The Raging Tempest)", "count": 0},
            391967: {"name": "Electrical Overload (The Raging Tempest)", "count": 0},
            386916: {"name": "The Raging Tempest (The Raging Tempest)", "count": 0},
            388104: {"name": "Ritual of Desecration (Environment)", "count": 0},
            385193: {"name": "Earthsplitter (Maruuk) - TODO which is correct?", "count": 0},
            384960: {"name": "Earthsplitter (Maruuk) - TODO which is correct?", "count": 0},
            395669: {"name": "Aftershock (Maruuk)", "count": 0},
            386063: {"name": "Frightful Roar (Maruuk)", "count": 0},
            386037: {"name": "Gale Arrow, Whirls (Teera)", "count": 0},
            376685: {"name": "Iron Stampede (Balakar Khan) - TODO which is correct?", "count": 0},
            376688: {"name": "Iron Stampede (Balakar Khan) - TODO which is correct?", "count": 0},
            375943: {"name": "Upheaval (Balakar Khan)", "count": 0},
            376737: {"name": "Lightning (Balakar Khan)", "count": 0},
            376892: {"name": "Crackling Upheaval (Balakar Khan)", "count": 0},
            376899: {"name": "Crackling Cloud (Balakar Khan) - TODO is first tick avoidable?", "count": 0}
            },
        
        encounterId[7]: {
            369811: {"name": "Brutal Slam (Hulking Berserker)", "count": 0},
            369854: {"name": "Throw Rock (Burly Rock-Thrower)", "count": 0},
            382576: {"name": "Scorn of Tyr (Earthen Guardian)", "count": 0},
            369573: {"name": "Heavy Arrow (Baelog, The Lost Dwarves)", "count": 0},
            369792: {"name": 'Skullcracker (Eric "The Swift", The Lost Dwarves)', "count": 0},
            375286: {"name": "Searing Cannonfire (The Lost Dwarves)", "count": 0},
            377825: {"name": "Burning Pitch (The Lost Dwarves)", "count": 0},
            369703: {"name": "Thundering Slam (Bromach)", "count": 0},
            368996: {"name": "Purging Flames (Emberon)", "count": 0},
            369029: {"name": "Heat Engine (Emberon)", "count": 0},
            369052: {"name": "Seeking Flame (Vault Keeper, Emberon)", "count": 0},
            376325: {"name": "Eternity Zone (Chrono-Lord Deios)", "count": 0},
            377561: {"name": "Time Eruption (Chrono-Lord Deios)", "count": 0}
            }
        }
    return encounterAvoidableDamage

def getAvoidableDeaths(queryData, encounterAvoidableDamage, authToken, i, ad, encounterId):

    # playerName, serverName, specName, metricType, keyLevelCutoff, 
    playerName = queryData['name']
    serverName = queryData['server']
    
    # grabs all fights for the player based on encounter id
    logs = api.getPlayerPerformanceFromEncounter(playerName, authToken, encounterId[i], '', serverName, 'dps', True)

    # gets the relevant data fron the json text
    try: allFights = logs["data"]["characterData"]["character"]["encounterRankings"]["ranks"];
    # if the information is incorrect, exit the function and do not continue
    except: 
        queryData['avgPar'] = 'error'
        return 0

    def parseAvoidableDeaths(queryList, encounterAvoidableDamage, i, ad):
        for x in queryList:
            try: 
                encounterAvoidableDamage[encounterId[i]][x['killingAbilityGameID']]['count'] += 1
                ad[i]['avoidableDeaths'] += 1
            except: pass;
        return 0

    def parseFights(allFights, queryData, authToken, encounterAvoidableDamage, i, ad):
    
        # iterates through all the fights of the selected encounter to analyze amount/parse
        for fight in allFights:
            
            if fight['bracketData'] >= 2:
                
                
                ad[i]['runs'] += 1
            
                code = fight['report']['code']
                fightId = fight['report']['fightID']
                specc = fight['spec']
                charId = api.getCharacterId(queryData['name'].capitalize(), specc, code, fightId, authToken)
                    
                testing = api.reportInfo(code, fightId, charId, authToken)
                try: allTests = testing['data']['reportData']['report']['events']['data']
                except: error();
                
                if len(allTests) != 0:
                
                    deathLists = util.splitList(allTests)

                    t0 = threading.Thread(target = parseAvoidableDeaths, args = (deathLists[0], encounterAvoidableDamage, i, ad,))
                    t1 = threading.Thread(target = parseAvoidableDeaths, args = (deathLists[1], encounterAvoidableDamage, i, ad,))
                    t2 = threading.Thread(target = parseAvoidableDeaths, args = (deathLists[2], encounterAvoidableDamage, i, ad,))
                    t3 = threading.Thread(target = parseAvoidableDeaths, args = (deathLists[3], encounterAvoidableDamage, i, ad,))
                    t0.start()
                    t1.start()
                    t2.start()
                    t3.start()
                    t0.join()
                    t1.join()
                    t2.join()
                    t3.join()
                    
        return 0
    
    

    
    fightLists = util.splitList(allFights)
    
    t0 = threading.Thread(target = parseFights, args = (fightLists[0], queryData, authToken, encounterAvoidableDamage, i, ad,))
    t1 = threading.Thread(target = parseFights, args = (fightLists[1], queryData, authToken, encounterAvoidableDamage, i, ad,))
    t2 = threading.Thread(target = parseFights, args = (fightLists[2], queryData, authToken, encounterAvoidableDamage, i, ad,))
    t3 = threading.Thread(target = parseFights, args = (fightLists[3], queryData, authToken, encounterAvoidableDamage, i, ad,))
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t0.join()
    t1.join()
    t2.join()
    t3.join()

def printAvoidableDamage(encounterAvoidableDamage, encounterName, encounterId):

    # initialize list to store avoidable deaths
    remember = {}
    # figure out how many times each avoidable damage killed the player and add it to the list
    for encounterKey in encounterAvoidableDamage:
        x = []
        for abilityKey in encounterAvoidableDamage[encounterKey]:
            if encounterAvoidableDamage[encounterKey][abilityKey]['count'] != 0: 
                x.append(abilityKey)
        remember[encounterKey] = x

    
    # print the list of deaths caused by avoidable damage
    encounterDict = encounterAsDict(encounterName, encounterId)
    translatedRemember = {}
    for encounterKey in remember:
        x = {}
        for abilityKey in remember[encounterKey]:
            y = encounterAvoidableDamage[encounterKey][abilityKey]
            x[y['name']] = y['count'] 
        translatedRemember[encounterDict[encounterKey]] = x
    
    return translatedRemember

def sortAvoidableDamageDict(dictObj):

    sortedDict = {}
    
    for key in dictObj:
   
        sortedDict[key] = sorted(dictObj[key].items(), key = lambda item: item[1], reverse = True)
        
    return sortedDict

def returnDeaths(dictObj, encNumber, encounterName):
    
    deaths = ''
    for i in range(len(dictObj)):
        try: 
            death = dictObj[encounterName[encNumber]][i];
            p = death[0]
            p = p.split(' (')
            o = death[1]
            death = '► ' + str(p[0]) + ': ' + str(o)
        except: death = '';
        if i == 0: deaths = death;
        else: deaths = deaths + '\n' + death;
    deaths = deaths.split('\n')
    return deaths
    
def adprCalc(encNumber, ad):
    if ad[encNumber]['runs'] == 0: return 0;
    adpr = ad[encNumber]['avoidableDeaths'] / ad[encNumber]['runs']
    adpr = '{:.1f}'.format(adpr)
    return adpr
    
def threadAvoidableDeaths(queryData, avoidableDamage, authToken, ad, encounterId):
    t0 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 0, ad, encounterId,))
    t1 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 1, ad, encounterId,))
    t2 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 2, ad, encounterId,))
    t3 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 3, ad, encounterId,))
    t4 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 4, ad, encounterId,))
    t5 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 5, ad, encounterId,))
    t6 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 6, ad, encounterId,))
    t7 = threading.Thread(target = getAvoidableDeaths, args = (queryData, avoidableDamage, authToken, 7, ad, encounterId,))

    # rev em up
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()

    # so fast
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    
    return
