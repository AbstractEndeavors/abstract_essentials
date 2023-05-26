from pdf2image import convert_from_path
import cv2 
import pytesseract
import os
import sys
import json
import PyPDF2

from pathlib import Path
def isFold(x):
    return os.path.isdir(x)
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
def pen(x,p):
    with open(p, 'w',encoding='UTF-8') as f:
        return f.write(str(x))
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def createPath(x,y):
    while slash == x[-1]:
        x = x[:-1]
    while y[0] == slash:
        y = y[1:]
    return x + slash + y
def copy_it(x,y):
	x_r = reader(x)
	x_n = x.split('/')[-1]
	if str(y)[-1] !='/':
		y =str(y) + '/'
	y = y + x_n
	pen(x_r,y)
def list_files(x):
    return os.listdir(x)
def exists(x):
    if str(x)[-1] !='/':
        y = str(x).split('/')
        y_1 = str(x).replace('/'+y[-1],'')
    z = list_files(y_1)
    if y[-1] in z:
        return True
    return False
def js_it(x):
    return json.loads(str(x).replace('[,','[').replace('{,','{').replace("'",'"'))
def exists_make(x,y):
    if exists(y) == True:
        return reader(y)
    pen(x,y)
    return x
def createPath(x,y):
    while slash == x[-1]:
        x = x[:-1]
    while y[0] == slash:
        y = y[1:]
    return x + slash + y
def makeAllPaths(ls):
    n = ls[0]
    for i in range(1,len(ls)):
        n = createPath(n,ls[i])
    return n
def mkDir(x):
    if isFold(x) == False:
        os.makedirs(x, exist_ok = True)
    return x
# Store Pdf with convert_from_path function
def pdfToImg(y):
   
    images = convert_from_path(js['pdfs'][flatName]['locations']["file"])
 
    imageFold = y
    
    for i in range(0,len(images)):
        js['pdfs']['locations'][flatName]["images"]['names'].append(createPath(js['pdfs'][flatName]['locations']["images"]+'_page'+ str(i) +'.jpg'))
        images[i].save(createPath(js['pdfs'][flatName]['locations']["images"]+'_page'+ str(i) +'.jpg'), 'JPEG')
        images[i],

def isInt(x):
    if type(x) is int:
        return x
    try:
        y = int(x)
        return x
    except:
        return False
def isWhileGood(x,i,boolIt):
    if len(x)<1:
        return False
    if int(i) >= len(x):
        return False
    return boolIt
def readTillNumeric(x):
    intInt,boolIt,ints,js,i,z = [],True,False,{'nums':['0']},0,''
    while isWhileGood(x,i,boolIt):
        if x[i]== '.' and len(intInt)>0:
            js[js['nums'][-1]] = z[:-len(intInt)]
            js['nums'].append(z[-len(intInt):])
            intInt = []
            ints == False
            z = ''
        elif isInt(x[i]):
             ints = True
             intInt.append(i)
             z =z + x[i]
        else:
            intInt = []
            ints == False
            k = i
            z =z + x[i]
        i +=1
    js[js['nums'][-1]] = z[:-len(intInt)]
    return js
def pageMerge():
    ls = os.listdir('curr/txt')
    pages = ''
    for i in range(0,len(ls)):
        read = reader(createPath('curr/txt',ls[i]))
        pages = pages+'\n'+read
    pen(pages,'pages.txt')
    return pages
def cutInHalf(x,y):
  

    import cv2   
    # Read the image
    img = cv2.imread(x)
    print(img.shape)
    

    input(misc)
def isInt(x):
    if type(x) is int:
        return x
    try:
        y = int(x)
        return x
    except:
        return False
def isStopper(y):
    if isInt(y[:-1]) and y[-1] == '.':
        return True
    return False
def importWorkSheet(lineSheet,na):
  sys.path.insert(0,createPath(home,'excels'))
  pen("import sys\nsys.path.insert(0,'"+createPath(home,'excels')+"')\nimport xlsxwriter\nworkbook = xlsxwriter.Workbook('excels/"+na+".xlsx')\nworksheet = workbook.add_worksheet()\n"+lineSheet+'workbook.close()','excels/workit.py')
  import workit

def ifLs(ls):
    if type(ls) is list:
        return True
    return False
def combineLss(ls):
    lsN = []
    for i in range(len(ls)):
        currLs = ls[i]
        for k in range(len(currLs)):
            lsN.append(currLs[k])
    return lsN
