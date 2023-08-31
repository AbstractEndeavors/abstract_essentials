#!/usr/bin/env python
import PySimpleGUI as sg
import rpc as rpcFuns
import slectApi as selApi
import grabApi
import functions as fun
import json,urllib.request
import time
import json
import requests
import clipboard
from pathlib import Path
import os
def chooseSave(text):
  layout = [[[sg.Input(key='-INPUT-'),sg.FolderBrowse('FolderBrowse',key='path')],[sg.Input('',key='foldName'),sg.Button("createFold")],[sg.Input('input File Name',key='fileName'),sg.Button("createFile")],[sg.Input('',key='created'),sg.Button('saveFile')]]]
  window = sg.Window('Title', layout)
  while True:
      event, values = window.read()
      if event == sg.WINDOW_CLOSED:
     
        window.close()
        break
      elif event == 'saveFile':
        fun.pen(text,values['created'])
        window.close()
        break
      elif event == 'createFold':
        if values['foldName'] != '':
          fun.mkDirsAll(fun.mkLs(values['foldName'].split(slash)))
      elif event == 'createFile':
          window['created'].update(value=os.path.join(ifRet(values['foldName'],'',values['path']),values['fileName']))
          filename = values['-INPUT-']
          if Path(filename).is_file():
              try:
                  with open(filename, "rt", encoding='utf-8') as f:
                      text = f.read()
                  popup_text(filename, text)
              except Exception as e:
                  print("Error: ", e)
def ifRet(x,y,z):
  if x == y:
    return z
  return x
def homeIt():
  changeGlob('home',os.getcwd()) 
  changeGlob('slash','/') 
  if '/' not in home:
    changeGlob('slash','//') 
def copyToClBoard(x):
  clipboard.copy(str(x))
def changeGlob(x,y):
  globals()[x] = y
def ti():
    return time.time()
def getKeys(js):
  lsN = []
  try:
    for key in js.keys():
      lsN.append(key)
    return lsN
  except:
    return lsN
def sites(A):
    U = [A]
    check_sleep(last_api[1])
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)['result']
        changeGlob('lastRequest',time.time())
    return JS
def sites(A):
    U = [A]
    check_sleep(fun.existJsRead('[0,0]','last_api.txt')[1])
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        changeGlob('lastRequest',time.time())
        return r.json()
def check_sleep(x):
    curr = ti() - float(x)
    if curr < 1.5:
        printer('asdffsdsdf')
        time.sleep(1.5 - curr)
    return
def getRound(x):
  last_api = fun.existJsRead('[0,0]','last_api.txt')
  check_sleep(last_api[1])
  data = urllib.request.urlopen(x).read()
  last_api[1] = ti()
  fun.pen(last_api,'last_api.txt')
  printer(data)
  return data
def printer(x):
  changeGlob('recentPrint',x)
  print(x)
def sites_scan(x):
    end = 0
    printer(x)
    last_api = fun.existJsRead('[0,0]','last_api.txt')
    check_sleep(last_api[1])
    output = sites(x)
    output = sites(x)
    if output['message'] == 'NOTOK':
      return output
    fun.pen(output,'lastOut.txt')
    last_api[1] = ti()
    fun.pen(last_api,'last_api.txt')
    printer(output)
    if output == {'status': '0', 'message': 'No records found', 'result': []}:
        return output
    if str(output['result']) == '{}':
        return 0
    try:
        js = output[x]['results']
        c = ','
        if len(curr_prices) == 0:
            c = ''
        pen(str(curr_prices).replace('}','')+c+'"'+str(x)+'":"'+str(js)+'"}','price_now.txt')
        return js
    except:
        printer('scan sleeping ')
        printer(x,output)
        time.sleep(20)
def changeKeys(js,ls):
  jsN = {}
  keys = getKeys(js)
  for k in range(0,len(keys)):
    newVal = js[keys[k]]
    for i in range(0,len(ls)):
      if keys[k] == ls[i][0]:
        keys[k] = ls[i][1]
    jsN[keys[k]] = newVal
  return jsN
