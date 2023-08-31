import os
import os.path
import requests
import json
import time
import datetime
import math
def home_it():
    curr = get_curr_path()
    slash = '//'
    if '//' not in str(curr):
        slash = '/'
    changeGlob('slash',slash)
    changeGlob('home',curr)
    return curr,slash
def countit(js,add):
    L = int(count_js(js)) - int(2)
    N = 0
    A = js[N]
    while L != N:
        if str(A) != str(add):
            A = js[N]
            print(A,add)
            N = timer(N)
    print(N)
    return N
def wall_call(add,B_L,B_G):
    link = wall_sup(add,B_L,B_G)
    JS = sites(link)
    js = JS["result"]
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
            if int(B_L) == int(B_G) :
                return Y,1
            else:
                return Y,0
    except:
        return Y,0
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
def sites(A):
    U = [A]
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)
    return JS
def keys():

    return '4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1'
def block(A):
    key = keys()
    U = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp='+str(A)+'&closest=before&apikey='+str(key)
    print(U)
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
        return '[]'
def exists(file):
    try:
        f = reader_B(file)
    except IOError:
        pen('',file)
        return ''
def dirs_A():
    #path = "C:/Users/Dialectic/Desktop/new_uni/wallets/"
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

def dirs_B(U):   
    parent_dir = U
    path = os.chdir(parent_dir)
    os.chdir(str(path))
    print(path)
    return path

def get_ti():
    import datetime
    T_S = datetime.datetime.now().timestamp()
    T_S_D = str(datetime.datetime.now())[0:10]
    day = int(int(T_S) - int(86400))
    B_L = block(day)
    B_G = block(int(T_S))
    
    TS = '{"TS":["'+str(T_S)+'","'+str(T_S_D)+'","'+str(B_L)+'","'+str(B_G)+'"]}'
    pen(TS, 'T_S_pow.py')
    return B_L,B_G,T_S,T_S_D,day
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
def sites(A):
    U = [A]
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)
    return JS
def supply(add,Ad_pa):
    key = keys()
    CONT_SUP = 'http://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='+str(add).lower()+'&address='+str(Ad_pa).lower()+'&tag=latest&apikey='+key
    return  CONT_SUP
def wall_sup(Ad_pa,B_L,B_G):
    key = keys()
    WALL_TR = 'http://api.etherscan.io/api?module=account&action=tokentx&address='+str(Ad_pa)+'&startblock='+str(B_L)+'&endblock='+str(B_G)+'&sort=asc&apikey='+key
    return WALL_TR
def tok_sup(Ad_pa):
    key = keys()
    TOK_LP = 'https://api-cn.etherscan.com/api?module=stats&action=tokensupply&contractaddress=' + str(Ad_pa).lower() + '&apikey='+key
    return TOK_LP
def JS_prep(A):
    A = str(A).replace(' ','').replace("'",'"').replace(']','').replace('[','').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','')
    return A
def JS_prep_B(A):
    A = str(A).replace(' ','').replace("'",'"').replace(',}','}').replace('{,','{').replace('}{','},{').replace('or"s','ors').replace('[,','[').replace('None','').replace('}','').replace('{','').replace(']','').replace('[','')
    return A
def projs(A):
    J = JS_prep(A)
    if J == '':
        return J
    
    while J[-1] == '' or J[-1] == ',' or J[-1] == ']' or J[-1] == ' ':
        J = J[:-1]
    while J[0] == '' or J[0] == ',' or J[0] == ']' or J[0] == ' ':
        J = J[1:]
    
    J =  str(J).replace('"tokenName":"","','"tokenName":"0","').replace('"tokenSymbol":"","','"tokenSymbol":"0","').replace('"tokenDecimal":"","','"tokenDecimal":"0","')
    J =  str(J).replace('":"","','":"0","')
    J =  str(J).replace('""','"')
    pen_B(str(J),'recent.txt')
    J = '[' +J+ ']'
    return json.loads(J)
def projs_B(A):
    J = JS_prep_B(A)
    if J == '':
        return J
    
    while J[-1] == '' or J[-1] == ',' or J[-1] == ']' or J[-1] == ' ':
        J = J[:-1]
    while J[0] == '' or J[0] == ',' or J[0] == ']' or J[0] == ' ':
        J = J[1:]
    J = '{' + str(J) + '}'
    return json.loads(J)
def timer(N):
    N = N + 1
    return N
def timermin(N):
    N = N - 1
    return N
def find_point(B,D,X):
    B = projs(B)
    N = 1
    done = 1
    L = count_js(B)
   
    while done != 0:
        C = B[N]
        if C[D] == X:
            done = 0
        
        N = timer(N)
    N = int(N)
    B = B[0:N]
    return B
