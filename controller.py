
class Controller:
    def __init__(self, model, view):
        self.table = model
        self.view = view

    def changeTableSize(self, height, width):
        self.table.setHeight(height)
        self.table.setWidth(width)
        print(height, ' ', width)


    def getTable(self, tab):
        print(self.table.getContent())
        for i in range(len(self.table.getContent())):
            for j in range(len(self.table.getContent()[i])):
                self.table.getContent()[i][j].setValue(tab[i][j])
                print(self.table.getContent()[i][j].getValue())

    
    #def mergeCells(self, cells):
        