def global_registry(name:str,glob:dict):
    global_ledger = if_none_default(string='global_ledger',glob=globals(),default={"registry_names":[],"registry_index":[]})
    if name not in global_ledger['registry_names']:
        if glob == None:
            return None
        global_ledger['registry_names'].append(name)
        global_ledger['registry_index'].append(glob)
    length = len(global_ledger['registry_names']) 
    change_glob('global_ledger',global_ledger)
    for i in range(0,length):
        if name == global_ledger['registry_names'][i]:
            return i
def get_registry_number(name:str):
    return global_registry(name=name,glob=None)
def update_registry(var:str,val:any,name:str):
    global_ledger=get_globes(string='global_ledger',glob=globals())
    change_glob(var=var,val=val,glob=get_global_from_registry(name))
    global_ledger['registry_index'][get_registry_number(name)] = get_global_from_registry(name)
    change_glob(var='global_ledger',val=global_ledger)
def get_global_from_registry(name:str):
    global_ledger=get_globes(string='global_ledger',glob=globals())
    return global_ledger['registry_index'][get_registry_number(name)]
def return_globals() -> dict:
    """
    Returns the global variables.

    Args:
        globs (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        dict: The global variables dictionary.
    """
    return globals()
def change_glob(var: str, val: any, glob: dict = return_globals()) -> any:
    """
    Changes the value of a global variable.

    Args:
        var (str): The name of the global variable.
        val (any): The new value.
        glob (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        any: The new value of the variable.
    """
    glob[var] = val
    return val
def get_globes(string:str='',glob:dict=return_globals()):
    if string in glob:
        return glob[string]
def if_none_default(string:str, default:any,glob:dict=return_globals()):
    piece = get_globes(string=string,glob=glob)
    if piece is None:
        piece = default
    return change_glob(var=string,val=piece,glob=glob)

