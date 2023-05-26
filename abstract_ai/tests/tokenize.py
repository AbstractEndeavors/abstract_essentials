from putkoff_functions import*
from putkoff_chatGPT_API import *
def get_max_tokens():
  return 8200
def temp_max_tokens(tokens):
  return get_max_tokens()/2
def count_tokens(text):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return len(tokenizer.encode(text))
js_path={}
if os.path.isdir('response_data'):
  path = os.path.join(os.getcwd(),'response_data')
  objects = os.listdir(path)
  for k in range(0,len(objects)):
    obj=objects[k]
    path = os.path.join(path,obj)
    objects2 =os.listdir(path)
    if os.path.isfile(str(path)):
      js = reader(str(path))
    else:
      for j in range(0,len(objects2)):
        obj2 = objects2[j]
        path = os.path.join(path,obj2)
        ls = os.listdir(path)
        for c in range(0,len(ls)):
          if os.path.isfile(ls[c]):
            js = reader(os.path.join(path,ls[c]))
            try:
              jsN = json.dumps(json.loads(js)['messages'][0]['content'])
              print(jsN)
            except Exception(e):
              print(e)
def gogo():
  temp_max = temp_max_tokens(get_max_tokens())  
  os.listdir()
  reader()
  max_tokens = 8200/2
  title_gen = title_generation()
  
  content = content.split(' ')
  for k in range(0,len(content)):
    n = n + ' '+content[k]
    count_tokens(n)
