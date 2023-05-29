from endpoints import *
from prompts import *
def send_chunks(prompt: str = default_prompt(), content: str = '', model: str = default_model(),
                endpoint: str = default_endpoint(), max_tokens: int = default_tokens(), title: str = 'current'):
    """
    Sends the content in chunks to the specified endpoint using the specified model and returns the responses.

    Args:
        prompt (str, optional): The prompt for the API request. Defaults to default_prompt().
        content (str): The content to be sent in chunks.
        model (str, optional): The model to use for the API request. Defaults to default_model().
        endpoint (str, optional): The endpoint for the API request. Defaults to default_endpoint().
        max_tokens (int, optional): The maximum number of tokens for each chunk. Defaults to default_tokens().
        title (str, optional): The title of the data set. Defaults to 'current'.

    Returns:
        list: A list of dictionaries containing the responses for each chunk. Each dictionary has 'notation'
              and 'target_response' keys.
    """
    content_chunks = re.findall('.{1,%s}' % (max_tokens // 2), content)
    responses = []
    for k, chunk in enumerate(content_chunks):
        chunk_prompt = f"{prompt}, this is part {k + 1} of {len(content_chunks)} for the data set {title}.:\n{chunk}"
        response = requests.post(endpoint, json=create_prompt({}, model=model, prompt=chunk_prompt,
                                                               max_tokens=max_tokens, endpoint=endpoint),
                                 headers=headers())
        generated_text = response['choices'][0]['text'].strip()
        try:
            response_json = json.loads(generated_text)
            notation = response_json["notation"]
            target_response = response_json["target_response"]
            responses.append({"notation": notation, "target_response": target_response})
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
    return responses


def create_chunks(content, max_chunk_size):
    """
    Creates chunks of content based on the specified maximum chunk size.

    Args:
        content (str): The content to be split into chunks.
        max_chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of chunks where each chunk has a size less than or equal to the maximum chunk size.
    """
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


def chunk_size(user_input=None):
    """
    Determines the appropriate chunk size for the user input content.

    Args:
        user_input (str): The user input content.

    Returns:
        int: The calculated maximum chunk size for the content.
    """
    initial_max_chunk_size = len(user_input)
    content_chunks = create_chunks(user_input, initial_max_chunk_size)
    max_chunk_size = calculate_max_chunk_size(user_input, len(content_chunks), selected_model)
    if max_chunk_size != initial_max_chunk_size:
        content_chunks = create_chunks(content, max_chunk_size)

    return max_chunk_size
