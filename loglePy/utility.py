import requests
import ast

def checkSetCookie(requestCookiesGet):
    
    # default values for the cookie
    default = {
        'name': '',
        'server': '',
        'spec': '',
        'metric': 'DPS',
        'keyLvlCO': '2',
        'rio': '',
        'specTog': 'false',
        'rioTog': 'false',
        'pasteRioTog': 'false', 
        'avoidableDeathsTog': 'false',
        'specList': [],
        'avgPar': ''}
    
    
    # get the cookie from the user
    queryInfo = requestCookiesGet
    
    # attempt to convert the cookie into a dict object
    try:
        queryInfo = ast.literal_eval(queryInfo)
        
        # reset the cookie to defaults if the keys are different
        if default.keys() != queryInfo.keys(): queryInfo = default;
        
    # if the cookie cannot be converted to a dict object,set cookie to default
    except: queryInfo = default;

    return queryInfo



# splits a list into 4 parts and returns them as a list
def splitList(listObj):

    splitList = []
    
    # divide the original list into two lists
    x = listObj[:len(listObj)//2]
    y = listObj[len(listObj)//2:]
    
    # divide each of the half lists and set them
    splitList.append(x[:len(x)//2])
    splitList.append(x[len(x)//2:])
    splitList.append(y[:len(y)//2])
    splitList.append(y[len(y)//2:])
    
    return splitList

