#!/opt/rh/rh-python35/root/usr/python
import os
import os.path
import requests
import json
import time
import datetime
import math
import gc
import sys
def mkdirs(f):
    import os  
    directory = f
    parent_dir = home
    path = os.path.join(parent_dir, directory)
    A = check_dirs(path)
    if A == False:
        os.mkdir(path)  
        print("Directory '% s' created" % directory)
    return path
def check_dirs(fname):
    path = home+str(fname)
    isFile = os.path.isdir(path)
    return isFile 
def timer(N):
    N = N + 1
    return N
def get_ti():
    import datetime
    T_S = datetime.datetime.now().timestamp()
    pen(str(T_S),'last.txt')
    T_S_D = str(datetime.datetime.now())[0:10]
    day = int(int(T_S) - int(86400))
    B_L = block(day)
    B_G = block(int(T_S))
    
    TS = '{"TS":["'+str(T_S)+'","'+str(T_S_D)+'","'+str(B_L)+'","'+str(B_G)+'"]}'
    pen(TS, 'T_S_pow.py')
    return B_L,B_G,T_S,T_S_D,day
def add_brac(S):
    return str('{'+str(S)+'}')
def rem_comm(S):
    S = str(S)
    if str(S[0]) == ',':
        S = str(S)[1:]
    if str(S[-1]) == ',':
        S = str(S)[:-1]
    return S
def ch_quote(S):
    return str(str(S).replace("'",'"'))
def foldersave():
    print('checking folders')
    B_L,B_G,Ts,date,day = get_ti()
    foldate = 'fri','sat','sun','mon','tues','wed','thur',
    sec = float(1)
    mi = float(60)
    hour = float(60*mi)
    day = float(24*hour)
    week = float(7*day)
    fri = 1609510651.1613681
    since = (float(Ts)-(float(fri)))
    D = mi,hour,day,week
    D_2 = 'sec,hour,day,week'
    D_3 = D_2.split(',')
    N = 0
    jas = ''
    while N <= int(3):
        i = float(since)/float(D[N])
        jas = jas+',"'+str(D_3[N])+'":"'+str(float(i))+'"'
        N = timer(N)
        TSH = str(ch_quote(add_brac(rem_comm(jas))))
        timesheet = json.loads(TSH)
    days = int(float(timesheet['day']))
    date = str(date).replace('-','_')
    fold_name = home + str(date)+'\\'
    num_add = len(add_ls)
    A = check_dirs(fold_name)
    if A == True:
        print(fold_name,' good')
        i = timer(i)
    elif A == False:
        try:
            mkdirs(fold_name)
            print('creating ',fold_name)
            i = timer(i)
        except:
            print('failed to create ',fold_name)
            i = timer(i)
    print('creating address folders')
    i = 0
    while i != num_add:
        print('starting')
        new = str(fold_name)+'\\'+add_ls[i]
        print(new)
        A= check_dirs(new)
        if A == True:
            print(new,' good')
            i = timer(i)
        elif A == False:
            try:
                mkdirs(new)
                print('creating ',new)
                i = timer(i)
            except:
                print('failed to create ',new)
                i = timer(i)
    return fold_name
def tryit(A,N):
    try:
        tr = A[N]
        return 0, N
    except:
        N = N - 1
        return -1, N
def globular():
    global fname,curr_arr,pairs,add,fname,last_site,home,scanners,add_ls,num_add,num_scan
    last_site = 0
    home = os.getcwd()+'\\'
    scanners = 'etherscan.io'

    
def reader_B(file):
    with open(file, 'r',encoding='UTF-8') as f:
        text = f.read()
        return text
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def pen_B(paper, place):
    with open(place, 'w',encoding='UTF-8') as f:
        f.write(str(paper))
        f.close()
        return
def pen(paper, place):
    with open(place, 'w') as f:
        f.write(str(paper))
        f.close()
        return
def keys():
    if scanners == 'bscscan.com':
        key = 'JYVRVFFC32H2ZSKDY1JZKNY7XV1Y5MCJHM'
    elif scanners == 'polygonscan.com':
        key = 'S6X6NY29X4ARWRVSIZJTG1PJS4IG86B3WJ'
    elif scanners == 'ftmscan.com':
        key = 'WU2C3NZAQC9QT299HU5BF7P8QCYX39W327'
    elif scanners == 'moonbeam.moonscan.io':
        key = '5WVKC1UGJ3JMWQZQAT8471ZXT3UJVFDF4N'
    else:
        key = '4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1'
    return key
