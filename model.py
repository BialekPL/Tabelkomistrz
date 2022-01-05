class Cell:
    '''
    Klasa odzwierciedlająca komórki zawiera indeks
    póki co zawiera tylko wartość pozycje i to czy jest scalona
    mergedWith - lista zawierająca pozycje komórek z którymi owa komórka jest scalona
    gettery/settery
    '''
    def __init__(self, value, position, index):
        self.__value = value
        self.__position = position
        self.__index = index #indeks typu A1, B5, nie chce usuwać pozycji bo łatwiej się z nich korzysta np przy mergowaniu 
        self.__mergedWith = []
        self.__styles = {'bold':0, 'cursive':0, 'underlined':0, 'left-justified':0, 'right-justified':0, 'center-justified':0 }

    def getValue(self):
        return self.__value
    
    def getPosition(self):
        return self.__position

    def getIndex(self):
        return self.__index

    def getMergedWith(self):
        return self.__mergedWith

    def getStyles(self):
        return self.__styles

    def setValue(self, x):
        self.__value = x

    def setPosition(self, x):
        self.__position = x

    def setIndex(self, x):
        self.__index=x

    def setStyle(self, key): #key to byłby string, value 1 lub 0 
        if self.__styles[key] == 1:
            self.__styles[key] = 0
        else:
            self.__styles[key] = 1

#wsm tabela mogłaby być singletonem ale aż tak dużo sie u nas nie dzieje więc nwm czy jest większy sens :v
class Table:
    '''
    Klasa odzwierciedlająca tabele, składającą się
    z obiektów Cell i zawierająca informacje o rozmiarze
    (kolumny i wiersze), informacje o scalonych komórkach
    idk czy to potrzebne ;_;)...
    mergedCells - to bd lista list chyba... lub lepiej żeby po pozycjach leciec idk ;_;
    gettery, settery
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
                        tmp.append(Cell(None, position, alphabet[j]+str(i)))
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

    def setMergedCells(self, x): # jak import bd robiony to sie przyda a narazie to raczej nie bardzo
        self.__mergedCells = x 

    def mergeCells(self, indexStr):
        '''
        Dodajemy LISTE z pozycjami scalonych komórek,
        potem najlepiej jakby w widoku była rozciągnięta jakby pierwsza komórka
        egzampul:
        ________________
        |  |  |  |  |  | wiersz
        ________________
        |        |  |  | wiersz z scalonymi 3 komórkami a tak naperawde pierwszą rozciągniętą na tamte dwie

        egzampul 2:
        ____
        |  | jest sobie taka kolumna dwu komórkowa
        ---
        |  |
        ----
        ____ kolumna z scalonymi komórkami 
        |  |
        |  |
        ----
        x D
        '''
        try:
            cellsIndexes = [cell.getIndex() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            print(cellsIndexes)
            for ind in indexStr:
                if ind not in cellsIndexes:
                    raise ValueError

            positions = []
            cellsPos = [cell.getPosition() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            for i in range(len(cellsIndexes)):
                if cellsIndexes[i] in indexStr:
                    positions.append(cellsPos[i])
            print('Pozycje',positions)

            positions = sorted(positions)
            if positions == [positions[0] + i for i in range(len(positions))]:
                if len(positions)<=self.__width:
                    print('Pierwszy warunek działa')
                    self.__mergedCells.append(positions)
            elif positions == [positions[0] + self.__width * i for i in range(len(positions))]:
                print('Drugi warunek działa')
                self.__mergedCells.append(positions)
            else: return 0

            self.nullIfMerged()
        except ValueError:
            print('Zły format indeksów/komórki nie da się rozdzielić')
            return 0

    def divideCells(self, index):
        '''
        Służy do dzielenia komórek
        position - pozycja komórki którą rozdzielamy 
        '''
        try:
            cellsIndexes = [cell.getIndex() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
            cellsPos = [cell.getPosition() for i in range(len(self.getContent())) for cell in self.getContent()[i]]
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
        for positions in self.getMergedCells():
            for row in range(len(self.__content)):
                for cell in self.__content[row]:
                    if cell.getPosition() in positions and cell.getPosition() != positions[0]:                        
                        cell.setValue('')




#Jakieś podstawowe testy żeby zobaczyć czy to wgl bangla
table = Table(3, 3)
table.mergeCells(['A1', 'B1'])
table.mergeCells(['A2', 'B2'])
#print(table.getMergedCells())
#print(table.getContent()[0][2].setValue(6))
#print([cell.getIndex() for i in range(len(table.getContent())) for cell in table.getContent()[i]])
#table.divideCells('A1')