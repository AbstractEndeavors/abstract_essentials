from nltk.tokenize import word_tokenize
from .endpoints import default_tokens
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


def calculate_token_distribution(max_tokens:int=default_tokens(), prompt:str="null", completion_percentage:float=40, size_per_chunk:int=None,chunk_prompt:str="",tokenize_js:dict={}):
    total_prompt = ''
    for each in tokenize_js.keys():
        if each != "prompt_data":
            total_prompt+=str(tokenize_js[each])
    total_chunk_data = tokenize_js["prompt_data"]
    completion_percent = convert_to_percentage(tokenize_js["completion_percentage"])
    max_tokens = int(tokenize_js["max_tokens"])
    completion_desired = int(max_tokens*completion_percent)

    request_data_total_length = int(max_tokens)-int(completion_desired)
    total_prompt_length = int(count_tokens(total_prompt))
    ficticious_chunk_length = int(request_data_total_length) - int(total_prompt_length)
    total_chunk_length = int(count_tokens(total_chunk_data))
    ficticious_chunk_length=ficticious_chunk_length
    num_chunks=1
    while ficticious_chunk_length < total_chunk_length:
         total_chunk_length = total_chunk_length- ficticious_chunk_length
         num_chunks+=1
         print(num_chunks)
    chunked_data = create_chunks(total_chunk_data, ficticious_chunk_length)
    token_distribution = {
        "prompt": {
            "available": request_data_total_length-total_prompt_length-ficticious_chunk_length,
            "used": total_prompt_length,
            "desired": request_data_total_length
        },
        "completion": {
            "available": int(request_data_total_length-total_prompt_length-ficticious_chunk_length) + completion_desired,
            "used": 0,
            "desired": completion_desired
        },
        "chunks": {
            "total": num_chunks,
            "length_per": ficticious_chunk_length,
            "data": chunked_data
        }
    }
    print(token_distribution)
    return token_distribution

