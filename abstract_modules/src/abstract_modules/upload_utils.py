import os
import math
import json
from abstract_utilities.read_write_utils import read_from_file,write_to_file
from abstract_utilities.cmd_utils import get_sudo_password,get_env_value,get_sudo_password,cmd_run_sudo,cmd_run,pexpect_cmd_with_args
from abstract_utilities.string_clean import eatAll
from abstract_gui import get_browser,create_row_of_buttons,create_window_manager,get_yes_no,expandable
from abstract_gui import get_gui_fun as ggf
from .module_utils import get_installed_versions,scan_folder_for_required_modules,load_alias_map,save_alias_map
windows_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())

def get_parent_directory(directory: str = os.getcwd()) -> str:
    """
    Opens a file browser to allow the user to pick a module directory and returns the chosen directory.
    If no directory is chosen, it keeps prompting until a selection is made.
    
    :param directory: The initial directory to open the file browser. Defaults to current working directory.
    :return: The path of the selected directory.
    """
    browser_values = None
    while browser_values is None:
        browser_values = get_browser(title="pick a module directory", type="folder", initial_folder=directory)
    return browser_values
def get_output_text(parent_directory: str = os.getcwd()) -> str:
    """
    Generate the path for the output text file based on the provided directory.

    :param parent_directory: Base directory.
    :return: Path to the output text file.
    """
    return os.path.join(parent_directory, 'output.txt')
def install_setup() -> str:
    """
    Return the command to install setup.

    :return: Command string.
    """
    return "sudo python3 setup.py sdist"
def install_twine() -> str:
    """
    Return the command to install twine.

    :return: Command string.
    """
    return "pip3 install build twine --break-system-packages"

def build_module(dist_dir: str) -> str:
    """
    If the 'dist' directory doesn't exist, create it. 
    Return the command to build the module.

    :param dist_dir: Directory to build the module in.
    :return: Command string.
    """
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    return "sudo python3 setup.py bdist_wheel"

def module_upload_cmd() -> str:
    """
    Return the command to upload the module.

    :return: Command string.
    """
    return "python3 -m twine upload dist/*.whl --skip-existing"

def upload_module(output_text: str = get_output_text()) -> str:
    """
    Execute the module upload command and handle the required child runs.

    :param output_text: Path to the output text.
    :return: Response from the command execution.
    """
    return pexpect_cmd_with_args(
        command=module_upload_cmd(),
        child_runs=[
            {"prompt": "Enter your username: ", "pass": None, "key": "PYPI_USERNAME"},
            {"prompt": "Enter your password: ", "pass": None, "key": "PYPI_PASSWORD"}
        ],
        output_text=output_text
    )

def save_new_setup(contents, filepath: str = os.getcwd()):
    """
    Save the new setup contents to a file.

    :param contents: Contents to be written to the file.
    :param filepath: Path to the file.
    """
    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(contents)
def read_setup(filepath) -> dict:
    """
    Read the setup file and extract necessary information.

    :param filepath: Path to the setup file.
    :return: Dictionary with extracted information.
    """
    with open(filepath, 'r', encoding='utf-8') as fh:
        setup_file = fh.read()
    cleaner_ls = ['', ' ', '\n', '\t', '"', "'"]
    version = eatAll(x=setup_file.split('version=')[-1].split(',')[0], ls=cleaner_ls)
    name = eatAll(x=setup_file.split('name=')[-1].split(',')[0], ls=cleaner_ls)
    url = eatAll(x=setup_file.split('url=')[-1].split(',')[0], ls=cleaner_ls)
    install_requires = eatAll(x=setup_file.split('install_requires=')[-1].split(']')[0] + ']', ls=cleaner_ls)
    return {
        "filepath": filepath,
        "file": setup_file,
        "version": version,
        "name": name,
        "url": url,
        "install_requires": install_requires
    }
