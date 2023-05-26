import openai
import requests
from abstract_essentials.abstract_security.envy_it import get_openai_key 
def getAPIkey():
    return get_openai_key()
def headers():
    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {getAPIkey()}'}
def raw_request(endpoint:str,js:dict):
    return requests.post(endpoint, json=js, headers=headers())
def hard_request(max_tokens, prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response
def quick_request():
    prompt = "Your Prompt Here"
    max_tokens = 4096  # Set this to the appropriate value
    response = hard_request(max_tokens, prompt)
    print(json.dumps(response.choices[0].text.strip(), indent=4))
def chunk_size(user_input:any=None):
    initial_max_chunk_size = len(user_input)  # Or some other reasonable assumption
    # First, create 'content_chunks' using initial_max_chunk_size
    content_chunks = create_chunks(content, initial_max_chunk_size)
    # Then, calculate 'max_chunk_size' based on actual 'content_chunks'
    max_chunk_size = calculate_max_chunk_size(user_input, len(content_chunks), selected_model)
    # If max_chunk_size is different from initial_max_chunk_size, recreate 'content_chunks'
    if max_chunk_size != initial_max_chunk_size:
        content_chunks = create_chunks(content, max_chunk_size)
def create_chunks(content, max_chunk_size):
    words = content.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk)) + len(word) > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(word)

    chunks.append(' '.join(current_chunk))

    return chunks
def count_tokens(text):
    return len(word_tokenize(text))

def getAPIkey():
    return os.getenv('OPENAI_API_KEY')

def time_stamp():
    now = datetime.now()
    return datetime.timestamp(now)

def get_time_stamp():
    return datetime.now()

def date():
    return datetime.fromtimestamp(time_stamp()).strftime('%d-%m-%y')

def check_token_size(prompt_data: dict, max_tokens: int) -> int:
    message_tokens = sum([count_tokens(message["content"]) for message in prompt_data["messages"]])
    max_tokens = max_tokens - message_tokens
    if max_tokens < 1:
        raise Exception("Max tokens reduced to less than 1, please adjust your messages or max tokens.")
    return max_tokens

def default_prompt():
    return "I haven't sent anything. How's your day though?"

def create_prompt(js: dict = None, model: str = get_default_models(), prompt: str = default_prompt(), max_tokens: int = get_default_tokens()) -> dict:
    if js is None or not isinstance(js, dict):
        js = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    else:
        js.setdefault("model", model)
        js.setdefault("prompt", prompt)
        js.setdefault("max_tokens", max_tokens)
    
    prompt_data = {"model": js['model'], "messages": [{"role": "user", "content": f'{js["prompt"]}' }], "max_tokens": js['max_tokens']}
    prompt_data["max_tokens"] = check_token_size(prompt_data, prompt_data['max_tokens'])
    # Adjust max_tokens if it exceeds the model's maximum context length minus message tokens
    if prompt_data["max_tokens"] > 8192 - len(prompt_data["messages"]):
        prompt_data["max_tokens"] = 8192 - len(prompt_data["messages"])
    return prompt_data


def raw_data(prompt: str = default_prompt(), js: dict = {}, endpoint: str = get_default_endpoint()):
    if 'prompt' not in js:
        js['prompt'] = prompt
    message_tokens = sum([len(js['prompt']) for message in js['prompt']])
    js['max_tokens'] = get_default_tokens() - 10 - (int(message_tokens) - int(check_token_size(create_prompt(js), int(message_tokens))))
    return save_response(js, requests.post(endpoint, json=create_prompt(js), headers=headers()))

def save_response(js: dict, response: dict, title: str = str(get_time_stamp())):
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
    
    path = mkdirs(os.path.join(mkdirs(os.path.join(mkdirs('response_data'), date())), js['model']))
    pen(os.path.join(path, title + '.json'), json.dumps(js))
    return generated_text
