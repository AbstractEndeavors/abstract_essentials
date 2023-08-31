import requests
import json
import datetime
import time
import grabApi
import guiFunctions as guiFun
import dropDown as dropDown
import functions as fun
import callFuns
import json,urllib.request
from data.settings import rpcVals
from web3.contract import ContractEvent
from web3.contract import Contract
from web3._utils.events import get_event_data
from web3 import Web3
from web3.auto import w3
def getKeys(js):
  lsN = []
  try:
    for key in js.keys():
      lsN.append(key)
    return lsN
  except:
    return lsN
def changeGlob(x,y):
  globals()[x] = y
def create_ask(x,y):
        alph = get_alph()
        n = 'which '+str(y)+' would you like to use?\n'
        for i in range(0,len(x)):
                n = n + str(alph[i]) + ') '+str(x[i])+'\n'
        ask = input(n)
        i = find_it_alph(alph,str(ask))
        return x[i]
def call_glob():
    globals('last_api',ti())
def getDrop(js,st):
  if fun.isLs(st):
      fun.changeGlob('varDesc',st[0])
      st= st[1]
  keys,lsA = getKeys(js),[]
  for i in range(0,len(keys)):
    key = keys[i]
    lsA.append(guiFun.dropDown({"title":st,"ls":js[key],"key":key,"size":(fun.getLongest(js[key]),1),"default_value":None,"visible":True,"enable_events":True,}))
  return callFuns.defaultWindow(lsA,st)
def createDrop(js,title):
  return getDrop(js,title)
def createNewJsVar(jsN,js,st):
  jsN[str(st)] = js[str(st)]
  return jsN
def getFromJs(js,ls):
  jsN = {}
  for i in range(0,len(ls)):
    jsN = createNewJsVar(jsN,js,ls[i])
  return jsN
def getJsVarFromJsKey(js,var):
  ls,keys = [],getKeys(js)
  for i in range(0,len(keys)):
    ls.append(js[keys[i]][var])
  return ls
def getLsFroJsLSVar(ls,var):
  lsN=[]
  for i in range(0,len(ls)):
    if ls[i][var] not in lsN:
      lsN.append(ls[i][var])
  return lsN
def mkJsFroJsLs(js,ls,ls2):
  jsN = {}
  for i in range(0,len(ls)):
    jsN[ls2[i]] = getLsFroJsLSVar(js[ls[i]],ls2[i])
  return jsN
def ifAllInJsEq(js,keyLs,varLs):
  for i in range(0,len(keyLs)):
    if js[keyLs[i]] != varLs[i]:
      return False
  return True
def froLsJsGetOnly(lsJs,keyLs,varLs):
 for i in range(0,len(lsJs)):
   if ifAllInJsEq(lsJs[i],keyLs,varLs):
     return lsJs[i]
 return False
def isDict(js):
  if len(getKeys(js)) == 0:
    if str(js) == '{}':
      return True
    return False
  return True
def ifNotNone(x):
  if len(x) == 0:
    return True
  return False
def strAdd(ls):
  y = str(ls[0])
  for i in range(1,len(ls)):
    y = y+str(ls[i])
  return y
def addLikeJstoLs(ls,js2):
  lsA = []
  for i in range(0,len(ls)):
    lsA.append('')
    if ls[i] in js2:
      lsA[i] = js2[ls[i]]
  return ls,lsA
def addJstoJs(js,js2):
  keys = getKeys(js2)
  for i in range(0,len(keys)):
    js[keys[i]] = js2[keys[i]]
  return js
def removeFromJs(js,ls):
  keys,jsN = getKeys(js),{}
  for i in range(0,len(keys)):
    if keys[i] not in ls:
      jsN[keys[i]] = js[keys[i]]
  return jsN
def getStartLs():
  rpcJs,callV = fun.jsRead('data/rpcVariables.json'),fun.jsRead('data/callsV.json')
  keys = fun.getKeys(callV)
  jsN,largest = {},[0,0]
  for i in range(0,len(keys)):
      callKeys = fun.getKeys(callV[keys[i]]['pieces'])
      if len(callKeys) > largest[1]:
          largest = [i,len(callKeys)]
  callKeys = fun.getKeys(callV[keys[largest[0]]]['pieces'])
  for k in range(0,len(callKeys)):
      jsN[callKeys[k]] = []

  for i in range(0,len(keys)):
      callKeys = fun.getKeys(callV[keys[i]]['pieces'])
      for k in range(0,len(callKeys)):
          callKeys[k] = callKeys[k].replace('https://api.etherscan.io/api?','').replace('<br>','')
          if callKeys[k] not in jsN:
              jsN[callKeys[k]] = []
          if callV[keys[i]]['pieces'][callKeys[k]] not in jsN[callKeys[k]] and len(callV[keys[i]]['pieces'][callKeys[k]]) != 0:
              jsN[callKeys[k]].append(callV[keys[i]]['pieces'][callKeys[k]])
  return jsN
