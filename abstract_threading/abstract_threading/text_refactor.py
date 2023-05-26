def text_output():
    event_queue = queue.Queue()

    def thread_function(win, event_queue):
        while veri_win(win):
            event, values = win.read()
            if win_closed(event):
                break
            event_queue.put((event, values))
        close_window(win)

    while True:
        js = raw_data(prompt=speech_to_text.main())
        save_audio(js['response'])
        win = get_window(title='chat GPT output', layout=[[get_T('query: '), get_T(js['prompt'])],
                                                         [get_T('response: '), get_T(string=js['response'])]])
        thread = threading.Thread(target=thread_function, args=(win, event_queue), daemon=True)
        thread.start()
        play_audio()

        # Check the queue and handle events
        while True:
            try:
                event, values = event_queue.get_nowait()
                # Handle the event
            except queue.Empty:
                # No events to handle
                break
