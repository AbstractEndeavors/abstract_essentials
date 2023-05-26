import pyautogui
import numpy as np
import cv2
import os, sys
from PIL import Image
import pyscreenshot as ImageGrab
import time
import json
from python_imagesearch.imagesearch import imagesearcharea,region_grabber
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
def screenShot():
    ImageGrab.grab().save("Screenshot.png")
    return "Screenshot.png"
def getKeys(js):
    lsN = []
    for key, value in js.items():
        lsN.append(key)
    return lsN
def homeIt():
    curr = os.getcwd()
    slash = '//'
    if '//' not in str(curr):
        slash = '/'
    changeGlob('slash',slash)
    changeGlob('home',curr)
    return home
def changeGlob(x,v):
    globals()[x] = v
def ifGood(x,y,z):
    if len(x) == 0:
        return False
    if x[y] != z:
        return False
    return True
def eliminateEnd(x,y,z):
    while ifGood(x,y,z):
        if y == -1:
            x = x[:-1]
        else:
            x = x[1:]
    return x
def createPathLs(ls):
    if len(ls) > 0:
        y = eliminateEnd(ls[0],-1,slash)+slash
    if len(ls) >1:
        y = y+eliminateEnd(ls[1],0,slash)
    for i in range(2,len(ls)):
        y = y+slash+eliminateEnd(ls[1],0,slash)
    return y
def createPath(x,y):
    return eliminateEnd(x,-1,slash)+slash+eliminateEnd(y,-1,slash)
def parseOutHome(x):
    ls = home.split(slash)
    ls2 = x.split(slash)
    for i in range(0,len(ls)):
        if ls[i] == ls2[0]:
            ls2= ls2[1:]
    return createPathLs(ls2)
def imgToStr(x):
    filename = x
    img1 = np.array(Image.open(filename))
    text = pytesseract.image_to_string(img1)
def openPage(x):
    os.popen('x-www-browser '+x)
def screenShotGnome(x):
    os.popen('gnome-screenshot --file='+x)
    time.sleep(2)
    return x
def openFile(x):
    os.popen("open "+createPath(home,parseOutHome(x)))
    return x
def readImage(x):
    return cv2.imread(x)
def getDimensions(x):
    return readImage(x).shape[:-1]
def keepDimensions(dim,testDim,add):
    height=[0,dim[0]]
    length=[0,dim[1]]
    right,left = add
    height=[0+right,dim[0]+right]
    length = [0+left,dim[1]+left]
    return [height,length]
def getNewImgFromDim(dim,img,name):
    return readImage(img)[dim[0][0]:dim[0][1], dim[1][0]:dim[1][1]]
def saveNewImgFromDim(dim,img,name):
    saveImg(name, readImage(img)[dim[0][0]:dim[0][1], dim[1][0]:dim[1][1]])
    return name
def getExt(x):
    return '.'+x.split('.')[-1]
def getNewDimAndReturn(img,name,dim,testDim,add):
    dim = keepDimensions(dim,testDim,add)
    if dim[1][1] > testDim[1] or dim[0][0] > testDim[0]:
        return False
    return dim,img,name
def colorRange(x):
    if type(x) is str:
        return plt.imread(x)
    return plt.img
def getLower(ls):
    ls.sort()
    return ls[-1]
def saveImg(x,img):
    cv2.imwrite(x,img)
    return x
def isLs(ls):
    if type(ls) is list:
        return True
    return False
def isDict(ls):
    if type(ls) is dict:
        return True
    return False
def getNum():
    return str('1,2,3,4,5,6,7,8,9,0').split(',')
def isNum(x):
    ls = getNum()+[',','.']
    if str(x) in ls:
        return True
    return False
def turnToFloat(ls):
   lsN = []
   if 'array(' in str(ls):
       ls = ls[0]
   for i in range(0,len(ls)):
       if isLs(ls[i]):
           for k in range(0,len(ls[i])):
               lsN.append(ls[i][k])
       elif isDict(ls[i]):
           ls[i] = ls[i][0]
       else:
           lsN.append(ls[i])
   return lsN
