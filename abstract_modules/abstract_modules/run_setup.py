import os
import subprocess
from abstract_security.envy_it import *
import time
import pexpect
from abstract_gui.simple_gui.gui_presets import get_browser
from abstract_gui.simple_gui.gui_template import *
import os
# Load environment variables from .env file
def get_parent_directory():
    globals()['parent_dir'] = get_browser(title="pick a module directory",type="folder",initial_folder=os.getcwd())
get_parent_directory()

def get_output_txt():
    return os.path.join(parent_dir,'output.txt')
def get_sudo_password():
    return find_and_read_env_file(key="SUDO_PASSWORD")

def get_pypi_username():
    return find_and_read_env_file(key="PYPI_USERNAME")

def get_pypi_password():
    return find_and_read_env_file(key="PYPI_PASSWORD")

def get_src_dir():
    globals()['src_dir'] = os.path.join(parent_dir,project,"src")

def get_project_dirs():
    globals()['project_dirs'] = [name for name in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, name))]

def install_setup():
    return "python3 setup.py install"

def install_twine():
    return "pip3 install build twine --break-system-packages"

def build_module():
    # Create the 'dist' directory if it doesn't exist
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    return "python3 setup.py sdist bdist_wheel"

def upload_module():
    username = get_pypi_username()
    password = get_pypi_password()
    
    cmd = "python3 -m twine upload dist/* --skip-existing"
    child = pexpect.spawn(cmd)

    # Wait for the process to prompt for the username and respond with it
    child.expect("Enter your username: ")
    child.sendline(username)

    # Wait for the process to prompt for the password and respond with it
    child.expect("Enter your password: ")
    child.sendline(password)

    # Wait for the process to finish
    child.expect(pexpect.EOF)
    output = child.before.decode("utf-8")

    # Write output to the output file
    with open(get_output_txt(), "w") as f:
        f.write(output)

    print_cmd(cmd, output)

    return child.exitstatus
def print_cmd(input,output):
    print(f"Command Line Arguments: {input}")
    print(f"Output:\n{output}")

def cmd_run(cmd):
    # Clear the output file before running the command
    with open(get_output_txt(), 'w') as f:
        pass
    
    cmd += f' >> '+get_output_txt()+'; echo END_OF_CMD >> '+get_output_txt()  # Add the delimiter at the end of cmd
    print(cmd)
    output = subprocess.call(f'gnome-terminal -- bash -c "{cmd}"', shell=True)

    # Wait until the delimiter appears in the output file
    while True:
        time.sleep(0.5)  # Sleep for a while to reduce CPU usage
        with open(get_output_txt(), 'r') as f:
            lines = f.readlines()
            if lines:  # Check if the file is not empty
                last_line = lines[-1].strip()  # Read the last line of the file
                if last_line == 'END_OF_CMD':
                    break  # Break the loop if the delimiter is found

    # Print the command and its output
    with open(get_output_txt(), 'r') as f:
        output = f.read().strip()  # Read the entire output
    print_cmd(cmd, output)
    print(output)
    # Delete the output file and the bash script
    os.remove(get_output_txt())

def cmd_run_sudo(cmd):
    cmd_run(f'echo "{get_sudo_password()}" | sudo -S -k {cmd}')
def get_list_of_projects():
    win=get_window(title="list_window",layout=[[get_gui_fun('Listbox',{"values":os.listdir(parent_dir),"size":(25,10),'key':'projects',"enable_events":True}),get_gui_fun('Button',{'button_text':'submit','key':'exit'})]])
    globals()['project'] = while_basic(win=win)['projects'][0]
def run_setup_loop():

    cmd_run_sudo(install_twine())
    get_list_of_projects()
    get_src_dir()
    get_project_dirs()
    globals()['project_dir'] = os.path.join(parent_dir,project)
    os.chdir(project_dir)
    print(f"Running setup.py for project: {project_dir}")
    cmd_run_sudo(install_setup())
    cmd_run_sudo(build_module())
    upload_module()

    print(f"Completed setup.py for project: {project_dir}")
    print()

cmd_run(install_twine())
run_setup_loop()
