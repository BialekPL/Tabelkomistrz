import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Grid, PhotoImage, messagebox
import string
from controller import Controller
import datetime

class View():
    def __init__(self,master):
        self.root = master
        self.controller = None
        self.lastClickedi = None  #style
        self.lastClickedj = None
        p1 = PhotoImage(file = 'table.png')
        self.root.iconphoto(False, p1)
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
        self.usedFont = {'family': 'Segoe UI', 'size': 9, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0} #style
        #wieght: bold, normal
        #slant: italic, roman
        #underline: 1(underlined), 0(normal)

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
        self.tabsPanel.add(self.tabImpExp, text='Eksport')
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

        self.basicBtemplate = tk.Button(self.tabBasic, text="Załaduj szablon", command = lambda: self.basicLoadTemplate())
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

        self.editBdev = tk.Button(self.tabEdit, text="Rozdziel", command=lambda: self.divideCell())
        self.editBdev.grid(row=0, column=5,sticky=tk.W)

        self.editBb = tk.Button(self.tabEdit, text="B", command=lambda: self.setStyle('bold'))
        self.editBb.configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold'))
        self.editBb.grid(row=0, column=6,sticky=tk.E)

        self.editBi = tk.Button(self.tabEdit, text="I", command=lambda: self.setStyle('cursive'))
        self.editBi.configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'italic'))
        self.editBi.grid(row=0, column=7,sticky=tk.E)

        self.editBu = tk.Button(self.tabEdit,text="U", command=lambda: self.setStyle('underlined'))
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
        self.impexpBimp = tk.Button(self.tabImpExp, text="Eksportuj", command=lambda: self.controller.exportLatex())
        self.impexpBimp.grid(row=0, column=1,sticky=tk.W)
        #endregion

        #region Siatka z komórkami
        self.mainFrame = self.createCellFrame()
        self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
        #endregion
    
    def onClick(self, row, col):
        self.lastClickedi = row
        self.lastClickedj = col
        
    def setStyle(self, styleStr):
        self.controller.setStyle(styleStr, self.lastClickedi, self.lastClickedj)
        cellStyle = self.controller.getStyle(self.lastClickedi, self.lastClickedj)
        if cellStyle['bold']==1 and cellStyle['cursive']==0 and cellStyle['underlined']==0:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==1 and cellStyle['underlined']==0:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'italic'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==0 and cellStyle['underlined']==1:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'underline'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==1 and cellStyle['underlined']==1:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'italic', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==1 and cellStyle['underlined']==0:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'italic'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==0 and cellStyle['underlined']==1:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==1 and cellStyle['underlined']==1:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'italic', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==0 and cellStyle['underlined']==0:
            self.cells[self.lastClickedi][self.lastClickedj].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman'))
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
                self.cells[i][j].bind("<1>", lambda event, row=i, col=j: self.onClick(row,col)) #style!

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
        #merge w modelu
        indexStr = self.editEmerge.get().split(',')
        indexStr = [i.upper() for i in indexStr]
        if len(indexStr)>1:
            message = self.controller.mergeCells(indexStr)
            if message == 0:
                tk.messagebox.showerror("Błąd", "Komórki wpisane w złym formacie, lub nie sąsiadują ze sobą")
            else:
                self.merging(message)
        else:
            tk.messagebox.showerror("Błąd", "Komórki wpisane w złym formacie, lub nie sąsiadują ze sobą")
    #endregion

    def merging(self, mes):
        mergedCells = self.controller.getMerged()
        for merged in mergedCells:
            #sprawdzanie czy poziomo
            if merged == [merged[0] + i for i in range(len(merged))]:
                visible = merged[0]
                #scalanie pierwszego rzędu
                if (visible >= 0 and visible < self.columns):
                    content = self.controller.getContent()
                    sv = tk.StringVar()
                    sv.set(content[0][visible].getValue())
                    sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                    self.cells[0][visible] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                    self.cells[0][visible].grid(row=1, column=visible+1, columnspan=len(merged),sticky='news')
                    self.styling(0,visible)
                #reszta
                else:
                    content = self.controller.getContent()
                    sv = tk.StringVar()
                    #sprawdzanie rzędu
                    for i in range(self.rows):
                        if i*self.columns<=visible and visible<i*self.columns+self.columns:
                            content[i][visible%self.columns].getValue()
                            sv.set(content[i][visible%self.columns].getValue())
                            sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                            self.cells[i][visible%self.columns] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                            self.cells[i][visible%self.columns].grid(row=i+1, column=visible%self.columns+1, columnspan=len(merged),sticky='news')
                            self.styling(i,visible%self.columns)

            elif merged == [merged[0] + self.columns * i for i in range(len(merged))]:
                visible = merged[0]
                for i in range(self.rows):
                    if i*self.columns<=visible and visible<i*self.columns+self.columns:
                        content = self.controller.getContent()
                        sv = tk.StringVar()
                        sv.set(content[i][visible%self.columns].getValue())
                        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                        self.cells[i][visible%self.columns] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                        self.cells[i][visible%self.columns].grid(row=i+1, column=visible%self.columns+1, rowspan=len(merged),sticky='news')
                        self.styling(i,visible%self.columns)
            
            else:
                visible = merged[0]
                for i in range(self.rows):
                    if i*self.columns<=visible and visible<i*self.columns+self.columns:
                        content = self.controller.getContent()
                        sv = tk.StringVar()
                        sv.set(content[i][visible%self.columns].getValue())
                        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                        self.cells[i][visible%self.columns] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                        rowspanVal = int(len(merged)/mes)
                        colspanVal = mes
                        self.cells[i][visible%self.columns].grid(row=i+1, column=visible%self.columns+1, rowspan=rowspanVal, columnspan=colspanVal,sticky='news')
                        self.styling(i,visible%self.columns)

    def setController(self, controller):
        self.controller = controller

    def callback(self, *args):
        '''
        Daje znać o zmianie tekstu w komórce
        '''
        self.controller.setTable(self.returnTable())
       

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

    def divideCell(self):
        '''
        Funkcja służąca do dzielenia komórek.
        '''
        index = self.editEdev.get()
        if len(index) == 2:
            mergedCells = self.controller.dividing(index)
            self.setNotMerged(mergedCells)

    def setNotMerged(self, mergedCells):
        for i in range(self.rows):
            for j in range(self.columns):
                if i == 0:
                    position = j
                else:
                    position = self.columns * i + j
                if any(position in sub for sub in mergedCells)!=True:
                    content = self.controller.getContent()
                    sv = tk.StringVar()
                    sv.set(content[i][j].getValue())
                    sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                    self.cells[i][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                    self.cells[i][j].grid(row=i+1, column=j+1, columnspan=1, rowspan=1, sticky='news')
                    self.styling(i,j)
    
    def mergeTemplate(self, indexStr):
        indexStr = [i.upper() for i in indexStr]
        if len(indexStr)>1:
            message = self.controller.mergeCells(indexStr)
        else:
            tk.messagebox.showerror("Błąd", "Komórki wpisane w złym formacie, lub nie sąsiadują ze sobą")
        if message == 0:
            tk.messagebox.showerror("Błąd", "Komórki wpisane w złym formacie, lub nie sąsiadują ze sobą")
        self.merging(message)

    def basicLoadTemplate(self):    #funkcja ładująca szablony (cz.1)
        #nowe okienko z wyborem dostępnych szablonów
        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.title("Wybór szablonu")
        self.newWindow.geometry("600x250")
        self.newWindow.resizable(False, False)

        Grid.rowconfigure(self.newWindow,index=0,weight=1)
        Grid.rowconfigure(self.newWindow,index=1,weight=1)
        Grid.rowconfigure(self.newWindow,index=2,weight=1)
        Grid.rowconfigure(self.newWindow,index=3,weight=1)
        Grid.rowconfigure(self.newWindow,index=4,weight=1)
        Grid.rowconfigure(self.newWindow,index=5,weight=1)
        Grid.rowconfigure(self.newWindow,index=6,weight=1)
        Grid.rowconfigure(self.newWindow,index=7,weight=1)
        Grid.columnconfigure(self.newWindow,index=0,weight=1)

        windowLname = tk.Label(self.newWindow,text ="Wybierz szablon:")
        windowLname.configure(font=(f"{self.usedFont['family']}", 16, 'bold'))
        windowLname.grid(row=0)

        var = tk.StringVar()
        var.set('yearCal')

        windowR1 = tk.Radiobutton(self.newWindow, text="Kalendarz roczny ", variable=var, value='yearCal')
        windowR1.grid(row=1,sticky='w')

        windowR2 = tk.Radiobutton(self.newWindow, text="Kalendarz miesięczny (6 tygodni)", variable=var, value='monCal6')
        windowR2.grid(row=2,sticky='w')

        windowR3 = tk.Radiobutton(self.newWindow, text="Kalendarz miesięczny (5 tygodni)", variable=var, value='monCal5')
        windowR3.grid(row=3,sticky='w')

        windowR4 = tk.Radiobutton(self.newWindow, text="Kalendarz miesięczny (4 tygodnie)", variable=var, value='monCal4')
        windowR4.grid(row=4,sticky='w')

        windowR5 = tk.Radiobutton(self.newWindow, text="Kalendarz dzienny", variable=var, value='dayCal')
        windowR5.grid(row=5,sticky='w')

        windowBok = tk.Button(self.newWindow,text='Załaduj', command=lambda: self.newWindowButton(var))
        windowBok.grid(row=7,sticky='we')

    def newWindowButton(self,var): #funkcja ładująca szablony (cz.2)
        #pobranie zaznaczonej wartości i zamknięcie okienka 
        self.selectedRbutton = var.get()
        self.newWindow.destroy()

        #ładowanie wybranego szablonu
        if self.selectedRbutton=='yearCal':     #jeśli wybrano kalendarz roczny
            #utworzenie tabeli o odpowiednich wymiarach
            self.columns = 3
            self.rows = 13
            self.mainFrame = self.createCellFrame()
            self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
            self.controller.changeTableSize(int(self.rows), int(self.columns))

            #informacja dla modelu, które komórki są scalone
            lettersAC = list(string.ascii_uppercase)[:3]
            self.mergeTemplate([f'{i}0' for i in lettersAC])
            for i in range(2,12,3):
                for j in range(3):
                    self.mergeTemplate([f'{lettersAC[j]}{i}',f'{lettersAC[j]}{i+1}'])

            #wypełnienie tabeli i scalanie komórek
            sv = tk.StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
            sv.set(datetime.date.today().year)
            # self.cells[0][0] = tk.Entry(self.cellFrame,width=15, textvariable=sv, justify='center')
            self.cells[0][0] = tk.Entry(self.cellFrame,width=15, textvariable=sv)
            self.cells[0][0].grid(row=1, column=1, columnspan=4, sticky='news')

            monthNames = ['Styczeń', 'Luty', 'Marzec',
                        'Kwiecień', 'Maj', 'Czerwiec',
                        'Lipiec', 'Sierpień', 'Wrzesień',
                        'Październik', 'Listopad', 'Grudzień']
            iter = 0
            for i in range(1,12,3):
                for j in range(3):
                    sv = tk.StringVar()
                    sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                    # self.cells[i][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv, justify='center')
                    self.cells[i][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                    self.cells[i][j].grid(row=i+1, column=j+1, columnspan=1, sticky='news')
                    sv.set(monthNames[iter])

                    iter += 1
                    sv1 = tk.StringVar()
                    sv1.trace("w", lambda name, index, mode, sv1=sv1: self.callback(sv1))
                    self.cells[i+1][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv1)
                    self.cells[i+1][j].grid(row=i+2, column=j+1, columnspan=1, rowspan=2, sticky='news')

        #jeśli wybrano kalendarz miesięczny
        elif self.selectedRbutton=='monCal6' or self.selectedRbutton=='monCal5' or self.selectedRbutton=='monCal4':
            #określenie ilości tygodni w miesiącu
            nWeeks = self.selectedRbutton[-1:]

            #utworzenie tabeli o odpowiednich wymiarach
            self.columns = 7
            self.rows = int(nWeeks)*3+2 
            self.mainFrame = self.createCellFrame()
            self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
            self.controller.changeTableSize(int(self.rows), int(self.columns))

            #informacja dla modelu, które komórki są scalone
            lettersAG = list(string.ascii_uppercase)[:7]
            self.mergeTemplate([f'{i}0' for i in lettersAG])
            for i in range(3,3*int(nWeeks)+1,3):
                for j in range(0,7):
                    self.mergeTemplate([f'{lettersAG[j]}{i}',f'{lettersAG[j]}{i+1}'])

            #wypełnienie tabeli i scalanie komórek
            sv = tk.StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
            sv.set("NAZWA MIESIĄCA")
            # self.cells[0][0] = tk.Entry(self.cellFrame,width=15, textvariable=sv, justify='center')
            self.cells[0][0] = tk.Entry(self.cellFrame,width=15, textvariable=sv)
            self.cells[0][0].grid(row=1, column=1, columnspan=7, sticky='news')

            #uzupełnienie dni tygodnia
            dayNames = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
            for i in range(len(dayNames)):
                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                
                # self.cells[1][i] = tk.Entry(self.cellFrame,width=15, textvariable=sv, justify='center')
                self.cells[1][i] = tk.Entry(self.cellFrame,width=15, textvariable=sv)
                self.cells[1][i].grid(row=2, column=i+1, columnspan=1, sticky='news')
                sv.set(dayNames[i])

            #format komórek z dniami miesiąca
            for i in range(2,self.rows,3):
                for j in range(7):
                    sv1 = tk.StringVar()
                    sv1.trace("w", lambda name, index, mode, sv1=sv1: self.callback(sv1))
                    # self.cells[i][j] = tk.Entry(self.cellFrame, width=15, justify='right', textvariable=sv1)
                    self.cells[i][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv1)
                    self.cells[i][j].grid(row=i+1, column=j+1, columnspan=1, sticky='news')

                    sv2 = tk.StringVar()
                    sv2.trace("w", lambda name, index, mode, sv1=sv1: self.callback(sv2))
                    # self.cells[i+1][j] = tk.Entry(self.cellFrame, width=15, justify='left',textvariable=sv1)
                    self.cells[i+1][j] = tk.Entry(self.cellFrame, width=15, textvariable=sv2)
                    self.cells[i+1][j].grid(row=i+2, column=j+1, rowspan=2, sticky='news')

        elif self.selectedRbutton=='dayCal':    #jeśli wybrano kalendarz dzienny
            #utworzenie tabelki o odpowiednich rozmiarach
            self.columns = 6
            self.rows = 19
            self.mainFrame = self.createCellFrame()
            self.mainFrame.grid(row=1, column=0, sticky='news', pady = 10, padx = 10)
            self.controller.changeTableSize(int(self.rows), int(self.columns))

            #informacja dla modelu, które komórki są scalone
            self.mergeTemplate(['a0','b0','c0','d0','e0','f0'])
            for i in range(1,19):
                self.mergeTemplate([f'b{i}',f'c{i}',f'd{i}',f'e{i}',f'f{i}'])

            #wypełnienie tabeli i scalanie komórek
            monthNames = ['Styczeń', 'Luty', 'Marzec',
                        'Kwiecień', 'Maj', 'Czerwiec',
                        'Lipiec', 'Sierpień', 'Wrzesień',
                        'Październik', 'Listopad', 'Grudzień']
            sv = tk.StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
            dateToday = f"{datetime.date.today().day} {monthNames[int(datetime.date.today().month)-1]} {datetime.date.today().year}"
            sv.set(dateToday)
            # self.cells[0][0] = tk.Entry(self.cellFrame, width=15, textvariable=sv, justify='center')
            self.cells[0][0] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
            self.cells[0][0].grid(row=1, column=1, columnspan=6, sticky='news')

            #uzupełnienie godzin
            hourList = [f"{i}:00" for i in range(6,24)]
            for i in range(1,self.rows):
                #wpisanie godzin do odpowiednich komórek
                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
                # self.cells[i][0] = tk.Entry(self.cellFrame, width=15, textvariable=sv, justify='center')
                self.cells[i][0] = tk.Entry(self.cellFrame, width=15, textvariable=sv)
                self.cells[i][0].grid(row=i+1, column=1, columnspan=1, sticky='news')
                sv.set(hourList[i-1])

                #ustawienie odpowiedniej szerokości prawej kolumny
                sv1 = tk.StringVar()
                sv1.trace("w", lambda name, index, mode, sv1=sv1: self.callback(sv1))
                self.cells[i][1] = tk.Entry(self.cellFrame, width=15, textvariable=sv1)
                self.cells[i][1].grid(row=i+1, column=2, columnspan=5, sticky='news')

    def styling(self, i, j):
        cellStyle = self.controller.getStyle(i, j)
        if cellStyle['bold']==1 and cellStyle['cursive']==0 and cellStyle['underlined']==0:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==1 and cellStyle['underlined']==0:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'italic'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==0 and cellStyle['underlined']==1:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'underline'))
        elif cellStyle['bold']==1 and cellStyle['cursive']==1 and cellStyle['underlined']==1:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'bold', 'italic', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==1 and cellStyle['underlined']==0:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'italic'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==0 and cellStyle['underlined']==1:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==1 and cellStyle['underlined']==1:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman', 'italic', 'underline'))
        elif cellStyle['bold']==0 and cellStyle['cursive']==0 and cellStyle['underlined']==0:
            self.cells[i][j].configure(font=(f"{self.usedFont['family']}", self.usedFont['size'], 'roman'))