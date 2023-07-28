from nltk.tokenize import word_tokenize

def count_tokens(text):
    """
    Counts the number of tokens in the given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of tokens.
    """
    return len(word_tokenize(text))

def convert_to_percentage(number):
    if number > 1:
        return number / 100
    else:
        return number

def create_chunks(content, size_per_chunk):
    tokens = word_tokenize(content)
    chunks = []
    current_chunk = []
    current_size = 0
    for token in tokens:
        current_size += 1
        if current_size > size_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 1
        current_chunk.append(token)
    chunks.append(' '.join(current_chunk))
    return chunks

def calculate_token_distribution(max_tokens, prompt:str, completion_percentage:float=40, size_per_chunk:int=None):
    max_tokens = int(max_tokens)
    completion_percentage = convert_to_percentage(completion_percentage)
    prompt_length = count_tokens(prompt)
    prompt_percentage = 1 - completion_percentage
    prompt_desired = int(max_tokens * prompt_percentage)
    prompt_available = max(0, prompt_desired - prompt_length)
    completion_available = int(max_tokens * completion_percentage)
    completion_desired = completion_available

    if size_per_chunk is None:
        size_per_chunk = prompt_length if prompt_length < max_tokens else max_tokens

    num_chunks = prompt_length // size_per_chunk + 1 if prompt_length % size_per_chunk > 0 else prompt_length // size_per_chunk

    chunked_data = create_chunks(prompt, size_per_chunk)

    token_distribution = {
        "percent_distribution": {
            "prompt": prompt_percentage * 100,
            "completion": completion_percentage * 100
        },
        "prompt": {
            "available": prompt_available,
            "used": prompt_length,
            "desired": prompt_desired
        },
        "completion": {
            "available": prompt_available + completion_available,
            "used": 0,
            "desired": completion_desired
        },
        "chunks": {
            "total": num_chunks,
            "length_per": size_per_chunk,
            "data": chunked_data
        }
    }
    return token_distribution
