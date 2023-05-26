import queue
import threading
import PySimpleGUI as sg

def worker_thread(shared_queue):
    # put data into the queue
    for i in range(10):
        shared_queue.put(i)
        time.sleep(1)
def create_queue():
  # create a queue
  shared_queue = queue.Queue()
  # create a thread
  thread = threading.Thread(target=worker_thread, args=(shared_queue,), daemon=True)
  # start the thread
  thread.start()
  # create a window
  layout = [[sg.Text("Data from thread:"), sg.Text(size=(15,1), key="-DISPLAY-")]]
  window = sg.Window("Window Title", layout)

  # event loop
  while True:
      event, values = window.read(timeout=100) # check every 100 ms
      if event == sg.WINDOW_CLOSED:
          break
      try:
          # try to get data from the queue
          data = shared_queue.get_nowait()
          # update the window
          window["-DISPLAY-"].update(data)
      except queue.Empty:
          pass
  window.close()
create_queue()