def getSizes(desc,ls,title):
  js = {}
  if title[:len('th')].lower() == 'th':
   title ='E'+title
  for i in range(0,len(ls)):
    desc = desc.replace('and'+ls[i],'&'+ls[i])
    ex = desc.split(ls[i]+'=')[1].split('&')[0]
    tot =len(ex)+int(float(len(ex))*float(0.2))
    if int(tot) < int(8):
      tot = int(8)
    js[ls[i]]={'size':len(ex),'example':str(ex),'pad':int(float(len(ex))*float(0.2)),'totSize':tot}
  return js,desc,title
def mkInputs(ls,prev,title,desc):
  sizeJs,desc,title = getSizes(desc,ls,title)
  lsA=[guiFun.txtBox({"text":desc,"key":None,"font":None,"background_color":None,"enable_events":False,"grab":None})]
  for i in range(0,len(ls)):
    lsA.append([guiFun.txtBox({"text":ls[i]}),
                guiFun.inputTxt({"text":prev[i],"size":(sizeJs[ls[i]]['totSize'],1),"font":None,"key":ls[i],"autoscroll":None,"disabled":False,"pad":(sizeJs[ls[i]]['pad'],0),"change_submits":False,"enable_events":True}),
                guiFun.txtBox({"text":'e.g. '+sizeJs[ls[i]]['example']+' | size: '+str(sizeJs[ls[i]]['size'])+' char.'}),
                guiFun.pushBox({"background_color":None})])
  return callFuns.defaultWindow(lsA,title)
def buildApi():
  title = createDrop({'apiCalls':getKeys(apiCallDesc)},[callJsData,'select api endpoint'])['apiCalls']
  js = apiCallDesc[title]
  inputs,prevInp = addLikeJstoLs(js['inputs'],fun.existJsRead('{}','prevInputs.json'))
  keyDrop = mkInputs(inputs,prevInp,title,js['description'])
  prev = fun.jsRead('prevInputs.json')
  fun.pen(str(removeFromJs(addJstoJs(prev,keyDrop),[0])),'prevInputs.json')
  return concateUrl(js['pieces'],keyDrop),title
def concateUrl(js,keyDrop):
  keys,beg = getKeys(js),'https://api.'+scanners+'/api?'
  for i in range(0,len(keys)):
    key = keys[i]
    curr = js[keys[i]]
    if ifNotNone(curr):
      beg = strAdd([beg,str(key),'=',str(keyDrop[key]),'&'])
    elif keys[i] == 'apikey':
      beg = strAdd([beg,str(keys[i]),'=',grabApi.apiKeys(scanners)])
    else:
      beg = strAdd([beg,str(keys[i]),'=',str(fun.mkLs(curr)[0]),'&'])
  return beg
def createMix():
    js = getStartLs()
    keys,lsNone,lsA,jsN = fun.getKeys(js),[],[],{}
    for i in range(0,len(keys)):
        if len(js[keys[i]]) == 0:
            lsA.append(dropDown.getInput(keys[i],''))
        else:
            lsA.append(dropDown.getMenuLs(keys[i],js[keys[i]]))
    lsA.append(dropDown.getButtons(['override','OK']))
   
    values = dropDown.defaultOverWindow(lsA,'customCreate')
    keys = fun.getKeys(values)
    for i in range(0,len(keys)):
        if values[keys[i]] is not None:
            if len(values[keys[i]]) != 0:
                jsN[keys[i]] = values[keys[i]]
                if fun.isLs(values[keys[i]]):
                    jsN[keys[i]] = values[keys[i]][0]
                jsN[keys[i]] = jsN[keys[i]]
    jsN['apikey'] = grabApi.apiKeys(scanners)
    return concateUrl(jsN,values)
def theVars():
  return [[callJsData,apiCallDesc,callsTemplate,callVars,rpcVariables],['callJsData','apiCallDesc','callsTemplate','callVars','rpcVariables']]
def loadIt():
  ls = theVars()  
  for k in range(0,len(ls[0])):
    changeGlob(ls[1][k],json.loads(ls[0][k]))
  return 
def dumpIt():
  n,ls = '',theVars()
  for k in range(0,len(ls[1])):
    dump = ls[0][k]
    if fun.isLs(ls[0][k]) != False:
      dump = json.dumps(dump)
    n = n + ls[1][k]+'='+str(dump)+'\n'
  fun.pen(n,'allJs.py')
def selectRpcVals():
  network = createDrop(getFromJs(rpcJs,['networks']),'select the network you want to utilize')['networks']
  mainnet = createDrop(mkJsFroJsLs(rpcJs,[network],['network']),'select the type of network you want to utilize')['network']
  netType = createDrop(mkJsFroJsLs(rpcJs,[network],['RPC']),'select the rpc you want to utilize')['RPC']
  return froLsJsGetOnly(rpcJs[network],['network','RPC'],[mainnet,netType])
def getManualRpc():
    netName,chainId,nativeCurrency,explorer,rpc,scanners,w3 = grabApi.deriveFrom(selectRpcVals())
global scanners,net,ch_id,main,file,w3,network,add,B_L,B_G,topic,callJsData,apiCallDesc,callsTemplate,callVars,rpcVariables

from allJs import callJsData,apiCallDesc,callsTemplate,callVars,rpcVariables
netName,chainId,nativeCurrency,explorer,rpc,scanners,w3 = grabApi.deriveFrom(rpcVals)
