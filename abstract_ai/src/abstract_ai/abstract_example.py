import os
##ModelBuilder.py
from abstract_ai import ModelManager
model='gpt-4'
model_mgr = ModelManager(input_model_name=model)
model_mgr.selected_endpoint    #output: https://api.openai.com/v1/chat/completions
model_mgr.selected_max_tokens  #output: 8192

#ApiBuilder.py
#you can put in either your openai key directly or utilize an env value
# the env uses abstract_security module, it will automatically search the following folders for a .env to matcha that value
# - current_directory
# - home/env_all
# - documents/env_all
from abstract_ai import ApiManager
api_env='OPENAI_API_KEY'
api_mgr = ApiManager(api_env=api_env,content_type=None,header=None,api_key=None)
api_mgr.content_type #output application/json
api_mgr.header       #output: {'Content-Type': 'application/json', 'Authorization': 'Bearer ***private***'}
api_mgr.api_key      #output: ***private***



#InstructionBuilder.py
from abstract_ai import InstructionManager
#Each of these methods, with their signature features, enhances the usability and functionality of the Abstract_AI system,
#ensuring optimized interactions, easy navigation through data chunks, and adept handling of responses.
notation = True # allows the module a method of notation that it can utilize to maintain comtext and contenuity from one prompt query to the next
suggestions = True # encourages suggestions on the users implimentation of the current query
abort = True # allows for the module to put a full stop to the query loop if the goal is unattainable or an anamolous instance occurs
generate_title = True # the module wil generate a title for the response file
additional_responses = True # allows for the module to delegate the relooping of a prompt interval, generally to form a complete response if token length is insuficcient, or if context is too much or too little
additional_instruction = "please place any iterable data inside of this key value unless otherwise specified"
request_chunks = True # allows for the module to add an interval to the query loop to retrieve the previous prompt the previous prompt
instruction_mgr = InstructionManager(notation=notation,
                                     suggestions=suggestions,
                                     abort=abort,
                                     generate_title=generate_title,
                                     additional_responses=additional_responses,
                                     additional_instruction=additional_instruction
                                     )

instruction_mgr.instructions 
#output:
"""
your response is expected to be in JSON format with the keys as follows:

0) api_response - place response to prompt here
1) notation - A useful parameter that allows a module to retain context and continuity of the prompts. These notations can be used to preserve relevant information or context that should be carried over to subsequent prompts.
2) suggestions - ': A parameter that allows the module to provide suggestions for improving efficiency in future prompt sequences. These suggestions will be reviewed by the user after the entire prompt sequence is fulfilled.
3) additional_responses - This parameter, usually set to True when the answer cannot be fully covered within the current token limit, initiates a loop that continues to send the current chunk's prompt until the module returns a False value. This option also enables a module to have access to previous notations
4) abort - if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was
5) generate_title - A parameter used for title generation of the chat. To maintain continuity, the generated title for a given sequence is shared with subsequent queries.
6) request_chunks - you may request that the previous chunk data be prompted again, if selected, the query itterate once more with the previous chunk included in the prompt. return this value as True to impliment this option; leave sufficient notation as to why this was neccisary for the module recieving the next prompt
7) additional_instruction - please place any iterable data inside of this key value unless otherwise specified

below is an example of the expected json dictionary response format, with the default inputs:
{'api_response': '', 'notation': '', 'suggestions': '', 'additional_responses': False, 'abort': False, 'generate_title': '', 'request_chunks': False, 'additional_instruction': '...'}"""


#PromptBuilder.py
from abstract_ai import PromptManager
#Calculates the token distribution between prompts, completions, and chunks to ensure effective token utilization.
completion_percentage = 40 #allows the user to specify the completion percentage they are seeking for this prompt(s) currently at 40% of the token allotment
request = "thanks for using abstract_ai the description youre looking for is in the prompt_data"
prompt_data = """The code snippet is a part of `PromptBuilder.py` from the `abstract_ai` module. This specific part shows the crucial role of chunking strategies in the functioning of `abstract_ai`.\n\nThe `chunk_data_by_type` function takes in data, a maximum token limit, and a type of chunk (with possible values like 'URL', 'SOUP', 'DOCUMENT', 'CODE', 'TEXT').Depending on the specified type, it applies different strategies to split the data into chunks. If a chunk type is not detected, the data is split based on line breaks.\n\nThe function `chunk_text_by_tokens` is specifically used when the chunk type is 'TEXT'. It chunks the input data based on the specified maximum tokens, ensuring eachchunk does not exceed this limit.\n\nWith the `chunk_source_code` function, you can chunk source code based on individual functions and classes. This is crucial to maintainthe context and readability within a code snippet.\n\n`extract_functions_and_classes` is a helper function used within `chunk_source_code`, it extracts all the functions andclasses from the given source code. The extracted functions and classes are then used to chunk source code accordingly.\n\nThese functions are called numerous times in the abstract_ai platform, emphasizing their key role in the system."""
chunk_type="Code" #parses the chunks based on your input types, ['HTML','TEXT','CODE']
prompt_mgr = PromptManager(instruction_mgr=instruction_mgr,
                           model_mgr=model_mgr,
                           completion_percentage=completion_percentage,
                           prompt_data=prompt_data,
                           request=request,
                           token_dist=None,
                           bot_notation=None,
                           chunk=None,
                           role=None,
                           chunk_type=chunk_type)

