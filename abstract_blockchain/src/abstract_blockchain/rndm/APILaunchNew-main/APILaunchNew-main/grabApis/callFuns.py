import PySimpleGUI as sg
import functions as fun
def getDefMenu():
    return [sg.Menu([['File', ['Open', 'Save', 'Exit',]],['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],['Help', 'About...'],])]
def getDefButtons():
    return [sg.OK('OK'),sg.Button('Show'),sg.Button('Auto'),sg.Button('Exit')]
def getDefaultSetOptions():
    return sg.set_options(suppress_raise_key_errors=bool(False), suppress_error_popups=bool(False), suppress_key_guessing=bool(False))
def getDefaults(sg1):
    return [getDefMenu(),sg1,getDefButtons()]
def mkTxtLs(beg,ls):
  for i in range(0,len(ls)):
    beg = beg +str(ls[i])+'\n'
  return beg
def mkInputs(ls,prev,title,desc):
  lsA=[sg.Text(desc)]
  for i in range(0,len(ls)):
    lsA.append(getInput(ls[i],prev[i]))
  return defaultWindow(lsA,title)
def checkValues(values):
  keys,error,er,errKeys = fun.getKeys(values)[1:],'you have not selected an input for the following:\n',True,[]
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
          popUp('variable descriptions',createListFromJs(varDesc,fun.getKeys(values),'description'))
  elif event == 'OK':
    if checkValues(values):
      window.close()
      return values
  return False
def popUp(title,text):
  window = sg.popup(title,text)
def defaultWindow(sg1,title):
    getDefaultSetOptions()
    window = sg.Window(title, getDefaults(sg1), finalize=False)
    while True:
      vals = eventCall(window)
      if vals != False:
        return vals
