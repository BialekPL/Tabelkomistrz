
class Controller:
    def __init__(self, model, view):
        self.table = model
        self.view = view

    def changeTableSize(self, height, width):
        self.table.setHeight(height)
        self.table.setWidth(width)