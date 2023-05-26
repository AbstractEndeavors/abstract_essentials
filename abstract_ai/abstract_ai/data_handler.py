def send_chunks(prompt:str =default_prompt(), content:str='', model: str = get_default_models(),endpoint: str = get_default_endpoint(),max_tokens:int = get_default_tokens(),title:str='current'):
    content_chunks = re.findall('.{1,%s}' % (max_tokens // 2), content)  # Change the number based on the desired chunk size
    responses = []
    for k, chunk in enumerate(content_chunks):
        chunk_prompt = f"{prompt}, this is part {k + 1} of {len(content_chunks)} for the data set {title}.:\n{chunk}"
        response = requests.post(endpoint, json=create_prompt({}, model=model, prompt=chunk_prompt, max_tokens=max_tokens, endpoint=endpoint), headers=headers())
        generated_text = response['choices'][0]['text'].strip()
        try:
            response_json = json.loads(generated_text)
            notation = response_json["notation"]
            target_response = response_json["target_response"]
            responses.append({"notation": notation, "target_response": target_response})
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
    return responses
