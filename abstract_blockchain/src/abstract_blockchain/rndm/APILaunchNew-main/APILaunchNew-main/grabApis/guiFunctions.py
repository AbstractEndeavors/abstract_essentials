import PySimpleGUI as sg
import functions as fun
def getDefs(js,jsDef):
    keys = fun.getKeys(js)
    for k in range(0,len(keys)):
        key = keys[k]
        jsDef[key] = js[key]
    return jsDef
def inputTxt(js):
    js = getDefs(js,{"val":0,"key":None,"size":(25,15),"orientation":'h',"enable_events":False})
    return sg.ProgressBar(js['val'],key=js['key'],size=js['size'],orientation=js['orientation'],enable_events=['enable_events'])
def inputTxt(js):
    js = getDefs(js,{"text":"","key":None,"font":None,"size":(25,15),"background_color":None,"enable_events":False})
    return  sg.InputText(js["text"],key=js["key"],size=js["size"],font=js["font"],background_color=js["background_color"],enable_events=js["enable_events"])
def txtBox(js):
    js = getDefs(js,{"text":"","key":None,"font":None,"background_color":None,"enable_events":False,"grab":None})
    return  sg.Text(js["text"],key=js["key"],font=js["font"],background_color=js["background_color"],enable_events=js["enable_events"], grab=js["grab"])
def pushBox(js):
	js = getDefs(js,{"background_color":None})
	return  sg.Push(background_color=js["background_color"])
def getT(na,key):
    return sg.T(na,key=key)
def slider(js):
	js = getDefs(js,{"title":"","range":(1,1),"visible":True,"key":None,"default_value":None,"resolution":1,"tick_interval":1,"pad":(0,0),"orientation":'h',"disable_number_display":False,"enable_events":False,"size":(25,15)})
	return  sg.Slider(range=js["range"],visible=js["visible"],key=js["key"],size=js["size"],default_value=js["default_value"],resolution=js["resolution"],pad=js["pad"],orientation=js["orientation"],disable_number_display=js["disable_number_display"], enable_events=js["enable_events"])
def checkBox(js):
	js = getDefs(js,{"title":"","visible":True,"key":None,"default":None,"pad":(0,0),"enable_events":False,})
	return  sg.Checkbox(js["title"],visible=js["visible"],key=js["key"],default=js["default"],pad=js["pad"],enable_events=js["enable_events"])
def dropDown(js):
	js = getDefs(js,{"ls":"","key":None,"size":(25,15),"default_value":None,"visible":True,"key":None,"enable_events":False,})
	return  sg.Combo(js["ls"],visible=js["visible"],key=js["key"],enable_events=js["enable_events"],size=js["size"],default_value=js["default_value"])
def getButton(js):
	js = getDefs(js,{"title":"","visible":True,"key":None,"enable_events":False," button_color":None,"bind_return_key":None})
	return sg.Button(js["title"],visible=js["visible"],key=js["key"],enable_events=js["enable_events"],bind_return_key=js["bind_return_key"])
def txtInputs(js):
	js = getDefs(js,{"title":"","size":None,"font":None,"key":None,"autoscroll":None,"disabled":False,"pad":(0,0),"change_submits":False,"enable_events":False})
	return sg.Multiline(js["title"],size=js["size"],font=js["font"],key=js["key"],autoscroll=js["autoscroll"],disabled=js["disabled"],change_submits=js["change_submits"],enable_events=js["enable_events"])
def vertSep(js):
        js = getDefs(js,{"title":"","size":None,"font":None,"key":None,"autoscroll":None,"disabled":False,"pad":(0,0)})
        return sg.VerticalSeparator(pad=js["pad"])
def getTab(js,layout):
	js = getDefs(js,{"title":"","layout":"","key":None,"visible":True,"disabled":False,"title_color":'green',"enable_events":True})
	return sg.Tab(js["title"],layout,key=js["key"],visible=js["visible"],disabled=js["disabled"],title_color=js["title_color"],enable_events=js["enable_events"],change_submits=js["change_submits"])
def getFileBrowse(js):
        js = getDefs(js,{"type":"file","key":None,"ext":"txt","enable_events":False})
        return sg.FileBrowse(file_types=((js["type"], "*."+str(js["ext"])),),key=js["key"],enable_events=js["enable_events"])
def getTabGroup(js):
	js = getDefs(js,{"tabs":"","key":None,"enable_events":True})
	return  sg.TabGroup(js["tabs"],key=js["key"],enable_events=js["enable_events"])
def column(layout):
    return sg.Column(layout, scrollable=True,  vertical_scroll_only=True, size_subsample_height=5)
def adjustablescreen():
    column_layout = [[sg.Text(f'Line {i+1:0>3d}'), sg.Input()] for i in range(100)]
    layout = [[sg.Column(column_layout, scrollable=True,  vertical_scroll_only=True, size_subsample_height=5)]]
    sg.Window('Title', layout).read(close=True)
def getList(layout,colR,rowR):
        return [[layout for col in range(colR)] for row in range(rowR)]
def getFullParams(js):
        return [[checkBox({"title":"def","visible":True,"key":js["title"]+'_default_'+str(js["default"]),"default":js["default"],"pad":(len('default'),len('default')),"enable_events":True})],[js["layout"]],[getButton({"title":js["title"],"visible":True,"key":js["title"]+"_info","enable_events":True,"button_color":None,"bind_return_key":True})]]
def mkParam(na,defa,layout):
        return [getFullParams({"title":na,"default":defa,"layout":layout})]
'''
txtBox({"title":"","key":None,"font":None,"background_color":None,"enable_events":False," grab":None})
slider({"title":"","range":None,"visible":True,"key":None,"default_value":None,"resolution":None,"tick_interval":None,"pad":(0,0),"orientation":None,"disable_number_display":None,"enable_events":False})
checkBox({"title":"","visible":True,"key":None,"default":None,"pad":(0,0),"enable_events":False})
dropDoiwn{"ls":"","key":None,"size":None,"default_value":None})
getButton({"title":"","visible":True,"key":None,"enable_events":False," button_color":None,"bind_return_key":None})
txtInputs({"title":"","size":None,"font":None,"key":None,"autoscroll":None,"disabled":False,"sg.VerticalSeparator(pad":None})
getTab({"title":"","layout":"","key":None,"visible":True,"disabled":False,"title_color":None})
getTabGroup({"tabs":"","key":None})
getList({"title":"",'''