def pr():
    return last_site
def pr_glob(x):
    global last_site
    last_site = x
def sites(A):
    last_site = pr()
    JS = 'Max rate limit reached, rate limit of 5/1sec applied'
    diff = float(datetime.datetime.now().timestamp()) - float(last_site)
    #print('diff',diff)
    if float(diff) < float(5):
        time.sleep(float(5) - float(diff))
    if str(scanners) == 'moonbeam.moonscan.io':
        A = str(A).replace('api.','api-').replace('api-cn.','api-')
    U = [A]
    for url in U:
        X = str(U[0])
        while JS == 'Max rate limit reached, rate limit of 5/1sec applied':
            r = requests.get(X)
            pr_glob(float(datetime.datetime.now().timestamp()))
            PS = r.text
            try:
                JS = json.loads(PS)
            except:
                time.sleep(5)
    return JS

def supply(add,Ad_pa):
    key = keys()
    x = 'http://api.'+scanners+'/api?module=account&action=tokenbalance&contractaddress='+str(add).lower()+'&address='+str(Ad_pa).lower()+'&tag=latest&apikey='+key
    return  x
def wall_sup(Ad_pa,B_L,B_G):
    key = keys()
    x = 'http://api.'+scanners+'/api?module=account&action=tokentx&address='+str(Ad_pa)+'&startblock='+str(B_L)+'&endblock='+str(B_G)+'&sort=asc&apikey='+key
    return  x
def tok_sup(Ad_pa):
    key = keys()
    x = 'https://api-cn.'+scanners+'/api?module=stats&action=tokensupply&contractaddress=' + str(Ad_pa).lower() + '&apikey='+key
    return  x
def JS_prep(A):
    A = str(A).replace(' ','').replace("'",'"').replace(']','').replace('[','').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','')
    return A
def eth_sup(add):
    key = keys()
    x = 'https://api.'+scanners+'/api?module=account&action=balance&address='+str(add)+'&tag=latest&apikey='+key
    if str(scanners) == 'moonbeam.moonscan.io':
        x = str(x).replace('api.','api-')
    return  x
def block(A):
    key = keys()
    U = 'https://api.'+scanners+'/api?module=block&action=getblocknobytime&timestamp='+str(A)+'&closest=before&apikey='+str(key)
    if str(scanners) == 'moonbeam.moonscan.io':
        U = str(U).replace('api.','api-')
    JS = sites(U)
    Bl = JS['result']
    return Bl
def block_em():
    now = float(datetime.datetime.now().timestamp()) - float(24*60*60)
    x = 'https://api.'+str(scanners)+'/api?module=block&action=getblocknobytime&timestamp='+str(int(now))+'&closest=before&apikey='+keys()
    x = sites(x)
    x = x['result']
def comp_check(A): 
    A = json.loads(str(A).replace("'",'"'))
    try:
        TS = A['timeStamp']
        B_L = A['blockNumber']
        hashs = A["hash"]
        fro = A["from"]
        cont = A["contractAddress"]
        to =  A["to"]
        gas = A["gasUsed"]
        return TS,B_L,hashs,fro,cont,to,gas
    except:
        return 0,0,0,0,0,0,0
def comp(A,B):
    a,b,c,d,e,f,g = comp_check(A)
    A = a,b,c,d,e,f,g
    aa,bb,cc,dd,ee,ff,gg = comp_check(B)
    B = aa,bb,cc,dd,ee,ff,gg
    num = count_ls(A)
    i = 0
    while i != num:
        if str(A[i]) == str(B[i]):
            i = i + 1
        elif str(A[i]) != str(B[i]):
            return -1
    return 1
def get_txns(add,B_L,B_G):
    js = sites(wall_sup(add,B_L,B_G))
    msg = js['message']
    js = js['result']
    if str(msg) == 'No transactions found':
        return '', 0, 0, 0, B_G
    old = js[0]
    new = js[-1]
    TS = new['timeStamp']
    B_L = new['blockNumber']
    return js, old, new, TS, B_L
def count_ls(x):
    i = 0
    n = 0
    while n != 1:
        try:
            x_n = x[i]
            i = i + 1
        except:
            n = 1
    return i
def count_js(B):
    N = 0
    M = 0
    while M != -1:
        M,L_B = tryit(B,N)
        N = N + 1
    L_B = L_B
    return L_B
def checkit_new(x,x_2):
    if str(x) == str(x_2):
        return 1
    else:
        return 0
def scan_glob(x):
    global scanners
    scanners = x
