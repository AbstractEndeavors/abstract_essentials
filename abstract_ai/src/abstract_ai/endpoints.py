from abstract_utilities.json_utils import invert_json
from abstract_utilities.global_utils import change_glob, get_globes, if_none_default
def get_token_js():
    """
    Returns the JSON dictionary containing token information and endpoints.

    Returns:
        dict: The JSON dictionary containing token information and endpoints.
    """
    return {
        "token_info": {
            "8192": ['gpt-4', 'gpt-4-0314'],
            "32768": ['gpt-4-32k', 'gpt-4-32k-0314'],
            "4097": ['gpt-3.5-turbo', 'gpt-3.5-turbo-0301', 'text-davinci-003', 'text-davinci-002'],
            "8001": ["code-davinci-002", "code-davinci-001"],
            "2048": ['code-cushman-002', 'code-cushman-001'],
            "2049": ['davinci', 'curie', 'babbage', 'ada', 'text-curie-001', 'text-babbage-001', 'text-ada-001']
        },
        "endpoints": {
            'https://api.openai.com/v1/chat/completions': [
                "gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"],
            'https://api.openai.com/v1/completions': [
                "text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"],
            'https://api.openai.com/v1/edits': [
                "text-davinci-edit-001", "code-davinci-edit-001"],
            'https://api.openai.com/v1/audio/transcriptions': ['whisper-1'],
            'https://api.openai.com/v1/audio/translations': ['whisper-1'],
            'https://api.openai.com/v1/fine-tunes': [
                "davinci", "curie", "babbage", "ada"],
            'https://api.openai.com/v1/embeddings': [
                "text-embedding-ada-002", "text-search-ada-doc-001"],
            'https://api.openai.com/v1/moderations': [
                "text-moderation-stable", "text-moderation-latest"]
        }
    }


def get_model_info():
    """
    Retrieves the inverted JSON dictionary of model information.

    Returns:
        dict: The inverted JSON dictionary where the keys are model names and the values are token numbers.
    """
    return invert_json(get_token_js()["endpoints"])


def get_endpoint_info():
    """
    Retrieves the JSON dictionary containing endpoint information.

    Returns:
        dict: The JSON dictionary where the keys are endpoints and the values are lists of models.
    """
    return get_token_js()["endpoints"]


def get_token_info():
    """
    Retrieves the inverted JSON dictionary of token information.

    Returns:
        dict: The inverted JSON dictionary where the keys are token numbers and the values are lists of models.
    """
    return invert_json(get_token_js()["token_info"])


def default_endpoint():
    """
    Returns the default endpoint based on the 'endpoint_selection' setting.

    Returns:
        str: The default endpoint.
    """
    return if_none_default(string='endpoint_selection', default=list(get_endpoint_info().keys())[0])


def default_model():
    """
    Returns the default model based on the 'model_selection' setting.

    Returns:
        str: The default model.
    """
    return if_none_default(string='model_selection', default=list(get_endpoint_info()[default_endpoint()])[0])


def default_tokens():
    """
    Returns the default number of tokens based on the 'token_selection' setting.

    Returns:
        int: The default number of tokens.
    """
    return if_none_default(string='token_selection', default=get_token_info()[default_model()])


def get_defaults(endpoint=default_endpoint(), model=default_model(), tokens=default_tokens()):
    """
    Returns a dictionary containing the default values for endpoint, model, and tokens.

    Args:
        endpoint (str, optional): The default endpoint. Defaults to default_endpoint().
        model (str, optional): The default model. Defaults to default_model().
        tokens (int, optional): The default number of tokens. Defaults to default_tokens().

    Returns:
        dict: A dictionary containing the default values for endpoint, model, and tokens.
    """
    return {"endpoint": endpoint, "model": model, "tokens": tokens}