def integers():
    return str('1,2,3,4,5,6,7,8,9,0').split(',')
def letters():
    return str('a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z').split(',')
def upperLs(ls):
    lsN=[]
    for i in range(len(ls)):
        lsN.append(ls[i].upper())
    return lsN
def lowerLs(ls):
    lsN=[]
    for i in range(len(ls)):
        lsN.append(ls[i].lower())
    return lsN
def alph(i):
    al = upperLs(letters())
    k = 0
    main = ''
    while i >=26:
        main = al[k]
        k +=1
        i -=26
    main = main+al[i]   
    return main
def whileGood(x):
    if len(x) == 0:
        return False
    return True
def cleanFront(x):
    lsN = combineLss([integers(),upperLs(letters()),lowerLs(letters())])
    while whileGood(x):
        if x[0] in lsN:
            return x
        x = x[1:]
    return x
def cleanEnd(x):
    lsN = combineLss([integers(),upperLs(letters()),lowerLs(letters())])
    while whileGood(x):
        if x[-1] in lsN:
            return x
        x = x[:-1]
    return x
def cleanAll(x):
    return cleanFront(cleanEnd(x))
def cleanLs(ls):
    lsN = []
    for i in range(0,len(ls)):
        if ls[i] not in ['','␌',' ','\n','\t']:
            lsN.append(ls[i])
    return lsN
def clearFold(x):
    import shutil
    if isFold(x):
        shutil.rmtree(x)
def rmFold(x):
    clearFold(x)
    if isFold(x):
        os.rmdir() 
global js,home
homeIt()
js={'pdfs':{}}
mkDir('excels')
rmFold('curr')
pdfLs = os.listdir('currPDF')
lsN = []
for i in range(0,len(pdfLs)):
    if '.pdf' in pdfLs[i]:
        lsN.append(pdfLs[i])
pdfLs = lsN
lineSheet = ''
for i in range(0,len(pdfLs)):
    jsN  = {}
    pdfName = pdfLs[i].replace('.pdf','')
    path = createPath('currPDF',pdfLs[i])
    js={'pdfs':{str(pdfLs[i]):{'pages':{},}}}
    flatName = str(pdfLs[i].replace('.pdf',''))
    newPath = mkDir(makeAllPaths([flatName]))
    js['pdfs'][flatName] = {}
    js['pdfs'][flatName]['locations'] = {"fold":newPath}
    js['pdfs'][flatName]['locations']["images"] = {}
    js['pdfs'][flatName]['locations']["images"]['fold'] = {}
    js['pdfs'][flatName]['locations']["images"]['fold']['imgs'] = mkDir(makeAllPaths([newPath,'img/']))
    js['pdfs'][flatName]['locations']["images"]['fold']['txt'] = mkDir(makeAllPaths([newPath,'txt/']))
    js['pdfs'][flatName]['locations']["images"]['names'] = []
    js['pdfs'][flatName]['locations']["file"] = str(createPath(home,pdfLs[i]))
    images = convert_from_path(path)
    for k in range(2,len(images)):
        images[k].save(makeAllPaths([newPath,'img/'])+'page'+ str(k) +'.jpg', 'JPEG')
        img = cv2.imread(makeAllPaths([newPath,'img/'])+'page'+ str(k) +'.jpg')
        height = img.shape[0]
        width = img.shape[1]
        width_cutoff = width // 2
        s1 = img[:, :width_cutoff]
        s2 = img[:, width_cutoff:]
        custom_config = r'--oem 3 --psm 6'
        list1 = [pytesseract.image_to_string(s1, config=custom_config).split('\n'),pytesseract.image_to_string(s2, config=custom_config).split('\n')]
        stop = False
        for j in range(0,len(list1)):
            for kk in range(0,len(list1[j])):
                piece = cleanLs(list1)[j][kk]
                pieces = cleanLs(piece.split(' '))
                for c in range(0,len(pieces)):
                    if isStopper(pieces[c]):
                        m = pieces[c]
                        jsN[m] = []
                        cc = 0
                        stop = True
                if stop == True:
                    lineSheet = lineSheet + "worksheet.write('"+str(alph(cc))+str(m).replace('.','')+"','"+str(cleanAll(piece.replace(m,''))).replace("'",'').replace('"','')+"')\n"
                    cc +=1
    importWorkSheet(lineSheet,pdfName)