def wall_scan(x,y,z,n):
    num = int(count_ls(x))
    i = int(0)
    f = float(0)
    farm =(0)
    inn = float(0)
    out = float(0)
    while i != num:
        new = x[i]
        cont = new["contractAddress"]
        if str(cont).lower() == str(y).lower():
            #power_list = str(power_list) + '\n'+str(new)+','
            #pen(power_list,coins+'/'+str(pairs[pair_i])+'.txt')
            fro = new["from"]
            to = new["to"]
            val = new["value"]
            dec = new["tokenDecimal"]
            hashs = new['hash']
            expo = float(10)**(float(-1)*float(dec))
            val = float(val)*float(expo)
            
            if "farm" in z:
                farm_add = z["farm"]
                f = 1
            else:
                f = 0
            if n == 1:
                ti = str(new["timeStamp"])
                n_globs(z)
                node_get(float(ti),float(val),str(to).lower(),str(fro).lower())
            if str(to).lower() == str(add).lower():
                inn = float(inn) + float(val)
            if str(fro).lower() == str(add).lower():
                out = float(out) - float(val)
            if f == 1:
                if str(fro).lower() == str(farm_add).lower():
                    farm = float(farm) - float(val)
                elif str(to).lower() == str(farm_add).lower():
                    farm = float(farm) + float(val)
            glob_expo(expo)
        i = i + int(1)
    return inn,out,farm
def glob_expo(x):
    global expo
    expo = float(x)
def n_globs(z):
    global n_cont,n_num,n_acc,n_claim
    n_cont = z["node_cont"]
    n_num = z["node_#"]
    n_acc = z["acc"]
    n_claim = z["claim"]
def tots_globs(x,y,z):
    x = json.loads('['+str(x).replace("'",'"')+']')
    y = json.loads('['+str(y).replace("'",'"')+']')
    z = json.loads('['+str(z).replace("'",'"')+']')
    global price_total,inn_total,out_total
    price_total = x
    inn_total = y
    out_total = z
def get_old(file):
    js = json.loads('['+str(reader_B(file))[:-1].replace("'",'"')+']')
    old = js[0]
    new = js[-1]
    TS = new['timeStamp']
    B_L = new['blockNumber']
    return js, old, new, TS, B_L
def block_em():
    now = float(datetime.datetime.now().timestamp()) - float(24*60*60)
    x = 'https://api.'+str(scanners)+'/api?module=block&action=getblocknobytime&timestamp='+str(int(now))+'&closest=before&apikey='+keys()
    x = sites(x)
    x = x['result']
    return x
def wall(): 
    B_L = '00000000'
    B_G = '99999999'
    new_2 = ''
    done = int(0)
    coun = int(0)
    while done == int(0):
        if coun == int(0):
            try:
                js, old, new, TS, B_L = get_old(fname)
            except:
                pen('',fname)
                js, old, new, TS, B_L = get_txns(add,B_L,B_G)
            coun = coun + 1
        else:
            js, old, new, TS, B_L = get_txns(add,B_L,B_G)
        js_2, old_2, new_2, TS_2, B_L_2 = get_txns(add,B_L,B_G)
        check = comp(new,new_2)
        if check == int(1):
            js = hashem(js)
            pen(js,fname)
            return
        else:
            js = str(js) + str(js_2)
            js = hashem(js)
            pen(js,fname)
            B_L = B_L_2
    return
def hashem(js):
    tot = ''
    wall = '['+str(js).replace("'",'"').replace('[','').replace(']','').replace(' ','').replace('}{','},{')+']'
    pen(wall,'recent.txt')
    wall = json.loads(str(wall).replace("'",'"'))
    i = 0
    num = count_ls(wall)
    while i != int(num):
        new = wall[i]
        tot = tot + '\n'+ str(new)+','
        i = i + 1
    tot = str(tot).replace("'",'"')
    return tot