def get_url(setup_js):
    """
    Determine if the URL in the setup information needs to be updated and prompt the user for changes.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
    """
    if setup_js["url"].split('/')[-1] != setup_js["name"]:
        url_new = setup_js["url"][:-len(setup_js["url"].split('/')[-1])]+setup_js["name"]
        permission = get_yes_no(text=f"would you like to change the url requires from {setup_js['url']} to {url_new}?'")
        windows_mgr.while_quick(windows_mgr.get_new_window(title='version number', args={"layout": [
                [[ggf("T", {"text": "would you like to change the url requires from {setup_js['url']} to {url_new}?"})],
                [ggf('Input', {"default_text": url_new, "key": "output"})],
                create_row_of_buttons("OK")]]},exit_events=["OK","Override"]))["output"]
        if permission == 'Yes':
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(install_requires,install_requires_new))
def edit_installs(event):
    """
    Handle the event of editing module installations based on user action.
    
    Args:
        event (str): Event trigger for editing installations.
    """
    if event == "Default":
        input(windows_mgr.get_values()["-DEFAULT_INSTALLS-"])
        windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-EDIT_INSTALLS-",value=windows_mgr.get_values()["-DEFAULT_INSTALLS-"])
def split_module_name(module):
    module_name=''
    for i,char in enumerate(module):
        if char not in '=,>,<'.split(','):
            module_name+=char           
        elif char in '=,>,<':
            return module_name
    return module_name
def convert_install_requires(install_requires):
    if isinstance(install_requires,list):
        return install_requires
    if isinstance(install_requires,str):
        install_requires=list(eatAll(install_requires,['(','"',"'",' ','','[',']']).split(','))
    update = []
    for i,each in enumerate(install_requires):
        update.append(eatAll(each,["'",'"','',' ']))
    return update
def clean_install_requires(install_requires,project_name):
    install_requires=convert_install_requires(install_requires)
    update = []
    for i,each in enumerate(install_requires):
        value = eatAll(each,["'",'"','',' '])
        if value not in update and split_module_name(value) != project_name:
            update.append(value)
    return update
def compare_lists(list_1,list_2):
    if len(list_1)>len(list_2):
        return False
    for each in list_1:
        if each not in list_2:
            return False
    return True
def alias_events(event):
    values = windows_mgr.get_values(windows_mgr.get_last_window_method())
    
    if event == "-SEARCH-":
        search_modules = []
        for each in values.keys():
            if "-ALIAS_" in each:
                search_modules.append(values[each])
                each = each[len("-ALIAS_"):-1]
                windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-ADD_"+each+'-',args={"value":False,"disabled":True})
        search,ignored = get_installed_versions(search_modules)
        if search:
            for module in search:
                split = False
                module_name=split_module_name(module)
                for each in values.keys():
                    if "-ORIGINAL_" in each:
                        original_name = each[len("-ORIGINAL_"):-1]
                        if values["-ALIAS_"+original_name+"-"] == module_name:
                            windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-FOUND_"+original_name+'-',args={"value":module,"disabled":True}),
                            windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-ALIAS_"+original_name+'-',value=module_name)
                            windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-ADD_"+original_name+'-',args={"value":True,"disabled":False})
    if event == "-SAVE-":
        alias = load_alias_map()
        for each in values.keys():
            if "-ADD_" in each:
                if values[each] == True:
                    original_name = values['-ORIGINAL_'+each[len("-ADD_"):]]
                    if original_name not in alias:
                        alias["ALIAS"][original_name]=values[f'-ALIAS_{original_name}-']
                    ignored_install = values[f'-FOUND_{original_name}-']
                    if ignored_install not in approved_ignored_installs:
                        approved_ignored_installs.append(ignored_install)
            if "-NEVER_" in each:
                if values[each] == True:
                    original_name = values['-ORIGINAL_'+each[len("-NEVER_"):]]
                    if original_name not in alias["NEVER"]:
                        alias["NEVER"].append(original_name)
            if "-DEFAULT_" in each:
                if values[each] == True:
                    original_name = values['-ORIGINAL_'+each[len("-DEFAULT_"):]]
                    if original_name not in alias["DEFAULT"]:
                        alias["DEFAULT"].append(original_name)
        save_alias_map(alias)
        return "Done"
def get_push():
    return ggf("Push")
