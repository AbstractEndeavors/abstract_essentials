from nltk.tokenize import word_tokenize


def check_token_size(prompt_data: dict, max_tokens: int) -> int:
    """
    Checks the token size of the prompt data and adjusts the maximum tokens.

    Args:
        prompt_data (dict): The prompt data dictionary.
        max_tokens (int): The maximum number of tokens.

    Returns:
        int: The adjusted maximum tokens.
    
    Raises:
        Exception: If the adjusted maximum tokens are less than 1.
    """
    message_tokens = sum([count_tokens(message["content"]) for message in prompt_data["messages"]])
    max_tokens = max_tokens - message_tokens
    if max_tokens < 1:
        raise Exception("Max tokens reduced to less than 1, please adjust your messages or max tokens.")
    return max_tokens


def count_tokens(text):
    """
    Counts the number of tokens in the given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of tokens.
    """
    return len(word_tokenize(text))