def gek(x):
    try:
        x = float(x)
        return x
    except:
        price_ls = reader(home + 'price_ls.txt')
        
        if str(price_ls) == "None":
            last = float(0)
            price_ls = ''
            price_js = json.loads('['+str(price_ls).replace("'",'"')+']')
        else:
            price_js = json.loads('{'+str(price_ls).replace("'",'"')+'}')
            last = float(price_js["last"])
            rem = '"last":"'+str(last)+'"'
            price_ls = str(price_ls).replace(rem,'')
            if price_ls[0] == ',':
                price_ls = price_ls[1:]
            price_js = json.loads('{'+str(price_ls).replace("'",'"')+'}')
        if x not in price_js:
            diff = float(datetime.datetime.now().timestamp()) - float(last)
            if float(diff) < float(3):
                t = float(3) - float(diff)
                time.sleep(t)
            last = datetime.datetime.now().timestamp()
            r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+str(x)+'&vs_currencies=usd')
            page_source = r.text
            pr = json.loads(page_source)[x]['usd']
            price_ls = '"last":"'+str(last)+'",'+price_ls+',"'+str(x)+'":"'+str(pr)+'"'
            
        else:
            pr = price_js[x]
            price_ls = '"last":"'+str(last)+'",'+price_ls
        pen(str(price_ls).replace("'",'"').replace(',,',','),home + 'price_ls.txt')
        return pr

def LP(x):
    pairs = [x]
    LP = {"WGLMR-GLINT":{"cont":"0x99588867e817023162f4d4829995299054a5fc57","dec":"18","farm":"0xC6ca172FC8BDB803c5e12731109744fb0200587b"}}
    specs = {"WGLMR":{"cont":"0xacc15dc74880c9944775448304b263d191c6077f","dec":"18","gek":"wrapped-moonbeam"},"GLINT":{"cont":"0xcd3b51d98478d53f4515a306be565c6eebef1d58","dec":"18","gek":"beamswap"}}
    dec_const = '1e-'
    pair = pairs[0]
    tok = str(pair).split('-')
    A = tok[0]
    B = tok[1]
    farm = LP[pairs[0]]["farm"]
    lp_add = LP[pairs[0]]["cont"]
    A_add = specs[A]["cont"]
    B_add = specs[B]["cont"]
    lp_dec = dec_const + LP[pairs[0]]["dec"]
    A_dec = dec_const + specs[A]["dec"]
    B_dec = dec_const + specs[B]["dec"]
    A_gek = specs[A]["gek"]
    B_gek = specs[B]["gek"]
    LP_sup = float(sites(tok_sup(lp_add))['result'])*float(lp_dec)
    A_sup = float(sites(supply(A_add,lp_add))['result'])*float(A_dec)
    B_sup = float(sites(supply(B_add,lp_add))['result'])*float(B_dec)
    i = 0
    last = 0
    A_price = gek(A_gek)
    B_price = gek(B_gek)
    A_liq = float(A_price)*float(A_sup)
    B_liq = float(B_price)*float(B_sup)
    LP_liq = A_liq + B_liq
    LP_price = LP_liq/LP_sup
    varis = pair,LP_sup,A_sup,B_sup,LP_price,A_price,B_price
    tots = '{"'+str(varis[0])+'":{"sup":{"LP":"'+str(varis[1])+'","A":"'+str(varis[2])+'","B":"'+str(varis[3])+'"},"prices":{"LP":"'+str(varis[4])+'","A":"'+str(varis[5])+'","B":"'+str(varis[6])+'"}}'
    add = '0x19De2695BCb688712f4D65597537F9419a47aD72'
    LP_pers = float(sites(supply(lp_add,add))['result'])*float(lp_dec)
    B_L = '00000000'
    B_G = '99999999'
    txns = sites(wall_sup(add,B_L,B_G))['result']
    num = count_ls(txns)
    i = 0
    out = 0
    inn = 0
    while i != num:
        new = txns[i]
        cont = str(new['contractAddress']).lower()
        lp_cont = str(lp_add).lower()
        farm = str(farm).lower()
        if cont == lp_cont:
            to = str(new['to']).lower()
            fro = str(new['from']).lower()
            if to == farm:
                val = float(out) + float(new['value'])
                out = out + float(val)*float(lp_dec)
            elif fro == farm:
                val = float(new['value'])
                inn = inn + float(val)*float(lp_dec)
        i = i + 1
    farm = out - inn
    liq_pers = float(farm)*float(LP_price)
    print('total_lp: ',str(farm),' total_price: ',str(liq_pers))
    A_perc = A_liq/LP_liq
    B_perc = B_liq/LP_liq
    LP_pers = farm + LP_pers
    LP_perc = float(LP_pers)/float(LP_sup)
    A_pers = float(A_sup)*float(LP_perc)
    B_pers = B_sup*LP_perc
    print(LP_pers,A_pers,B_pers)
    return A,A_pers,B,B_pers,lp_add
