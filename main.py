# kod z https://stackoverflow.com/questions/7208961/which-widget-do-you-use-for-a-excel-like-table-in-tkinter

from tkinter import *

root = Tk()

height = 5
width = 5
for i in range(height): #Rows
    for j in range(width): #Columns
        b = Entry(root, text="")
        b.grid(row=i, column=j)

mainloop()