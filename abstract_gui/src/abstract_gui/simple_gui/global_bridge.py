class WindowGlobalBridge:
    def __init__(self):
        self.global_vars = {}

    def retrieve_global_variables(self, script_name, global_variables):
        self.global_vars[script_name] = global_variables
        
    def return_global_variables(self, script_name):
        return self.global_vars.get(script_name, {})