def check_lp(x):
    print('checking lp',x)
    lp_specs = LP(x)
    new_lp = '"'+str(lp_specs[0])+'":"'+str(lp_specs[1])+'","'+str(lp_specs[2])+'":"'+str(lp_specs[3])+'"'
    LP_ADD = lp_specs[4]
    print('{'+str(new_lp).replace("'",'"').replace('}','').replace('{','')+'}')
    new_lp = json.loads('{'+str(new_lp).replace("'",'"').replace('}','').replace('{','')+'}')
    pen(str(new_lp),'new_lp.txt')
    return new_lp
def json_up(x,i):
    if i == 0:
        n = '"'+str(x)+'"'
    else:
        n = ',"'+str(x)+'"'
    return n
def node_get(ti,val,to,fro):
    node = json.loads(reader('node_stats.txt'))
    node_num =  count_ls(node)
    unclaimed = float(node[0])
    node_claim = float(node[1])
    node_tot = float(node[2])
    node_input = float(node[3])
    tot_acc = float(node[4])
    acc_day_tot = float(node[5])
    acc_sec = float(node[6])
    last_cl = float(node[7])
    T_S = float(datetime.datetime.now().timestamp())
    n = ''
    w = n_claim
    x = n_cont
    y = n_num
    z = n_acc
    n_ti = float(ti)
    cl_ii = count_ls(x)
    cl_ii_2 = 0
    while float(cl_ii_2) != float(cl_ii):
        if to == str(x[cl_ii_2]).lower():
            val_i = 0
            val_ii = count_ls(y)
            if str(int(val)) in y and val_ii != 1:
                fin = 0
                while val_i != val_ii and fin != 1:
                    if y[val_i] == str(int(val)):
                        fin = 1
                    else:
                        val_i = val_i + 1
            if str(int(val)) not in y:
                partial = (float(val)/float(y[0]))
            else:
                partial = 1
            node_tot = float(node_tot) + float(1)
            node_input = float(node_input) + float(val)
            acc_sec = float(((float(z[val_i])/float(60*60*24)))*float(partial))
            acc_day_tot = float(acc_day_tot) + (float(z[val_i])*float(partial))
            tot_acc = float(tot_acc) + ((float(T_S)-float(n_ti))*float(acc_sec))
        cl_ii_2 = cl_ii_2 + 1
    cl_i = count_ls(w)
    cl_i_2 = 0
    while cl_i_2 != cl_i:
        if fro == str(w[cl_i_2]).lower():
            claim = 1
            node_claim = float(node_claim) + float(val)
            if float(last_cl) < float(n_ti):
                last_cl = float(n_ti)
                c_ti = float(datetime.datetime.now().timestamp())
                unclaimed = float(float(c_ti) - float(last_cl))*float(acc_sec)
        cl_i_2 = cl_i_2 + 1
    b = float(unclaimed), node_claim, node_tot, node_input, tot_acc, acc_day_tot, acc_sec,last_cl
    i = 0
    i_num = len(b)
    while i != i_num:
        new = str(b[i])
        n = n + json_up(new,i)
        
        i = i + 1
    pen('['+n+']','node_stats.txt')
def tot_maker(x,y,z,x_x,y_y,z_z,i):
    x = x + json_up(str(x_x),i)
    y = y + json_up(str(y_y),i)
    z = z + json_up(str(z_z),i)
    
    return x,y,z
def tot_js(x,y,z):
    x = json.loads('['+x+']')
    y = json.loads('['+y+']')
    z = json.loads('['+z+']')
    return x,y,z
def node_globs():
    global unclaimed, node_claim, node_tot, node_input, tot_acc, acc_day_tot, acc_sec, node_tot, node_claim, node_input
    return unclaimed, node_claim, node_tot, node_input, tot_acc, acc_day_tot, acc_sec, node_tot, node_claim, node_input
def node_glob_zero():
    global unclaimed, node_claim, node_tot, node_input, tot_acc, acc_day_tot, acc_sec, node_tot, node_claim, node_input
    unclaimed = 0
    node_claim = 0
    node_tot = 0
    node_input = 0
    tot_acc = 0
    acc_day_tot = 0
    acc_sec = 0
    node_tot = 0
    node_claim = 0
    node_input = 0
