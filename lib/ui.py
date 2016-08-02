''' GUI design '''

from time import time
import Tkinter as tk
import core

class MainApp(tk.Frame, object):
    ''' Main window UI '''
    def __init__(self, parent = None):
        ''' Initialize attributes, frames, and widgets. '''
        self.parent = parent
        super(MainApp, self).__init__(self.parent)

        self.is_recording = False
        self.time_press = 0 # time when 'signal' button is pressed
        self.signals = [] # whole list of signals

        # frames
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(padx = 10, pady = 10)

        self.frame_control = tk.Frame(self.frame_main)
        self.frame_signal = tk.Frame(self.frame_main)
        self.frame_status = tk.Frame(self.frame_main)
        
        self.frame_control.grid(row = 0, column = 0)
        self.frame_signal.grid(row = 0, column = 1)
        self.frame_status.grid(row = 0, column = 2)

        # widgets
        self.button_start = tk.Button(self.frame_control,
                                      text = 'start',
                                      width = 8,
                                      command = self.callback_start)
        self.button_stop = tk.Button(self.frame_control,
                                     text = 'stop',
                                     width = 8,
                                     command = self.callback_stop)
        self.button_analyze = tk.Button(self.frame_control,
                                        text = 'analyze',
                                        width = 8,
                                        command = self.callback_analyze)
        self.button_clear = tk.Button(self.frame_control,
                                      text = 'clear',
                                      width = 8,
                                      command = self.callback_clear)
        self.button_quit = tk.Button(self.frame_control,
                                     text = 'quit',
                                     width = 8,
                                     command = self.callback_quit)
        
        self.button_start.grid(row = 0, column = 0)
        self.button_stop.grid(row = 0, column = 1)
        self.button_analyze.grid(row = 1, column = 0)
        self.button_clear.grid(row = 1, column = 1)
        self.button_quit.grid(row = 2, column = 0)

        self.button_signal = tk.Canvas(self.frame_signal,
                                       width = 100,
                                       height = 100)
        
        self.button_signal.bind('<ButtonPress-1>',
                                self.callback_signal_press)

        self.button_signal.bind('<ButtonRelease-1>',
                                self.callback_signal_release)
        
        self.id_bg = self.button_signal.create_rectangle(
            (0, 0, 100, 100), fill = 'skyblue', outline = '')
        self.id_circle = self.button_signal.create_oval(
            (20, 20, 80, 80), fill = 'red', outline = '')

        self.button_signal.pack(padx = 20, pady = 20)

        self.text_status = tk.Text(self.frame_status,
                                   width = 20,
                                   height = 10)
        self.text_status.pack()

    def callback_start(self):
        ''' Clear the data and start recording. '''
        self.clear_status()
        self.write_status('recording...')
        self.is_recording = True
        self.signals = []
        
        print '[Log] Recording started.'

    def callback_stop(self):
        ''' Stop recording '''
        self.clear_status()
        self.write_status('recording finished')
        self.is_recording = False

        print '[Log] Recording finished.'
        print '[Log] Received signals :', self.signals

    def callback_analyze(self):
        ''' Analyze the data and print the decoded message. '''
        if self.is_recording:
            return

        if len(self.signals) == 0:
            print '[Log] No signals.'
            return

        self.clear_status()
        self.write_status('Analyzing...')
        print '[Log] Analyzing...'

        message = core.decode_signals(self.signals)

        self.clear_status()
        self.write_status('Result : ' + message)

    def callback_clear(self):
        ''' Clear the status panel and the data. '''
        self.clear_status()
        self.is_recording = False
        self.signals = []

    def callback_quit(self):
        ''' Close the app. '''
        self.parent.destroy()

    def callback_signal_press(self, e):
        ''' Highlight the signal button, and start measuring time. '''
        t = time()
        self.highlight_signal_on()
        
        if not self.is_recording:
            return

        self.time_press = t

    def callback_signal_release(self, e):
        ''' Highlight the signal button, and record elapsed time. '''
        t = time()
        self.highlight_signal_off()
        
        if not self.is_recording:
            return

        self.signals.append((self.time_press, t))

    def highlight_signal_on(self):
        ''' Highlight the signal button. '''
        self.button_signal.itemconfig(self.id_bg, fill = 'blue')
        self.button_signal.itemconfig(self.id_circle, fill = 'brown')

    def highlight_signal_off(self):
        ''' Cancel highlighting the signal button. '''
        self.button_signal.itemconfig(self.id_bg, fill = 'skyblue')
        self.button_signal.itemconfig(self.id_circle, fill = 'red')

    def clear_status(self):
        ''' Clear the status panel. '''
        self.text_status.delete(1.0, 'end')

    def write_status(self, message):
        ''' Write a string on the status panel. '''
        self.text_status.insert(1.0, message)

def test():
    ''' Test function '''
    root = tk.Tk()
    app = MainApp(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    test()
