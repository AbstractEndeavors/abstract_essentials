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
def glob():
    global den
    den = int(0)
    return den
def reques_timer():
    import datetime
    now = datetime.datetime.now().timestamp()
    i = (float(now) - float(reader('last.txt')))
    if float(i) < float(0.3):
        return (float(0.3) - float(i)), now
    return 0, now
def wall_call(add,B_L,B_G):
    link = wall_sup(add,B_L,B_G)
    JS = sites(link)
    js = JS["result"]
    js = json.loads(js)
    return js
def first_last(js,X):
    Y = X
    try:
        W = js[0]
        F = W['timeStamp']
        B_L = W['blockNumber']
        W = js[-1]
        L = W['timeStamp']
        B_G = W['blockNumber']   
        Y = F,L,B_L,B_G
        if X !=0:
            if int(X[3]) == int(B_G) :
                return Y,int(1)
            else:
                return Y,int(0)
    except:
        return Y,int(-1)

def reader_B(file):
    with open(file, 'r',encoding='UTF-8') as f:
        text = f.read()
        return text
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def pen_B(paper, place):
    #print('pen_B',paper,place)
    with open(place, 'w',encoding='UTF-8') as f:
        f.write(str(paper))
        f.close()
        return
def pen(paper, place):
    with open(place, 'w') as f:
        f.write(str(paper))
        f.close()
        return
def sites(A):
    U = [A]
    for url in U:
        X = str(U[0])
        i,now = reques_timer()
        time.sleep(i)
        r = requests.get(X)
        pen(str(now),'last.txt')
        PS = r.text
        pen(str(PS),'recent.txt')
        JS = json.loads(PS)
    return JS
def keys():
    if scanners == 'bscscan.com':
        key = 'JYVRVFFC32H2ZSKDY1JZKNY7XV1Y5MCJHM'
    elif scanners == 'polygonscan.com':
        key = 'S6X6NY29X4ARWRVSIZJTG1PJS4IG86B3WJ'
    elif scanners == 'ftmscan.com':
        key = 'WU2C3NZAQC9QT299HU5BF7P8QCYX39W327'
    else:
        key = '4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1'
    return key
def block():
    key = keys()
    A = int(datetime.datetime.now().timestamp())
    Bl = 'Block timestamp too far in the future'
    while 'Block timestamp too far in the future' in str(Bl): 
        A = A - int(1000)
        U = 'https://api.'+str(scanners)+'/api?module=block&action=getblocknobytime&timestamp='+str(A)+'&closest=before&apikey='+str(key)    
        JS = sites(U)
        Bl = JS['result']
    return Bl
def exists_js(file):
    try:
        f = reader_B(file)
        if f !='':
            try:
                A = projs(f)
                return A
            except IOError:
                print('json not formed')
        else:
            f = '[]'
            return f
    except IOError:
        pen('[]',file)
        return json.loads('[]')
def exists(file):
    try:
        f = reader_B(file)
    except IOError:
        pen('',file)
        return ''
def exists_cust(file,x):
    try:
        f = reader_B(file)
        return f
    except IOError:
        pen(x,file)
        return x
def dirs_main():
    path = "/home4/putkoff/gtsgate.com/script/wallets"
    # Check current working directory.
    retval = os.getcwd()
    print ("Current working directory %s" % retval)
    # Now change the directory
    os.chdir(path)
    # Check current working directory.
    retval = os.getcwd()
    print("Directory changed successfully %s" % retval)
    #print("Directory '% s' created" % directory)
    return
def dirs_A(fname):
    path = 'C:\\Users\\ruz\\Documents\\ethcatcher\\ethcatcher.io\\'+str(fname)
    # Check current working directory.
    retval = os.getcwd()
    print ("Current working directory %s" % retval)
    # Now change the directory
    os.chdir(path)
    # Check current working directory.
    retval = os.getcwd()
    print("Directory changed successfully %s" % retval)
    #print("Directory '% s' created" % directory)
    return 
def check_dirs(fname):
    path = 'C:\\Users\\ruz\\Documents\\ethcatcher\\ethcatcher.io\\'+str(fname)
    isFile = os.path.isdir(path)
    return isFile 
def change_dir(f):
    path = "/home4/putkoff/gtsgate.com/script/wallets" + '/'+str(f)
    retval = os.getcwd()
    print ("Current working directory %s" % retval)
    os.chdir(path)
    retval = os.getcwd()
    print("Directory changed successfully %s" % retval)
    return
def mkdirs(f):
    import os  
    directory = f
    parent_dir = 'C:\\Users\\ruz\\Documents\\ethcatcher\\ethcatcher.io\\'
    path = os.path.join(parent_dir, directory)  
    os.mkdir(path)  
    print("Directory '% s' created" % directory)
    return path
def dirs_B(U):   
    parent_dir = U
    path = os.chdir(parent_dir)
    os.chdir(str(path))
    print(path)
    return path
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
def tryit_js(js):
    try:
        js = projs(str(js))
        return js
    except:
        return 0
def tryit(A,N):
    try:
        tr = A[N]
        
        return 0, N
    except:
        N = N - 1
        return -1, N
