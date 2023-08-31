import PySimpleGUI as sg
import functions as fun
def changeGlob(x,y):
    globals()[x] = y
    return y
def getDropLs(na,ls):
    return [sg.Combo(ls)]
def getDefMenu():
    return [sg.Menu([['File', ['Open', 'Save', 'Exit',]],['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],['Help', 'About...'],])]
def getDefButtons():
    return [sg.OK('OK'),sg.Button('Show'),sg.Button('Auto'),sg.Button('Exit')]
def getDefaultSetOptions():
    return sg.set_options(suppress_raise_key_errors=bool(False), suppress_error_popups=bool(False), suppress_key_guessing=bool(False))
def getDefaults():
    return [getDefMenu()]
def getDefaultLayout(sg1):
    lsA = getDefaults()
    lsA.append(sg1)
    lsA.append(getDefButtons())
    return lsA
def getMenu(ls):
    return [sg.Menu(ls)]
def getyChkBox(na,boo):
    return [js,sg.Checkbox(na, size=(10,1),default=boo)],
def getLsSect(js):
    return [sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))]
def getBrwsSect(na):
    return [sg.Text('Your Folder', size=(15, 1), auto_size_text=bool(false), justification='right'),sg.InputText('Default Folder'), sg.FolderBrowse()]
def getTxtBox(js):
    return [sg.Text('Here is some text.... and a place to enter text')]
def getSect(js):
    return [sg.Slider(range=(js['obj'][0], js['obj'][1]), orientation='v', size=(5, 20), default_value=25, tick_interval=25)]
def isFile():
    return [sg.Text('Choose A Folderg', size=(35, 1))]
def getSlider(na,ran,default):
    return [sg.Slider(range=(ran[0],ran[1]),default_value=default,size=(20,15),orientation='horizontal',font=('Helvetica', 12))]
def getMenuLs(na,ls):
    return [sg.Text(na),sg.Combo(ls,key=na),sg.Push()]
def getPopup(text):
    return [sg.Text(text)]
def getInput(na,st):
    return [sg.Text(na),sg.InputText(st,key=na),sg.Push()]
def getButtons(butts):
  butts,lsN = fun.mkLs(butts),[]
  for i in range(0,len(butts)):
    lsN.append(sg.Button(butts[i]))
  return lsN
def getKeys(js):
  lsN = []
  try:
    for key in js.keys():
      lsN.append(key)
    return lsN
  except:
    return lsN
def getVals(js):
  lsN = []
  try:
    for key in js.values():
      lsN.append(key)
    return lsN
  except:
    return lsN
def mkTxtLs(beg,ls):
  for i in range(0,len(ls)):
    beg = beg +str(ls[i])+'\n'
  return beg
def mkInputs(ls,prev,title,desc):
  lsA=[sg.Text(desc)]
  for i in range(0,len(ls)):
    lsA.append(getInput(ls[i],prev[i]))
  return defaultWindow(lsA,title)
def getDrop(js,st):
  if fun.isLs(st):
      changeGlob('varDesc',st[0])
      st= st[1]
  keys,lsA = getKeys(js),[]
  for i in range(0,len(keys)):
    key = keys[i]
    lsA.append(getMenuLs(key,js[key]))
  return defaultWindow(lsA,st)
def checkValues(values):
  keys,error,er,errKeys = getKeys(values)[1:],'you have not selected an input for the following:\n',True,[]
  for i in range(0,len(keys)):
    key = keys[i]
    if values[key] == '':
      errKeys.append(key)
      er = False
  if er == False:
    popUp('error: values unchecked',mkTxtLs(error,errKeys))
    return False
  return True
def createListFromJs(js,keys,var):
    beg = 'descriptions of selected values below:\n'
    print(keys)
    for i in range(0,len(keys)):
        if keys[i] in js:
    
            beg = beg + str(keys[i])+ ' - '+str(js[keys[i]][var])+'\n'
    return beg
def eventCall(window):
  event,values = window.read()
  if event == sg.WIN_CLOSED or event == 'Exit':
    window.close()
    return values
  elif event == 'override':
      window.close()
      return values
  elif event == 'Show':
      if varDesc != None:
          popUp('variable descriptions',createListFromJs(varDesc,getKeys(values),'description'))
  elif event == 'OK':
    if checkValues(values):
      window.close()
      return values
      
  return False
def popUp(title,text):
  window = sg.popup(title,text)
def defaultOverWindow(sg1,title):
    getDefaultSetOptions()
    window = sg.Window(title, getDefaultLayout(sg1), finalize=False)
    while True:
      vals = eventCall(window)
      if vals != False:
        return vals
def defaultWindow(sg1,title):
    getDefaultSetOptions()
    window = sg.Window(title, getDefaultLayout(sg1),getDefButtons(), finalize=False)
    while True:
      vals = eventCall(window)
      if vals != False:
        return vals