prompt_mgr.token_dist = [{
    'completion':{'desired': 3276,
                  'available': 3076,
                  'used': 200},
    'prompt': {'desired': 4915,
               'available': 4035,
               'used': 880},
    'chunk': {'number': 0,
              'total': 1,
              'length': 260,
              'data': "\nThe code snippet is a part of `PromptBuilder.py` from the `abstract_ai` module. This specific part shows the crucial role of chunking strategies in the functioning of `abstract_ai`.\n\n\nThe `chunk_data_by_type` function takes in data, a maximum token limit, and a type of chunk (with possible values like 'URL', 'SOUP', 'DOCUMENT', 'CODE', 'TEXT').\nDepending on the specified type, it applies different strategies to split the data into chunks. If a chunk type is not detected, the data is split based on line breaks.\n\n\nThe function `chunk_text_by_tokens` is specifically used when the chunk type is 'TEXT'. It chunks the input data based on the specified maximum tokens, ensuring each\nchunk does not exceed this limit.\n\nWith the `chunk_source_code` function, you can chunk source code based on individual functions and classes. This is crucial to maintain\nthe context and readability within a code snippet.\n\n`extract_functions_and_classes` is a helper function used within `chunk_source_code`, it extracts all the functions and\nclasses from the given source code. The extracted functions and classes are then used to chunk source code accordingly.\n\n\nThese functions are called numerous times in the abstract_ai platform, emphasizing their key role in the system."}}]
completion_percentage = 90 # completion percentage now set to 90% of the token allotment
request = "ok now we chunk it up with abstract_ai the description youre looking for is still in the prompt_data"
prompt_mgr = PromptManager(instruction_mgr=instruction_mgr,
                           model_mgr=model_mgr,
                           completion_percentage=completion_percentage,
                           prompt_data=prompt_data,
                           request=request)
prompt_mgr.token_dist = [{'completion':
                          {'desired': 7372,
                           'available': 7172,
                           'used': 200},
                          'prompt':
                          {'desired': 819,
                           'available': 7,
                           'used': 812},
                          'chunk':
                          {'number': 0,
                           'total': 2,
                           'length': 192,
                           'data': "\n\nThe code snippet is a part of `PromptBuilder.py` from the `abstract_ai` module. This specific part shows the crucial role of chunking strategies in the functioning of `abstract_ai`.\n\nThe `chunk_data_by_type` function takes in data, a maximum token limit, and a type of chunk (with possible values like 'URL', 'SOUP', 'DOCUMENT', 'CODE', 'TEXT').Depending on the specified type, it applies different strategies to split the data into chunks. If a chunk type is not detected, the data is split based on line breaks.\n\nThe function `chunk_text_by_tokens` is specifically used when the chunk type is 'TEXT'. It chunks the input data based on the specified maximum tokens, ensuring eachchunk does not exceed this limit.\n\nWith the `chunk_source_code` function, you can chunk source code based on individual functions and classes. This is crucial to maintainthe context and readability within a code snippet."}},

                         {'completion':
                          {'desired': 7372,
                           'available': 7172,
                           'used': 200},
                          'prompt':
                          {'desired': 819,
                           'available': 135,
                           'used': 684},
                          'chunk':
                          {'number': 1,
                           'total': 2,
                           'length': 64,
                           'data': '`extract_functions_and_classes` is a helper function used within `chunk_source_code`, it extracts all the functions andclasses from the given source code. The extracted functions and classes are then used to chunk source code accordingly.\n\nThese functions are called numerous times in the abstract_ai platform, emphasizing their key role in the system.'}}]

from abstract_ai import ResponseManager
#The `ResponseManager` class handles the communication process with AI models by managing the sending of queries and storage of responses. It ensures that responses are correctly interpreted, errors are managed, and that responses are saved in a structured way, facilitating easy retrieval and analysis.
#It leverages various utilities from the `abstract_utilities` module for processing and organizing the data and interacts closely with the `SaveManager` for persisting responses.
response_mgr = ResponseManager(prompt_mgr=prompt_mgr,
                api_mgr=api_mgr,
                title="Chunking Strategies in PromptBuilder.py",
                directory='response_data')

