import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Grid
import string

#region Utworzenie głównego okna
root = tk.Tk()
#root.geometry("500x250")
root.title("Tabelkomistrz")
usedFont = {'family': 'Segoe UI', 'size': 9, 'weight': 'normal', 'slant': 'italic', 'underline': 0, 'overstrike': 0}
#endregion

Grid.rowconfigure(root,index=0,weight=1)
Grid.rowconfigure(root,index=1,weight=10)
Grid.columnconfigure(root,index=0,weight=1)

#region Utworzenie panelu z zakładkami
tabsPanel = Notebook(root, height=55)
tabsPanel.grid(row=0, sticky='we')
#endregion

#region Dodawanie nowych zakładek
Grid.columnconfigure(tabsPanel, index=0, weight=1)
Grid.rowconfigure(tabsPanel, index=0, weight=1)

tabBasic = tk.Frame(tabsPanel, height=30)
tabEdit = tk.Frame(tabsPanel, height=30)
tabImpExp = tk.Frame(tabsPanel, height=30)

tabBasic.grid(row=0, column=0, sticky='news')
tabEdit.grid(row=0, column=0, sticky='news')
tabImpExp.grid(row=0, column=0)

tabsPanel.add(tabBasic, text='Podstawowe')
tabsPanel.add(tabEdit, text='Edytuj')
tabsPanel.add(tabImpExp, text='Import/Eksport')
#endregion

#region Zawartość zakładki "Podstawowe"
Grid.columnconfigure(tabBasic, index=0, weight=0.5)
Grid.columnconfigure(tabBasic, index=1, weight=0.5)
Grid.columnconfigure(tabBasic, index=2, weight=0.5)
Grid.columnconfigure(tabBasic, index=3, weight=0.5)
Grid.columnconfigure(tabBasic, index=4, weight=0.5)
Grid.columnconfigure(tabBasic, index=5, weight=1)
Grid.columnconfigure(tabBasic, index=6, weight=7)
Grid.rowconfigure(tabBasic, index=0, weight=1)

basicLdim = tk.Label(tabBasic, text='Wymiary tabeli: ')
basicLdim.configure(font=(f"{usedFont['family']}", usedFont['size'], 'bold'))
basicLdim.grid(row=0, column=0,sticky=tk.W)

basicLr = tk.Label(tabBasic,text="L. wierszy:")
basicLr.grid(row=0, column=1,sticky=tk.W)
basicSr = tk.Spinbox(tabBasic, from_=1, to_=6, width=5)
basicSr.grid(row=0, column=2,sticky=tk.W)

basicLc = tk.Label(tabBasic,text="L. kolumn:")
basicLc.grid(row=0, column=3,sticky=tk.W)
basicSc = tk.Spinbox(tabBasic, from_=1, to_=6, width=5)
basicSc.grid(row=0, column=4,sticky=tk.W)

basicBchange = tk.Button(tabBasic, text="Zmień")
basicBchange.grid(row=0, column=5)

basicBtemplate = tk.Button(tabBasic, text="Załaduj szablon")
basicBtemplate.grid(row=0,column=6,sticky=tk.E)
#endregion


#region Zawartość zakładki "Edytuj"
Grid.columnconfigure(tabEdit, index=0, weight=100)
Grid.columnconfigure(tabEdit, index=1, weight=1)
Grid.columnconfigure(tabEdit, index=2, weight=1)
Grid.columnconfigure(tabEdit, index=3, weight=1)
Grid.rowconfigure(tabEdit, index=0, weight=1)

editBmerge = tk.Button(tabEdit, text="Scal komórki")
editBmerge.grid(row=0, column=0,sticky=tk.W)

editBb = tk.Button(tabEdit, text="B")
editBb.configure(font=(f"{usedFont['family']}", usedFont['size'], 'bold'))
editBb.grid(row=0, column=1,sticky=tk.W)

editBi = tk.Button(tabEdit, text="I")
editBi.configure(font=(f"{usedFont['family']}", usedFont['size'], 'italic'))
editBi.grid(row=0, column=2,sticky=tk.W)

editBu = tk.Button(tabEdit,text="U")
editBu.configure(underline=0)
editBu.grid(row=0, column=3,sticky=tk.W)
#endregion

#region Zawartość zakładki "Import/Eksport"
Grid.columnconfigure(tabImpExp, index=0, weight=0.5)
Grid.columnconfigure(tabImpExp, index=1, weight=1)
Grid.columnconfigure(tabImpExp, index=2, weight=1)
Grid.columnconfigure(tabImpExp, index=3, weight=0.5)
Grid.rowconfigure(tabImpExp, index=0, weight=1)

impexpLimp = tk.Label(tabImpExp, text="Eksport do LaTeX: ")
impexpLimp.grid(row=0, column=0,sticky=tk.W)
impexpBimp = tk.Button(tabImpExp, text="Eksportuj")
impexpBimp.grid(row=0, column=1,sticky=tk.W)

impexpLexp = tk.Label(tabImpExp, text="Import tabeli z LaTeX: ")
impexpLexp.grid(row=0, column=2,sticky=tk.E)
impexpBexp = tk.Button(tabImpExp, text="Importuj")
impexpBexp.grid(row=0, column=3,sticky=tk.E)
#endregion

#region Siatka z komórkami
main_frame = tk.Frame(root)
main_frame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)

rows = 10
columns = 5

# listy indexów komórek wyświetlane nad siatką i po lewej stronie siatki
rowIndex = [i for i in range(0,rows,1)]
columnIndex = list(string.ascii_uppercase)
for i in range(columns):
    Grid.columnconfigure(main_frame, index=i+1, weight=1)
    columnIndex[i] = tk.Label(main_frame, text=f'{columnIndex[i]}')
    columnIndex[i].grid(row=0, column=i+1, sticky='news')

for i in range(rows):
    Grid.rowconfigure(main_frame, index=i+1, weight=1)
    rowIndex[i] = tk.Label(main_frame, text=f'{rowIndex[i]}')
    rowIndex[i].grid(column=0, row=i+1, sticky='news')

# siatka komórek edytowalnych
cells = [[None for i in range(columns)] for j in range(rows)]
for i in range(rows):
    for j in range(columns):
        cells[i][j] = tk.Entry(main_frame, bd=3)
        cells[i][j].grid(row=i+1, column=j+1,sticky='news')
#endregion

root.mainloop()