def get_longest_len(length_list:list):
    if len(length_list) ==0:
        return 0
    highest = length_list[0]
    for each in length_list[1:]:
        if len(each) > len(highest):
            highest = each
    return len(highest)
def get_install_requires(setup_js, project_dir,project_name):
    """
    Get the list of required module installations for the given project directory.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
        project_dir (str): Path to the project directory.
    """
    approved_ignored_installs=[]
    globals()["approved_ignored_installs"]=approved_ignored_installs
    install_requires_new, ignored_all = get_installed_versions(scan_folder_for_required_modules(folder_path=project_dir,exclude=["setuptools",project_name]))
    alias = load_alias_map()
    if ignored_all:
        layout = []
        longest = get_longest_len(ignored_all)
        ignored = []
        for i,each in enumerate(ignored_all):
            if each not in alias["NEVER"] and each not in alias["DEFAULT"]:
                ignored.append(each)
        for i,each in enumerate(list(ignored)):
                lay = ggf("Frame",args={"title":each,"layout":[[
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"add"})],[
                                       ggf("Checkbox",args={"text":'',"key":"-ADD_"+each+'-',"default_value":False,"enable_events":False})]]}),
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"never"})],[
                                       ggf("Checkbox",args={"text":'',"key":"-NEVER_"+each+'-',"default_value":False,"enable_events":False})]]}),
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"default"})],[
                                       ggf("Checkbox",args={"text":'',"key":"-DEFAULT_"+each+'-',"default_value":False,"enable_events":False})]]}),
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"Alias"})],[
                                       ggf("Input",args={"key":"-ALIAS_"+each+'-',"size":(longest,1)})]]}),
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"Module"})],[
                                       ggf("Input",args={"default_text":each,"key":"-ORIGINAL_"+each+'-',"size":(longest,1),"disabled":True})]]}),
                                   ggf("Column",args={"layout":[[ggf("T",args={"text":"FOUND"}),get_push()],[ggf("Input",args={"key":"-FOUND_"+each+'-',"size":(longest,1),"disabled":True})]]}),
                                               ]]})
                if i%3 == float(0):
                    layout.append([lay])
                else:
                    layout[-1].append(lay)
        if len(layout)>0:
            layout.append([ggf("Button",args={"button_text":"SEARCH","key":"-SEARCH-","enable_events":True}),ggf("Button",args={"button_text":"SAVE","key":"-SAVE-","enable_events":True}),ggf("Button",args={"button_text":"Done","key":"Done","enable_events":True})])
            installs = windows_mgr.while_basic(windows_mgr.get_new_window(title='Ignored Dependencies', args={"layout": layout},event_function="alias_events",exit_events=["Done"]))
            event = windows_mgr.get_event(window=windows_mgr.get_last_window_method())
    if isinstance(setup_js['install_requires'],str):
        try:
            setup_js['install_requires'] = json.loads(str(setup_js['install_requires']))
        except:
            pass
    install_requires_new=clean_install_requires(install_requires_new,project_name)
    update = convert_install_requires(setup_js['install_requires'])
    if not compare_lists(update,install_requires_new):
        new_text = f"would you like to change the install requires from {update} to :"
        default_length = len(install_requires_new)/len(new_text)
        line = "Multiline"
        if math.ceil(default_length) == 1:
            line = "Input"
        layout =[
            [[ggf("T",args={"text":new_text})],
             [ggf(line,args={"default_text":install_requires_new,"key":"-DEFAULT_INSTALLS-","size":(len(new_text),math.ceil(default_length)),"disabled":True}),
              ggf("T",args={"text":"?"})],
             ggf("Multiline",args={"default_text":install_requires_new,"size":(len(new_text),10),"key":"-EDIT_INSTALLS-",**expandable()}),
             ],
            [create_row_of_buttons("Yes","No","Choose Edited","Default")]
            ]
        installs = windows_mgr.while_basic(windows_mgr.get_new_window(title='Install Requirements', args={"layout": layout},event_function="edit_installs",exit_events=["Yes","No","Choose Edited"]))
        event = windows_mgr.get_event(window=windows_mgr.get_last_window_method())
        install_requires_list = installs["-DEFAULT_INSTALLS-"][1:-1].split(',')
        if event == "Choose Edited":
            update=convert_install_requires(installs["-EDIT_INSTALLS-"])
        if event not in ["No","exit","Exit","EXIT"]:
            input([update,read_setup(setup_js['filepath'])["file"]])
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(str(setup_js['install_requires']),str(update)))
    