def second_window():
    sg.theme('DarkGrey14')
    menu_def = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo', 'Options::this_is_a_menu_key'], ],
                ['&Toolbar', ['---', 'Command &1', 'Command &2','---', 'Command &3', 'Command &4']],
                ['&NetworkTools', ['---','RPC',['Add RPC', 'Choose RPC','get Manual RPC'], 'Choose RPC &2','---', 'Command &3', 'Command &4']],
                ['APIs',['chainScan'],
                ['&Help', ['&About...']]]]
    right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]
    layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')],
        [sg.Text('Right click me for a right click menu example')],
        [sg.ButtonMenu('ButtonMenu',  right_click_menu, key='-BMENU-', text_color='red', disabled_text_color='green'), sg.Button('Plain Button')],
        [sg.Text('Script output....', size=(40, 1))],
        #[sg.Output(size=(88, 20), font='Courier 10',key='output')],
        [sg.Multiline(size=(88, 20), font='Courier 10',key='output')],
        [sg.Button('create API'), sg.Button('Preset API'),sg.Button('Choose RPC'),sg.Button('Add RPC'),sg.Button('EXIT')],
        [sg.Text('scan function'),sg.Input('',key='scanFunction'),sg.Push()],
        [sg.Text('api url',size=(15, 1)), sg.Input('input scan URL',focus=True,  key='scan'), sg.Button('SCAN'), sg.Button('copyUrl'),sg.Button('saveOutput')],
        [sg.Frame('',[[sg.Text('Network Name'),sg.Input('',key='NetworkName'),sg.Push()],[sg.Text('network'),sg.Combo(['Mainnet','TestNet'],key='network'),sg.Push()],[sg.Text('nativeCurrency'),sg.Input('',key='nativeCurrency'),sg.Push()],[sg.Text('chainId'),sg.Input('',key='chainId'),sg.Push()],[sg.Text('RPC'),sg.Input('',key='RPC'),sg.Push()],[sg.Text('BlockExplorer'),sg.Input('',key='blockExplorer'),sg.Push()],[sg.Text('contractName'),sg.Input('',key='contractName'),sg.Push()]],pad=(0,0),visible=True, background_color='#1B2838', expand_x=True, border_width=0, grab= True)]]
    window = sg.Window('Script launcher', layout)
    # ---===--- Loop taking in user input and using it to call scripts --- #
    while True:
        event, values = window.read()
        if event == 'EXIT'  or event == sg.WIN_CLOSED:
            break # exit button clicked
        if event == 'create API':
            url = selApi.createMix()
            window['output'].update(value=url)
            window['scan'].update(value=url)
        elif event == 'Preset API':
            scanUrl,callDesc = selApi.buildApi()
            window['scanFunction'].update(value=callDesc)
            window['scan'].update(value=scanUrl)
        elif event == 'saveOutput':
          chooseSave(str(recentPrint))
        elif event == 'SCAN':
              #data = urllib.request.urlopen(values['scan']).read()
              fun.pen(json.dumps(sites(values['scan'])['result']),'recent.json')
              window['output'].update(value=fun.reader('recent.json'))
              #printer()
              #printer(data)
        elif event == 'copyUrl':
          copyToClBoard(values['scan'])
        elif event == 'Choose RPC':
            changeKeys(rpcFuns.chooseDefaultRPC(),[['netName','NetworkName']])
            rpcVals = json.loads(fun.reader('currRPCvals.json'))
            upLs = ['NetworkName','network','nativeCurrency','chainId','blockExplorer','RPC']
            for k in range(0,len(upLs)):
              if upLs[k] in rpcVals:
                window[upLs[k]].update(value=rpcVals[upLs[k]])
        elif event == 'Add RPC':
            rpcFuns.AddRPC()
def test_menus():
    sg.theme('LightGreen')
    sg.set_options(element_padding=(0, 0))
    # ------ Menu Definition ------ #

    # ------ GUI Defintion ------ #
    layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')],
        [sg.Text('Right click me for a right click menu example')],
        [sg.Output(size=(60, 20))],
        [sg.ButtonMenu('ButtonMenu',  right_click_menu, key='-BMENU-', text_color='red', disabled_text_color='green'), sg.Button('Plain Button')],
        [sg.Button('Run'), sg.Button('Shortcut 1'), sg.Button('Fav Program'), sg.Button('EXIT')],[sg.Text('Your output will go here', size=(40, 1))],[sg.Output(size=(127, 30), font=('Helvetica 10'))],[sg.Text('Command History'),sg.Text('', size=(20, 3), key='history')],[sg.ML(size=(85, 5), enter_submits=True, key='query', do_not_clear=False),sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))],]
    window = sg.Window("Windows-like program",layout,default_element_size=(12, 1),default_button_element_size=(12, 1))
    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # ------ Process menu choices ------ #
        if event == 'chainScan':
            second_window()
        if event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 1.0', 'PySimpleGUI Version', sg.get_versions())
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
        elif event == 'Properties':
            second_window()
    window.close()
changeGlob('recentPrint','')
homeIt()
second_window()
