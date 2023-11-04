# Abstract AI

## Table of Contents
- [Abstract AI](#abstract-ai)
  - [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Images](#images)
- [Installation](#installation)
- [Usage](#usage)
- [Abstract AI Module](#abstract-ai-module)
  - [GptManager Overview](#gptmanager-overview)
  - [Purpose](#purpose)
  - [Motivation](#motivation)
  - [Objective](#objective)
    - [Extended Overview](#extended-overview)
  - [Detailed Components Documentation](#main-Detailed-Components_Documentation)
    - [GptManager](#gptmanager)
    - [ModelManager](#modelmanager)
    - [PromptManager](#promptmanager)
    - [InstructionManager](#instructionmanager)
    - [ResponseManager](#responsemanager)
    - [ApiManager](#apimanager)
  - [Dependencies](#dependencies)
  - [Detailed Components Documentation](#detailed-components-documentation)
    - [ModelManager](#modelmanager-1)
    - [InstructionManager](#instructionmanager-1)
    - [PromptManager](#promptmanager-1)
  - [Additional Information](#additional-information)
- [Contact](#contact)
- [License](#license)

# `abstract_ai` Module

`abstract_ai` is a  feature-rich Python module for interacting with the OpenAI GPT-3 and 4 API. It provides an easy way to manage requests and responses with the AI and allows for detailed interaction with the API, giving developers control over the entire process. This module manages data chunking for large files, allowing the user to process large documents in a single query. It is highly customizable, with methods allowing modules to maintain context, repeat queries, adjust token sizes, and even terminate the query loop if necessary.

## Installation

To utilize the `api_calls.py` module, install the necessary dependencies and configure your OpenAI API key:

1. Install the required Python packages:

   ```bash
   pip install abstract_ai
   ```

2. Set your OpenAI API key as an environment variable. By default, the module searches for an environment variable named `OPENAI_API_KEY` for API call authentication. Ensure your `.env` is saved in `home/envy_all`, `documents/envy_all`, within the `source_folder`, or specify the `.env` path in the GUI settings tab.

## Abstract Ai Overciew

```markdown
# Dynamic Data Chunking & API Query Handler

## Overview

This repository presents a sophisticated code example engineered to efficiently process extensive datasets via an intelligent chunking algorithm, tailored for API interactions where data size and query constraints are predominant. It assures a smooth operation with minimal user input.

## Key Features

### Dual Input System
- `Request` and `Prompt Data` sections for straightforward data incorporation.
- Automatic division of prompt data into manageable chunks based on user-specified parameters.

### Intelligent Chunking
- Dynamically segments data considering the set percentage for expected completion per API query and the maximum token limit.
- Executes iterative queries through a response handler class until data processing completes.

### Iterative Query Execution
- Handles documents split into multiple chunks (e.g., 14 chunks result in at least 14 API queries), with real-time adaptive query decisions.

### Instruction Set
- `bot_notation`: allows the module to create notes about the current data chunk to be recieved upon the next query, this is such that they can keep context, and understand why the previous selections were made.
- `additional_response`: Allows repeated query execution until a specified condition is met, bypassing token limitations.
- `select_chunks`: allows the module to review either the previous or next chunk of data alongside the current or by itself, if needed, the loop will essentially impliment additional_response for this.
- `token_size_adjustment`: allows the module to adjust the size of the chunks being sent, this is a neat feature because they do get finicky about this and it can be used in combination with any of the above. 
- `abort`: Authorizes termination of the query loop to conserve resources.
- `suggestions`: Provides a system for leaving future improvement notes.

## Autonomy & Efficiency

Empowers modules with significant autonomy for managing large data volumes efficiently, ensuring the output is streamlined and user post-processing is minimal.

## User Convenience

Simplifies user involvement by automating data chunking and handling multiple prompts in a single operation. The modules are also equipped to independently address typical query-related issues.

## Conclusion

Developers seeking to automate and refine data handling for API-centric applications will find this repository a valuable asset. It's crafted to mitigate common data processing challenges and implement proactive solutions for enhanced user and module performance.

---

Your journey towards seamless data handling starts here! Dive into the code, and feel free to contribute or suggest improvements.

```
## Usage

```python
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
                                     additional_instruction=additional_instruction,
                                     request_chunks=self.request_chunks
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
```

## Images

![URL Grabber Component](https://raw.githubusercontent.com/AbstractEndeavors/abstract-ai/main/src/abstract_ai/documentation/images/url_grabber_bs4_component.png)

*URL grabber component: Allows users to add URL source code or specific portions of the URL source code to the prompt data.*

![Settings Tab](https://raw.githubusercontent.com/AbstractEndeavors/abstract-ai/main/src/abstract_ai/documentation/images/settings_tab.png)

*Settings Tab: Contains all selectable settings, including available, desired, and used prompt and completion tokens.*

![Instructions Display](https://raw.githubusercontent.com/AbstractEndeavors/abstract-ai/main/src/abstract_ai/documentation/images/instructions_display.png)

*Instructions Display: Showcases all default instructions, which are customizable in the same pane. All instructions are derived from the `instruction_manager` class.*

![File Content Chunks](https://raw.githubusercontent.com/AbstractEndeavors/abstract-ai/main/src/abstract_ai/documentation/images/file_content_chunks.png)

*File Browser Component: Enables users to add the contents of files or specific portions of file content to the prompt data.*

### Detailed Components Documentation
The `GptManager.py` module provides an extensive class management to interact with the GPT-3 model conveniently. This module combines various functionalities into a unified and structured framework. Some of the significant classes it encapsulates are as follows:

- GptManager: This is the central class that administers the interactions and data flow amongst distinct components.
- ApiManager: This manages the OpenAI API keys and headers.
- ModelManager: This takes care of model selection and querying.
- PromptManager: This takes care of the generation and management of prompts. 
- InstructionManager: This encapsulates the instructions for the GPT model.
- ResponseManager: This administers the responses received from the model.

These classes work collectively to simplify the task of sending queries, interpreting responses, and managing the interactions with the GPT-3 model. The module heavily depends on packages like `abstract_webtools`, `abstract_gui`, `abstract_utilities`, and `abstract_ai_gui_layout`.

### Dependencies

- **abstract_webtools**: Provides web-centric tools.
- **abstract_gui**: Houses GUI-related tools and components.
- **abstract_utilities**: Contains general-purpose utility functions and classes.
- **abstract_ai_gui_layout**: Lays out the AI GUI.

#abstract_ai_gui_backend.py

## Overview
To use the `abstract_ai_gui_backend.py`, first, initialize the GptManager class. Following this step, use the update methods to set or change configurations. Finally, use the `get_query()` method to query the GPT model and retrieve a response.
This chunk of code contains several methods for the abstract_ai_gui_backend module of the Abstract AI system:

### Class: GptManager

1. `update_response_mgr`: This method updates the ResponseManager instance used by the module, linking it with the existing instances of PromptManager and ApiManager. The ResponseManager generates AI response to prompts that are sent.

2. `get_query`: The method is used for making respective calls to get responses. If a response is already computed, it stops the existing request (using `ThreadManager`) and starts a new thread for response retrieval.

3. `update_all`: This method is used to update all the managers used by the module, to keep their data in sync.

4. `get_new_api_call_name`: This method generates a new unique name for API call and appends it in the API call list.

5. `get_remainder`: It returns what's left when 100 is subtracted from the value from a specific key.

6. `check_test_bool`: This method checks if a test run is initiated. According to the result, it sets different statuses and updates the GUI accordingly.

7. `get_new_line`: The method simply returns a newline character(s).

8. `update_feedback`: This method fetches a value from the last response, based on the given key, and updates the GUI accordingly.

9. `update_text_with_responses`: This method loads the last response and if it contains API response, it updates the GUI with the Title, Request text, and Response. For other feedback, it appends the information to the output.

10. `get_bool_and_text_keys`: This method simply returns a list of keys formed by the given key_list and sections_list.

11. `text_to_key`: The static method uses the function from utilities to generate a key name from text.

12. `get_dots`: This method is used for decorating progress status.

13. `update_progress_chunks`: This method provides a visual representation of the overall progress with respect to total chunks.

14. `check_response_mgr_status`: This method checks whether the response manager's query process is finished by checking the `query_done` attribute.

15. `submit_query`: This method controls the sending and receiving of queries and updating the GUI with the AI response.

16. `update_chunk_info`: This method updates information related to the chunk based on the progress.

17. `adjust_chunk_display`: This method modifies the GUI value responsible for displaying the chunk number in GUI based on the navigation number provided.

The above chunk contains a sequence of function definitions that manage different parts of the AI interaction process within the abstract_ai module. Here's a concise guide about each method:

- `get_chunk_display_numbers`: Retrieves the display number for the current data chunk.

- `determine_chunk_display`: Determines if a data chunk should be displayed based on the input event.

- `append_output`: Appends new content to a particular key in the output.

- `add_to_chunk`: Appends new content to the current data chunk.

- `clear_chunks`: Resets the current chunk data.

- `get_url`: Retrieves the URL for a script.

- `get_url_manager`: Checks if a URL manager exists for a particular URL.

- `test_files`: Performs tests on the AI model with a hard-coded query.

- `update_last_response_file`: Stores the path of the most recent response file, and updates the related GUI elements.

- `update_response_list_box`: Updates the list box displaying response files.

- `aggregate_conversations`: Aggregates all conversations from JSON files in a specified directory.

- `initialize_output_display`: Initializes the display for the output and sets the data to the first item of the latest output.
This code chunk contains four methods for managing output display in the application.

1) `get_output_display_numbers`: This functions fetches from `window_mgr` the value associated with the `-RESPONSE_TEXT_NUMBER-` key and stores it in `response_text_number_display`. Additionally, it calculates `response_text_number_actual` by subtracting 1 from `response_text_number_display`.

2) `determine_output_display`: This function checks the current `event` and decides whether the output display needs to be adjusted and in which direction (back or forward). It checks the conditions and, if valid, calls the `adjust_output_display` method.

3) `adjust_output_display`: This function accepts one argument `num` which is used to adjust `response_text_number_actual` and `response_text_number_display`. It updates the output display and updates the `-RESPONSE_TEXT_NUMBER-` key in the `window_mgr` with the new value of `response_text_number_display`.

4) `update_output`: This function accepts `output_iteration` as an argument and checks if it lies within the valid range. If valid, it assigns the designated output to `self.latest_output[output_iteration]` and then calls `update_text_with_responses`.

This code manages the logic for traversing through the returned responses. It correctly fetches the number of responses, decides whether to go back or forward based on the event, adjusts the display accordingly and updates it. It is important to update the documentation with these details to allow the users to understand the flow of control in the script.

# ModelManager

The ModelManager class, as part of the `abstract_ai` module, provides functionalities for selecting, querying, and managing information about the available GPT models. The class initializes a list of models and their related information like endpoint and token limits. It also has methods to get model-specific details like endpoints, names, and token limits.

Below are the method descriptions:

- `__init__`: Initialises the ModelManager instance with information about all available models. It also sets up the default model, endpoints, and maximum tokens.

- `get_all_values`: Takes a key as an input parameter and returns all unique values associated with this key in the `all_models` list.

- `_get_all_values`: An alternate private method to `get_all_values` that performs the same functionality with a reduced number of lines by using a list comprehension.

- `_get_endpoint_by_model`: Returns the endpoint associated with the input model name.

- `_get_models_by_endpoint`: Returns a list of models associated with a given endpoint.

- `_get_max_tokens_by_model`: Returns the maximum tokens that can be processed by a given model.

Note: In the `__init__` function, depending on the given inputs, the function prioritizes model_name over endpoint in setting the selected model, endpoint, and maximum tokens.

# PromptBuilder.py

PromptBuilder is a sophisticated module within the Abstract AI's ApiConsole, designed to handle the intricacies of token distribution, chunking of data, and prompt construction necessary for interfacing with language model APIs.

## Overview

PromptBuilder.py specializes in calculating and managing token allocations for prompt and completion outputs, considering the user's specifications and the constraints of the API's token limits. It ensures that queries are not only well-formed but also optimally structured for the language model to understand and respond effectively. The module's responsibilities extend to sizing the current query, evaluating the total prompt data, and segmenting it into processable chunks before final prompt assembly.

### PromptManager

## Key Features

- **Token Distribution:** Allocates tokens between prompts and completions based on instruction weight, verbosity, and available token quota.
- **Data Chunking:** Separates prompt data into manageable chunks, conforming to the calculated token budget.
- **Prompt Construction:** Assembles the full prompt incorporating user instructions, chunk data, and module notation, ready for API interaction.
- **Integration:** Serves as a foundational tool for the system, called upon in nearly every significant interaction with Abstract AI.

## Dependencies

PromptBuilder.py relies on the `nltk` and `tiktoken` libraries for accurate tokenization and text encoding, ensuring precise calculations and data handling.

## Usage

To utilize the PromptBuilder.py, import the module and instantiate the required class. Utilize its methods by adjusting parameters to fit the needs of your query. Here's an example using `calculate_token_distribution`:

```python
from PromptBuilder import PromptBuilder

# Create an instance of the PromptBuilder class
prompt_builder = PromptBuilder()

# Example usage of calculate_token_distribution
token_distribution = prompt_builder.calculate_token_distribution(user_query)
```

## Integration with Abstract AI

PromptBuilder.py is deeply integrated with the Abstract AI suite, often collaborating with `ApiBuilder.py`, `ModelBuilder.py`, and `abstract_ai_gui_backend.py` for a cohesive and efficient API interaction experience.

## Methods Overview

- `get_token_calcs`: Evaluates token distribution for each chunk, ensuring balance between prompts and completions.
- `get_token_distributions`: Distributes tokens optimally across chunks based on the prompt and completion needs.


### Helpful Methods in PromptBuilder.py

Among the functions in this module, the token calculation functions `get_token_calcs` and `get_token_distributions` are quite crucial. They carefully calculate the tokens used and available for prompts and completion. If, at any point, available prompt tokens fall below zero, they get added to the available completion tokens leading to a balance distribution.

Here's an overview of two prominent methods:

- `get_token_calcs`: Evaluates individual token calculations for prompt and completion data. On detecting a shortage in available tokens, it redistributes tokens from the completion pool.

- `get_token_distributions`: It distributes tokens between the prompt and completion parts of the GPT-3 model query, ensuring a smooth and balanced query and keeping within the maximum token limit for the task.

#api_response#

```json
{
  "title": "Chunking Strategies in PromptBuilder.py",
  "prompt_type": "Python Code",
  "prompt": "The code snippet is a part of `PromptBuilder.py` from the `abstract_ai` module. This specific part shows the crucial role of chunking strategies in the functioning of `abstract_ai`.\n\nThe `chunk_data_by_type` function takes in data, a maximum token limit, and a type of chunk (with possible values like 'URL', 'SOUP', 'DOCUMENT', 'CODE', 'TEXT'). Depending on the specified type, it applies different strategies to split the data into chunks. If a chunk type is not detected, the data is split based on line breaks.\n\nThe function `chunk_text_by_tokens` is specifically used when the chunk type is 'TEXT'. It chunks the input data based on the specified maximum tokens, ensuring each chunk does not exceed this limit.\n\nWith the `chunk_source_code` function, you can chunk source code based on individual functions and classes. This is crucial to maintain the context and readability within a code snippet.\n\n`extract_functions_and_classes` is a helper function used within `chunk_source_code`, it extracts all the functions and classes from the given source code. The extracted functions and classes are then used to chunk source code accordingly.\n\nThese functions are called numerous times in the abstract_ai platform, emphasizing their key role in the system.",
  "suggested_formatting": [
    {
      "code": {
        "language": "python",
        "content": [
          "def chunk_data_by_type(data, max_tokens, chunk_type=None):",
          "...",
          "def chunk_text_by_tokens(prompt_data, max_tokens):",
          "...",
          "def extract_functions_and_classes(source_code):",
          "...",
          "def chunk_source_code(source_code, max_tokens):"
        ]
      }
    }
  ]
}
```
#InstructonBuilder.py

##OverView

This module is a segment of the Abstract AI system that manages the creation and modifications of instructions used by the GPT-3 model. It composes a significant component of `abstract_ai_gui_backend.py`, working closely with classes like GptManager, ApiManager, ModelManager, PromptManager, and ResponseManager to ensure efficient and structured interactions with the model.

### Class: InstructionManager
- Main Methods:

1. `update_response_mgr`: Links the existing instances of PromptManager and ApiManager, updating the ResponseManager used by the module.
2. `get_query`: Controls interrupting ongoing requests and starting a new thread for response retrieval through the `ThreadManager`.
3. `update_all`: Keeps the model, API, and other managers up to date and synchronized.
4. `get_new_api_call_name`: Generates unique ID for each API call and maintains them in a list.
5. `get_remainder`: Works on value subtraction for a particular key.
6. `get_new_line`: A simple method for returning newline characters.
7. `update_feedback`: Fetches a key-value pair from the prior response and updates the GUI.
8. `update_text_with_responses`: Loads the latest response, extracts necessary information, and updates the GUI accordingly.
9. `update_chunk_info`: Manages updates relating to the chunk based on the progression of the query.
10. `adjust_chunk_display`: Alters the GUI value responsible for showing the chunk number based on the provided navigation number.

Each of these methods, with their signature features, enhances the usability and functionality of the Abstract_AI system, ensuring optimized interactions, easy navigation through data chunks, and adept handling of responses.

# ApiManager
Overview
The ApiBuilder.py is a component of the abstract_ai GPT API console that streamlines the usage of the OpenAI API. It serves as a utility module for managing API keys and constructing request headers required for API interactions.

Features
API Key Retrieval: Securely fetches the OpenAI API key from environmental storage, ensuring that sensitive data is not hardcoded into the application.
Header Construction: Automates the creation of the necessary authorization headers for making requests to the OpenAI API.
Prerequisites
To use ApiBuilder.py, ensure that you have an OpenAI API key stored in your environment variables under the name OPENAI_API_KEY.

Getting Started
To begin with ApiBuilder.py, you can create an instance of ApiManager and then use it to perform operations requiring API access. The ApiManager class encapsulates all you need to manage API keys and headers for the OpenAI GPT API requests.

Usage
python
Copy code
from ApiBuilder import ApiManager

# ResponseBuilder.py

## Overview

The Purpose of the `ResponseBuilder.py` is to handle interactions and communications with AI models primarily through API endpoints. It ensures that responses are correctly interpreted, any errors are handled gracefully, and the responses are saved in a structured manner to facilitate easy retrieval and analysis at a later stage. It’s a core part of the `abstract_ai`, module we are currently communicating through.

### Class: ResponseManager

The `ResponseManager` class is a single handler of all in-query events and module interactions. It leverages various utilities from the `abstract_utilities` module to process and organise the data, interacting closely with the `SaveManager` to persist responses.

This class can be initialised with an instance of `prompt manager`' and `API manager`, optional `title` for the session or the file saved, and `directory` path where responses are to be saved.

Below is a brief description of the methods of this class:

- `re_initialize_query`: Resets query-related attributes to their default state for a new query cycle.
- `post_request`: Sends a POST request with the current prompt and headers to the AI model and handles the response.
- `get_response`: Extracts and formats the response from the API call.
- `try_load_response`: Attempts to load the response content into a structured format.
- `extract_response`: Processes the response and manages the creation of a save point through `SaveManager`.
- `get_last_response`: Retrieves the last response from the save location.
- `get_response_bools`: Checks and sets boolean flags based on the content of the latest response.
- `send_query`: Prepares and sends a new query to the AI model, then processes the response.
- `test_query`: Simulates sending a query for testing purposes.
- `prepare_response`: Handles the response after a query has been sent.
- `initial_query`: Manages the initial sequence of sending queries and processing responses.

## Benefits and Features

- The `ResponseBuilder` automatically chunks large data sets into manageable segments based on the percentage delegated for expected completion per query relative to the max tokens limit. This prevents wasting compute cycles on unnecessarily large queries and helps ensure more efficient responses. 
- It handles the communication with the AI model, sending queries and storing/interpreting responses, significantly simplifying the interaction process for the end-users.
- It also gives the chat modules sufficient autonomy to efficiently handle the requests, preserving context and continuity in the responses. This helps avoid the need for users to stitch together the responses manually, leading to a more seamless interaction experience.

# ApiManager
api_manager = ApiManager()

# API key and headers are set up and ready to be used for requests
print(api_manager.api_key)          # Displays the loaded API key
print(api_manager.header)           # Displays the generated headers
Class ApiManager
ApiManager is responsible for handling API keys and headers. It comes with a default configuration but can be customized during instantiation.

Attributes:
content_type (str): The MIME type of the request content. Defaults to 'application/json'.
api_env (str): The environment variable name where the API key is stored. Defaults to 'OPENAI_API_KEY'.
api_key (str): The actual API key used for authentication with the OpenAI API.
header (dict): The authorization headers used in API requests.
Methods:
get_openai_key(): Retrieves the API key from the environment variable.
load_openai_key(): Loads the API key into the OpenAI library for authenticating requests.
get_header(): Constructs the headers required for making API requests.
Security
The ApiManager leverages environment variables to manage the API key, which is a secure practice. Ensure not to expose your API key in the codebase or any version control systems.


### Additional Information

- **Author**: putkoff
- **Date**: 10/29/2023
- **Version**: 1.0.0

## Contact

For issues, suggestions, or contributions, open a new issue on our [Github repository](https://github.com/AbstractEndeavors/abstract-ai/).

## License

`abstract_ai` is distributed under the [MIT License](https://opensource.org/licenses/MIT).