def organize_versions_from_high_to_low(version_list) -> list:
    """
    Organize the list of version numbers from highest to lowest.
    :param version_list: A list of version numbers to organize.
    :return: A new list of version numbers sorted from highest to lowest.
    """
    sorted_versions = sorted(version_list, key=lambda x: list(map(int, x.split('.'))), reverse=True)
    return sorted_versions

def get_distributions_from_packages(setup_js, version_numbers: list = []) ->list:
    """
    Retrieve distribution versions from package directory and populate the provided version_numbers list.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
        version_numbers (list): List of version numbers to populate.
        
    Returns:
        list: Updated version_numbers list.
    """
    dist_dir = os.path.join(setup_js['filepath'][:-len(os.path.basename(setup_js['filepath']))], 'dist')
    if os.path.isdir(dist_dir):
        dist_list = os.listdir(dist_dir)
        for dist in dist_list:
            rest = dist[len(setup_js['name'] + '-'):]
            version = ''
            while len(rest) > 0 and rest[0] in '0123456789.':
                version += rest[0]
                rest = rest[1:]
            version = version.rstrip('.')
            if version not in version_numbers:
                version_numbers.append(version)
    return version_numbers
def get_version_input(highest) ->str:
    """
    Get user input for a new version number.
    
    Args:
        highest (dict): Dictionary containing version information.
        
    Returns:
        str: New version number provided by the user.
    """
    text = ''
    if highest["exists"] == True:
        text += f"Version number {highest['version']} already exists."
    if highest["exists"] == True:
        text += f"Version number {highest['version']} does not exist."
    if highest["bool"] == False:
        text += f"\nYour version number {highest['version']} is lower than the highest version number {highest['highest']}."
    if highest["bool"] == True:
        text += f"\nYour version number {highest['version']} is the highest version number found."
    text += '\n\nplease enter a new version number:'
    layout = [
        [ggf("T", {"text": text})],
        [ggf('Input', {"default_text": highest['highest'], "key": "version_number"})],
        create_row_of_buttons("OK")
    ]
    new_version = windows_mgr.while_basic(windows_mgr.get_new_window(title='Version number', args={"layout": layout},exit_events=["OK", "Override"]))["version_number"]
    return new_version
def get_highest(distributions, version) -> dict:
    """
    Determine the highest version in a list of distributions relative to a given version.
    
    Args:
        distributions (list): List of distribution versions.
        version (str): Version to compare against.
        
    Returns:
        dict: Dictionary containing comparison results.
    """
    if len(distributions) == 0:
        return '0.0.0.0'
    highest = {"bool":False,"version":version,"highest":version,"exists":False}
    if highest['version'] in distributions:
        highest["bool"] = False
        highest["highest"] = distributions[0]
        highest["exists"] = True
    if highest['version'] not in distributions:
        highest["exists"] = False
        curr_high = organize_versions_from_high_to_low([distributions[0],version])
        if curr_high[0] == version:
            highest["bool"]=True
            highest["highest"] = version
        if curr_high[0] != version:
            highest["bool"]=False
            highest["highest"] = curr_high[0]
    return highest
def get_all_versions(distributions, installed) -> list:
    """
    Get all versions by combining distributions and installed versions.
    
    Args:
        distributions (list): List of distribution versions.
        installed (list): List of installed versions.
        
    Returns:
        list: List of combined versions, organized from high to low.
    """
    if len(installed) != 0:
        if '=' in installed[0]:
            version_number = installed[0].split('=')[-1]
            if version_number not in distributions:
                distributions.append(version_number)
    return organize_versions_from_high_to_low(distributions)