def JS_rev(js):
    pen_B(js,'other1.txt')
    js = projs(js)
    L = count_js(js)
    js = js[L:]
    pen_B(js,'other.txt')
    return js
def check_blk(f,B_L):
    A = exists_js(f)
    if A != '':
        J = JS_prep(A)
        pen(J,'checkblk.txt')
        J = projs(J)
            
        B = J[0]
        
        C = B['blockNumber']
        D = J[-1]
        E = D['blockNumber']
        
        if int(E) >= int(B_L):
            J = find_point(A,'blockNumber',C)
            A = JS_prep(J)
    return A
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
def wall(add,B_L,B_G,day,file):
    import time
    L = day,(int(day)+int(86400)),B_G,B_L
    J = ''
    first = 0
    txt = ''
    #J_B = check_blk(file,B_L)
    done = 0
    while done == 0:
        link = wall_sup(add,B_L,B_G)
        JS = sites(link)
        js = JS["result"]
        while str(js) == 'Max rate limit reached':
            time.sleep(5)
            print('sleeping... wallets')
            js = wall_call(add,B_L,B_G)
        L,done = first_last(js,L)
        js = JS_prep(js)
        J =  str(js)+str(JS_prep(J))
        B_L = L[3]
   
    J = projs(J)
    pen_B(str(J),file)
    return J
def hashit(js,add):
    from variables import array, pairs
    arr = ''
    exists_js('burn_wall.txt')
    B = reader('burn_wall.txt')
    B = JS_prep(B)
    #pairs = pairs['pai']
    #L = count_js(pairs)
    #N = 0
    #while N != L:
        #P = pairs[N]
        
        #arrs = array[P]
        
        #arr = arr + ',"'+arrs['pair']+'"\n'
        #arr = str(arr).lower()
        #print(arr)
        #N = N + 1
    L_N = 0
    #pai = JS_prep(arrs)
    L_B = count_js(js)
    H_js = exists_js('hashs.txt')
    H = reader('hashs.txt')
    while int(L_N) != int(L_B):
        line = js[L_N]
        Ts = line["timeStamp"]
        cont = line['contractAddress']
        if cont.lower() in arr and line['hash'].lower() not in H_js:
            if line['to'].lower() == add.lower() or line['from'].lower() == add.lower():
                B = str(B) +','+ str(line)+'\n'
                H =H.lower()+ ',"'+str(line['hash']).lower()+'"\n'
                H_js = projs(H)
        L_N = timer(L_N)
    pen(H,'hashs.txt')
    B = projs(B)
    pen(str(B),'burn_wall.txt')
    return
def prices(tok_A, tok_B,array_specs):
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
    sheet_hist = reader('sheet_hist.txt')
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
    pen(sheet_hist,'sheet_hist.txt')
    return worksheet
def renum(old,A,day,T_S):
    A = json.loads(A)
    print('renum')
    eth_chart = ''
    count = 0
    prev_B = int(day)
    A_txt = str(A)
    B = int(day)
    C = 1
    while C == 1:
        if str(B) not in A:
            B = timer(B)
        else:
            prev_price = float(A[str(B)])
            while int(prev_B) != int(B):
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
        
    eth_chart = '"last":"'+str(T_S)+'"\n'+',"avg":"'+str(A['avg'])+'"\n'+str(eth_chart) + str(old)
    pen(str(eth_chart),'eth_price.txt')
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
addr = input("Enter your value: ") 

time_eth = ''
burn = addr
tots = '{'
B_L,B_G,T_S,T_S_D,day = get_ti()
H_js = exists_js('hashs.txt')
times = exists_js('times.txt')
eth_chart = exists('eth_price.txt')
eth_chart_js = projs(eth_chart)

if 'last' in eth_chart_js:
    last = int(eth_chart_js['last'])
    L_eth = count_js(eth_chart_js)
    if str(day) in eth_chart_js:
        L_eth = findit(eth_chart_js,str(day))
    eth_chart_js = eth_chart_js[2:L_eth]
    eth_chart_old = (eth_chart_js).replace('{','').replace('}','')
    
else:
    eth_chart_old = ''
    last = day
counter = 0
eth_avg = 0
count = 0
counter = 0
times = ''
contract_A = '['
to_A = '['
fro_A = '['
wall_A = '['
to_js = json.loads('[]')
fro_js = json.loads('[]')
contract_js = json.loads('[]')

