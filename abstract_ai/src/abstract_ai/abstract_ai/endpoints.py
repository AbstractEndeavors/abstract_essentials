"""
abstract_ai_calls.py
=====================
This module is part of the `abstract_ai` module of the `abstract_essentials` package. It provides functionality to abstract calls to OpenAI's API, enabling a higher-level interface for users.

Functions:
----------
- initialize_key(): Sets the OpenAI API key for interactions.
- prepare_headers(): Generates the headers for OpenAI API requests.
- send_post(): A generalized POST request to OpenAI's endpoints.
- detailed_request(): Sends an extensive request with full parameters.
- simple_request(): Sends a minimalist request, returning a response.
- additional_response_handling(): Fetches additional responses if required.
- notation_processing(): Analyzes and interprets response notations.
- response_suggestions(): Provides potential improvements or clarifications for the returned output.
- abort_check(): Evaluates if the ongoing request should be terminated.
- default_response_handling(): Processes and returns the default or a user-defined response if needed.
- standard_instruction_creation(): Generates a typical instruction format.
- chunked_data_communication(): Manages communication for chunked data inputs.
- abort_action(): Manages the procedure if a query needs to be terminated.
- response_to_dict(): Transforms the OpenAI API response to a Python dictionary format.
- fetch_current_data_chunk(): Gets the current chunk of data from a series.
- string_to_response_dict(): Parses a string representation to extract the response dictionary.
- fetch_response(): Extracts the JSON formatted response post API call.
- generate_prompt_json(): Creates a JSON structure for API calls.
- save_api_output(): Stores the result of the OpenAI API call.
- secure_request_send(): Safely manages the request considering token limits and chunked data.

Notes:
------
This module is intricately tied with environment variables and dependent modules. For seamless requests and response handling, ensure proper setup of dependencies and appropriate setting of environment variables.

About abstract_ai
--------------------
Part of: abstract_ai
Version: 0.1.7.1
Author: putkoff
Contact: partners@abstractendeavors.com

Source and Documentation:
For the source code, documentation, and more details, visit the official GitHub repository.
github: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai

Notes:
------
This module relies heavily on environment variables and other dependencies to successfully send requests and handle responses. Ensure that you've set up all dependencies correctly and provided the right environment variables.
"""
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
def get_endpoint_defaults():
    return {"audio":{
        "transcriptions":{
            "endpoint":"https://api.openai.com/v1/audio/transcriptions",
            "Content-Type": "multipart/form-data",
            "response_key":"text",
            "models":['whisper-1'],
            "request":{
                "file":"/path/to/file/audio.mp3",
                "model":"whisper-1"
                },
            "response":{
                "text":"""Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."""
                }
            },
        "translations":{
            "endpoint":"https://api.openai.com/v1/audio/translations",
            "Content-Type": "multipart/form-data",
            "request":{
                "file":"/path/to/file/audio.mp3",
                "model":"whisper-1"
                },
            "response":{"text": "Hello, my name is Wolfgang and I come from Germany. Where are you heading today?"}
            }
        },
       "chat":{
        "completions":{
            "endpoint":"https://api.openai.com/v1/chat/completions",
            "Content-Type": "application/json",
            "response_key":"content",
            "models":["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"],
            "request":
            {
                "model":"gpt-4",
                "messages":
                [
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user", 
                        "content": "Hello!"
                    }
                ]
            },
            "response":{
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-3.5-turbo-0613",
                "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "\n\nHello there, how may I assist you today?",
                },
                "finish_reason": "stop"
                }],
                "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
                }
                }
            }
        },
    "embeddings":{
        "endpoint":"https://api.openai.com/v1/embeddings",
        "Content-Type": "application/json",
        "response_key":"data",
        "request":{
            "input": "The food was delicious and the waiter...",
            "model": "text-embedding-ada-002"
        },
        "response":{
            "object": "list",
            "data": [
            {
                "object": "embedding",
                "embedding": [0.0023064255,-0.009327292,-0.0028842222],
                "index": 0
            }
            ],
            "model": "text-embedding-ada-002",
            "usage": {
            "prompt_tokens": 8,
            "total_tokens": 8
            }
        }},
        "images":{
            "create":{
                    "endpoint":"https://api.openai.com/v1/images/generations",
                    "Content-Type": "application/json",
                    "response_key":"data",
                    "models":["default"],
                    "request":{
                        "prompt": "A cute baby sea otter",
                        "n": 2,
                        "size": "1024x1024"
                        },
                    "response":{
                        "created": 1589478378,
                        "data": [{"url": "url"},{"url": "url"}]
                        }
                    },
                "edit":{
                    "endpoint":"https://api.openai.com/v1/images/edits",
                    "Content-Type": "application/json",
                    "response_key":"data",
                    "request":{
                        "image":"otter.png",
                        "mask":"mask.png",
                        "prompt":"A cute otter",
                        "n":2,
                        "size":"1024x1024"
                    },
                    "response":{
                        "created": 1589478378,
                        "data": [{"url": "url"},{"url": "url"}]}
                    },
                "variations":{
                    "endpoint":"https://api.openai.com/v1/images/variations",
                    "Content-Type": "application/json",
                    "response_key":"data",
                    "request":{
                        "image":"@otter.png",
                        "n":2,
                        "size":"1024x1024"
                    },
                    "response":{
                        "created": 1589478378,
                        "data": [{"url": "url"},{"url": "url"}]
                        }
                    }
                },
        
        "moderations":{
            "endpoint":"https://api.openai.com/v1/moderations",
            "Content-Type: application/json"
            "response_key":"results",
            "models":["text-moderation-005"],
            "request":{
                "input": "I want to kill them."
                },
            "response":{
                "id": "modr-XXXXX",
                "model": "text-moderation-005",
                "results": [
                    {
                        "flagged": True,
                        "categories": {
                            "sexual": False,
                            "hate": False,
                            "harassment": False,
                            "self-harm": False,
                            "sexual/minors": False,
                            "hate/threatening": False,
                            "violence/graphic": False,
                            "self-harm/intent": False,
                            "self-harm/instructions": False,
                            "harassment/threatening": True,
                            "violence": True,
                        },
                        "category_scores": {
                            "sexual": 1.2282071e-06,
                            "hate": 0.010696256,
                            "harassment": 0.29842457,
                            "self-harm": 1.5236925e-08,
                            "sexual/minors": 5.7246268e-08,
                            "hate/threatening": 0.0060676364,
                            "violence/graphic": 4.435014e-06,
                            "self-harm/intent": 8.098441e-10,
                            "self-harm/instructions": 2.8498655e-11,
                            "harassment/threatening": 0.63055265,
                            "violence": 0.99011886,
                        }
                    }
                ]
            }
        },
        "models":{
            "list":{
                "endpoiont":"https://api.openai.com/v1/models",
                "request":None,
                "response_key":"data",
                "response":{
                    "object": "list",
                    "data": [
                    {
                        "id": "model-id-0",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "organization-owner"
                    },
                    {
                        "id": "model-id-1",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "organization-owner",
                    },
                    {
                        "id": "model-id-2",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "openai"
                    },
                    ],
                    "object": "list"
                }
            },
            "retrieve":{
                "endpoint":"https://api.openai.com/v1/models/{model}",
                "request":"",
                "response":{
                    "id": "text-davinci-003",
                    "object": "model",
                    "created": 1686935002,
                    "owned_by": "openai"
                }
            }
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
