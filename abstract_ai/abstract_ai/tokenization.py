from nltk.tokenize import word_tokenize
def check_token_size(prompt_data: dict, max_tokens: int) -> int:
    message_tokens = sum([count_tokens(message["content"]) for message in prompt_data["messages"]])
    max_tokens = max_tokens - message_tokens
    if max_tokens < 1:
        raise Exception("Max tokens reduced to less than 1, please adjust your messages or max tokens.")
    return max_tokens
def count_tokens(text):
    return len(word_tokenize(text))
