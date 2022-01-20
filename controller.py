import copy

class Controller:
    def __init__(self, model, view, export):
        self.table = model
        self.view = view
        self.export = export
        self.table.setHeight(self.view.rows)
        self.table.setWidth(self.view.columns)

    def changeTableSize(self, height, width): 
        '''
        Metoda zmieniająca rozmiar tabeli.
        '''
        self.table.setHeight(height)
        self.table.setWidth(width)

    def setTable(self, tab): 
        '''
        Metoda ustawiająca komórki np. po aktualizacji widoku.
        '''
        for i in range(len(self.table.getContent())):
            for j in range(len(self.table.getContent()[i])):
                self.table.getContent()[i][j].setValue(tab[i][j])
                self.table.nullIfMerged()

    def mergeCells(self, indexStr): 
        '''
        Metoda scalająca komórki w modelu z widoku.
        '''
        message = self.table.mergeCells(indexStr)
        return message

    def getMerged(self):
        return self.table.getMergedCells()

    def getContent(self):
        return self.table.getContent()

    def dividing(self, index):
        '''
        Metoda dzieląca komórki w modelu
        '''
        self.table.divideCells(index)
        return self.getMerged()
    
    def exportLatex(self):
        '''
        Metoda eksportująca przy pomocy obiektu export.
        '''
        tableToExport = copy.copy(self.table)
        merged = copy.deepcopy(self.table.getMergedCells())
        self.export.generateCode(tableToExport)
        self.table.setMergedCells(merged)

    def setStyle(self, styleStr,i , j):
        '''
        Metoda ustawiająca styl w komórce tabeli
        '''
        self.table.setStyle(styleStr, i, j)

    def getStyle(self, i, j):
        return self.table.getCellStyle(i,j)