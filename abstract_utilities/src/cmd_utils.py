import os
import time
import pexpect
from abstract_security.envy_it import find_and_read_env_file, get_env_value
import subprocess
def get_output_text(parent_dir:str=os.getcwd()):
    return os.path.join(parent_dir,'output.txt')
def get_env_value(key:str=None,env_path:str=None):
    args={}
    if key != None:
        args["key"]=key
    if env_path != None:
        args["start_path"]=env_path
    return find_and_read_env_file(**args)
def print_cmd(input,output):
    print(f"Command Line Arguments: {input}")
    print(f"Output:\n{output}")
def get_sudo_password(key:str="SUDO_PASSWORD"):
    return find_and_read_env_file(key=key)
def cmd_run_sudo(cmd,password:str=None,key:str=None,output_text:str=None):
    if password !=None:
        cmd_run(f'echo "{password}" | sudo -S -k {cmd}',output_text)
    elif key != None:
        cmd_run(f'echo "{get_env_value(key)}" | sudo -S -k {cmd}',output_text)
    else:
        cmd_run(f'echo "{get_sudo_password()}" | sudo -S -k {cmd}',output_text)
def cmd_run(cmd,output_text:str=None):
    if output_text == None:
        output_text=get_output_text()
    # Clear the output file before running the command
    with open(get_output_text(), 'w') as f:
        pass
    cmd += f' >> '+output_text+'; echo END_OF_CMD >> '+output_text  # Add the delimiter at the end of cmd
    print(cmd)
    output = subprocess.call(f'gnome-terminal -- bash -c "{cmd}"', shell=True)
    # Wait until the delimiter appears in the output file
    while True:
        time.sleep(0.5)  # Sleep for a while to reduce CPU usage
        with open(output_text, 'r') as f:
            lines = f.readlines()
            if lines:  # Check if the file is not empty
                last_line = lines[-1].strip()  # Read the last line of the file
                if last_line == 'END_OF_CMD':
                    break  # Break the loop if the delimiter is found
    # Print the command and its output
    with open(output_text, 'r') as f:
        output = f.read().strip()  # Read the entire output
    print_cmd(cmd, output)
    print(output)
    # Delete the output file and the bash script
    os.remove(get_output_text())
def pexpect_cmd_with_args(command, child_runs, output_text=str(os.getcwd())):
    child = pexpect.spawn(command)

    for each in child_runs:
        # Wait for the process to prompt for the input and respond with it
        child.expect(each["prompt"])

        # Respond with the corresponding input
        if each["pass"] is not None:
            pass_phrase = each["pass"]
        else:
            args = {}
            if "key" in each:
                if each["key"] is not None:
                    args["key"] = each["key"]
            if "env_path" in each:
                if each["env_path"] is not None:
                    args["start_path"] = each["env_path"]

            pass_phrase = get_env_value(**args)

        child.sendline(pass_phrase)

        print("Output after handling prompt:")
        print(each["prompt"])

    # Wait for the process to finish
    child.expect(pexpect.EOF)
    output = child.before.decode("utf-8")

    # Write output to the output file
    with open(get_output_text(), "w") as f:
        f.write(output)

    print_cmd(command, output)

    return child.exitstatus
