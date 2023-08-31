import os
import json
import errno
#globals-----------------------------------------------------------------------------------------------------------------------
def changeGlob(x,y):
    globals()[x] = y
    return y
#creationFuncs-----------------------------------------------------------------------------------------------------------------
def pen(x,p):
  with open(p, 'w',encoding='UTF-8') as f:
    f.write(str(x))
    return p
def reader(x):
  with open(x, 'r',encoding='UTF-8') as f:
    return f.read()
def readerB(file):
  with open(file, 'r',encoding='UTF-8') as f:
    text = f.read()
    return text
def readerC(file):
    with open(file, "r",encoding="utf-8-sig") as f:
        text = f.read()
        return text
#pathFuncs---------------------------------------------------------------------------------------------------------------------
def homeIt():
    changeGlob('home',os.getcwd())
    if changeGlob('slash','/') not in home:
        changeGlob('slash','\\')
    return home,slash
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
        return path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        return path
def mkDirsAll(ls):
  y = make_sure_path_exists(ls[0])
  for k in range(1,len(ls)):
    y = make_sure_path_exists(crPa(y,ls[k]))
  return y
def mkDirTrue(x):
  return os.makedirs(x, exist_ok=True)
def mkDir(x):
  return os.mkdir(x)
def crPa(x,y):
  return os.path.join(str(x), str(y))
def isFile(x):
    return os.path.isfile(crPa(home,x))
def isDir(x):
    isdir = os.path.isdir(x)
def exists(x):
    if isFile(x):
        return True
    return False
def lsDir(x):
    return os.listdir(x)
def existJsRead(x,y):
    if exists(str(y)) == False:
        pen(str(x),str(y))
    return jsRead(str(y))
def jsRead(x):
    return jsIt(reader(x))
def existRead(x,y):
    if exists(y) == False:
        pen(str(x),y)
    return reader(y)
#timeFuncs---------------------------------------------------------------------------------------------------------------------
def ti():
    return float(datetime.datetime.now().timestamp())
#jsonFuncs---------------------------------------------------------------------------------------------------------------------
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
#typeFuncs--------------------------------------------------------------------------------------------------------------------
def isLs(ls):
  if type(ls) is list:
    return True
  return False
def isFloat(x):
  if type(x) is float:
    return True
  return False
def isInt(x):
  if type(x) is int:
    return True
  return False
def isStr(x):
  if type(x) is str:
    return True
  return False
def isDict(x):
  if type(x) is dict:
    return True
  return False
def isBool(x):
    if type(x) is bool:
        return True
    return False
def isNum(x):
  if isInt(x):
    return True
  if isFloat(x):
    return True
  x = str(x)
  for i in range(0,len(x)):
    if x[i] not in numLs():
      return False
  return True

#makeFuncs--------------------------------------------------------------------------------------------------
def mkFloat(x):
  if isFloat(x):
    return x
  if isInt(x):
    return float(str(x))
  if isNum(x):
    return float(str(x))
  z = ''
  for i in range(0,len(x)):
    if isNum(x[i]):
      z = z + str(x[i])
  if len(z) >0:
    return float(str(z))
  return float(str(1))
def mkBool(x):
    if isBool(x):
        return x
    boolJS = {'0':'True','1':'False','true':'True','false':'False'}
    if str(x) in boolJS:
        return bool(str(boolJs[str(x)]))
    return None
def mkJsLs(jsN,st,js):
  if st not in jsN:
    jsN[st] = []
  if js[st] not in jsN[st]:
    jsN[st].append(js[st])
  return jsN
def mkLs(ls):
  if isLs(ls) == False:
    ls = [ls]
  return ls
def mkStr(ls):
  ls = mkLs(ls)
  for k in range(0,len(ls)):
    ls[k] = str(ls[k])
  return ls
def mkFloat(x):
  if canMkFloat(x):
    return float(x)
  return False
def mkInt(x):
  if canMkInt(x):
    return int(x)
  return False
def mkNum(x):
  if canMkFloat(x):
    return mkFloat(x)
  if canMkInt(x):
    return mkInt(x)
  return len(str(x))
def canMkFloat(x):
  if isFloat(x):
      return True
  if int(countIt(str(x),'.')) <=1:
      return isNum(remFroStr(x,'.'))
  return False