js = wall(burn,0,B_G,day,'burn_wall_temp.txt')
L_T = count_js(js)
I = 0
hashit(js,burn)
prev_stamp = T_S
hashs_A = 0
hashs_B = 0
vol_B = 0
tok_A_T = 0
tok_B_T = 0
val_B = 0
val_A = 0
count = 0
times = ''
hashs = ''
trans = ''
bal = ''
prev_I = 0
cont = ''
hash_keep = '['
contract_A = '['
to_A = '['
hashs_A = '['
fro_A = '['
wall_A = '['
to_js = json.loads('[]')
fro_js = json.loads('[]')
contract_js = json.loads('[]')
hashs_js = json.loads('[]')
L_T = count_js(js)
I = 0
now = ''
new = ''
while I != L_T:
    hashs_prev = hashs
    contract_prev = cont
    trans_prev = trans
    bal_prev = bal
    W = js[I]
    hashs = W['hash']
    St = W['timeStamp']
    to = str(W['to'])
    hashs = str(W['hash'])
    if hashs not in hashs_js:
        hashs_A = str(hashs_A) + ',"'+str(hashs)+'"'
        hashs_js = str(hashs_A + ']').replace('[,','[')
        hashs_js = json.loads(hashs_js)
    if to not in to_js:
        to_A = str(to_A) + ',"'+str(to)+'"'
        to_js = str(to_A + ']').replace('[,','[')
        to_js = json.loads(to_js)
    fro = str(W['from'])
    if fro not in fro_js:
        fro_A = str(fro_A) + ',"'+str(fro)+'"'
        fro_js = str(fro_A + ']').replace('[,','[')
        fro_js = json.loads(fro_js)
    cont = str(W["contractAddress"])
    if str(cont) not in contract_js:
        print(cont)
        contract_A = str(contract_A)+',"'+str(cont)+'"'
        contract_js = str(contract_A + ']').replace('[,','[')
        contract_js = json.loads(contract_js)
    to = str(W['to'])
    to_N = findit(to_js,to)
    cont_N = findit(contract_js,cont)
    fro_N = findit(fro_js,fro)
    hashs_N = findit(hashs_js,hashs)
    val = int(W['value'])
    symbol = W['tokenSymbol']
    dec = W['tokenDecimal']
    expo = float(10)**(float(-1)*float(dec))
    bal = float(float(val) * float(expo))
    if str(fro).lower() == str(addr).lower():  
        bal = float(0.0) - float(bal)
        trans = to
    elif str(to).lower() == str(addr).lower():
        trans = fro
    else:
        trans = to
    if I != 0:
        if hashs_prev == hashs and counter == 0:
            print(contract_prev)
            hash_new = '"'+str(hashs)+':{"trans_A":["'+str(contract_prev)+'","'+str(bal_prev)+'","'+str(trans_prev)+'"]},"trans_B":["'+str(cont)+'":"'+str(bal)+'","'+str(trans)+'"]}'
            counter = counter + 1
        elif hashs_prev == hashs and counter == 1:
            hash_new = str(hash_new)+',{"trans_C":["'+str(cont)+'":"'+str(bal)+'","'+str(trans)+'"]}'
            counter = counter + 1
        elif hashs_prev == hashs and counter == 2:
            hash_new = str(hash_new)+',{"trans_D":["'+str(cont)+'":"'+str(bal)+'","'+str(trans)+'"]}'
            counter = counter + 1
        elif hashs_prev == hashs and counter == 3:
            hash_new = str(hash_new)+',{"trans_E":["'+str(cont)+'":"'+str(bal)+'","'+str(trans)+'"]}'
            counter = counter + 1
        elif hashs_prev != hashs and counter !=0:
            hash_keep = str(hash_keep) + ',{'+str(hash_new)+'}\n'
            counter = 0
            prev_I = I
        elif hashs_prev != hashs and counter ==0:
            hash_keep = str(hash_keep) + ',{"'+str(hashs)+'{"trans_A":["'+str(cont)+'","'+str(bal)+'","'+str(trans)+'"}]\n'
            counter = 0
            prev_I = I
    if int(I) == int(int(L_T) - int(1)):
        new = str(new)+ '["'+symbol+'","'+str(hashs)+'","'+str(cont)+'","'+str(to)+'","'+str(fro)+'","'+str(bal)+'"]'
        now = str(now)+ '["'+str(hashs_N)+'","'+str(cont_N)+'","'+str(to_N)+'","'+str(fro_N)+'","'+str(bal)+'"]'

    else:
        new = str(new) +'["'+symbol+'","'+str(hashs)+'",'+str(cont)+'","'+str(to)+'","'+str(fro)+'","'+str(bal)+'"],\n'
        now = str(now)+ '["'+str(hashs_N)+'","'+str(cont_N)+'","'+str(to_N)+'","'+str(fro_N)+'","'+str(bal)+'"],\n'
    I = timer(I)
total = str(to_js)+'\n'+str(fro_js)+'\n'+str(contract_js)
pen_B(total,'totals.txt')
pen_B(str(new),'new.txt')
pen_B(str(now),'now.txt')
pen_B(str(hash_keep).replace('[,','['),'hash_keep.txt')