response_mgr.initial_query()
response_mgr.output = [{'prompt': {'model': 'gpt-4', 'messages': [{'role': 'assistant', 'content': "\n-----------------------------------------------------------------------------\n#instructions#\n\nyour response is expected to be in JSON format with the keys as follows:\n\n0) api_response - place response to prompt here\n1) notation - A useful parameter that allows a module to retain context and continuity of the prompts. These notations can be used to preserve relevant information or context that should be carried over to subsequent prompts.\n2) suggestions - ': A parameter that allows the module to provide suggestions for improving efficiency in future prompt sequences. These suggestions will be reviewed by the user after the entire prompt sequence is fulfilled.\n3) additional_responses - This parameter, usually set to True when the answer cannot be fully covered within the current token limit, initiates a loop that continues to send the current chunk's prompt until the module returns a False value. This option also enables a module to have access to previous notations\n4) abort - if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was\n5) generate_title - A parameter used for title generation of the chat. To maintain continuity, the generated title for a given sequence is shared with subsequent queries.\n6) request_chunks - you may request that the previous chunk data be prompted again, if selected, the query itterate once more with the previous chunk included in the prompt. return this value as True to impliment this option; leave sufficient notation as to why this was neccisary for the module recieving the next prompt\n7) additional_instruction - please place any iterable data inside of this key value unless otherwise specified\n\nbelow is an example of the expected json dictionary response format, with the default inputs:\n{'api_response': '', 'notation': '', 'suggestions': '', 'additional_responses': False, 'abort': False, 'generate_title': '', 'request_chunks': False, 'additional_instruction': '...'}\n-----------------------------------------------------------------------------\n#prompt#\n\nok now we chunk it up with abstract_ai the description youre looking for is still in the prompt_data\n-----------------------------------------------------------------------------\n\n-----------------------------------------------------------------------------\n#data chunk#\n\nthis is chunk 0 of 2\n\n\n\nThe code snippet is a part of `PromptBuilder.py` from the `abstract_ai` module. This specific part shows the crucial role of chunking strategies in the functioning of `abstract_ai`.\n\nThe `chunk_data_by_type` function takes in data, a maximum token limit, and a type of chunk (with possible values like 'URL', 'SOUP', 'DOCUMENT', 'CODE', 'TEXT').Depending on the specified type, it applies different strategies to split the data into chunks. If a chunk type is not detected, the data is split based on line breaks.\n\nThe function `chunk_text_by_tokens` is specifically used when the chunk type is 'TEXT'. It chunks the input data based on the specified maximum tokens, ensuring eachchunk does not exceed this limit.\n\nWith the `chunk_source_code` function, you can chunk source code based on individual functions and classes. This is crucial to maintainthe context and readability within a code snippet.\n-----------------------------------------------------------------------------\n"}], 'max_tokens': 7172},
                              'response': {'id': '**id**', 'object': 'chat.completion', 'created': 1699054738, 'model': 'gpt-4-0613', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': "{'api_response': 'This chunk describes a part of the `PromptBuilder.py` from the `abstract_ai` module. It underlines the significance of chunking methods in the `abstract_ai` operations. The mentioned `chunk_data_by_type` function accepts data, a maximum token limit, and a type of chunk to appropriately divide the data into chunks. The chunking process depends on the specified type, and in case the type is not identified, the data is divided based on line breaks. The `chunk_text_by_tokens` and `chunk_source_code` functions are used when the chunk type is 'TEXT' and 'CODE' respectively. The former chunks the data considering the max token limit, while the latter chunks source code as per individual classes and functions, maintaining the context and readability of a code snippet.', \n 'notation': 'The chunked data tells about the `abstract_ai` chunking mechanisms, which include `chunk_data_by_type`, `chunk_text_by_tokens` and `chunk_source_code` functions.', \n 'suggestions': 'It can be improved by providing specific examples of how each chunking function works.', \n 'additional_responses': True, \n 'abort': False, \n 'generate_title': 'Review of `abstract_ai` Chunking Mechanisms',\n 'request_chunks': False, \n 'additional_instruction': ''}"}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 621, 'completion_tokens': 271, 'total_tokens': 892}}, 'title': 'Chunking Strategies in PromptBuilder.py'},
                             {'prompt': {'model': 'gpt-4', 'messages': [{'role': 'assistant', 'content': "\n-----------------------------------------------------------------------------\n#instructions#\n\nyour response is expected to be in JSON format with the keys as follows:\n\n0) api_response - place response to prompt here\n1) notation - A useful parameter that allows a module to retain context and continuity of the prompts. These notations can be used to preserve relevant information or context that should be carried over to subsequent prompts.\n2) suggestions - ': A parameter that allows the module to provide suggestions for improving efficiency in future prompt sequences. These suggestions will be reviewed by the user after the entire prompt sequence is fulfilled.\n3) additional_responses - This parameter, usually set to True when the answer cannot be fully covered within the current token limit, initiates a loop that continues to send the current chunk's prompt until the module returns a False value. This option also enables a module to have access to previous notations\n4) abort - if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was\n5) generate_title - A parameter used for title generation of the chat. To maintain continuity, the generated title for a given sequence is shared with subsequent queries.\n6) request_chunks - you may request that the previous chunk data be prompted again, if selected, the query itterate once more with the previous chunk included in the prompt. return this value as True to impliment this option; leave sufficient notation as to why this was neccisary for the module recieving the next prompt\n7) additional_instruction - please place any iterable data inside of this key value unless otherwise specified\n\nbelow is an example of the expected json dictionary response format, with the default inputs:\n{'api_response': '', 'notation': '', 'suggestions': '', 'additional_responses': False, 'abort': False, 'generate_title': '', 'request_chunks': False, 'additional_instruction': '...'}\n-----------------------------------------------------------------------------\n#prompt#\n\nok now we chunk it up with abstract_ai the description youre looking for is still in the prompt_data\n-----------------------------------------------------------------------------\n\n-----------------------------------------------------------------------------\n#data chunk#\n\nthis is chunk 1 of 2\n\n`extract_functions_and_classes` is a helper function used within `chunk_source_code`, it extracts all the functions andclasses from the given source code. The extracted functions and classes are then used to chunk source code accordingly.\n\nThese functions are called numerous times in the abstract_ai platform, emphasizing their key role in the system.\n-----------------------------------------------------------------------------\n"}], 'max_tokens': 7172},
                              'response': {'id': '**id**', 'object': 'chat.completion', 'created': 1699054759, 'model': 'gpt-4-0613', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': "{'api_response': '`extract_functions_and_classes` is a helper function used within `chunk_source_code`. It extracts all the functions and classes from the given source code. These extracted elements are then used to chunk source code accordingly.', 'notation': 'Explanation about `extract_functions_and_classes` and `chunk_source_code` functions.', 'suggestions': '', 'additional_responses': True, 'abort': False, 'generate_title': '', 'request_chunks': False, 'additional_instruction': ''}"}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 494, 'completion_tokens': 99, 'total_tokens': 593}}, 'title': 'Chunking Strategies in PromptBuilder.py_0'
                              }]




#now lets give it the whole things!
current_file_full_data = read_from_file(os.path.abspath(__file__))
completion_percentage = 60 # completion percentage now set to 90% of the token allotment
request = "here is the entire example use case, please review the code and thank you for your time with abstract_ai"
prompt_data=current_file_full_data
title="Chunking Example Review.py"
response_mgr = ResponseManager(prompt_mgr=PromptManager(prompt_data=prompt_data,
                                                        request=request,
                                                        completion_percentage=completion_percentage,
                                                        model_mgr=model_mgr,
                                                        instruction_mgr=instruction_mgr),
                               api_mgr=api_mgr,
                               title=title,
                               directory='response_data')

response_mgr.initial_query()
output = response_mgr.initial_query()    
from abstract_ai import collate_response_que
colate_responses = collate_response_que(output)
#api_response:
"""The provided code is a walkthrough of how the `abstract_ai` module can be used for text processing tasks. It first demonstrates how to initialize the `ModelManager`, `ApiManager`, and `InstructionManager` classes. These classes are responsible for managing model-related configurations, API interactions, and instruction-related configurations, respectively.

The `PromptManager` class is initialized to manage prompt-related operations. This class handles the calculation of token distribution for various component parts of the prompt (i.e., the prompt itself, the completion, and the data chunk). In the example, the completion percentage is adjusted from 40% to 90%, demonstrating the flexibility of the `abstract_ai` module in shaping the AI's response. Additionally, the module supports different types of chunks, such as code, text, URL, etc., which adds further flexibility to the text processing.

The `ResponseManager` class interacts with AI models to handle the sending of queries and storing of responses. This class ensures responses are processed correctly and saved in a structured way for easy retrieval and analysis.

Overall, this use case provides a comprehensive view of how `abstract_ai` can be used for sophisticated and efficient management of AI-based text processing tasks."

All of those functions enable `abstract_ai` to manage large volumes of data effectively, ensuring legibility and context preservation in the chunks produced by recognizing their critical role within the platform.

Your request to review the provided example was processed successfully. The entire operation was completed in a single iteration, consuming about 60% of the allotted tokens."""

#suggestions:
"Please provide more context or specific requirements if necessary. Additional details about the specific use case or problem being solved could also be helpful for a more nuanced and tailored review."

#suggested_title:
"Review and Analysis of Chunking Strategies in the `abstract_ai` Framework"

#notation:
"The provided example included the usage of `PromptBuilder.py` from the `abstract_ai` module and the necessary chunking functions."

#abort
"false"

#additional_responses:
"false"
