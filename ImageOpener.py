import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PIL import Image

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue')
canvas1.pack()


def getImage():
    global import_file_path
    import_file_path = filedialog.askopenfilename()
    img = Image.open(import_file_path)
    img.show()


browseButton_Imagify = tk.Button(
    text='Open Image File', command=getImage, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_Imagify)

root.mainloop()
