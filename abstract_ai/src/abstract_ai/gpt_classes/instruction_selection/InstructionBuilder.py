class InstructionManager:
    def __init__(self,notation=True,suggestions=True,abort=True,generate_title=True,additional_responses=True,additional_instruction=False,test_it=False):
        self.notation=notation
        self.suggestions=suggestions
        self.abort=abort
        self.generate_title=generate_title
        self.additional_instruction=additional_instruction
        self.additional_responses=additional_responses
        self.test_it=test_it
        self.instructions_js = {}
        self.initialize_instructions()
        self.instructions=self.get_instructions()
    def get_additional_responses(self):
        """
        Determines the additional response based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the response is determined.
            
        Returns:
            str: The determined response.
        """
        if isinstance(self.additional_responses,str):
            return self.additional_responses
        if self.additional_responses:
            return "this value is to be returned as a bool value,this option is only offered to the module if the user has allowed a non finite completion token requirement. if your response is constrained by token allowance, return this as True and the same prompt will be looped and the responses collated until this value is False at which point the loop will ceased and promptng will resume once again"
        return "return false"
    def get_generate_title(self):
        """
        Retrieves the notation based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the notation is determined.
            
        Returns:
            str: The determined notation.
        """
        if isinstance(self.generate_title,str):
            return self.generate_title
        if self.generate_title:
            return 'please generate a title for this chat based on the both the context of the query and the context of your response'
        return "return false"
    def get_notation(self):
        """
        Retrieves the notation based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the notation is determined.
            
        Returns:
            str: The determined notation.
        """
        if isinstance(self.notation,str):
            return self.notation
        if self.notation:
            return "insert any notes you would like to recieve upon the next chunk distribution in order to maintain context and proper continuity"
        return "return false"
    def get_suggestions(self):
        """
        Retrieves the suggestions based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the suggestion is determined.
            
        Returns:
            str: The determined suggestions.
        """
        if isinstance(self.suggestions,str):
            return self.suggestions
        if self.suggestions:
            return "insert any suggestions you find such as correcting ambiguity in the prompts entirety such as context, clear direction, anything that will benefit your ability to perform the task"
        return "return false"
    def get_abort(self):
        """
        Retrieves the abort based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the abort is determined.
            
        Returns:
            str: The determined abort.
        """
        if isinstance(self.abort,str):
            return self.abort
        if self.abort:
            return "if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was"
        return "return false"
    def initialize_instructions(self):
        if self.additional_instruction:
            if isinstance(self.additional_instruction,dict):
                self.instruction_js=self.additional_instruction
            elif isinstance(self.additional_instruction,str):
                self.instruction_js={"additional_instruction":self.additional_instruction}
        else:
            self.instructions_js = {}
        if 'response' not in self.instructions_js and "api_response" not in self.instructions_js:
            self.instructions_js["api_response"]="place response to prompt here"
        if self.notation or self.test_it:
           self.instructions_js["notation"]=self.get_notation()
        if self.instructions_js or self.test_it:
            self.instructions_js["suggestions"]=self.get_suggestions()
        if self.additional_responses or self.test_it:
            self.instructions_js["additional_responses"]=self.get_additional_responses()
        if self.abort or self.test_it:
            self.instructions_js["abort"]=self.get_abort()
        if self.generate_title or self.test_it:
            self.instructions_js["generate_title"]= self.get_generate_title()
        return self.instructions_js
    def get_instructions(self,instructions_js=None):
        """
        Retrieves instructions for the conversation.

        Returns:
            None
        """
        if instructions_js == None:
            instructions_js = self.initialize_instructions()
        instructions = "your response is expected to be in JSON format with the keys as follows:\n"
        if self.test_it:
            instructions += 'this query is a test, please place a test response in every key\n'
        instructions += '\n'
        for i,key in enumerate(instructions_js.keys()):
            instructions+=f"{i}) {key} - {instructions_js[key]}\n"
        return instructions
