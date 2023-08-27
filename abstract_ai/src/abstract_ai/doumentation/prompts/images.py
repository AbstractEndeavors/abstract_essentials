images={"images":{
        "create":{
            "endpoint":"https://api.openai.com/v1/images/generations",
            "Content-Type: application/json",
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
            "Content-Type: application/json",
            "request":{
                "image":"otter.png",
                "mask":"mask.png",
                "prompt:"",
                "n":2,
                "size":"1024x1024"
            },
            "response":{
                "created": 1589478378,
                "data": [{"url": "url"},{"url": "url"}]
                }
            },
        "variations":{
            "endpoint":"https://api.openai.com/v1/images/variations",
            "Content-Type: application/json",
            "request":{
                "image":"@otter.png",},
                "n":2,
                "size":"1024x1024"
            }
            "response":{
                "created": 1589478378,
                "data": [
                    {"url": "url"},
                    {"url": "url"}
                ]
            }
        }
        }
input(images)
