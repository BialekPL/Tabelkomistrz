import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Grid
import string

#region rozmiary itp. 
rows = 30
columns = 15
vis_rows = 15
vis_cols = 7
#endregion

#region Funkcja - tworzenie siatki komórek
def createCellFrame(root, rows, columns, vis_rows, vis_cols):
    mainFrame = tk.Frame(root)
    mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)

    mainCanvas = tk.Canvas(mainFrame)
    mainCanvas.grid(row=0, column=0)

    mainSvertical = tk.Scrollbar(mainFrame, orient='vertical', command=mainCanvas.yview)
    mainSvertical.grid(row=0,column=1,sticky='ns')
    mainCanvas.configure(yscrollcommand=mainSvertical.set)

    mainShorizontal = tk.Scrollbar(mainFrame, orient='horizontal', command=mainCanvas.xview)
    mainShorizontal.grid(row=1, column=0, sticky='ew')
    mainCanvas.configure(xscrollcommand=mainShorizontal.set)

    # listy indexów komórek wyświetlane nad siatką i po lewej stronie siatki
    cellFrame = tk.Frame(mainCanvas)

    rowIndex = [i for i in range(0,rows,1)]
    columnIndex = list(string.ascii_uppercase)
    for i in range(columns):
        columnIndex[i] = tk.Label(cellFrame, text=f'{columnIndex[i]}', width=17)
        columnIndex[i].grid(row=0, column=i+1, sticky='news')

    for i in range(rows):
        rowIndex[i] = tk.Label(cellFrame, text=f'{rowIndex[i]}')
        rowIndex[i].grid(column=0, row=i+1, sticky='news')

    # siatka komórek edytowalnych
    cells = [["" for i in range(columns)] for j in range(rows)]
    for i in range(rows):
        for j in range(columns):
            cells[i][j] = tk.Text(cellFrame, width=15, height=1)
            cells[i][j].grid(row=i+1, column=j+1,sticky='news')

    mainCanvas.create_window((0,0), window=cellFrame, anchor='nw')
    cellFrame.update_idletasks()
    bbox=mainCanvas.bbox('all')

    # w,h = bbox[2]-bbox[1], bbox[3]-bbox[1]
    dw, dh = int(127 * vis_cols), int(25 * vis_rows)
    mainCanvas.configure(scrollregion=bbox, width=dw, height=dh)

    return mainFrame
#endregion

#region Funkcja - zminana rozmiaru siatki
def basicSizeButton():
    columns = int(basicSc.get())
    rows = int(basicSr.get())
    mainFrame = createCellFrame(root, rows, columns, vis_rows, vis_cols)
    mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
# endregion

#region Funkcja - scalanie komórek
def mergeCells():
    text = editEmerge.get().split(',')
    text = [i.upper() for i in text]
    for i in text:
        print("scalane komórki: ",i[0]," ",int(i[1]))
    
    #sprawdzić czy poprawnie wpisane komórki

    #sprawdzić czy komórki mogą być scalone

    #sprawdzić czy są scalane rzędami czy kolumnami

    #łącznie komórek w wierszu
    # cells[0][4] = tk.Text(cellFrame,width=15,height=1)
    # cells[0][4].grid(row=1, column=5, columnspan=2, sticky='news')
    
    #łączenie komórek w kolumnie
    # cells[0][1] = tk.Text(cellFrame,width=15,height=1)
    # cells[0][1].grid(row=1, column=2, rowspan=2, sticky='news')

#endregion

#region Utworzenie głównego okna
root = tk.Tk()
root.geometry("950x510")
root.title("Tabelkomistrz")
root.resizable(False, False)
usedFont = {'family': 'Segoe UI', 'size': 9, 'weight': 'normal', 'slant': 'italic', 'underline': 0, 'overstrike': 0}

Grid.rowconfigure(root,index=0,weight=1)
Grid.rowconfigure(root,index=1,weight=10)
Grid.columnconfigure(root,index=0,weight=1)
#endregion

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
basicSr = tk.Spinbox(tabBasic, from_=1, to_=50, width=5)
basicSr.grid(row=0, column=2,sticky=tk.W)

basicLc = tk.Label(tabBasic,text="L. kolumn:")
basicLc.grid(row=0, column=3,sticky=tk.W)
basicSc = tk.Spinbox(tabBasic, from_=1, to_=21, width=5)
basicSc.grid(row=0, column=4,sticky=tk.W)

basicBchange = tk.Button(tabBasic, text="Zmień", command = lambda: basicSizeButton())
basicBchange.grid(row=0, column=5)

basicBtemplate = tk.Button(tabBasic, text="Załaduj szablon")
basicBtemplate.grid(row=0,column=6,sticky=tk.E)
#endregion

#region Zawartość zakładki "Edytuj"
Grid.columnconfigure(tabEdit, index=0, weight=0.5)
Grid.columnconfigure(tabEdit, index=1, weight=0.5)
Grid.columnconfigure(tabEdit, index=2, weight=1)
Grid.columnconfigure(tabEdit, index=3, weight=0.5)
Grid.columnconfigure(tabEdit, index=4, weight=0.5)
Grid.columnconfigure(tabEdit, index=5, weight=1)
Grid.columnconfigure(tabEdit, index=6, weight=0.5)
Grid.columnconfigure(tabEdit, index=7, weight=0.5)
Grid.columnconfigure(tabEdit, index=8, weight=0.5)
Grid.rowconfigure(tabEdit, index=0, weight=1)

editLmerge = tk.Label(tabEdit,text='Scal komórki:')
editLmerge.grid(row=0, column=0,sticky=tk.W)

editEmerge = tk.Entry(tabEdit)
editEmerge.grid(row=0, column=1,sticky=tk.W)

editBmerge = tk.Button(tabEdit,text="Scal",command=lambda: mergeCells())
editBmerge.grid(row=0, column=2,sticky=tk.W)

editLdev = tk.Label(tabEdit,text='Rozdziel komórki:')
editLdev.grid(row=0, column=3,sticky=tk.W)

editEdev = tk.Entry(tabEdit)
editEdev.grid(row=0, column=4,sticky=tk.W)

editBdev = tk.Button(tabEdit, text="Rozdziel")
editBdev.grid(row=0, column=5,sticky=tk.W)

editBb = tk.Button(tabEdit, text="B")
editBb.configure(font=(f"{usedFont['family']}", usedFont['size'], 'bold'))
editBb.grid(row=0, column=6,sticky=tk.E)

editBi = tk.Button(tabEdit, text="I")
editBi.configure(font=(f"{usedFont['family']}", usedFont['size'], 'italic'))
editBi.grid(row=0, column=7,sticky=tk.E)

editBu = tk.Button(tabEdit,text="U")
editBu.configure(underline=0)
editBu.grid(row=0, column=8,sticky=tk.E)
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
mainFrame = createCellFrame(root, rows, columns, vis_rows, vis_cols)
mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
#endregion

root.mainloop()