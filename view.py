import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Grid, messagebox
import string

from controller import Controller

class View():
    def __init__(self,master):
        self.root = master
        self.controller = None
        #region rozmiary itp.
        self.rows = 30      #liczba rzędów komórek
        self.columns = 15   #liczba kolumn komórek
        self.vis_rows = 15  #liczba widocznych rzędów komórek
        self.vis_cols = 7   #liczba widocznych kolumn komórek
        #endregion

        #region Utworzenie głównego okna
        self.root.geometry("950x510")       #rozmiar głównego okna (szer x wys)
        self.root.title("Tabelkomistrz")    #nazwa/tytuł okna głónego
        self.root.resizable(False, False)   #uniemożliwnie zmiany rozmiaru okna głównego
        self.usedFont = {'family': 'Segoe UI', 'size': 9, 'weight': 'normal', 'slant': 'italic', 'underline': 0, 'overstrike': 0}
        
        Grid.rowconfigure(self.root,index=0,weight=1)
        Grid.rowconfigure(self.root,index=1,weight=10)
        Grid.columnconfigure(self.root,index=0,weight=1)
        #endregion

        #region Utworzenie panelu z zakładkami
        self.tabsPanel = Notebook(self.root, height=55)
        self.tabsPanel.grid(row=0, sticky='we')
        #endregion

        #region Dodawanie nowych zakładek
        Grid.columnconfigure(self.tabsPanel, index=0, weight=1)
        Grid.rowconfigure(self.tabsPanel, index=0, weight=1)

        self.tabBasic = tk.Frame(self.tabsPanel, height=30)
        self.tabEdit = tk.Frame(self.tabsPanel, height=30)
        self.tabImpExp = tk.Frame(self.tabsPanel, height=30)

        self.tabBasic.grid(row=0, column=0, sticky='news')
        self.tabEdit.grid(row=0, column=0, sticky='news')
        self.tabImpExp.grid(row=0, column=0)

        self.tabsPanel.add(self.tabBasic, text='Podstawowe')
        self.tabsPanel.add(self.tabEdit, text='Edytuj')
        self.tabsPanel.add(self.tabImpExp, text='Import/Eksport')
        #endregion

        #region Zawartość zakładki "Podstawowe"
        Grid.columnconfigure(self.tabBasic, index=0, weight=0)
        Grid.columnconfigure(self.tabBasic, index=1, weight=0)
        Grid.columnconfigure(self.tabBasic, index=2, weight=0)
        Grid.columnconfigure(self.tabBasic, index=3, weight=0)
        Grid.columnconfigure(self.tabBasic, index=4, weight=0)
        Grid.columnconfigure(self.tabBasic, index=5, weight=1)
        Grid.columnconfigure(self.tabBasic, index=6, weight=7)
        Grid.rowconfigure(self.tabBasic, index=0, weight=1)

        self.basicLdim = tk.Label(self.tabBasic, text='Wymiary tabeli: ')
        self.basicLdim.configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold'))
        self.basicLdim.grid(row=0, column=0,sticky=tk.W)

        self.basicLr = tk.Label(self.tabBasic,text="L. wierszy:")
        self.basicLr.grid(row=0, column=1,sticky=tk.W)
        self.basicSr = tk.Spinbox(self.tabBasic, from_=1, to_=50, width=5)
        self.basicSr.grid(row=0, column=2,sticky=tk.W)

        self.basicLc = tk.Label(self.tabBasic,text="L. kolumn:")
        self.basicLc.grid(row=0, column=3,sticky=tk.W)
        self.basicSc = tk.Spinbox(self.tabBasic, from_=1, to_=21, width=5)
        self.basicSc.grid(row=0, column=4,sticky=tk.W)

        self.basicBchange = tk.Button(self.tabBasic, text="Zmień", command = lambda: self.basicSizeButton())
        self.basicBchange.grid(row=0, column=5)

        self.basicBtemplate = tk.Button(self.tabBasic, text="Załaduj szablon")
        self.basicBtemplate.grid(row=0,column=6,sticky=tk.E)
        #endregion

        #region Zawartość zakładki "Edytuj"
        Grid.columnconfigure(self.tabEdit, index=0, weight=0)
        Grid.columnconfigure(self.tabEdit, index=1, weight=0)
        Grid.columnconfigure(self.tabEdit, index=2, weight=1)
        Grid.columnconfigure(self.tabEdit, index=3, weight=0)
        Grid.columnconfigure(self.tabEdit, index=4, weight=0)
        Grid.columnconfigure(self.tabEdit, index=5, weight=1)
        Grid.columnconfigure(self.tabEdit, index=6, weight=0)
        Grid.columnconfigure(self.tabEdit, index=7, weight=0)
        Grid.columnconfigure(self.tabEdit, index=8, weight=0)
        Grid.rowconfigure(self.tabEdit, index=0, weight=1)

        self.editLmerge = tk.Label(self.tabEdit,text='Scal komórki:')
        self.editLmerge.grid(row=0, column=0,sticky=tk.W)

        self.editEmerge = tk.Entry(self.tabEdit)
        self.editEmerge.grid(row=0, column=1,sticky=tk.W)

        self.editBmerge = tk.Button(self.tabEdit,text="Scal",command=lambda: self.mergeCells())
        self.editBmerge.grid(row=0, column=2,sticky=tk.W)

        self.editLdev = tk.Label(self.tabEdit,text='Rozdziel komórki:')
        self.editLdev.grid(row=0, column=3,sticky=tk.W)

        self.editEdev = tk.Entry(self.tabEdit)
        self.editEdev.grid(row=0, column=4,sticky=tk.W)

        self.editBdev = tk.Button(self.tabEdit, text="Rozdziel")
        self.editBdev.grid(row=0, column=5,sticky=tk.W)

        self.editBb = tk.Button(self.tabEdit, text="B")
        self.editBb.configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold'))
        self.editBb.grid(row=0, column=6,sticky=tk.E)

        self.editBi = tk.Button(self.tabEdit, text="I")
        self.editBi.configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'italic'))
        self.editBi.grid(row=0, column=7,sticky=tk.E)

        self.editBu = tk.Button(self.tabEdit,text="U")
        self.editBu.configure(underline=0)
        self.editBu.grid(row=0, column=8,sticky=tk.E)
        #endregion

        #region Zawartość zakładki "Import/Eksport"
        Grid.columnconfigure(self.tabImpExp, index=0, weight=0)
        Grid.columnconfigure(self.tabImpExp, index=1, weight=1)
        Grid.columnconfigure(self.tabImpExp, index=2, weight=1)
        Grid.columnconfigure(self.tabImpExp, index=3, weight=0)
        Grid.rowconfigure(self.tabImpExp, index=0, weight=1)

        self.impexpLimp = tk.Label(self.tabImpExp, text="Eksport do LaTeX: ")
        self.impexpLimp.grid(row=0, column=0,sticky=tk.W)
        self.impexpBimp = tk.Button(self.tabImpExp, text="Eksportuj")
        self.impexpBimp.grid(row=0, column=1,sticky=tk.W)

        self.impexpLexp = tk.Label(self.tabImpExp, text="Import tabeli z LaTeX: ")
        self.impexpLexp.grid(row=0, column=2,sticky=tk.E)
        self.impexpBexp = tk.Button(self.tabImpExp, text="Importuj")
        self.impexpBexp.grid(row=0, column=3,sticky=tk.E)
        #endregion

        #region Siatka z komórkami
        self.mainFrame = self.createCellFrame()
        self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
        #endregion
    
        #region Funkcja - tworzenie siatki komórek
    def createCellFrame(self):
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)

        self.mainCanvas = tk.Canvas(self.mainFrame)
        self.mainCanvas.grid(row=0, column=0)

        self.mainSvertical = tk.Scrollbar(self.mainFrame, orient='vertical', command=self.mainCanvas.yview)
        self.mainSvertical.grid(row=0,column=1,sticky='ns')
        self.mainCanvas.configure(yscrollcommand=self.mainSvertical.set)

        self.mainShorizontal = tk.Scrollbar(self.mainFrame, orient='horizontal', command=self.mainCanvas.xview)
        self.mainShorizontal.grid(row=1, column=0, sticky='ew')
        self.mainCanvas.configure(xscrollcommand=self.mainShorizontal.set)

        # listy indexów komórek wyświetlane nad siatką i po lewej stronie siatki
        self.cellFrame = tk.Frame(self.mainCanvas)

        rowIndex = [i for i in range(0,self.rows,1)]
        columnIndex = list(string.ascii_uppercase)
        for i in range(self.columns):
            columnIndex[i] = tk.Label(self.cellFrame, text=f'{columnIndex[i]}', width=17)
            columnIndex[i].grid(row=0, column=i+1, sticky='news')

        for i in range(self.rows):
            rowIndex[i] = tk.Label(self.cellFrame, text=f'{rowIndex[i]}')
            rowIndex[i].grid(column=0, row=i+1, sticky='news')

        # siatka komórek edytowalnych
        self.cells = [["" for i in range(self.columns)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                self.cells[i][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                self.cells[i][j].grid(row=i+1, column=j+1,sticky='news')

        self.mainCanvas.create_window((0,0), window=self.cellFrame, anchor='nw')
        self.cellFrame.update_idletasks()
        bbox=self.mainCanvas.bbox('all')

        # w,h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int(127 * self.vis_cols), int(25 * self.vis_rows)
        self.mainCanvas.configure(scrollregion=bbox, width=dw, height=dh)

        return self.mainFrame
    #endregion

    #region Funkcja - zminana rozmiaru siatki
    def basicSizeButton(self):
        res = messagebox.askyesno('Zmiana rozmiaru tabeli','Ta operacja usunie dotychczasowe zawartości komórek i ich formatowanie. Czy na pewno chcesz kontynuować?')
        if res == True:
            self.columns = int(self.basicSc.get())
            self.rows = int(self.basicSr.get())
            self.mainFrame = self.createCellFrame()
            self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
            self.controller.changeTableSize(int(self.basicSr.get()), int(self.basicSc.get()))
    # endregion

    #region Funkcja - scalanie komórek
    def mergeCells(self):
        print('mergeCells button')
        indexStr = self.editEmerge.get().split(',')
        indexStr = [i.upper() for i in indexStr]
        message = self.controller.mergeCells(indexStr)
        if message == 0:
            tk.messagebox.showerror("Błąd", "Komórki wpisane w złym formacie, lub nie sąsiadują ze sobą")



        #text = self.editEmerge.get().split(',')
        #text = [i.upper() for i in text]
        #for i in text:
        #     print("scalane komórki: ",i[0]," ",int(i[1]))
        #sprawdzić czy poprawnie wpisane komórki

        #sprawdzić czy komórki mogą być scalone

        #sprawdzić czy są scalane rzędami czy kolumnami

        #łącznie komórek w wierszu
        # self.cells[0][4] = tk.Text(self.cellFrame,width=15,height=1)
        # self.cells[0][4].grid(row=1, column=5, columnspan=2, sticky='news')
        
        #łączenie komórek w kolumnie
        # self.cells[0][1] = tk.Text(self.cellFrame,width=15,height=1)
        # self.cells[0][1].grid(row=1, column=2, rowspan=2, sticky='news')

    #endregion

    def setController(self, controller):
        self.controller = controller

    def callback(self, *args):
        '''
        Daje znać o zmianie tekstu w komórce
        '''
        self.controller.getTable(self.returnTable())

    def returnTable(self):
        '''
        Funkcja zwracająca tabelkę
        '''
        table = []
        for i in range(self.rows):
            tmp=[]
            for j in range(self.columns):
                tmp.append(self.cells[i][j].get())
            table.append(tmp)
        return table