def countit(array,delim):
    array_count = str(array)
    len_count_A = len(array_count)
    array_short = array_count.replace(delim,"")
    len_count_B = len(array_short)
    arr_num = len_count_A - len_count_B
    arr_num = arr_num
    return arr_num
def count_js(B):
    N = 0
    M = 0
    while M != -1:
        M,L_B = tryit(B,N)
        N = N + 1
    L_B = L_B - 1
    return L_B
def find_place(js,str_js):
    str_js = str(str_js).lower()
    found = int(0)
    i = int(0)
    js = projs_B(js)
    num = int(countit(js,','))+int(1)
    while i != int(num) and found != int(1):
        if str(str_js) == js[i]:
            found = int(1)
        else:
            i = int(i) + int(1)
    if found == int(0):
        return 'none'
    else:
        return i
#def sites(A):
#    U = [A]
#    for url in U:
#        X = str(U[0])
#        r = requests.get(X)
#        PS = r.text
#        JS = json.loads(PS)
#    return JS
def supply(add,Ad_pa):
    key = keys()
    CONT_SUP = 'http://api.'+scanners+'/api?module=account&action=tokenbalance&contractaddress='+str(add).lower()+'&address='+str(Ad_pa).lower()+'&tag=latest&apikey='+key
    return  CONT_SUP
def wall_sup(Ad_pa,B_L,B_G):
    key = keys()
    WALL_TR = 'http://api.'+scanners+'/api?module=account&action=tokentx&address='+str(Ad_pa)+'&startblock='+str(B_L)+'&endblock='+str(B_G)+'&sort=asc&apikey='+key
    return WALL_TR
def tok_sup(Ad_pa):
    key = keys()
    TOK_LP = 'https://api-cn.'+scanners+'/api?module=stats&action=tokensupply&contractaddress=' + str(Ad_pa).lower() + '&apikey='+key
    return TOK_LP
def JS_prep(J):
    import gc
    gc.collect()
    J = str(J).replace(' ','').replace("'",'"').replace(']','').replace('[','').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','')
    if str(J) != ' ' and str(J) != '' and str(J) != '[]'and str(J) != '{}':
        J = str(J)
        L = int(len(J))
        i = int(-1)
        N,M = tryit(J,i)
        if int(N) == int(0):
            while (int(N) - int(L)) != int(0):
                if J[i] == '' or J[i] == ',' or J[i] == ']' or J[i] == ' ':
                    J = J[:-1]
                    #L = int(len(J))
                    
                    N = timer(N)
                else:
                    N = int(L)
        L = int(len(J))
        i = int(0)
        N,M = tryit(J,i)
        if int(N) == int(0):
            while (int(N) - int(L)) !=int(0):
                if J[i] == '' or J[i] == ',' or J[i] == ']' or J[i] == ' ':
                    J = J[1:]
                    #L = int(len(J))
                    N = timer(N)
                else:
                    N = int(L)
    return J
def JS_prep(A):
    A = str(A).replace(' ','').replace("'",'"').replace(']','').replace('[','').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','')
    return A
def get_i(x):
    n = count_ls(x)
    i,n = int(0),int(n)
    return i,n
def b_get_i(x):
    n = count_ls(x)
    i,n = int(-1),int(-n)
    return i,n
def b_timer(i):
    n = int(i),int(1)
    n = n[0] - n[1]
    return n
def add_int(ls):
    print(den)
    n = int(count_ls(ls))
    i = int(0)
    v = int(0)
    while i != n:
        v = v + int(ls[i])
        i = timer(i)
    return v
def comma(i):
    i = int(i)
    if i == int(0):
        return ''
    return ','

def int_it(x):
    i,n = get_i(x)
    while i != n:
        z.append(int(n[i]))
        i = timer(i)
    return z
def float_it(x):
    i,n = get_i(x)
    while i < n:
        z.append(float(n[i]))
        i = timer(i)
    return z
def find_brac(x,k):
    i,n = get_i(x)
    a = '[','{',' '
    while int(i) < int(n):
        c = 0
        y = str(x[0])
        while c < 3:
            z = str(x[0]).replace(str(a[c]),'')
            n_z = len(z)
            n_y = len(y)
            if n_z == n_y:
                return x
            c = timer(c)
        x = x[:i]
        i = timer(i)
def b_find_brac(x,k):
    i,n = b_get_i(x)
    a = ']','}',' '
    while int(i) > int(n):
        y = str(x[-1])
        c = 0
        while c < 3:
            z = str(x[-1]).replace(str(a[c]),'')
            n_z = len(z)
            n_y = len(y)
            if n_z == n_y:
                return x
            c = timer(c)
        x = x[:i]
        i = b_timer(i)
