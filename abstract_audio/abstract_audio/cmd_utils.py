def cmd_it(st):
    return subprocess.Popen(st, stdout=subprocess.PIPE, shell=True)