def finalize_version(setup_js):
    """
    Finalize the version for setup by interacting with the user.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
    """
    version = setup_js['version']
    distributions = get_all_versions(get_distributions_from_packages(setup_js),get_installed_versions([setup_js['name']]))
    while True:
        highest = get_highest(distributions,version)
        if highest["bool"] == False:
            new_version=get_version_input(highest)
            if highest['highest'] == organize_versions_from_high_to_low([highest['highest'],new_version])[0]:
                override_prompt = f"this is still not the highest version number;\nWould you like to override the version number with {new_version}?"
                override = get_yes_no(text=override_prompt)
                if override == "Yes":
                    break
            else:
                version = new_version
        if highest["bool"] == True and highest["exists"] == False:
            break
    save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(str(setup_js['version']),str(version)))
def install_module(event):
    """
    Install a module based on event trigger.
    
    Args:
        event (str): Event trigger for installation.
    """
    if event == "install_module":
        cmd_run(f'pip install {read_setup(globals()["setup_file_path"])["name"]}=={read_setup(globals()["setup_file_path"])["version"]} --break-system-packages')
        cmd_run(f'pip install {read_setup(globals()["setup_file_path"])["name"]}=={read_setup(globals()["setup_file_path"])["version"]} --break-system-packages')
def install_mods_layout():
    """
    Display installation module layout.
    """
    win=windows_mgr.get_new_window(title="install module",layout=[create_row_of_buttons('install_module','EXIT')],event_function='install_module')
    events = windows_mgr.while_basic(window=win)
def get_list_of_projects(parent_directory) -> str:
    """
    Get a list of projects in the given directory.
    
    Args:
        parent_directory (str): Parent directory to search for projects.
        
    Returns:
        str: Selected project from the list.
    """
    win=windows_mgr.get_new_window(title="list_window",args={"layout":[[ggf('Listbox',{"values":os.listdir(parent_directory),"size":(25,10),'key':'projects',"enable_events":True}),
                                                                        ggf('Button',{'button_text':'submit','key':'exit'})]]})
    return windows_mgr.while_basic(window=win)['projects'][0]
def clear_output_text(file_path):
    write_to_file(file_path=file_path,contents='')
def run_setup_loop(parent_directory: str = os.getcwd()) -> str:
    """
    Run the setup process in a loop for a given parent directory.
    
    Args:
        parent_directory (str): Parent directory containing projects.
        
    Returns:
        str: Project directory where setup was run.
    """
    output_text = get_output_text(parent_directory)
    cmd_run_sudo(cmd=install_twine(),key="SUDO_PASSWORD",output_text=output_text)
    clear_output_text(output_text)
    if "project_name" not in globals():
        globals()["project_name"]=get_list_of_projects(parent_directory)
    project_dir = os.path.join(parent_directory,project_name)
    setup_file_path = os.path.join(project_dir,"setup.py")
    src_dir = os.path.join(project_dir,"src")
    dist_dir = os.path.join(project_dir,"dist")
    setup_js = read_setup(setup_file_path)
    finalize_version(setup_js)
    get_install_requires(setup_js,project_dir,project_name)
    get_url(setup_js)
    print(f"Running setup.py for project: {project_dir}")
    globals()["setup_file_path"]=setup_file_path
    os.chdir(project_dir)
    cmd_run_sudo(cmd=install_setup(),key="SUDO_PASSWORD",output_text=output_text)
    clear_output_text(output_text)
    cmd_run_sudo(cmd=build_module(dist_dir),key="SUDO_PASSWORD",output_text=output_text)
    clear_output_text(output_text)
    upload_module(output_text=output_text)
    print(f"Completed setup.py for project: {project_dir}")
    install_mods_layout()
    clear_output_text(output_text)
    return project_dir
def upload_main(directory:str=os.getcwd(),project_dir:str=None):
    """
    Upload the main program for execution.
    
    Args:
        directory (str): Current working directory.
    """
    if project_dir != None:
        parent_directory=os.path.split(project_dir)[0]
        globals()["project_name"]=os.path.split(project_dir)[-1]
    else:
        parent_directory= get_parent_directory(directory)
    run_setup_loop(parent_directory)
