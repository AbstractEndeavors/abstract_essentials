import os
import pexpect
from abstract_utilities.read_write_utils import read_from_file,write_to_file
from abstract_utilities.cmd_utils import get_sudo_password,get_env_value,get_sudo_password,cmd_run_sudo,cmd_run,pexpect_cmd_with_args
from abstract_utilities.string_clean import eatAll
from abstract_gui import *
from .module_utils import get_installed_versions,scan_folder_for_required_modules
# Load environment variables from .env file
windows_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())
def get_parent_directory(directory:str=os.getcwd()):
    browser_values = None
    while browser_values == None:
        browser_values = get_browser(title="pick a module directory", type="folder", initial_folder=directory)
    # Now you can access the "Browse" key from browser_values dictionary
    if browser_values and "output" in browser_values:
        return browser_values["output"]
        # Just for debugging purposes, you can remove this line once it's working correctly
# Call the function to test it

def get_output_text(parent_directory:str=os.getcwd()):
    return os.path.join(parent_directory,'output.txt')
def install_setup():
    return "sudo python3 setup.py sdist"
def install_twine():
    return "pip3 install build twine --break-system-packages"
def build_module(dist_dir):
    # Create the 'dist' directory if it doesn't exist
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    return "sudo python3 setup.py bdist_wheel"
def module_upload_cmd():
    return "python3 -m twine upload dist/*.whl --skip-existing"
def upload_module(output_text:str=get_output_text()):
    return pexpect_cmd_with_args(command=module_upload_cmd(),child_runs=[{"prompt":"Enter your username: ","pass":None,"key":"PYPI_USERNAME"},
                                                                         {"prompt":"Enter your password: ","pass":None,"key":"PYPI_PASSWORD"}],
                                 output_text=output_text)
def save_new_setup(contents,filepath:str=os.getcwd()):
    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(contents)
def read_setup(filepath):
    with open(filepath, 'r', encoding='utf-8') as fh:
        setup_file = fh.read()
    cleaner_ls =['',' ','\n','\t','"',"'"]
    version = eatAll(x=setup_file.split('version=')[-1].split(',')[0],ls=cleaner_ls)
    name= eatAll(x=setup_file.split('name=')[-1].split(',')[0],ls=cleaner_ls)
    url = eatAll(x=setup_file.split('url=')[-1].split(',')[0],ls=cleaner_ls)
    install_requires = eatAll(x=setup_file.split('install_requires=')[-1].split(']')[0]+']',ls=cleaner_ls)
    return {"filepath":filepath,"file":setup_file,"version":version,"name":name,"url":url,"install_requires":install_requires}
def get_url(setup_js):
    if setup_js["url"].split('/')[-1] != setup_js["name"]:
        url_new = setup_js["url"][:-len(setup_js["url"].split('/')[-1])]+setup_js["name"]
        permission = get_yes_no(text=f"would you like to change the url requires from {setup_js['url']} to {url_new}?'")
        windows_mgr.while_quick(windows_mgr.get_new_window(title='version number', args={"layout": [
                [[get_gui_fun("T", {"text": "would you like to change the url requires from {setup_js['url']} to {url_new}?"})],
                [get_gui_fun('Input', {"default_text": url_new, "key": "output"})],
                [sg.Button("OK")]]]},exit_events=["OK","Override"]))["output"]
        if permission == 'Yes':
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(install_requires,install_requires_new))
def get_install_requires(setup_js):
    install_requires_new = get_installed_versions(scan_folder_for_required_modules())
    if setup_js['install_requires'] != install_requires_new:
        permission = get_yes_no(text=f"would you like to change the install requires from {setup_js['install_requires']} to {install_requires_new}?'")
        if permission == 'Yes':
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(str(setup_js['install_requires']),str(install_requires_new)))
def organize_versions_from_high_to_low(version_list):
    """
    Organize the list of version numbers from highest to lowest.
    :param version_list: A list of version numbers to organize.
    :return: A new list of version numbers sorted from highest to lowest.
    """
    sorted_versions = sorted(version_list, key=lambda x: list(map(int, x.split('.'))), reverse=True)
    return sorted_versions

def get_distributions_from_packages(setup_js,version_numbers:list=[]):
    dist_dir = os.path.join(setup_js['filepath'][:-len(os.path.basename(setup_js['filepath']))],'dist')
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
def get_version_input(highest):
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
        [get_gui_fun("T", {"text": text})],
        [get_gui_fun('Input', {"default_text": highest['highest'], "key": "version_number"})],
        [sg.Button("OK")]
    ]
    new_version = windows_mgr.while_basic(windows_mgr.get_new_window(title='Version number', args={"layout": layout},exit_events=["OK", "Override"]))["version_number"]
    return new_version
def get_highest(distributions,version):
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
def get_all_versions(distributions,installed):
    if len(installed) != 0:
        if '=' in installed[0]:
            version_number = installed[0].split('=')[-1]
    if version_number not in distributions:
        distributions.append(version_number)
    return organize_versions_from_high_to_low(distributions)
def finalize_version(setup_js):
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
    if event == "install":
        cmd_run(f'pip install {read_setup(globals()["setup_file_path"])["name"]}=={read_setup(globals()["setup_file_path"])["version"]} --break-system-packages')
def install_mods_layout():
    win=windows_mgr.get_new_window(title="install module",layout=[[get_gui_fun('Button',{'button_text':'install_module','key':'install'}),
                                                                   get_gui_fun('Button',{'button_text':'exit','key':'EXIT'})]],event_function='install_module')
    while True:
        events = windows_mgr.while_basic(window=win)
        if events == None:
            return 
def get_list_of_projects(parent_directory):
    win=windows_mgr.get_new_window(title="list_window",layout=[[get_gui_fun('Listbox',{"values":os.listdir(parent_directory),"size":(25,10),'key':'projects',"enable_events":True}),
                                                                get_gui_fun('Button',{'button_text':'submit','key':'exit'})]])
    return windows_mgr.while_basic(window=win)['projects'][0]
def run_setup_loop(parent_directory:str=os.getcwd()):
    output_text = get_output_text(parent_directory)
    cmd_run_sudo(cmd=install_twine(),key="SUDO_PASSWORD",output_text=output_text)
    project_name = get_list_of_projects(parent_directory)
    project_dir = os.path.join(parent_directory,project_name)
    setup_file_path = os.path.join(project_dir,"setup.py")
    src_dir = os.path.join(project_dir,"src")
    dist_dir = os.path.join(project_dir,"dist")
    setup_js = read_setup(setup_file_path)
    finalize_version(setup_js)
    get_install_requires(setup_js)
    get_url(setup_js)
    print(f"Running setup.py for project: {project_dir}")
    globals()["setup_file_path"]=setup_file_path
    os.chdir(project_dir)
    cmd_run_sudo(cmd=install_setup(),key="SUDO_PASSWORD",output_text=output_text)
    cmd_run_sudo(cmd=build_module(dist_dir),key="SUDO_PASSWORD",output_text=output_text)
    upload_module(output_text=output_text)
    print(f"Completed setup.py for project: {project_dir}")
    install_mods_layout()
    return project_dir
def upload_main(directory:str=os.getcwd()):
    parent_directory= get_parent_directory(directory)
    run_setup_loop(parent_directory)
