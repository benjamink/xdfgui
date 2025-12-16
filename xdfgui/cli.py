from tkinter import Tk
from xdfgui.gui import App
import sys


def main():
    # Change the process name on macOS to show "xdfgui" in menu bar
    if sys.platform == 'darwin':
        try:
            import setproctitle
            setproctitle.setproctitle('xdfgui')
        except ImportError:
            pass
    
    root = Tk()
    root.title('xdfgui')
    
    # Bring window to front on macOS
    if sys.platform == 'darwin':
        root.createcommand('::tk::mac::ShowPreferences', lambda: None)
        root.lift()
        root.focus_force()
    
    app = App(root)
    root.mainloop()
