import copy

class Cell:
    '''
    Klasa odzwierciedlająca komórki z których stworzona jest tabela zawiera:
    - wartość w komórce
    - pozycja komórki
    - index komórki
    - style komórki
    '''
    def __init__(self, value, position, index):
        self.__value = value
        self.__position = position
        self.__index = index
        self.__styles = {'bold':0, 'cursive':0, 'underlined':0, 'left-justified':0, 'right-justified':0, 'center-justified':0 }

    def getValue(self):
        return self.__value
    
    def getPosition(self):
        return self.__position

    def getIndex(self):
        return self.__index

    def getStyles(self):
        return self.__styles

    def setValue(self, x):
        self.__value = x

    def setPosition(self, x):
        self.__position = x

    def setIndex(self, x):
        self.__index=x

    def setStyle(self, key):
        if self.__styles[key] == 1:
            self.__styles[key] = 0
        else:
            self.__styles[key] = 1

    def resetStyles(self):
        self.__styles = {'bold':0, 'cursive':0, 'underlined':0, 'left-justified':0, 'right-justified':0, 'center-justified':0 }

class Table:
    '''
    Klasa odzwierciedlająca tabele, składającą się
    z obiektów Cell i zawierająca informacje o rozmiarze
    (kolumny i wiersze), informacje o scalonych komórkach
    '''
    def __init__(self, height, width):
        try:
            if width<26 and isinstance(width, int) == True and isinstance(height, int) == True:
                self.__height = height
                self.__width = width 
                self.__content = []
                self.__mergedCells = []

                alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                for i in range(height):
                    tmp = []
                    for j in range(width):
                        if i == 0:
                            position = j
                        else:
                            position = width * i + j
                        tmp.append(Cell('', position, alphabet[j]+str(i)))
                    self.__content.append(tmp)
            else:
                raise ValueError
        except ValueError:
            print("Width and height should be integer and width < 27")
    
    def getHeight(self):
        return self.__height

    def getWidth(self):
        return self.__width

    def getContent(self):
        return self.__content
    
    def getMergedCells(self):
        return self.__mergedCells

    def setHeight(self, x):
        self.__height = x
        self.__init__(self.__height, self.__width)

    def setWidth(self, x):
        self.__width = x
        self.__init__(self.__height, self.__width)

    def setMergedCells(self, x):
        self.__mergedCells = x 

    def mergeCells(self, indexStr):
        '''
        Metoda służąca do scalania komórek podanych jako string np.'A1, B1', 'A1, A2', 'A1, B1, A2, B2'
        '''
        try:
            cellsIndexes = [cell.getIndex() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            for ind in indexStr:
                if ind not in cellsIndexes:
                    raise ValueError

            positions = []
            cellsPos = [cell.getPosition() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            for i in range(len(cellsIndexes)):
                if cellsIndexes[i] in indexStr:
                    positions.append(cellsPos[i])

            positions = sorted(positions)
            #scalanie poziome
            if positions not in self.__mergedCells:
                if positions == [positions[0] + i for i in range(len(positions))]:
                    if len(positions)<=self.__width:
                        self.__mergedCells.append(positions)
                        self.nullIfMerged()
                        return 1
                #scalanie pionowo
                elif positions == [positions[0] + self.__width * i for i in range(len(positions))]:
                    self.__mergedCells.append(positions)
                    self.nullIfMerged()
                    return 1
                #blokowe scalanie
                for i in range(len(positions)):
                    if i!=0:
                        if len(positions)%i==0:
                            tmp = []
                            for j in range(i):
                                tmp.append(positions[j])
                            size = len(tmp)
                            it = 0
                            while size < len(positions): 
                                tmp.append(tmp[it]+self.__width)
                                it = it + 1
                                size = size + 1
                            if sorted(tmp) == positions:
                                self.__mergedCells.append(positions)
                                self.nullIfMerged()
                                return i
            else: return 0
        except ValueError:
            print('Zły format indeksów/komórki nie da się rozdzielić')
            return 0

    def divideCells(self, index):
        '''
        Metoda do dzielenia komórek
        position - pozycja komórki którą rozdzielamy 
        '''
        try:
            cellsIndexes = [cell.getIndex() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            for i in range(len(cellsIndexes)):
                if cellsIndexes[i] == index:
                    position = i
            if index not in cellsIndexes:
                raise ValueError
            for row in self.__mergedCells:
                if position in row:
                    self.__mergedCells.remove(row)
        except ValueError:
            print('Zły index')

    def nullIfMerged(self):
        '''
        Metoda ustawiająca scalone komórki oprócz pierwszej na wartosć ''
        '''
        for positions in self.getMergedCells():
            for row in range(len(self.__content)):
                for cell in self.__content[row]:
                    if cell.getPosition() in positions and cell.getPosition() != positions[0]:                        
                        cell.setValue('')
                        cell.resetStyles()
                

    def setStyle(self, key, i, j):
        '''
        Metoda ustawiająca style
        '''
        self.__content[i][j].setStyle(key)

    def getCellStyle(self, i, j):
        return self.__content[i][j].getStyles()