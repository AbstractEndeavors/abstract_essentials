import os
def browser(initial_folder:str=os.getcwd()):
    window = sg.Window('directory_browser',[[sg.Input('',key="selection"),sg.FolderBrowse("Select File", key="-FOLDER_SELECT-", initial_folder=initial_folder, target="-FOLDER_SELECT-", enable_events=True), sg.Button("select", key="-GRAB_FILE-", enable_events=True), sg.Button("EXIT", key="-EXIT-")]], resizable=True, finalize=True)
    while True:
        event,values = window.read()
        if event == '-GRAB_FILE-':
            window.close()
            break
    return values["selection"]