def JS_prep_B(A):
    A = str(A).replace(' ','').replace("'",'"').replace(',}','}').replace('{,','{').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','').replace('}','').replace('{','').replace(']','').replace('[','')
    return A
def projs(A): 
    J = JS_prep(A)
    if J == '' or J == ' ':
        return J
    a = '{"'
    b = '":"'
    c = '"},{"'
    d = '","'
    e = '"}'
    aa = '~~~~'
    bb = '^^^'
    cc = 'VVV'
    dd = '>>>'
    ee = '<<<'
    J = str(J).replace('[','').replace(']','').replace(' ','').replace("'",'"').replace(a,aa).replace(e,ee).replace(b,bb).replace(d,dd).replace(c,cc)
    J = str(J).replace(cc,c).replace(dd,d).replace(bb,b).replace(ee,e).replace(aa,a).replace('":"","','":"0","')
    J = J.replace('},{','}\n,{').replace("'",'"')
    #J =  str(J).replace('"tokenName":"","','"tokenName":"0","').replace('"tokenSymbol":"","','"tokenSymbol":"0","').replace('"tokenDecimal":"","','"tokenDecimal":"0","')
    #J =  str(J).replace('":"","','":"0","')
    #J =  str(J).replace('""','"').replace(',,',',')
    #gc.collect()
    #J = str('[' +J+ ']').replace(' ','')
    #J =  str(J).replace('[,','[').replace(',]',']').replace('":"s','*:*s').replace('","s','*,*s').replace('"s',"s")
    #J = str(J).replace('*:*s','":"s').replace('*,*s','","s')
    
    J = str(J).replace(' ','').replace('},','}').replace(',{','{')
    J = str(J).replace('}{','}{').replace('{',',{').replace("'",'"').replace('[,','[').replace(',]',']').replace(' ','').replace('[','').replace(']','').replace(',{','{').replace(' ','').replace('\n','').replace('}{','},{')
    J = find_brac(J,'{')
    J = b_find_brac(J,'}')
    print('den')

    J = '['+str(J).replace("'",'"')+']'


    return json.loads(J)
def projs_B(A):
    J = JS_prep_B(A)
    if J == '':
        return J
    while J[-1] == '' or J[-1] == ',' or J[-1] == ']' or J[-1] == ' ':
        J = J[:-1]
    while J[0] == '' or J[0] == ',' or J[0] == ']' or J[0] == ' ':
        J = J[1:]
    J = '[' + str(J) + ']'
    return json.loads(J)



def count_ls(x):
    i = 0
    n = 0
    while n != 1:
        try:
            y = x[i]
            i = i + 1
        except:
            n = 1
    return i
def timer(i):
    #n = int(i),int(1),int(0),int(den)
    #if n[3] < n[2]: 
    #    return n[0] - n[1] 
    return int(i) + int(1) 
def find_point(B,D,X):
    N = 0
    done = 1
    L = count_js(B)
    while done != 0:
        C = B[N]
        if C[D] == str(X):
            done = 0
        if int(N) == int(L):
            return ''
        N = timer(N)
    N = int(N)
    B = B[N:]
    return B
def check_comp(J):
    J = projs(J)
    tr,N = tryit(J,0)
    if tr != -1:
        B = J[0]
        E = B['blockNumber']
        F = B['timeStamp']        
        D = J[-1]
        G = D['blockNumber']
        H = D['timeStamp']
        print(E,F,G,H,day)
        if int(F) > int(H):
            J = reverse(J)
    return projs(J)
def JS_rev(js):
    pen_B(js,'other1.txt')
    js = projs(js)
    L = count_js(js)
    js = js[L:]
    pen_B(js,'other.txt')
    return js
def check_blk(f,bl,ts):
    print('checking blk')
    J = exists_js(f)
    tr,N = tryit(J,0)
    print(tr,N)
    try:
        J = check_comp(J)
        B = J[0]
        E = B['blockNumber']
        F = B['timeStamp']        
        D = J[-1]
        G = D['blockNumber']
        H = D['timeStamp']
        print(E,F,G,H,day)
        #if int(F) < int(day):
            #J = find_point(J,'timeStamp',int(day))
        return J,G,H
    except:
        return J,bl,ts
def crunch(js_A,js_B):
    JS_A = JS_prep(str(JS_A))
    JS_B = JS_prep(str(JS_B))
    JS_C = str(JS_A) + str(JS_B)
    return JS_C
def rev_js(js):
    L = int(count_js(js)) - int(1)
    A = js[0:L]
    B = js[-1]
    C = crunch(A,B)
    js = projs(str(C))
    return js
def get_stamps(js):
    if str(js) != '' and str(js)!=' ' and str(js) != '[]' and str(js) != '{}':
        A = js[0]
        A = A['timeStamp']
        L = count_js(js)
        B = js[L]
        B = B['timeStamp']
        return A,B
    return js
def reverse(js):
    print('reversing')
    js = projs(js)
    L_N = count_js(js)
    X = ''
    while int(L_N) != int(-1):
        X = str(X) +str(js[L_N])+','
        js = js[0:L_N]
        L_N = timermin(L_N)
    return projs(X)
def wall(add,B_L,B_G,day,file,node_num,node_str):
    js_new = ''
    js = ''
    L = day,0,B_L,B_G
    print('l')
    first = 0
    J,B_L,T_S = check_blk(file,B_L,day)
    pen(J,'wall_recent.txt')
    done = 0
    print(add,B_L,B_G,T_S)
    while int(done) == int(0):
        print('start_wall')
        link = wall_sup(node_str,B_L,B_G)
        print(link)
        JS = sites(link)
        js = JS["result"]
        pen(js,'new_wall_recent.txt')
        while str(js) == 'Max rate limit reached':
            time.sleep(5)
            print('sleeping... wallets')
            js = wall_call(add,B_L,B_G)
            
        L,done = first_last(js,L)
        print(L,done)
        done = int(done)
        print(js)
        A = js[0]
        B = js[-1]
        #if int(A['timeStamp']) > int(B['timeStamp']):
            #js = reverse(js)
        js,T_S = hashit(js,day,L[0],L[2],add,file,node_num,node_str)
        js = JS_prep(js)
        J =  str(J)+','+str(js)
        B_L = L[3] 
    return 0
def check_blk(f,B_L):
    A = exists_js(f)
    
    if A != '' and str(A) != '[]' and A != None:
        J = JS_prep(A)
        
        J = projs(J)
            
        B = J[0]
        print(B)
        C = B['blockNumber']
        D = J[-1]
        E = D['blockNumber']
        
        if float(E) > float(C):
            return E
        return C
    else:
        return B_L
def wall(add,B_L,B_G,day,file):
    import time
    B_G = block()
    L = 0,(int(0)),'000000000',B_G
    pen('','checked.txt')
    first = 0
    J = ''
    B_L = check_blk(file,B_L)
    
    done = 0
    mes = "OK"
    print('fetching txn data')
    while done == 0:
        ##print('willing')
        ms = 'Query Timeout occured. Please select a smaller result dataset'
        while 'Query Timeout occured. Please select a smaller result dataset' in ms:
            link = wall_sup(add,B_L,B_G)
            print(link)
            JS = sites(link) 
            if JS == None:
                return "none"
            ms = JS['message']
        js = JS["result"]
        if len(js) >int(9900):
            B_L = js[-1]['blockNumber']
            n_bl = B_L
            i_bl = -1
            while n_bl == B_L:
                n_bl = js[i_bl]['blockNumber']
                js = js[:i_bl]
                i_bl = i_bl - 1
        print('sorting ',str(len(js)),' more txns')
        

        
       
        #if mes == "No transactions found":
        #    ##print('NONE')
        #    return ['NONE']
        if str(js) == '[]':
            return J
        ##print(js)
        while 'Max rate limit reached' in str(js):
            time.sleep(5)
            ##print('sleeping... wallets')
            js = wall_call(add,B_L,B_G)
        L,done = first_last(js,L)

        J =  projs(str(J).replace(']}',',') + str(js).replace(' ',''))
        print('sorting ',str(len(J)),' total txns')
        B_L = L[3]
           
    J = projs(str(reader(fname)).replace("'",'"') + str(J))
    
    
    pen(str(J),fname)
    return J
def hashit(js,day,T_S,bl,add,fname,node_num,node_str):
    Ts = T_S
    dec_str = float(10)**(float(-1)*float(18))
    print('hashing it')
    js = projs(js)
    tr = 0
    L_B = count_js(js) - int(1)
    H_js = exists_js('hashs.txt')
    B = exists_js('new.txt')
    B = reader('new.txt')
    H = reader('hashs.txt')
    L_N = 0
    if fname == 'new.txt':
        arr = ''
        #L = count_js(pairs)
        L = int(1)
        N = 0
        #while int(N) != int(L):
            #P = pairs[N]
            #arrs = array[P]
            #arr = arr + ',"'+arrs['pair']+'"\n'
            #arr = str(arr).lower()
            #N = N + 1
        arr = '["'+str(add)+'"]'
        #arr = str(arr).replace('[,','[')
        arr = json.loads(arr)
        print(L_N,L_B)
        while int(L_N) != int(L_B) and tr != -1:
            tr,L_N = tryit(js,L_N)
            line = js[L_N]
            Ts = line["timeStamp"]
            cont = line['contractAddress']
            B_L = line['blockNumber']
            value = line['value']
            value_dec = float(value)*float(dec_str)
            if float(value_dec) == float(str(node_num)) and line['to'].lower() == node_str.lower():
                if line['hash'].lower() not in H_js:
                    B = str(B).replace('[]','[')+'\n'+str(line)+','
                    H =H.lower()+ ',"'+str(line['hash']).lower()+'"\n'
                    H_js = str(H).replace('[]','[')+']'
                    H_js = str(H_js).replace('[,','[')
                    H_js = json.loads(H_js)
                #print(L_N,L_B)
            L_N = timer(L_N)
    else:
        while int(L_N) != int(L_B) and tr != -1:
            tr,L_N = tryit(js,L_N)
            line = js[L_N]
            Ts = line["timeStamp"]
            cont = line['contractAddress']
            B_L = line['blockNumber']
            if line['hash'].lower() not in H_js and int(Ts) >= int(T_S) and int(B_L) > int(bl):
                if line['to'].lower() == nodestr.lower() or line['from'].lower() == node_str.lower():
                    B = str(B)+str(line)+',\n'
            L_N = timer(L_N)
            #print(L_N,L_B,fname,Ts,T_S)
    pen(H,'hashs.txt')
    tr,i = tryit(B,0)
    if int(tr) != int(-1):
        if B[0] == ',':
            B = B[1:]
    pen_B(str(B),'new.txt')
    return B,Ts
def prices(tok_A, tok_B,array_specs):
    array_specs = json.loads(array_specs)
    tok_A_allias = array_specs[str(tok_A)]
    tok_B_allias = array_specs[str(tok_B)]
    tok_A_allias = tok_A_allias['name_price']
    tok_B_allias = tok_B_allias['name_price']
    price_A = int(1)
    price_B = int(1)
    si = int(2)
    times = int(0)
    balance_C = ''
    num_tok = int(0)
    page=''
    currencies = [
        'https://api.coingecko.com/api/v3/simple/price?ids='+str(tok_A_allias)+'&vs_currencies=usd',
        'https://api.coingecko.com/api/v3/simple/price?ids='+str(tok_B_allias)+'&vs_currencies=usd'
        ]
    times = si
    while times > 0:
        for url in currencies:
            site_st = str(currencies[num_tok])
            if site_st =='https://api.coingecko.com/api/v3/simple/price?ids=take_other&vs_currencies=usd' or site_st =='https://api.coingecko.com/api/v3/simple/price?ids=dollar&vs_currencies=usd':
                new = site_st.replace('&vs_currencies=usd','')
                new = new.replace('https://api.coingecko.com/api/v3/simple/price?ids=','')
                price = new
            else:                    
                new = site_st.replace('&vs_currencies=usd','')
                new = new.replace('https://api.coingecko.com/api/v3/simple/price?ids=','')
                r = requests.get(url)
                page_source = r.text
                page_source = json.loads(page_source)
                price = page_source[new]
                price = price["usd"]
                new = str(new)
                price = str(price)
            if num_tok == int(0):
                toks = tok_A
                price_A = price
            else:
                toks = tok_B
                price_B = price
            num_tok = num_tok + int(1)
            times = times - int(1)
    if tok_A_allias == 'dollar':
        price_A = float(1.00)
    if tok_B_allias == 'dollar':
        price_B = float(1.00)
    return price_A, price_B
def works(worksheet, tok_A_B_add, tok_A, tok_B, tok_A_B, balance_A, balance_B, balance_C, price_A, price_B, tok_A_T, tok_B_T,tok_U_T,curr_val_B, avg_eth,num):
    if balance_A == float(0):
        balance_A = int(1)
    if balance_B == float(0):
        balance_B = int(1)
    if balance_C == float(0):
        balance_C = int(1)
    if price_B == "take_other" and price_A == 'take_other':
        price_A = int(1)
        price_B = int(1)
    if price_B == "take_other":
        if balance_B != int(0) and balance_B != float(0.0):
            price_B = (float(price_A)*float(balance_A))/float(balance_B)
        else:
            price_B = int(1)
    if price_A == "take_other":
        if balance_A != int(0) and balance_A != float(0.0) and (0 - float(balance_A)) < float(0.0):
            price_A = (float(price_B)*float(balance_B))/float(balance_A)
        else:
            price_A = int(1)
    liq_A = float(balance_A) * float(price_A)
    liq_B = float(balance_B) * float(price_B)
    tot_liq = liq_A + liq_B
    if price_A == int(0):
        price_A = liq_B / tok_A_T
    if price_B == int(0):
        price_B = liq_A / tok_B_T
    perc_A = liq_A/tot_liq
    perc_B = liq_B/tot_liq
    tok_A_per_UNI = float(balance_A)/float(balance_C)
    tok_vol_A = (float(tok_A_T) * float(price_A))
    tok_A_fee = float(tok_vol_A) * float(0.003)
    tok_per_UNI=tok_A_per_UNI
    tok_B_per_UNI = float(balance_B)/float(balance_C)
    if curr_val_B != float(0.0):
        tok_vol_B = float(curr_val_B)
    else:
        tok_vol_B = float(tok_B_T)
    tok_B_fee = tok_vol_B * float(0.003)
    tok_per_UNI = tok_B_per_UNI
    per_K = int(1000)/tot_liq
    per_ten_K = int(10000)/tot_liq
    per_K_A = per_K*tok_A_fee
    per_ten_K_A = per_ten_K*tok_A_fee
    per_K_B = per_K*tok_B_fee
    per_ten_K_B = per_ten_K*tok_B_fee
    cells = num + int(2)
    alpha_cell = int(0)
    cell = str(alpha[alpha_cell]) + str(cells)
    print(cell)
    timer = int(-1)
    price_diff_B = int(0)
    price_diff_A = int(0)
    price_diff_T = int(0)
    sheet_hist = exists(path_bal+'/sheet_hist.txt')
    sheet_keep = "tok_A_B", "balance_A", "balance_B", "balance_C", "price_A", "price_B", "liq_A", "liq_B", "perc_A", "perc_B", "tot_liq", "tok_A_T", "tok_B_T", "tok_U_T", "tok_A_per_UNI", "tok_B_per_UNI", "tok_vol_A", "tok_vol_B", "tok_A_fee", "tok_B_fee", "per_K_A", "per_ten_K_A", "per_K_B", "per_ten_K_B", "tok_A_B_add", "price_diff_A", "price_diff_B", "hours"   
    sheet_vari = str(tok_A_B), str(balance_A), str(balance_B), str(balance_C), str(price_A), str(price_B), str(liq_A), str(liq_B), str(perc_A), str(perc_B), str(tot_liq), str(tok_A_T), str(tok_B_T), str(tok_U_T), str(tok_A_per_UNI), str(tok_B_per_UNI), str(tok_vol_A), str(tok_vol_B), str(tok_A_fee), str(tok_B_fee), str(per_K_A), str(per_ten_K_A), str(per_K_B), str(per_ten_K_B), str("https://info.uniswap.org/pair/"+tok_A_B_add), str(price_diff_A), str(price_diff_B), str('24')    
    len_keet = countit(str(sheet_keep), ',')
    len_keet = len_keet + int(1)
    print(len_keet)
    num_keet = int(0)
    len_sheet = countit(str(sheet_vari), ',')
    len_sheet = len_sheet + int(1)
    num_sheet = int(0)
    while num_sheet != len_sheet:
        worksheet = worksheet +'\n'+'worksheet.write('+"'"+cell+"'"+', '+"'"+sheet_vari[num_sheet]+"'"+')'
        if num_sheet < int(14):
            if sheet_keep[num_sheet] == 'tok_A_B':
                sheet_hist = str(sheet_hist) + '\n"'+sheet_vari[num_sheet] +'":{'
            elif sheet_keep[num_sheet] == "tok_U_T":
                sheet_hist = str(sheet_hist) + '"'+sheet_keep[num_sheet] +'":"'+sheet_vari[num_sheet]+'"},'
            else:
                sheet_hist = str(sheet_hist) + '"'+sheet_keep[num_sheet] +'":"'+sheet_vari[num_sheet]+'",'
        alpha_cell = alpha_cell + int(1)
        cell = str(alpha[alpha_cell]) + str(cells)
        num_sheet = num_sheet + int(1)
    pen(sheet_hist,path_bal+'/sheet_hist.txt')
    Pr = reader(path_price+'/price.txt')
    P = projs_B(Pr)
    if tok[0] not in P:
        Pr = str(Pr) +'"'+str(tok[0])+'":"'+str(price_A)+'",'
    if tok[1] not in P:
        Pr = str(Pr) +'"'+str(tok[1])+'":"'+str(price_B)+'",'
    pen(Pr,path_price+'/price.txt')
    return worksheet
def renum(old,A_js,day,T_S,eth_avg):
    print('renum',day)
    A = projs(A_js)
    eth_chart = ''
    count = 0
    prev_B = int(day)
    A_txt = old
    B = int(day)
    prev_price = eth_avg
    C = 0
    while C == 1:
        if str(B) not in A:
            B = timer(B)
        else:
            prev_price = float(A[str(B)])
            while int(prev_B) >= int(B):
                print(prev_B)
                eth_chart = ',"'+str(prev_B)+'":"'+str(prev_price)+'"\n'+str(eth_chart)
                prev_B = timer(int(prev_B))
            C = 0
    while C == 0 and int(B) != int(T_S):
        if str(B) in A and int(count) == int(0):
            eth_chart = ',"'+str(B)+'":"'+str(A[str(B)])+'"\n'+str(eth_chart)
            prev_price = float(A[str(B)])
            prev_B = int(B)
        elif str(B) in A and int(count) != int(0):
            curr_price = float(A[str(B)])
            eth_avg = (float(prev_price)+ float(curr_price))/float(2)
            while int(prev_B) != int(B):
                eth_chart = ',"'+str(prev_B)+'":"'+str(eth_avg)+'"\n'+str(eth_chart)
                prev_B = int(timer(prev_B))
            B = int(prev_B)
            count = int(0)
        elif str(B) not in A:
            count = timer(count)
        B = timer(B)
    if int(B) == int(T_S) and int(count) != int(0):
        while int(prev_B) < int(T_S):
            
            prev_B = timer(int(prev_B))
            eth_chart = ',"'+str(prev_B)+'":"'+str(prev_price)+'"\n'+str(eth_chart)
    eth_chart = '"last":"'+str(T_S)+'"\n'+',"avg":"'+str(eth_avg)+'"\n'+str(eth_chart) 
    pen(str(eth_chart),path_price+'/eth_price.txt')
    return eth_chart
def findit(js,X):
    L_eth = count_js(js)
    N = 0
    while js[N] != str(X):
        N = timer(N)
    return N
def organ(js):
    js
    return js
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
    B_L,B_G,Ts,date,day = get_ti()
    foldate = 'fri','sat','sun','mon','tues','wed','thur',
    sec = float(1)
    mi = float(60)
    hour = float(60*mi)
    day = float(24*hour)
    week = float(7*day)
    fri = 1609510651.1613681
    print('fri',fri)
    since = (float(Ts)-(float(fri)))
    D = mi,hour,day,week
    D_2 = 'sec,hour,day,week'
    D_3 = D_2.split(',')
    N = 0
    jas = ''
    home = 'C:\\Users\\ruz\\Documents\\ethcatcher\\ethcatcher.io\\'
    while N <= int(3):
        i = float(since)/float(D[N])
        jas = jas+',"'+str(D_3[N])+'":"'+str(float(i))+'"'
        N = timer(N)
        TSH = str(ch_quote(add_brac(rem_comm(jas))))
        print(i,TSH,N)
        timesheet = json.loads(TSH)
    days = int(float(timesheet['day']))
    date = str(date).replace('-','_')
    print(date,days,foldate)
    fold_name = str(date)
    path_price = str(fold_name)+'/'+'price'
    path_bal = str(fold_name)+'/'+'bal'
    path_workbook = str(fold_name)+'/'+'workbook'
    X = fold_name, path_price,path_bal,path_workbook
    X_name = 'fold_name','path_price','path_bal','path_workbook'
    i = 0
    while i != 4:
        A= check_dirs(X[i])
        print(A)
        if A == True:
            i = timer(i)
        elif A == False:
            print('we change it')
            mkdirs(X[i])
            i = timer(i)
    return fold_name,home+path_price,home+path_bal,home+path_workbook
def make_js(js,str_js,delim,case):
    up_str_js,low_str_js = up_low(str_js)
    if case == '[' or case == ']':
        end = ']'
    elif case == '{' or case == '}':
        end == '}'
    js_whole = str(js)+str(end)
    js_whole = JS_prep_B(js_whole)
    num = countit(js_whole,'"')
    if num != 0 and str(str_js) != '':
        num = int(num)/int(2)
        js = str(js)+',\n"'+ str(low_str_js)+'"'
    elif num == 0 and str_js != '':
        js = str(js)+'\n"'+str(low_str_js)+'"'
    js_whole = str(js) + str(end)
    if js_whole != '[]' and js_whole != '{}':
        js_whole = JS_prep_B(js_whole)  
    return js,js_whole
def up_low(txt):
    up = str(txt).upper()
    low = str(txt).lower()
    return up,low
def get_txns(add,B_L,B_G):
    link = wall_sup(add,B_L,B_G)
    #print(link)
    JS = sites(link)
    #print(JS)
    js = JS["result"]
    return js
def fold_check(x):
    try:
        mkdirs(x)
        return
    except:
        return
def home_glob(x):
    global home
    home = x
def scan_glob(x):
    global scanners
    scanners = x
glob()
den = int(0)
exists_cust('last.txt','0')
note = 'new : 0, '
#net = input("enter the network: etherscan ")
#scan = ['etherscan.io','ftmscan.com','cronoscan.com','snowtrace.io','bscscan.com','polygonscan.com']
exists('saves.txt')
exists('save_names.txt')
save_data = str(reader('saves.txt'))[:-1]
print(save_data)
save_js = '{'+str(save_data)+'}'
save_names_ls = '['+str(reader('save_names.txt'))[:-1]+']'
scan = ['etherscan.io','ftmscan.com','cronoscan.com','snowtrace.io','bscscan.com','polygonscan.com']
save_names_js = json.loads(save_names_ls)
print(save_names_js)
save_num = len(save_names_js)

print('save_num',save_num)
if save_num != 0:
    i = 0
    while i != save_num:
        note = note +str(save_names_js[i])+' : '+str(i+1)+','
        i = i + 1
note = "which save would you like to use?\n" + str(note)[:-1]+'\nAfter input press enter: '
savem = input(note)
print(savem)
B_L = '0000000000'
B_G = '9999999999'
if int(savem) == int(0):
    net = input('what network will this be on?\netherscan.io :0, ,ftmscan.com: 1, cronoscan.com: 2, snowtrace.io: 3, bscscan.com: 4, polygonscan.com: 5\nAfter input press enter: ')
    net = scan[int(net)]
    scan_glob(net)
    add = input("enter the contract address: ")
    node_num = input("# of coin per node: ")
    node_str = input("enter the node address: ")
    link = wall_sup(add,B_L,B_G)
    print(link)
    js = sites(link)
    print('js')
    js = json.loads(str(js).replace("'",'"'))
    js = js["result"]
    num = len(js)
    i_js = 0
    while i_js < num:
        new = js[i_js]
        if str(new["contractAddress"]).lower() == str(add).lower():
            name_str = new["tokenName"]
            symbol_str = new["tokenSymbol"]
            i_js = num
        i_js = i_js + 1
    varis = '{"net":"'+str(net)+'","add":"'+str(add)+'","node_add":"'+str(node_str)+'","node_#":"'+str(node_num)+'","name":"'+str(name_str)+'","symbol":"'+str(symbol_str)+'","fold":"'+str(name_str)+'"}'
    save = input("would you like to save these inputs? (y/n):\nAfter input press enter: ")
    if save == 'y' or save == 'Y':
        save_name = str(name_str)
        if save_name == int(0):
            save_name = str(name_str)
        if save_name not in save_js:
            save_names = reader('save_names.txt')
            save_names_js = json.loads('['+str(save_names)[:-1]+']')
            save_names = save_names + '"'+str(save_name)+'",'
            print(save_name)
            pen(save_names,'save_names.txt')
            old_save = reader('saves.txt')
            new_save = old_save + '"'+str(save_name)+'":'+varis+','
            pen(new_save,'saves.txt')
else:
    varis = '{' + str(reader('saves.txt'))[:-1]+'}'
    varis = json.loads(varis)
    varis = varis[save_names_js[int(savem) - int(1)]]
    pen(str(varis),'curr_vars.txt')
    print(varis)
    add = varis["add"]
    net = varis["net"]
    node_num =  varis["node_#"]
    node_str =  varis["node_add"]
    name_str =  varis["name"]
    symbol_str =  varis["symbol"]
    scan_glob(net)
    
home = os.getcwd()
home_glob(home)
wall_fold = str(home) + '\\'+str(name_str)
print(wall_fold)
fold_check(wall_fold)
os.chdir(wall_fold)
pen(varis,'variables.txt')
exists_cust('last.txt','0')
up_add,low_add = up_low(add)
B_L = '0000000000'
B_G = '9999999999'
day = time.time()
day = int(day)
print('wall')
fname = name_str+'.txt'
no = wall(add,B_L,B_G,day,fname)
js = reader(fname)
js = projs(js)
num = countit(js,'{')
print(num)

up_name_str,low_name_str = up_low(name_str)

up_symbol_str,low_symbol_str = up_low(symbol_str)

counts = exists_cust('recent_scan.txt','{"new":"0","nums":["0","0","0"]}')
counts = json.loads(counts)
new = counts["new"]
counts_nums = counts["nums"]
print(counts_nums)
if str(new) == str(0):
    fro_js = '['
    fro_js,fro_js_whole = make_js(fro_js,'',',',']')
    fro_num_js = '['
    fro_num_js,fro_num_js_whole = make_js(fro_num_js,'',',',']')
else:
    nodes = reader("nodes.txt").replace("'",'"')
    nodes  = json.loads(nodes)
    fro_js = '['+str(nodes["address"])
    fro_js,fro_js_whole = make_js(fro_js,'',',',']')
    fro_num_js = '['+str(nodes["nodes"])
    fro_num_js,fro_num_js_whole = make_js(fro_num_js,'',',',']')
#print(fro_js,fro_num_js,fro_js_whole,fro_num_js_whole)
#print(counts)
glob()
i = int(counts_nums[0])
i_count = int(counts_nums[1])
tot_wall = int(counts_nums[2])
num = int(num) - int(1)
node_nums = int(0)
wal_count = 0
print('start')
while i != num:
    new = js[i]
    fro_str = new['from']
    if str(fro_str).lower() in fro_js_whole:
        fro_num_js,fro_num_js_whole = make_js(fro_num_js,'',',',']')
        fro_num_js_whole = str('['+str(fro_num_js_whole)+']').replace('[[','[').replace(']]',']').replace(',]',']').replace(',,',',')
        fro_num_js_whole = json.loads(fro_num_js_whole)
        place = find_place(fro_js_whole,fro_str)
        prev_num_node = fro_num_js_whole[int(int(place))]
        bef_count = countit(fro_num_js_whole,',')
        bef_fro_num_js_whole = fro_num_js_whole[int(0):int(int(place))]
        aft_fro_num_js_whole = fro_num_js_whole[int(int(place)+int(1)):]
        num_node = str(prev_num_node).replace('"','')
        num_node = int(num_node) + int(1)
        #print('adding 1 to ',prev_num_node,' to make ',num_node)
        new_fro_num_js = str(str(bef_fro_num_js_whole).replace(']',",'")+str(num_node) + str(aft_fro_num_js_whole).replace('[',"',")).replace(' ','')
        fro_num_js,fro_num_js_whole = make_js(new_fro_num_js,'',',',']')
        aft_count = countit(fro_num_js_whole,',')
        #print('bef:',str(bef_count),' aft',str(aft_count),' in spot:',str(place))
    else:
        tot_wall = int(tot_wall) + int(1)
        fro_js,fro_js_whole = make_js(fro_js,str(fro_str),',',']')
        fro_num_js,fro_num_js_whole = make_js(fro_num_js,'1',',',']')
        #print(fro_str, ' not in js_whole, total wallets: ',str(tot_wall))
    if i_count == int(1000):
        new_whole = '{"address":['+str(fro_js_whole) + '],\n' + '"nodes":['+str(fro_num_js_whole).replace('","','",\n"')+']}'
        num_wall = countit(fro_js_whole,',')
        num_num = countit(fro_num_js_whole,',')
        pen(str(new_whole),'nodes.txt')
        i_count = int(0)
        print(i,' txns scanned, ',str(tot_wall),' wallets, ',str(i),' nodes found\n',str(num_num),' nums ',str(num_wall), 'walls')
        pen('{"new":"1","nums":["'+str(i)+'","'+str(i_count)+'","'+str(tot_wall)+'"]}','recent_scan.txt')
    #print(fro_js,fro_js_whole)
    i_count = int(i_count) + int(1)
    i = int(i) + int(1)
new_whole = '{"address":['+str(fro_js_whole) + '],\n' + '"nodes":['+str(fro_num_js_whole).replace('","','",\n"')+']}'
pen(str(new_whole),'nodes.txt')
print('done')
print(i,' txns scanned, ',str(tot_wall),' wallets, ',str(node_nums),' nodes found')
print('tally')
import tally
print('JSON')
import json_test
print('WALLSUPP')
import wallet_supplys
