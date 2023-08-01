def get_output(result):
    stdout, _ = result.communicate()
    return stdout
def cmd_it(st):
    return subprocess.Popen(st, stdout=subprocess.PIPE, shell=True, text=True)
