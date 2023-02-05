import tkinter as tk
import ui



# start gui in main
if __name__ == "__main__":
    root = tk.Tk()
    root.state('normal')
    root.resizable(False,False)
    ui.showHomeFrame(root)
    root.mainloop()