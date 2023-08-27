params={"audio":{
        "transcriptrions":{
            "endpoint":"https://api.openai.com/v1/audio/transcriptions",
            "Content-Type": "multipart/form-data",
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
                "request":"",
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
input(params.keys())
"""
images ={
        
        ,
        ,
    
        }}
input(images)

params = {
    ,
    
    ,
    
         
}
    }
    """