def canMkInt(x):
  if isInt(x):
    return True
  if isFloat(x):
    return True
  if canMkFloat(x):
    return True
  return isNum(x)
def getObjObj(obj,x):
    if obj in ['str','file','image','mask','input','prompt']:
        return str(x)
    if obj == 'bool':
        return bool(x)
    if obj == 'float':
        return float(x)
    if obj == 'map':
        return map(x)
    if obj == 'int':
        return int(x)
    return x
#getFuncs--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_alph():
    alph = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo,pp,qq,rr,ss,tt,uu,vv,ww,xx,yy,zz,aaa,bbb,ccc,ddd,eee,fff,ggg,hhh,iii,jjj,kkk,lll,mmm,nnn,ooo,ppp,qqq,rrr,sss,ttt,uuu,vvv,www,xxx,yyy,zzz'
    sp = alph.split(',')
    return sp
def numLs():
  return str('0,1,2,3,4,5,6,7,8,9').split(',')
#stringprepFuncs-------------------------------------------------------------------------------------------------------------------------------------------------------------
def quoteIt(st,ls):
    lsQ = ["'",'"']
    for i in range(0,len(ls)):
        for k in range(0,2):
            if lsQ[k]+ls[i] in st:
                st = st.replace(lsQ[k]+ls[i],ls[i])
            if ls[i]+lsQ[k] in st:
                st = st.replace(ls[i]+lsQ[k],ls[i])
        st = st.replace(ls[i],'"'+str(ls[i])+'"')
    return st
def tIsF(bool):
    if bool == False:
        return True
    return False
def islenTrue(x):
    if len(x) <1:
        return False
    return True
def getendToEnd(x,k):
    return [abs(k)-1,abs(k),abs(k)-1+(-len(x)*k)]
def retEatLs(x,lsAll,ls):
    if x[lsAll[0]] in ls:
        return x[lsAll[1]:lsAll[2]]
    return False
def isEatWhile(x,k,ls):
    if tIsF(islenTrue(x)):
        return False
    return retEatLs(x,getendToEnd(x,k),ls)
def eatAll(x,ls):
    return eat(x,ls,[-1,1])
def eatInner(x,ls):
    return eat(x,ls,[-1,0])
def eatOuter(x,ls):
    return eat(x,ls,[0,1])
def eat(x,ls,lsN):
    for k in range(lsN[0],lsN[1]):
        while tIsF(isBool(isEatWhile(x,k,ls))):
            x = isEatWhile(x,k,ls)
    return x
def jsIt(x):
    return json.loads(quoteIt(str(x),['False','None','True']).replace("'",'"'))
def addStr(x,y):
  x = x + y
  return x
def remFroStr(x,y):
  x,y,n=mkStr([x,y,''])
  for k in range(0,len(x)):
    if x[k] != y:
      n = addStr(n,x[k])
  return n
#queryFuncs-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def find_it_alph(x,k):
    i = 0
    while str(x[i]) != str(k):
        i = i + 1
    return i
def countIt(x,y):
  ls = mkStr([x,y])
  if ls[1] not in ls[0]:
    return 0
  return (len(ls[0])-len(ls[0].replace(ls[1],'')))/len(ls[1])
def getHigher(k,c):
  if mkNum(k) > mkNum(c):
    return mkNum(k)
  return mkNum(c)
def getLongest(ls):
  high = mkNum(ls[0])
  for k in range(1,len(ls)):
    high = int(getHigher(high,len(ls[k])))
  return high
def ifInJsWLs(ls,js,ls2):
    for i in range(0,len(ls)):
        if ls[i] in js:
            ls2[int(i)] = js[ls[int(i)]]
    return ls2
def getgetAllJs():
    return json.loads(reader('data/allJs.json'))
def getlast_api():
    return reader('data/last_api.txt')
def getprevInputs():
    return json.loads(reader('data/prevInputs.json'))
def getrpcListNew():
    return json.loads(reader('data/rpcListNew.json'))
def getrpcValues():
    import dataFold.rpcValues as rpcValues
    return rpcValues
def getSettings():
    import dataFold.settings as settings
    return settings
homeIt()
