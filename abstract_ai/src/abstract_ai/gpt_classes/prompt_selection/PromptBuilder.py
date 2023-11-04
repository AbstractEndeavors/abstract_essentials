from abstract_utilities import convert_to_percentage
from abstract_utilities.type_utils import is_number
import tiktoken
import re
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-4")
encoding.encode("tiktoken is great!")
# Ensure you have OpenAI API credentials set up
def num_tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The input text.
        encoding_name (str, optional): The encoding name to use. Defaults to "cl100k_base".

    Returns:
        int: The count of tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens
def tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """
    Tokenize a text string using a specified encoding.

    Args:
        string (str): The input text.
        encoding_name (str, optional): The encoding name to use. Defaults to "cl100k_base".

    Returns:
        List[str]: A list of tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name)

    return encoding.encode(str(string))
class PromptManager:
    """
    Manages the generation and management of prompts. This includes creating prompts based on user input or predefined conditions, formatting prompts, and handling errors or special cases.
    """
    def __init__(self,instruction_mgr,model_mgr,role='assistant',completion_percentage=40,prompt_data=None,request=None,token_dist=None,bot_notation=None,chunk=None,chunk_type=None):
        """
        Initialize the PromptManager.

        Args:
            instruction_mgr: The instruction manager.
            model_mgr: The model manager.
            role (str, optional): The role of the issuer (e.g., user, assistant). Defaults to 'assistant'.
            completion_percentage (int, optional): The completion percentage. Defaults to 40.
            prompt_data: The preliminary data variable that gets converted to chunks.
            request: The prompt request.
            token_dist: Token distribution information.
            bot_notation: Additional notation for the bot.
            chunk: The current chunk.
            chunk_type: The type of chunk (e.g., URL, SOUP, DOCUMENT, CODE, TEXT).
        """
        self.chunk_type = chunk_type
        self.instruction_mgr = instruction_mgr
        self.model_mgr=model_mgr
        self.role=role
        self.completion_percentage=completion_percentage
        self.instructions=self.instruction_mgr.instructions
        self.request=request
        #this data is what the prompt request will be reffering to, it is also the preliminary data variable that gets converted to chunks
        self.prompt_data=prompt_data
        #will initialize as '', this 
        self.bot_notation=bot_notation or ''
        #if None it will initialize such that the prompt creation will initially intake the entirety of the prompt_data, otherwise it will utilize its cunk info
        self.token_dist=token_dist
        self.chunk=chunk or '00'
        self.total_chunks ='10'
        self.token_dist = self.calculate_token_distribution(bot_notation=self.bot_notation,
                                                     max_tokens=self.model_mgr.selected_max_tokens,
                                                     completion_percentage=self.completion_percentage,
                                                     prompt_guide=self.create_prompt_guide(),
                                                     chunk_prompt=self.prompt_data)
    def calculate_token_distribution(self,bot_notation=None,max_tokens=None,completion_percentage=None,prompt_guide=None,chunk_prompt=None,assume_bot_notation=True):
        """
        Calculates the token distribution between prompts, completions, and chunks to ensure effective token utilization.

        Args:
            bot_notation (str, optional): Additional notation for the bot.
            max_tokens (int, optional): The maximum number of tokens allowed.
            completion_percentage (float, optional): The completion percentage.
            prompt_guide: The prompt guide.
            chunk_prompt: The chunk prompt.

        Returns:
            dict: A dictionary containing token distribution information.
        """
        
        def chunk_any_to_tokens(blocks, max_tokens,delimeter='',reverse=False):
            """
            Splits the given data into chunks based on the provided chunking strategy determined by chunk_type.

            Args:
                data (str): The data to be chunked.
                max_tokens (int): The maximum number of tokens each chunk can have.
                chunk_type (str, optional): The strategy to be used for chunking. This can be 'URL', 'SOUP', 'DOCUMENT', 'CODE', or 'TEXT'. Defaults to None.

            Returns:
                list of str: A list of data chunks based on the specified chunking strategy.
            """
            if reverse:
                blocks = reversed(blocks)
            # Initialize the function analyzer.
            chunks=['']
            for block in blocks:
                if num_tokens_from_string(block) > max_tokens:
                    chunks=chunks+chunk_any_to_tokens(block.split("."),max_tokens,delimeter=".")
                elif num_tokens_from_string(chunks[-1] + block) > max_tokens:
                    chunks.append(block)
                else:
                    chunks[-1]+= delimeter+block
            return chunks
        def chunk_data_by_type(data, max_tokens,chunk_type=None,reverse=False):
            delimeter=None
            if chunk_type == "URL":
                delimeter=None
                blocks = re.split(r'<h[1-6].*?>.*?</h[1-6]>', data)
            if chunk_type == "SOUP":
                delimeter=None
                blocks = data
            elif chunk_type == "DOCUMENT":
                delimeter = "."
                blocks = data.split(delimeter)
            elif chunk_type == "CODE":
                chunks = chunk_source_code(data,max_tokens,reverse=reverse)
                for each in ['',' ','\n','\t']:
                    while each in chunks:
                        chunks.remove(each)
                return chunks
            elif chunk_type=="TEXT":
                chunks = chunk_text_by_tokens(data, max_tokens,reverse=reverse)
                for each in ['',' ','\n','\t']:
                    while each in chunks:
                        chunks.remove(each)
                return chunks
            else:
                delimeter="\n\n"
                blocks = data.split(delimeter)
            return chunk_any_to_tokens(blocks,max_tokens,delimeter,reverse=reverse)
        def chunk_text_by_tokens(prompt_data, max_tokens, reverse=False):
            """
            Chunks text data by tokens, ensuring that no chunk exceeds the maximum token limit.
            If reverse is True, chunks from the end of the text instead of the beginning.

            Args:
                prompt_data (str): The text data to be chunked.
                max_tokens (int): The maximum number of tokens per chunk.
                reverse (bool): If True, chunking starts from the end of the text.

            Returns:
                list of str: A list of strings where each string represents a chunk of the original text.
            """
            # Function to determine the number of tokens
            def num_tokens_from_string(string):
                # You'll need to define this function based on your specific tokenization logic
                pass
            
            # Reverse the sentences if chunking from the end
            sentences = prompt_data.split("\n")
            if reverse:
                sentences = reversed(sentences)

            chunks = []
            current_chunk = ""
            current_chunk_tokens = 0

            for sentence in sentences:
                sentence_tokens = num_tokens_from_string(sentence)

                # Check if adding the next sentence exceeds the max token count
                if current_chunk_tokens + sentence_tokens <= max_tokens:
                    if reverse:
                        current_chunk = sentence + "\n" + current_chunk
                    else:
                        current_chunk += "\n" + sentence
                    current_chunk_tokens += sentence_tokens
                else:
                    # If chunking from the end, prepend new chunks
                    if reverse and current_chunk:
                        chunks.insert(0, current_chunk)
                    else:
                        chunks.append(current_chunk)
                    current_chunk = sentence
                    current_chunk_tokens = sentence_tokens

            # Don't forget the last chunk
            if current_chunk:
                if reverse:
                    chunks.insert(0, current_chunk)
                else:
                    chunks.append(current_chunk)

            return chunks
        def extract_functions_and_classes(source_code,reverse=False):
            """
            Extracts and separates all the functions and classes from the provided source code.

            Args:
                source_code (str): A string containing the source code from which functions and classes are to be extracted.

            Returns:
                list of str: A list where each element is a string containing a single function or class definition.
            """
            functions_and_classes = []
            # Regular expressions to match function and class definitions
            func_pattern = re.compile(r'^\s*def\s+\w+\s*\(.*\):')
            class_pattern = re.compile(r'^\s*class\s+\w+\s*\(.*\):')
            
            lines = source_code.splitlines()
            current_block = []
            if reverse:
                lines = reversed(lines)
            for line in lines:
                
                if func_pattern.match(line) or class_pattern.match(line):
                    functions_and_classes.append("\n".join(current_block))
                    current_block = []
                current_block.append(line)
            if current_block:
                functions_and_classes.append("\n".join(current_block))        
            return functions_and_classes
        def chunk_source_code(source_code, max_tokens,reverse=False):
            """
            Chunks source code into segments that do not exceed a specific token limit, focusing on keeping functions and classes intact.

            Args:
                source_code (str): The source code to be chunked.
                max_tokens (int): The maximum number of tokens allowed in each chunk.

            Returns:
                list of str: A list of source code chunks, each within the specified token limit.
            """
            if reverse:
                functions_and_classes = reversed(functions_and_classes)
            # Initialize the function analyzer.
            chunks=['']
            functions_and_classes=extract_functions_and_classes(source_code)
            for block in functions_and_classes:
                if num_tokens_from_string(block) > max_tokens:
                    chunks=chunks+chunk_data_by_type(block, max_tokens)
                elif num_tokens_from_string(chunks[-1] + block) > max_tokens:
                    chunks.append(block)
                else:
                    chunks[-1]+= '\n'+block
            return chunks
        def get_token_calcs(i,chunk_data,total_chunks,initial_prompt_token_length,prompt_token_desired,initial_completion_token_length,completion_token_desired):
            """
            Calculates token usage statistics for a given chunk of data.

            Args:
                i (int): The index of the current chunk.
                chunk_data (str): The data within the current chunk.
                total_chunks (int): The total number of chunks.
                initial_prompt_token_length (int): The initial token length of the prompt.
                prompt_token_desired (int): The desired token length for the prompt.
                initial_completion_token_length (int): The initial token length of the completion.
                completion_token_desired (int): The desired token length for the completion.

            Returns:
                dict: A dictionary containing calculated token statistics for prompt and completion, as well as chunk details.
            """
            current_chunk_token_length = num_tokens_from_string(str(chunk_data))

            prompt_token_used = initial_prompt_token_length + current_chunk_token_length
            prompt_token_available = prompt_token_desired - prompt_token_used

            completion_token_used = initial_completion_token_length
            completion_token_available = (completion_token_desired - completion_token_used)
            if prompt_token_available <0:
                completion_token_available+=prompt_token_available
            chunk_js = {
                    "completion": {
                        "desired": completion_token_desired,
                        "available": completion_token_available,
                        "used": completion_token_used
                    },
                    "prompt": {
                        "desired": prompt_token_desired,
                        "available": prompt_token_available,
                        "used": prompt_token_used
                    },
                    "chunk": {
                        "number": i,
                        "total": total_chunks,
                        "length": current_chunk_token_length,
                        "data": chunk_data
                    }
                }
            return chunk_js

        def get_token_distributions(prompt_token_desired,
                                    initial_prompt_token_length,
                                    total_chunk_data,
                                    fictitious_chunk_token_length,
                                    completion_token_desired,
                                    initial_completion_token_length,chunk_type):
            """
            Computes token distributions for all chunks of data given the desired token allocations for prompts and completions.

            Args:
                prompt_token_desired (int): The desired number of tokens for the prompt.
                initial_prompt_token_length (int): The initial number of tokens used in the prompt.
                total_chunk_data (str): All the chunk data combined.
                fictitious_chunk_token_length (int): A hypothetical chunk token length used for chunking data.
                completion_token_desired (int): The desired number of tokens for the completion.
                initial_completion_token_length (int): The initial number of tokens used in the completion.
                chunk_type (str): The type of chunking to apply to the data.

            Returns:
                list of dict: A list where each dictionary contains the token distribution for a chunk.
            """
            # Function implementation ...
            get_token_distributions = []
            data_chunks_list = chunk_data_by_type(total_chunk_data, fictitious_chunk_token_length,chunk_type)
            total_chunks = len(data_chunks_list)

            for i, chunk_data in enumerate(data_chunks_list):
                chunk_js = get_token_calcs(i=i,chunk_data=chunk_data,total_chunks=total_chunks,initial_prompt_token_length=initial_prompt_token_length,prompt_token_desired=prompt_token_desired,initial_completion_token_length=initial_completion_token_length,completion_token_desired=completion_token_desired)
                get_token_distributions.append(chunk_js)

            if total_chunks == 0:
                # Handle the case where there are no chunks
                chunk_js = get_token_calcs(i=0,chunk_data='',total_chunks=total_chunks,initial_prompt_token_length=initial_prompt_token_length,prompt_token_desired=prompt_token_desired,initial_completion_token_length=initial_completion_token_length,completion_token_desired=completion_token_desired)
                get_token_distributions.append(chunk_js)

            return get_token_distributions
        tokenize_js={"bot_notation":bot_notation,
            "max_tokens":max_tokens,
            "completion_percentage":completion_percentage,
            "prompt_guide":prompt_guide,
            "chunk_prompt":chunk_prompt}
        total_prompt = ''
        for each in tokenize_js.keys():
            if each != "chunk_prompt":
                total_prompt+=str(tokenize_js[each])
                
        max_tokens = int(tokenize_js["max_tokens"])
        
        completion_percent = convert_to_percentage(tokenize_js["completion_percentage"])
        completion_token_desired = int(max_tokens*completion_percent)
        
        
        prompt_percent = convert_to_percentage(100-tokenize_js["completion_percentage"])
        prompt_token_desired = int(max_tokens*prompt_percent)
        bot_notation_token_count=int(200)
        initial_prompt_token_length = num_tokens_from_string(str(total_prompt))+bot_notation_token_count

        initial_completion_token_length=bot_notation_token_count
        
        total_chunk_data = tokenize_js["chunk_prompt"] or ''
    
        total_chunk_token_length = num_tokens_from_string(str(total_chunk_data))
        ficticious_chunk_token_length = prompt_token_desired-initial_prompt_token_length
        num_chunks = total_chunk_token_length // ficticious_chunk_token_length      
        instruction_token_size = 0
        
        token_distribution = get_token_distributions(prompt_token_desired,
                                                     initial_prompt_token_length,
                                                     total_chunk_data,
                                                     ficticious_chunk_token_length,
                                                     completion_token_desired,
                                                     initial_completion_token_length,
                                                     self.chunk_type)
        return token_distribution
            
    def create_prompt_guide(self,token_dist_prompt=None,bot_notation=None,data_chunk=None,generate_title=None,chunk_descriptions=None,request_chunks=None,select_data=None):
        """
        This method encapsulates the process of creating formatted communication for the current data chunk,
        which includes forming the prompt, bot_notation, and other required fields for personalized bot communication.
        This is returned as a formatted string.

        Args:
            token_dist_prompt: Token distribution information for the prompt.
            bot_notation (str, optional): Additional notation for the bot.
            data_chunk (str, optional): The data chunk.
            generate_title: Previously generated title.
            chunk_descriptions: Descriptions of the chunks.
            request_chunks: Previous chunk data requested.
            select_data: Selected data.

        Returns:
            str: A formatted communication guide.
        """
        def get_delimeters():
            return '\n-----------------------------------------------------------------------------\n'
        def get_for_prompt(title,data):
            if data:
                return f'#{title}#'+'\n\n'+f'{data}'
            return ''
        def get_chunk_header(chunk,total_chunks,data_chunk):
            return f'this is chunk {int(chunk)+1} of {total_chunks}'+'\n\n'+f'{data_chunk}'
        chunk=self.chunk
        total_chunks=self.total_chunks
        data_chunk= data_chunk or ''
        if token_dist_prompt != None:
            chunk=token_dist_prompt["chunk"]["number"]
            total_chunks=token_dist_prompt["chunk"]["total"]
            data_chunk=token_dist_prompt["chunk"]["data"]
        instructions = get_for_prompt('instructions',self.instructions)
        request_chunks=get_for_prompt('previous chunk data requested',request_chunks)
        generated_title=get_for_prompt('previously generated_title',generate_title)
        request=get_for_prompt('prompt',self.request)
        bot_notation=get_for_prompt('notation from the previous response',bot_notation)
        chunks_prompt=get_for_prompt('data chunk',get_chunk_header(chunk,total_chunks,data_chunk))
        return f'''{get_delimeters()}{instructions}{get_delimeters()}{request}{get_delimeters()}{bot_notation}{get_delimeters()}{chunk_descriptions}{get_delimeters()}{generated_title}{get_delimeters()}{request_chunks}{get_delimeters()}{chunks_prompt}{get_delimeters()}'''
    def create_prompt(self,dist_number=None,bot_notation=None,generate_title=None,chunk_descriptions=None,request_chunks=None,prompt_as_previous=None,token_adjustment=None):
        """
        This method forms a dictionary embodying the prompt for the chatbot. This includes the model name,
        the role of the issuer, the content, and other variables. The method also takes an optional distribution number
        and bot notation for more personalized prompts.

        Args:
            dist_number (int, optional): The distribution number for the prompt.
            bot_notation (str, optional): Additional notation for the bot.
            generate_title: Previously generated title.
            chunk_descriptions: Descriptions of the chunks.
            request_chunks: Previous chunk data requested.

        Returns:
            dict: A dictionary representing the prompt for the chatbot.
        """
        self.token_adjustment = token_adjustment
        if self.token_adjustment not in ['0',0]:
            if is_number(self.token_adjustment):
                adjusted_int = int(self.token_adjustment)
                prev_dists=chunk_list[dist_number-1]
                if 0< adjusted_int:
                    available = prev_dists['chunk']['available']
                    difference = prev_dists['chunk']['length']*self.token_adjustment
                    current_dist = self.token_dist[dist_number:]
                    
                    completion_used = prev_dists['completion']['used']
                    if available<difference:
                        difference=0-difference
                    prompt_used = prev_dists['prompt']['used']+difference
                    completion_desired = prev_dists['completion']['desired']
                    prompt_desired = prev_dists['prompt']['desired']
                    new_prompt_desired = prompt_desired+difference
                    new_completion_desired = (prompt_desired+completion_desired)-new_prompt_desired
                    chunk_list = chunk_any_to_tokens(collate, new_prompt_desired,chunk_type=self.chunk_type)
                    total_chunk_num = dist_number+len(chunk_list)
                    self.token_dist=self.token_dist[:dist_number-1]
                    for i,data in enumerate(chunk_list):
                        self.token_dist.append(get_token_calcs(i+dist_number,dist_number,total_chunk_num,prompt_used,new_prompt_desired,completion_used,new_completion_desired))
        if prompt_as_previous:
            num_tokens = num_tokens_from_string(prompt_as_previous)
            self.token_dist
            available = self.token_dist[dist_number]['prompt']['available']
            reverse=False
            if num_tokens<available:
                reverse=True
            prompt_desired = prev_dists['prompt']['available'] - num_tokens
            self.token_dist[dist_number]['chunk']['length'] += num_tokens
            
            chunk_data_by_type(prompt_as_previous, available,chunk_type=None,reverse=reverse)
               
        self.prompt_as_previous=prompt_as_previous
        self.prompt =""
        token_dist_prompt=self.token_dist[dist_number]
        if request_chunks:
            if dist_number != 0:
                request_chunks = self.token_dist[dist_number-1]["chunk"]["data"]
        self.prompt =self.create_prompt_guide(token_dist_prompt=token_dist_prompt,bot_notation=bot_notation,generate_title=generate_title,request_chunks=request_chunks)
        max_tokens = token_dist_prompt['completion']['available']
        self.prompt ={"model": self.model_mgr.selected_model_name, "messages": [{"role": self.role or "user", "content":self.prompt }],"max_tokens": max_tokens}
        return self.prompt

