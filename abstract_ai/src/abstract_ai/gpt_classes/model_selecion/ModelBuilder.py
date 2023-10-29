class ModelManager:
    """
    This class manages the selection and querying of models available for use.

    Attributes:
        selected_model_name (str): The name of the currently selected model.
        selected_endpoint (str): The endpoint associated with the currently selected model.
        selected_max_tokens (int): The maximum tokens associated with the currently selected model.
        default_model_info (dict): Information about the default model, including its name, endpoint, and maximum tokens.
        all_models (list): A list of all available models.

    Methods:
        get_all_values(key): Retrieves all unique values associated with the specified key from all available models.
        _get_endpoint_by_model(model_name): Returns the endpoint associated with the specified model.
        _get_models_by_endpoint(endpoint): Returns all models associated with the specified endpoint.
        _get_max_tokens_by_model(model_name): Returns the maximum tokens associated with the specified model.
    """
    def __init__(self, input_model_name=None, input_endpoint=None, default_selection=True):

        self.all_models = [{'model': 'whisper-1', 'endpoint': 'https://api.openai.com/v1/audio/transcriptions', 'tokens': None},
                       {'model': 'whisper-1', 'endpoint': 'https://api.openai.com/v1/audio/translations', 'tokens': None},
                       {'model': 'gpt-4', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 8192},
                       {'model': 'gpt-4-0613', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 8192},
                       {'model': 'gpt-4-32k', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 32768},
                       {'model': 'gpt-4-32k-0613', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 32768},
                       {'model': 'gpt-3.5-turbo', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 8001},
                       {'model': 'gpt-3.5-turbo-0613', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 4097},
                       {'model': 'gpt-3.5-turbo-16k', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 16385},
                       {'model': 'gpt-3.5-turbo-16k-0613', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 16385},
                       {'model': 'gpt-3.5-turbo-instruct', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 4097},
                       {'model': 'babbage-002', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 16384},
                       {'model': 'davinci-002', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 16384},
                       {'model': 'text-embedding-ada-002', 'endpoint': 'https://api.openai.com/v1/embeddings', 'tokens': None},
                       {'model': 'gpt-3.5-turbo', 'endpoint': 'https://api.openai.com/v1/fine_tuning/jobs', 'tokens': 8001},
                       {'model': 'babbage-002', 'endpoint': 'https://api.openai.com/v1/fine_tuning/jobs', 'tokens': 16384},
                       {'model': 'davinci-002', 'endpoint': 'https://api.openai.com/v1/fine_tuning/jobs', 'tokens': 16384},
                       {'model': 'text-moderation-stable', 'endpoint': 'https://api.openai.com/v1/moderations', 'tokens': 2049},
                       {'model': 'text-moderation-latest', 'endpoint': 'https://api.openai.com/v1/moderations', 'tokens': 2049}]
        self.all_model_names=self.get_all_values('model')
        self.all_endpoints=self.get_all_values('endpoint')
        self.default_model_info = {'model': 'gpt-4', 'endpoint': 'https://api.openai.com/v1/chat/completions', 'tokens': 8192}
        self.models_get_info_endpoint = "/v1/models"
        self.selected_model_name = input_model_name
        self.selected_endpoint = input_endpoint
        self.selected_max_tokens = None

        if not self.selected_model_name and not self.selected_endpoint and default_selection:
            self.selected_model_name = self.default_model_info['model']
            self.selected_endpoint = self.default_model_info['endpoint']
            self.selected_max_tokens = self.default_model_info['tokens']
        elif self.selected_model_name:
            self.selected_endpoint = self._get_endpoint_by_model(self.selected_model_name)
            self.selected_max_tokens = self._get_max_tokens_by_model(self.selected_model_name)
        elif self.selected_endpoint:
            # Assuming there could be multiple models for an endpoint.
            model_names_for_endpoint = self._get_models_by_endpoint(self.selected_endpoint)
            if model_names_for_endpoint:
                self.selected_model_name = model_names_for_endpoint[0]  # Default to the first model.
                self.selected_max_tokens = self._get_max_tokens_by_model(self.selected_model_name)
        if self.selected_model_name:
            self.selected_endpoint = self._get_endpoint_by_model(self.selected_model_name)
            self.selected_max_tokens = self._get_max_tokens_by_model(self.selected_model_name)
            if not self.selected_endpoint or not self.selected_max_tokens:
                # If model name not found and default_selection is True, revert to default model
                if default_selection:
                    self.selected_model_name = self.default_model_info['model']
                    self.selected_endpoint = self.default_model_info['endpoint']
                    self.selected_max_tokens = self.default_model_info['tokens']
    def get_all_values(self,key):
        all_values = []
        for value in self.all_models:
            if key in value:
                if value[key] not in all_values:
                    all_values.append(value[key])
        return all_values
    def _get_all_values(self, key):
        return list(set([value[key] for value in self.all_models if key in value]))

    def _get_endpoint_by_model(self, model_name):
        for model in self.all_models:
            if model["model"] == model_name:
                return model["endpoint"]
        return None

    def _get_models_by_endpoint(self, endpoint):
        return [model["model"] for model in self.all_models if model["endpoint"] == endpoint]

    def _get_max_tokens_by_model(self, model_name):
        for model in self.all_models:
            if model["model"] == model_name:
                return model["tokens"]
        return None
