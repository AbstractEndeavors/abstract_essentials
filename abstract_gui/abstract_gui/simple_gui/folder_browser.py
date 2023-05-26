def browser():
    window = sg.Window('directory_browser',[[sg.Input('',key="selection"),sg.FolderBrowse("Select File", key="-FOLDER_SELECT-", initial_folder="/home/bigrugz/Documents", target="-FOLDER_SELECT-", enable_events=True), sg.Button("select", key="-GRAB_FILE-", enable_events=True), sg.Button("EXIT", key="-EXIT-")]], resizable=True, finalize=True)
    while True:
        event,values = window.read()
        if event == '-GRAB_FILE-':
            window.close()
            break
    return values["selection"]
