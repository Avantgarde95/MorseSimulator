import sys

try:
    import tkinter as tk
except ImportError:
    print('[Error] Failed to load Tkinter.')
    sys.exit(0)

from lib import ui_py3 as ui

def main():
    root = tk.Tk()
    root.wm_title('Morse code simulator')
    app = ui.MainApp(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
