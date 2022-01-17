import copy

class Controller:
    def __init__(self, model, view, export):
        self.table = model
        self.view = view
        self.export = export
        self.table.setHeight(self.view.rows)
        self.table.setWidth(self.view.columns)

    def changeTableSize(self, height, width):
        self.table.setHeight(height)
        self.table.setWidth(width)
        print(height, ' ', width)


    def setTable(self, tab):
        print(self.table.getContent())
        for i in range(len(self.table.getContent())):
            for j in range(len(self.table.getContent()[i])):
                self.table.getContent()[i][j].setValue(tab[i][j])
                self.table.nullIfMerged()
                print(self.table.getContent()[i][j].getValue())


    def mergeCells(self, indexStr):
        #sprawdzanie czy komórki istnieją
        message = self.table.mergeCells(indexStr)
        return message

    def getMerged(self):
        return self.table.getMergedCells()

    def getContent(self):
        return self.table.getContent()

    def dividing(self, index):
        self.table.divideCells(index)
        print(self.getMerged())
        return self.getMerged()
    
    def exportLatex(self):
        print(self.table.getMergedCells())
        print([cell.getIndex() for i in range(len(self.table.getContent())) for cell in self.table.getContent()[i]])
        tableToExport = copy.copy(self.table)
        return self.export.generateCode(tableToExport)

    def setStyle(self, styleStr,i , j):
        self.table.setStyle(styleStr, i, j)

    def getStyle(self, i, j):
        return self.table.getCellStyle(i,j)