add_ls = ["0x19de2695bcb688712f4d65597537f9419a47ad72","0xde57cd4b0d5037ee7d1d8680aa021f9cfbca7f34","0x1b8da9e778815046c819750e22debe66b5265117"]
scan = ['moonbeam.moonscan.io','etherscan.io','ftmscan.com','cronoscan.com','snowtrace.io','bscscan.com','polygonscan.com']
price_name = {"SHARE":"0.005652","WGLMR":"wrapped-moonbeam","GLINT":"beamswap","GLMR":"moonbeam","NeBu":"5.10","MILK":"dairy-money-milk","USDT":"tether","USDC":"usd-coin","MATIC":"wmatic","WETH":"ethereum","ETH":"ethereum","CRN":"cronodes","CRO":"wrapped-cro","AVAX":"wrapped-avax","BSC":"wbnb","FTM":"fantom","POWER":"power-nodes","STRONG":"strong","LINK":"chainlink","SPORES":"spores-network","OXY-FI":"25","OXY":"oxygen"}
pairs = ["SHARE","WGLMR","GLINT","GLMR","NeBu","MILK","USDT","USDC","STRONG","WETH","OXY","LINK","SPORES","POWER","CRN","OXY-FI"]
nodes = ["NeBu","MILK","POWER","CRN","STRONG"]
array = {
        "etherscan.io":{
            "TOKEN":["ETH"],
            "STRONG":{"upg":"N","tax":"0","acc":["0.092"],"red":[],"node_cont":["0xfbddadd80fe7bda00b901fbaf73803f2238ae655"],"cont":"0x990f341946a3fdb507ae7e52d17851b87168017c","node_#":["10"],"claim":["0xfbddadd80fe7bda00b901fbaf73803f2238ae655"]},
            "WETH":{"cont":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"},
            "OXY":{"cont":"0x965697b4ef02f0de01384d0d4f9f782b1670c163"},
            "LINK":{"cont":"0x514910771af9ca656af840dff83e8264ecf986ca"},
            "SPORES":{"cont":"0x8357c604c5533fa0053beaaa1494da552cea38f7"},
            "USDC":{"cont":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"},
            "USDT":{"cont":"0xdac17f958d2ee523a2206206994597c13d831ec7"}
            },
        "ftmscan.com":{
            "TOKEN":["FTM"],
            "POWER":{"upg":"N","tax":"0.1","acc":["0.003","0.025","0.1","0.7"],"red":[],"node_cont":["0xf9f64b2c62210e6acc266169da7026f209cecd52"],"cont":"0x131c7afb4e5f5c94a27611f7210dfec2215e85ae","node_#":["1","5","10","50"],"claim":["0x0E759Ff4f4C0735c35BF0Fe87A4Ae6602C227DA9"]},
            "USDC":{"cont":"0x04068da6c83afcfa0e13ba15a6696662335d5b75"},
            "WETH":{"cont":"0x74b23882a30290451a17c44f4f05243b6b58c76d"}
            
        },
        "cronoscan.com":{
            "TOKEN":["CRO"],
            "CRN":{"upg":"N","tax":"0.05","acc":["1"],"red":[{"time":"1647237600","perc":"0.5"}],"node_cont":["0x8174bac1453c3ac7caed909c20ceadeb5e1cda00"],"cont":"0x8174bac1453c3ac7caed909c20ceadeb5e1cda00","node_#":["20"],"claim":["0x6ad4ff63fd7cf6672ee33cdad8e3ee14bad52b4e","0xb0dd5606a1201992e354fc820101db23113744ef"]},
            "USDT":{"cont":"0x66e428c3f67a68878562e79a0234c1f83c208770"},
            "WETH":{"cont":"0xe44fd7fcb2b1581822d0c862B68222998a0c299a"},
            "USDC":{"cont":"0xc21223249ca28397b4b6541dffaecc539bff0c59"}
            },
        "snowtrace.io":{
            "TOKEN":["AVAX"],
            "OXY-FI":{"upg":"Y","tax":"0.1","acc":["0.00417","0.027","0.1","0.291","1"],"red":[],"node_cont":["0x2dd0d1c14586731701706de1abf9b2dc47561645"],"cont":"0x2dd0d1c14586731701706de1abf9b2dc47561645","node_#":["1","6","20","50","150"],"claim":["0x2dd0d1c14586731701706de1abf9b2dc47561645"]},
            "MILK":{"upg":"N","tax":"0.1","acc":["0.6"],"red":[{"time":"1647093434","perc":"0.6666666666666667"}],"node_cont":["0x3212328f9adb6608f8a10a973ad7e8757f85023f","0x894aded08989ab2921d3a645461abfe1bfdbd505","0xa84a4e5088629052ee634763423763a6848f078a"],"cont":"0x4D81911F0E30D2E12dcc954091701B39dC59e34a","node_#":["10"],"claim":["0xa84a4e5088629052ee634763423763a6848f078a"]},
            "NeBu":{"upg":"N","tax":"0.1","acc":["1.44"],"red":[{"time":"1647093434","perc":"0.48412698412698412698412698412698"}],"node_cont":["0x1aea17a08ede10d158baac969f809e6747cb2b22"],"cont":"0x1aea17a08ede10d158baac969f809e6747cb2b22","node_#":["10"],"claim":["0x6912b4ee8370306c719f2f78129114b75581dcf8"]},
            "USDC":{"cont":"0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e"}
            },
        "bscscan.com":{
            "TOKEN":["BSC"],
            "WETH":{"cont":"0x4db5a66e937a9f4473fa95b1caf1d1e1d62e29ea"},
            "USDC":{"cont":"0xb04906e95ab5d797ada81508115611fee694c2b3"},
            "BUSD":{"cont":"0xe9e7cea3dedca5984780Bafc599bD69add087d56"}
            },
        "polygonscan.com":{
            "TOKEN":["MATIC"],
            "WETH":{"cont":"0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"},
            "USDC":{"cont":"0x2791bca1f2de4661ed88a30c99a7a9449aa84174"},
            "USDT":{"cont":"0xc2132d05d31c914a87c6611c10748aeb04b58e8f"}
            },
        "moonbeam.moonscan.io":{
            "LP":["WGLMR-GLINT"],
            "TOKEN":["GLMR"],
            "WGLMR":{"cont":"0xacc15dc74880c9944775448304b263d191c6077f"},
            "GLINT":{"cont":"0xcd3b51d98478d53f4515a306be565c6eebef1d58"},
            "SHARE":{"cont":"0x4204cad97732282d261fbb7088e07557810a6408","farm":"0xb6b3390b334fa2d35951e5700982d42a9e1e5771"},
            "USDT":{"cont":"0xefaeee334f0fd1712f9a8cc375f427d9cdd40d73"},
            "USDC":{"cont":"0x8f552a71efe5eefc207bf75485b356a0b3f01ec9"}
            }
        }
globular()

fold_name = foldersave()
i_add = int(0)
num_add = int(len(add_ls))


pen("None",'price_ls.txt')

for Q in range(0,1):
    add = add_ls[i_add]
    print(add)
    os.chdir(fold_name +str(add))
    Q = 2
for Q in range(2,3):
    i_scan = int(0)
    num_scan = int(len(scan))
    while i_scan != num_scan:
        x = scan[i_scan]
        print(x)
        scan_glob(x)
        fname = x +'.txt'
        wall()
        i_scan = i_scan + int(1)
    Q = 4
for Q in range(4,5):
    num_pa = int(count_ls(pairs))
    i_pri = int(0)
    price_total = ''
    out_total = ''
    inn_total = ''
    balances = ''
    while i_pri != num_pa:
        price_total,out_total,inn_total = tot_maker(price_total,out_total,inn_total,float(0),float(0),float(0),i_pri)
        i_pri = i_pri + int(1)
    price_total,out_total,inn_total = tot_js(price_total,out_total,inn_total)
    new_lp = ''
    balances = ''
    pen('','node_stats_perm.txt')
    i_scan = 0
    while i_scan != num_scan:
        lp = 0
        node = 0
        scanners = scan[i_scan]
        fname = scanners +'.txt'
        print(fname)
        if str(add).lower() == str('0x19de2695bcb688712f4d65597537f9419a47ad72').lower() and scanners == 'etherscan.io':
            B_ADD = "{'blockNumber': '13301750', 'timeStamp': '1635964658', 'hash': '0x3ebfd66adcbd12e06a5eab732f47656e652e47c955854ce6b4eec1257071657c', 'nonce': '163', 'blockHash': '0xe5c30900a51cde887708b2973aeb2537a193b68f1cf80b3866ea3ce118f0c036', 'from': '0x19de2695bcb688712f4d65597537f9419a47ad72', 'contractAddress': '0x990f341946a3fdb507ae7e52d17851b87168017c', 'to': '0xfbddadd80fe7bda00b901fbaf73803f2238ae655', 'value': '10000000000000000000', 'tokenName': 'Strong', 'tokenSymbol': 'STRONG', 'tokenDecimal': '18', 'transactionIndex': '215', 'gas': '148832', 'gasPrice': '51293067031', 'gasUsed': '144192', 'cumulativeGasUsed': '17256374', 'input': 'deprecated', 'confirmations': '984782'}\n,{'blockNumber': '13301749', 'timeStamp': '1635964657', 'hash': '0x3ebfd66adcbd12e06a5eab732f47656e652e47c955854ce6b4eec1257071657c', 'nonce': '163', 'blockHash': '0xe5c30900a51cde887708b2973aeb2537a193b68f1cf80b3866ea3ce118f0c036', 'from': '0x990f341946A3fdB507aE7e52d17851B87168017c', 'contractAddress': '0x990f341946a3fdb507ae7e52d17851b87168017c', 'to': '0x19de2695bcb688712f4d65597537f9419a47ad72', 'value': '10000000000000000000', 'tokenName': 'Strong', 'tokenSymbol': 'STRONG', 'tokenDecimal': '18', 'transactionIndex': '215', 'gas': '148832', 'gasPrice': '51293067031', 'gasUsed': '144192', 'cumulativeGasUsed': '17256374', 'input': 'deprecated', 'confirmations': '984782'}"
            js = '['+str(str(reader_B(fname))[:-1]).replace("'","'")+']'
            js = json.loads(js)
        else:
            js = '['+str(str(reader_B(fname))[:-1]).replace("'","'")+']'
            js = json.loads(js)
        curr_arr = array[str(scanners)]
        if "LP" in curr_arr:
            new_lp = check_lp(curr_arr["LP"][0])
            lp = 1
        tok = curr_arr["TOKEN"][0]
        main = float(sites(eth_sup(add))['result'])*float(float(10)**(float(-1)*float(18)))
        if float(main) > float(0.0001):
            balances = balances + '\n"'+str(tok)+'":{"in":"'+str(0)+'","out":"'+str(0)+'","total":"'+str(main)+'"},'
        i_pa = int(0)
        while i_pa != num_pa:
            new_tot_ls = ''
            new_out_ls = ''
            new_inn_ls = ''
            n = 0
            pen('["0","0","0","0","0","0","0","0"]','node_stats.txt')
            new = pairs[i_pa]
            price = gek(price_name[new])
            print(price)
            if new == "USDT" or new == "USDC":
                expo = float(10)**(float(-1)*float(6))
            else:
                expo = float(10)**(float(-1)*float(18))
            glob_expo(expo)
            if new in nodes:
                n = 1
            print('pair: ',new)
            if new in curr_arr:
                cont = curr_arr[new]["cont"]
                inn,out,farm = wall_scan(js,cont,curr_arr[new],n)
                total = float(float(expo) * float(sites(supply(cont,add))['result']))+float(farm)
                if lp == 1 and new in new_lp:
                    total = float(total) + float(new_lp[new])
                if n == 1:
                    node = json.loads(reader('node_stats.txt'))
                    node_p = reader('node_stats_perm.txt')
                    if node_p == '':
                        pen('{"'+str(new)+'":'+str(node)[1:-1]+'}','node_stats_perm.txt')
                    else:
                        pen(str(node_p)+'\n,"'+str(new)+'":{'+str(node)[1:-1]+'}','node_stats_perm.txt')
                    total = float(total) + float(node[0])*float(node[5])
                    print(node)
                if float(total) > float(0.0001):
                    i_tot = int(0)
                    while i_tot != num_pa:
                        if i_tot == i_pa:
                            new_tot_ls,new_out_ls,new_inn_ls = tot_maker(new_tot_ls,new_out_ls,new_inn_ls,float(price_total[i_tot])+ float(total),float(out_total[i_tot])+ float(out),float(inn_total[i_tot])+ float(inn),i_tot)
                        else:
                            new_tot_ls,new_out_ls,new_inn_ls = tot_maker(new_tot_ls,new_out_ls,new_inn_ls,float(price_total[i_tot]),float(out_total[i_tot]),float(inn_total[i_tot]),i_tot)
                        i_tot = int(i_tot) + int(1)
                    price_total,out_total,inn_total = tot_js(new_tot_ls,new_out_ls,new_inn_ls)
                    print('price_totals',price_total)
            i_pa = i_pa + int(1)
        i_scan = i_scan + int(1)
        print('iscan',i_scan)
    i_tot = int(0)
    new = ''
    while int(i_tot) != int(i_pa):
        if float(price_total[i_tot]) > float(0.0001):
            balances = balances + '\n"'+str(pairs[i_tot])+'":{"in":"'+str(inn_total[i_tot])+'","out":"'+str(out_total[i_tot])+'","total":"'+str(price_total[i_tot])+'","price":"'+str(float(gek(price_name[pairs[i_tot]])))+'},'
        i_tot  = int(i_tot) + int(1)
    pen_B(str(balances),'balances.txt')
    Q = 6

i_add = i_add + 1
if i_add != num_add:
    Q = 0
