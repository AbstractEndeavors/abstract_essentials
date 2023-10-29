import nltk
# Ensure you have OpenAI API credentials set up
import re

def count_openai_tokens(text):
    return len(list(tokenizer.tokenize(text)))
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from nltk.tokenize import word_tokenize
from abstract_utilities import convert_to_percentage
from abstract_utilities.type_utils import is_number
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-4")
encoding.encode("tiktoken is great!")
# Ensure you have OpenAI API credentials set up


def num_tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens
def tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)

    return encoding.encode(str(string))
class PromptManager:
    """
    Manages the generation and management of prompts. This might include creating prompts based on user input or predefined conditions, formatting prompts, and handling errors or special cases.
    """
    def __init__(self,instruction_mgr,model_mgr,role='assistant',completion_percentage=40,prompt_data=None,request=None,token_dist=None,bot_notation=None,chunk=None,chunk_type=None):
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
            max_tokens (int, optional): The maximum number of tokens allowed. Defaults to `default_tokens()`.
            prompt (str, optional): The prompt to be used. Defaults to "null".
            completion_percentage (float, optional): The completion percentage. Defaults to 40.
            size_per_chunk (int, optional): The size per chunk. Defaults to None.
            chunk_prompt (str, optional): The chunk prompt. Defaults to an empty string.
            tokenize_js (dict, optional): Tokenization data. Defaults to an empty dictionary.
            
        Returns:
            dict: A dictionary containing token distribution information.
        """
        def count_tokens(text):
            """
            Counts the number of tokens in the given text.

            Args:
                text (str): The input text.

            Returns:
                int: The number of tokens.
            """
            return len(word_tokenize(text))

        def chunk_text_by_tokens(prompt_data, max_tokens):
            # Split prompt_data into chunks based on max_tokens
            chunks = []
            current_chunk = ""
            current_chunk_tokens = 0

            for sentence in prompt_data.split("."):  # Split by sentences for example
                sentence_tokens = num_tokens_from_string(sentence)

                if current_chunk_tokens + sentence_tokens <= max_tokens:
                    current_chunk += sentence
                    current_chunk_tokens += sentence_tokens
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence
                    current_chunk_tokens = sentence_tokens

            if current_chunk:
                chunks.append(current_chunk)

            return chunks
        def chunk_data_by_type(data, max_tokens, data_type=None):
            chunks = []
            current_chunk = ""
            current_chunk_tokens = 0
            # Define chunking rules based on data type
            if data_type == "TEXT":
                paragraphs = data.split("\n\n")
                for paragraph in paragraphs:
                    paragraph_tokens = num_tokens_from_string(paragraph)
                    if current_chunk_tokens + paragraph_tokens <= max_tokens:
                        current_chunk += paragraph
                        current_chunk_tokens += paragraph_tokens
                    else:
                        chunks.append(current_chunk)
                        current_chunk = paragraph
                        current_chunk_tokens = paragraph_tokens
            elif data_type == "SCRIPT":
                blocks = re.split(r'\n\s*}\s*\n', data)
                for block in blocks:
                    block_tokens = num_tokens_from_string(block)
                    if current_chunk_tokens + block_tokens <= max_tokens:
                        current_chunk += block
                        current_chunk_tokens += block_tokens
                    else:
                        chunks.append(current_chunk)
                        current_chunk = block
                        current_chunk_tokens = block_tokens
            elif data_type == "URL":
                sections = re.split(r'<h[1-6].*?>.*?</h[1-6]>', data)
                for section in sections:
                    section_tokens = num_tokens_from_string(section)
                    if current_chunk_tokens + section_tokens <= max_tokens:
                        current_chunk += section
                        current_chunk_tokens += section_tokens
                    else:
                        chunks.append(current_chunk)
                        current_chunk = section
                        current_chunk_tokens = section_tokens
            elif data_type == "SOUP":
                for tag in tags:
                    tag_content = str(tag)
                    tag_tokens = num_tokens_from_string(tag_content)
                    if current_chunk_tokens + tag_tokens <= max_tokens:
                        current_chunk += tag_content
                        current_chunk_tokens += tag_tokens
                    else:
                        chunks.append(current_chunk)
                        current_chunk = tag_content
                        current_chunk_tokens = tag_tokens
            else:
               return chunk_text_by_tokens(data, max_tokens)

            if current_chunk:
                chunks.append(current_chunk)

            return chunks
        def get_token_calcs(i,chunk_data,total_chunks,initial_prompt_token_length,prompt_token_desired,initial_completion_token_length,completion_token_desired):
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
        def create_chunks(content, chunk_size):
            """
            This method is responsible for dividing large chunks of content into smaller, more manageable pieces, each of a specified size.
            This is done by tokenizing the content, and then appending each token to the current chunk until the chunk reaches the specified size.
            The list of all chunks is then returned to the caller.

            Parameters:
            - content (str): The large content that needs to be divided into chunks.
            - chunk_size (int): The size of each chunk in tokens.

            Returns:
            - list of str: A list of smaller content chunks.
            """
         
            tokens =  word_tokenize(content)
            chunks = []
            current_chunk = []
            current_size = 0
            for token in tokens:
                current_size += 1
                if current_size > size_per_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_size = 1
                current_chunk.append(token)
            chunks.append(' '.join(current_chunk))
            return chunks
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
            
    def create_prompt_guide(self,token_dist_prompt=None,bot_notation=None,data_chunk=None):
        """
        This method encapsulates the process of creating formatted communication for the current data chunk,
        which includes forming the prompt, bot_notation, and other required fields for personalized bot communication.
        This is returned as a formatted string.

        Parameters:
        - data_chunk (str): The data chunk for which to create the communication guide.

        Returns:
        - str: A formatted communication guide.
        """
        def get_for_prompt(title,data):
            if data:
                return f'#{title}#'+'\n\n'+f'{data}'
            return ''
        def get_chunk_header(chunk,total_chunks,data_chunk):
            return f'this is chunk {chunk} of {total_chunks}'+'\n\n'+f'{data_chunk}'
        chunk=self.chunk
        total_chunks=self.total_chunks
        data_chunk= data_chunk or ''
        if token_dist_prompt != None:
            chunk=token_dist_prompt["chunk"]["number"]
            total_chunks=token_dist_prompt["chunk"]["total"]
            data_chunk=token_dist_prompt["chunk"]["data"]
        instructions = get_for_prompt('instructions',self.instructions)
        request=get_for_prompt('prompt',self.request)
        bot_notation=get_for_prompt('notation from the previous response',bot_notation)
        chunks_prompt=get_for_prompt('data chunk',get_chunk_header(chunk,total_chunks,data_chunk))
        return f'''{instructions}{request}{bot_notation}{chunks_prompt}'''
    def create_prompt(self,dist_number=None,bot_notation=None):
        """
        This method forms a dictionary embodying the prompt for the chatbot. This includes the model name,
        the role of the issuer, the content, and other variables. The method also takes an optional distribution number
        and bot notation for more personalized prompts.

        Parameters:
        - model_name (str): The name of the chatbot model.
        - issuer_role (str): The role of the issuer (e.g., user, assistant).
        - content (str): The content or query for the chatbot.
        - distribution_number (int, optional): The distribution number for the prompt.
        - bot_notation (str, optional): Additional notation for the bot.

        Returns:
        - dict: A dictionary representing the prompt for the chatbot.
        """
        self.prompt =""
        token_dist_prompt=self.token_dist[dist_number]
        self.prompt =self.create_prompt_guide(token_dist_prompt=token_dist_prompt,bot_notation=bot_notation)
        max_tokens = token_dist_prompt['completion']['available']
        self.prompt ={"model": self.model_mgr.selected_model_name, "messages": [{"role": self.role or "user", "content":self.prompt }],"max_tokens": max_tokens}
        return self.prompt
