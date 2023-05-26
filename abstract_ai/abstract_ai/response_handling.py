def save_response(js:dict,response:dict,title:str=str(get_time_stamp())):
    generated_text = response.text
    try:
        js['response'] = response.json()
    except:
        print()
    try:
        generated_text = json.loads(js['response']['choices'][0]['message']['content'])
        if 'title' in generated_text:
            title = generated_text['title']
    except:
        print()
    path = mkdirs(os.path.join(mkdirs(os.path.join(mkdirs('response_data'),date())),js['model']))
    pen(os.path.join(path,title+'.json'),json.dumps(js))
    return generated_text