def compareMoreColorRange(lowest,name,x,y,imgStats):
    for i in range(0,len(x)):
        x[i],y[i] = turnToFloat(x[i]),turnToFloat(y[i])
        for k in range(0,len(x[i])):
            x[i][k],y[i][k] = turnToFloat(x[i][k]),turnToFloat(y[i][k])
            c = c+abs(float(float(sum(x[i][k])) - float(sum(y[i][k]))))
    if lowest[1] == None:
        lowest = [saveImg('lowestTest'+'.'+name.split('.')[-1],readImage(imgStats[2])),c,imgStats[0]]
        openFile(lowest[0])
    elif c < lowest[1] and c != 0:
        lowest = [saveImg('lowestTest'+'.'+name.split('.')[-1],readImage(imgStats[2])),c,imgStats[0]]
        openFile(lowest[0])
        input([x,y,c])    
    return lowest
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
def trurnGrey(x):
    import imageio
    import numpy as np
    import matplotlib.pyplot as plt

    pic = cv2.imread(x)
    gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114]) 
    gray = gray(pic)  
    plt.imshow(gray, cmap = plt.get_cmap(name = 'gray'))
    return gray
def getPix(x):
    return openImg(x).load()
def openImg(x):
  return Image.open(x)
def findIt(ls,x):
    for i in range(0,len(ls)):
        if ls[i] == x:
            return i
    return False
def getLowestLs(ls):
    ls.sort()
    return ls[-1]
def doAll(x):
    pixels = getPixelData(x)
    greyNa = x.split('.')[0]+'Grey'+'.'+x.split('.')[-1]
    saveImg(greyNa,trurnGrey(x))
    return readImage(x),getDimensions(x),getPix(x),colorRange(x),readImage(greyNa),getPix(greyNa),pixels
def getPixelData(x):
    dim = getDimensions(x)
    px = getPix(x)
    lsN,lsA = [],[]
    for i in range(0,dim[0]):
        
        for k in range(0,dim[1]):
            lsN.append(px[k,i])
        lsA.append(lsN)
        lsN = []
    pixToImgh(lsA)
    return lsA
def matchLine(f,s,dim,jsN):
    if dim[0] not in jsN:
        jsN[dim[0]] = []
        jsN["last"]=dim[0]
    lsDim = dim
    for i in range(dim[1],len(s)-findIt(s,f[dim[1]])):
        if f[i] != s[i]:
            return jsN
        lsDim[1] +=1
        jsN[dim[0]].append(lsDim)
    return lsN
def getLower(ls):
    ls.sort()
    return ls[0]
def verticalMove(vert,cur):
    move = abs(cur-vert)
    if cur < vert:
        move = vert-move
    pyautogui.move(move,0)
def horizontalMove(horiz,cur):
    move = cur-horiz
    if cur < horiz:
        move = horiz-cur
    pyautogui.move(0,move)
def getTo(x,y):
    curr = getCursorPos()
    verticalMove(y,curr[1])
    horizontalMove(x,curr[0])
def moveTo(x,y):
    pyautogui.moveTo(x,y)
def getCursorPos():
    return pyautogui.position()
def getScreenSize():
    return pyautogui.size()
def movePrecise(x,y):
    size = getScreenSize()
    if x <= size[0] and y <= size[1]:
        
        print(x-curs[0],y-curs[1])
        moveTo(x-curs[0],y-curs[1])
def rightClick():
    pyautogui.click(button='right')
def movePreciseAndClick(x,y):
    getTo(x,y)
    rightClick()
    rightClick()
def pixToImgh(ls):
    image_RGB = np.array(ls)
    image = Image.fromarray(image_RGB.astype('uint8')).convert('RGB')
    image.save('image.png')
def combinePixels(jsN,screenPx):
    lsA = []
    cs = jsN['height']
    
    for i in range(0,len(jsN['height'])):
        c = jsN['height'][i]
        
        for k in range(0,len(jsN[c])):
            screenPx[jsN[c][k][0]][jsN[c][k][1]] = jsN[c][k][2]
    pixToImgh(screenPx)
def findFind():
    find,findDim,findPx,findColor,findGrey,findGreyPx,s = doAll()
    screen,screenDim,screenPx,screenColor,screenGrey,screenGreyPx,f = doAll(screenShot())
    lsA,lsFind = [],[]
    for i in range(0,findDim[0]):
        lsN = []
        for k in range(0,findDim[1]):
            if findPx[k,i] not in lsFind:
                lsFind.append(findPx[k,i])
    for i in range(0,screenDim[0]):
        lsN = []
        for k in range(0,screenDim[1]):
            if screenPx[k,i] not in lsFind:
                lsN.append((255,255,255,255))
            else:
                lsN.append(screenPx[k,i])
                pyautogui.click(k,i,button='left')
        lsA.append(lsN)
    pixToImgh(lsA)         
homeIt()
findbuttons('pics/find.png')
