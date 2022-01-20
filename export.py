from model import Table

'''
to do:
- scalanie blokowe(2-3h) 
- dodac do scalania wertykalnego "cline"(max 1h) - zrobione(jednak 3h -_-)
'''


class Export:
    def __init__(self):
        self.header = ''
        self.body = ''
        self.ending = ''
        self.basicSigns = {'open': "{", 'close': "}", 'tab': "    ", '2tab': "        ", 'enter': '\n',
                           'newCellWithSpace': ' & ', 'newLine': '\\\\', 'hline': '\\hline', 'cline': '\\cline'}
        self.basicCommnads = {'pack': '\\usepackage', 'begin': '\\begin', 'end': '\\end', 'table': 'tabular',
                              'col': 'c|', 'cen': 'center', 'multi': '\\multicolumn', 'multiRow': '\\multirow',
                              'toLeft':'l|',
                              'toRight': 'r|'}
        self.deafultPackages = ['multirow']
        self.cellStyles = {'underlined': "\\ul", 'cursive': "\\textit", 'bold': '\\textbf'}
        self.skip = 0  # jesli jest zero nie pomija kolumny w danym wierszu(testowo dodane do scalania horyzontalnego)

    def generateMultiCol(self, targetCells, content):
        cellBody = ''
        justification = self.justificationCheck(content)
        cellsMerged = 1
        if len(targetCells) > 1:
            cellsMerged = len(targetCells)

        valueOfCell = content.getValue()
        if self.checkAnyStyle(content):
            valueOfCell = self.genereteCellContentWithStyle(content)

        cellBody += "{}{}{}{}".format(self.basicCommnads['multi'], self.basicSigns['open'],
                                      cellsMerged, self.basicSigns['close'])

        cellBody += "{}{}{}".format(self.basicSigns['open'], justification,
                                    self.basicSigns['close'])

        cellBody += "{}{}{}".format(self.basicSigns['open'], valueOfCell,
                                    self.basicSigns['close'])
        return cellBody

    def generateMultiRow(self, targetCells, content):
        cellBody = ''
        justification = self.justificationCheck(content)
        cellsMerged = targetCells

        valueOfCell = content.getValue()
        if self.checkAnyStyle(content):
            valueOfCell = self.genereteCellContentWithStyle(content)

        cellBody += "{}{}{}{}".format(self.basicCommnads['multiRow'], self.basicSigns['open'],
                                      cellsMerged, self.basicSigns['close'])

        cellBody += "{}{}{}".format(self.basicSigns['open'], "*", self.basicSigns['close'])

        cellBody += "{}{}{}".format(self.basicSigns['open'], valueOfCell,
                                    self.basicSigns['close'])

        return cellBody

    def generateMultiBox(self, targetCells, content):
        cellBody = ''
        # cellToMiss = []
        rowsToSkip = []  # <-nie wiadomo czy jest to tu potrzebne, zamist tego chyba mozna uzyc helperow, ktore sa nizej
        columnsToSkip = []
        # [0, 1, 2, 6, 7, 8, 12, 13, 14] przyklad z 6x6 scalenie trzech kolumn i trzech wierszy
        helperCol = 0
        helperRow = 1
        counter = 1
        # petla sprawdzajaca ile jest scalonych wierszy i ile jest scalonych kolumn
        for i in range(len(targetCells)):
            if targetCells[i] + 1 in targetCells:
                counter += 1
                if targetCells[i] + 1 == targetCells[-1]:
                    break
            else:
                helperCol = counter
                counter = 1
                helperRow += 1
                columnsToSkip.append(targetCells[i+1])  # zwraca pozycje w nastepnych wierszach ktore powinny zawierac, puste multicolumn

        rowsToSkip.append(helperRow)

        #columnsToSkip.append(helperCol)
        justification = self.justificationCheck(content)

        valueOfCell = content.getValue()
        if self.checkAnyStyle(content):
            valueOfCell = self.genereteCellContentWithStyle(content)

        cellBody += "{}{}{}{}".format(self.basicCommnads['multi'], self.basicSigns['open'],
                                      helperCol, self.basicSigns['close'])

        cellBody += "{}{}{}".format(self.basicSigns['open'], justification,
                                    self.basicSigns['close'])

        cellBody += "{}{}{}{}{}{}{}{}{}{}{}{}".format(self.basicSigns['open'], self.basicCommnads['multiRow'],
                                                      self.basicSigns['open'], helperRow, self.basicSigns['close'],
                                                      self.basicSigns['open'], "*", self.basicSigns['close'],
                                                      self.basicSigns['open'], valueOfCell, self.basicSigns['close'],
                                                      self.basicSigns['close'])

        return cellBody, helperRow, columnsToSkip, helperCol

    def justificationCheck(self, cellContent):  # sprawdzanie wyjustowania tekstu
        justification = '|c|'  # domyslnie bedzie po prostu centrowal
        if cellContent.getStyles()['left-justified']:
            justification = '|l|'
        if cellContent.getStyles()['right-justified']:
            justification = '|r|'
        return justification

    def checkAnyStyle(self, cellContent):
        result = False
        dictStyles = cellContent.getStyles()
        if dictStyles['bold'] == 1:
            result = True
            return result
        if dictStyles['cursive'] == 1:
            result = True
            return result
        if dictStyles['underlined'] == 1:
            result = True
            return result
        return result

    def genereteCellContentWithStyle(self, cellContent):
        cellBody = ''
        if cellContent.getStyles()['underlined'] == 1:
            cellBody += "{}{}".format(self.basicSigns['open'], self.cellStyles['underlined'])
            if cellContent.getStyles()['cursive'] == 0 and cellContent.getStyles()['bold'] == 0:
                cellBody += " {}{}".format(cellContent.getValue(), self.basicSigns['close'])
            elif cellContent.getStyles()['cursive'] == 0 and cellContent.getStyles()['bold'] == 1:
                cellBody += " {}{}{}{}{}".format(self.cellStyles['bold'], self.basicSigns['open'],
                                                 cellContent.getValue(), self.basicSigns['close'],
                                                 self.basicSigns['close'])
            elif cellContent.getStyles()['cursive'] == 1 and cellContent.getStyles()['bold'] == 0:
                cellBody += " {}{}{}{}{}".format(self.cellStyles['cursive'], self.basicSigns['open'],
                                                 cellContent.getValue(), self.basicSigns['close'],
                                                 self.basicSigns['close'])
            else:
                cellBody += " {}{}{}{}{}{}{}{}".format(self.cellStyles['cursive'], self.basicSigns['open'],
                                                       self.cellStyles['bold'], self.basicSigns['open'],
                                                       cellContent.getValue(), self.basicSigns['close'],
                                                       self.basicSigns['close'], self.basicSigns['close'])
        else:
            if cellContent.getStyles()['cursive'] == 1 and cellContent.getStyles()['bold'] == 1:
                cellBody += "{}{}{}{}{}{}{}".format(self.cellStyles['cursive'], self.basicSigns['open'],
                                                    self.cellStyles['bold'], self.basicSigns['open'],
                                                    cellContent.getValue(), self.basicSigns['close'],
                                                    self.basicSigns['close'])
            elif cellContent.getStyles()['cursive'] == 1 and cellContent.getStyles()['bold'] == 0:
                cellBody += "{}{}{}{}".format(self.cellStyles['cursive'], self.basicSigns['open'],
                                              cellContent.getValue(), self.basicSigns['close'])
            else:
                cellBody += "{}{}{}{}".format(self.cellStyles['bold'], self.basicSigns['open'],
                                              cellContent.getValue(), self.basicSigns['close'])

        return cellBody

    def howMerged(self, mergedCells, height, width):
        '''
        Funkcja sluzy do sprawdzania jakie sa pierwsze pozycje komorek, ktore zostaly scalone i w jaki sposob
        :param mergedCells: wszystkie scalone komorki
        :param height: wysokosc tabeli
        :param width: szerokosc tabeli
        :return: zwraca listy pierwszych pozycji komorek ktore zostaly scalone. Dokladniej zwraca 3 listy,
        ktore odpowiadaja za to jak zostaly dane komorki scalone
        '''
        firstPosVertMerged = []
        firstPosHoriMerged = []
        firstPosBoxMerged = []
        for i in range(len(mergedCells)):
            if (mergedCells[i][0] + width) in mergedCells[i]:
                if (mergedCells[i][0] + 1) in mergedCells[i]:
                    firstPosBoxMerged.append(mergedCells[i][0])
                else:
                    firstPosVertMerged.append(mergedCells[i][0])
            else:
                firstPosHoriMerged.append(mergedCells[i][0])
        return firstPosVertMerged, firstPosHoriMerged, firstPosBoxMerged

    def hasOnlyHorizontally(self, table, height, width):
        firstPosMergedCells = []  # pozycje pierwszych komorek, ktore sa scalone
        mergedCells = table.getMergedCells()
        for i in range(len(mergedCells)):
            firstPosMergedCells.append(table.getMergedCells()[i][0])
        print(firstPosMergedCells)

        for line in range(height):
            targetCells = []  # zmienna pomocnicza wyznaczajaca obecnie scalane komorki
            for column in range(width):
                position = table.getContent()[line][column].getPosition()  # pozycja komorki
                if column == width - 1:
                    if targetCells:
                        targetCells.pop()
                        self.body += "{} {}".format(self.basicSigns['hline'], self.basicSigns['enter'])
                        continue
                    else:
                        valueOfCell = table.getContent()[line][column].getValue()
                        if self.checkAnyStyle(table.getContent()[line][column]):
                            valueOfCell = self.genereteCellContentWithStyle(table.getContent()[line][column])

                        self.body += "{} {}{}{}{}".format(valueOfCell,
                                                          self.basicSigns['newLine'], self.basicSigns['enter'],
                                                          self.basicSigns['hline'],
                                                          self.basicSigns['enter'])
                else:
                    if position in firstPosMergedCells:
                        for i in mergedCells:
                            if position in i:
                                targetCells = i
                        mergedCells.remove(targetCells)
                        cellContent = self.generateMultiCol(targetCells, table.getContent()[line][column])
                        self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])
                        targetCells.pop()
                    else:
                        if targetCells:
                            targetCells.pop()
                            self.body += self.basicSigns['tab']
                            continue
                        else:
                            valueOfCell = table.getContent()[line][column].getValue()
                            if self.checkAnyStyle(table.getContent()[line][column]):
                                valueOfCell = self.genereteCellContentWithStyle(table.getContent()[line][column])

                            self.body += "{} {} ".format(valueOfCell, self.basicSigns['newCellWithSpace'])

    def generateCLine(self, clineCounter, clineHelper, width):
        cline = ''
        positionHelper = [x+1 for x in range(width)]
        for i in range(len(clineHelper)):
            for x in range(len(positionHelper)):
                if positionHelper[x] in clineHelper[i]:
                    positionHelper[x] = 0

        last_position = positionHelper[0]
        first_to_write = positionHelper[0]
        last_to_write = positionHelper[0]
        for i in range(len(positionHelper)):
            position_now = positionHelper[i]
            if i == 0:
                if position_now == 0:
                    continue
            elif i == len(positionHelper) - 1:
                if position_now == 0:
                    if last_position == 0:
                        continue
                    else:
                        cline += "{}{}{}{}{}{}{}".format(self.basicSigns['cline'], self.basicSigns['open'],
                                                         first_to_write, "-", last_to_write, self.basicSigns['close'],
                                                         self.basicSigns['tab'])
                else:
                    if last_position == 0:
                        first_to_write = position_now
                        last_to_write = position_now
                        cline += "{}{}{}{}{}{}{}".format(self.basicSigns['cline'], self.basicSigns['open'],
                                                         first_to_write, "-", last_to_write, self.basicSigns['close'],
                                                         self.basicSigns['tab'])
                    else:
                        last_to_write = position_now
                        cline += "{}{}{}{}{}{}{}".format(self.basicSigns['cline'], self.basicSigns['open'],
                                                         first_to_write, "-", last_to_write, self.basicSigns['close'],
                                                         self.basicSigns['tab'])

            else:
                if position_now == 0:
                    if last_position == 0:
                        continue
                    else:
                        cline += "{}{}{}{}{}{}{}".format(self.basicSigns['cline'], self.basicSigns['open'],
                                                         first_to_write, "-", last_to_write, self.basicSigns['close'],
                                                         self.basicSigns['tab'])
                else:
                    if last_position == 0:
                        first_to_write = position_now
                        last_to_write = position_now
                    else:
                        last_to_write = position_now
            last_position = positionHelper[i]

        #print(len(clineCounter))
        toPopCounter = 0
        for i in range(len(clineCounter)):
            if clineCounter[i] == 2:
                toPopCounter += 1
            else:
                clineCounter[i] -= 1
        if toPopCounter > 0:
            for i in range(toPopCounter):
                clineHelper.pop(0)
                clineCounter.pop(0)
                toPopCounter -= 1

        return cline, clineCounter, clineHelper

    def addHeader(self, table, packages):
        '''
        Dodawanie paczki z tabelami, zliczanie ile kolumn i ich układów
        najpierw sprawdzanie dla każdej komórki jej układu: od lewej, od prawej, centered,
        Przykład:
        usepackage()
        begin{tabular}{|c|c|c|c|}
        '''

        '''
        to do:
        - dodac zabezpieczenia
        - dodac scalanie blokowe
        '''

        width = table.getWidth()
        columns = '|'

        if packages is None:
            for package in self.deafultPackages:
                self.header += "{}{}{}{}".format(self.basicCommnads['pack'], self.basicSigns['open'],
                                                 package, self.basicSigns['close'])
                self.header += '\n'
        else:
            for package in packages:
                self.header += "{}{}{}{}".format(self.basicCommnads['pack'], self.basicSigns['open'],
                                                 package, self.basicSigns['close'])
                self.header += '\n'

        for i in range(width):  # zliczenie kolumn
            columns += (self.basicCommnads['col'])

        '''
        dodanie dodatkowych opcji oraz rozpoczecie tabeli z podaniem odpowiedniej ilosci kolumn
        '''
        accessories = "{}{}{}{}{}".format(self.basicCommnads['begin'], self.basicSigns['open'],
                                          self.basicCommnads['cen'], self.basicSigns['close'], self.basicSigns['enter'])

        endHeader = "{}{}{}{}{}{}{}{}".format(self.basicCommnads['begin'], self.basicSigns['open'],
                                              self.basicCommnads['table'], self.basicSigns['close'],
                                              self.basicSigns['open'], columns, self.basicSigns['close'],
                                              self.basicSigns['enter'])

        if accessories == "":
            self.header += endHeader
            self.header += self.basicSigns['hline'] + " " + self.basicSigns['enter']

        else:
            self.header += accessories
            self.header += endHeader
            self.header += self.basicSigns['hline'] + " " + self.basicSigns['enter']

    def addToBody(self, table):
        '''
        Ciało tabeli, czyli główna funkcja. Sprawdza czy komórki są scalone itd, po wierszach znaki nawych lini
        Dodaje kolejne komórki do ciała tabeli, dodaje hline itp., sprawdza style
        '''

        height = table.getHeight()
        width = table.getWidth()

        if table.getMergedCells():
            mergedCells = table.getMergedCells()
            firstPosVertMerged, firstPosHoriMerged, firstPosBoxMerged = self.howMerged(mergedCells, height, width)
            if firstPosBoxMerged:
                #print("OK")
                verticalyMerged = []
                for i in range(len(mergedCells)):
                    if len(mergedCells[i]) > width and len(mergedCells[i]) > height:
                        continue
                    else:
                        if (mergedCells[i][0] + width) in mergedCells[i]:
                            if (mergedCells[i][0] + 1) in mergedCells[i]:
                                continue
                            else:
                                verticalyMerged.append(mergedCells[i])
                verticalyTargets = []
                boxTargets = []
                clineHelper = []
                clineCounter = []
                firstColumnsToSkipInNextRows = []
                #rowSkipper = []
                #rowsToSkipHelper = []
                colSkipper = []

                for line in range(height):
                    targetCellHorizontally = []
                    for column in range(width):
                        position = table.getContent()[line][column].getPosition()
                        if column == width - 1:
                            if position in firstPosVertMerged:  # dla pierwszej pozycji scalonej wertykalnie
                                cellsMerged = 1
                                for i in verticalyMerged:
                                    if position in i:
                                        verticalyTargets.append(i)
                                        verticalyMerged.remove(i)
                                        cellsMerged = len(i)
                                clineHelper.append([column + 1])
                                clineCounter.append(cellsMerged)
                                cellContent = self.generateMultiRow(cellsMerged, table.getContent()[line][column])
                                rowSign = self.basicSigns['hline']
                                if clineCounter:
                                    rowSign, clineCounter, clineHelper = self.generateCLine(clineCounter, clineHelper,
                                                                                            width)
                                    self.body += "{} {}{}{}{}".format(cellContent, self.basicSigns['newLine'],
                                                                      self.basicSigns['enter'], rowSign,
                                                                      self.basicSigns['enter'])
                                else:
                                    self.body += "{} {}{}{}{}".format(cellContent, self.basicSigns['newLine'],
                                                                      self.basicSigns['enter'], rowSign,
                                                                      self.basicSigns['enter'])
                                for merged in verticalyTargets:
                                    if position in merged:
                                        merged.remove(position)
                            else:
                                if targetCellHorizontally:
                                    targetCellHorizontally.pop()
                                    self.body += "{} {}".format(self.basicSigns['hline'], self.basicSigns['enter'])
                                    continue
                                else:
                                    if boxTargets:
                                        skip = False
                                        for merged in boxTargets:
                                            if position in merged:
                                                merged.remove(position)
                                                # TU BYLY WPROWADZONE ZMIANY
                                                rowSign = self.basicSigns['hline']
                                                if clineCounter:
                                                    rowSign, clineCounter, clineHelper = self.generateCLine(
                                                        clineCounter,
                                                        clineHelper,
                                                        width)
                                                    self.body += "{} {}".format(rowSign, self.basicSigns['enter'])
                                                else:
                                                    self.body += "{} {}".format(rowSign, self.basicSigns['enter'])
                                                skip = True
                                                break
                                        if skip:
                                            continue
                                        else:
                                            if verticalyTargets:
                                                added = False
                                                for i in verticalyTargets:
                                                    if position in i:
                                                        rowSign = self.basicSigns['hline']
                                                        if clineCounter:
                                                            rowSign, clineCounter, clineHelper = self.generateCLine(
                                                                clineCounter,
                                                                clineHelper,
                                                                width)
                                                            self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                            self.basicSigns['enter'],
                                                                                            rowSign,
                                                                                            self.basicSigns['enter'])
                                                        else:
                                                            self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                            self.basicSigns['enter'],
                                                                                            rowSign,
                                                                                            self.basicSigns['enter'])
                                                        i.remove(position)
                                                        added = True
                                                if added:
                                                    continue
                                                else:
                                                    valueOfCell = table.getContent()[line][column].getValue()
                                                    if self.checkAnyStyle(table.getContent()[line][column]):
                                                        valueOfCell = self.genereteCellContentWithStyle(
                                                            table.getContent()[line][column])

                                                    rowSign = self.basicSigns['hline']

                                                    if clineCounter:
                                                        rowSign, clineCounter, clineHelper = self.generateCLine(
                                                            clineCounter,
                                                            clineHelper,
                                                            width)
                                                        self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                          self.basicSigns['newLine'],
                                                                                          self.basicSigns['enter'],
                                                                                          rowSign,
                                                                                          self.basicSigns['enter'])
                                                    else:
                                                        self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                          self.basicSigns['newLine'],
                                                                                          self.basicSigns['enter'],
                                                                                          rowSign,
                                                                                          self.basicSigns['enter'])

                                            else:
                                                valueOfCell = table.getContent()[line][column].getValue()
                                                if self.checkAnyStyle(table.getContent()[line][column]):
                                                    valueOfCell = self.genereteCellContentWithStyle(
                                                        table.getContent()[line][column])

                                                rowSign = self.basicSigns['hline']

                                                if clineCounter:
                                                    rowSign, clineCounter, clineHelper = self.generateCLine(
                                                        clineCounter,
                                                        clineHelper,
                                                        width)
                                                    self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                      self.basicSigns['newLine'],
                                                                                      self.basicSigns['enter'],
                                                                                      rowSign,
                                                                                      self.basicSigns['enter'])
                                                else:
                                                    self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                      self.basicSigns['newLine'],
                                                                                      self.basicSigns['enter'],
                                                                                      rowSign,
                                                                                      self.basicSigns['enter'])

                                                # self.body += "{} {}{}{}{}".format(valueOfCell,
                                                #                                   self.basicSigns['newLine'],
                                                #                                   self.basicSigns['enter'],
                                                #                                   self.basicSigns['hline'],
                                                #                                   self.basicSigns['enter'])
                                    elif verticalyTargets:
                                        added = False
                                        for i in verticalyTargets:
                                            if position in i:
                                                rowSign = self.basicSigns['hline']
                                                if clineCounter:
                                                    rowSign, clineCounter, clineHelper = self.generateCLine(
                                                        clineCounter,
                                                        clineHelper,
                                                        width)
                                                    self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                    self.basicSigns['enter'],
                                                                                    rowSign,
                                                                                    self.basicSigns['enter'])
                                                else:
                                                    self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                    self.basicSigns['enter'],
                                                                                    rowSign,
                                                                                    self.basicSigns['enter'])
                                                i.remove(position)
                                                added = True
                                        if added:
                                            continue
                                        else:
                                            valueOfCell = table.getContent()[line][column].getValue()
                                            if self.checkAnyStyle(table.getContent()[line][column]):
                                                valueOfCell = self.genereteCellContentWithStyle(
                                                    table.getContent()[line][column])

                                            rowSign = self.basicSigns['hline']

                                            if clineCounter:
                                                rowSign, clineCounter, clineHelper = self.generateCLine(clineCounter,
                                                                                                        clineHelper,
                                                                                                        width)
                                                self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                  self.basicSigns['newLine'],
                                                                                  self.basicSigns['enter'], rowSign,
                                                                                  self.basicSigns['enter'])
                                            else:
                                                self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                  self.basicSigns['newLine'],
                                                                                  self.basicSigns['enter'], rowSign,
                                                                                  self.basicSigns['enter'])

                        else:
                            if position in firstPosBoxMerged:
                                cellsBoxMerged = []
                                for i in mergedCells:
                                    if position in i:
                                        cellsBoxMerged = i
                                        boxTargets.append(i)
                                cellContent, rowSkipper, helperToAdd, helperToAdd2 = self.generateMultiBox(
                                    cellsBoxMerged, table.getContent()[line][column])
                                clineCounter.append(rowSkipper)
                                clineHelper.append([column + 1 + i for i in range(helperToAdd2)])
                                firstColumnsToSkipInNextRows.append(helperToAdd)
                                colSkipper.append(helperToAdd2)
                                self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])

                                for merged in boxTargets:
                                    if position in merged:
                                        merged.remove(position)

                                for merged in boxTargets:
                                    for cell in firstColumnsToSkipInNextRows:
                                        for i in range(len(cell)):
                                            if cell[i] in merged:
                                                merged.remove(cell[i])

                            elif position in firstPosVertMerged:
                                cellsMerged = 1
                                for i in verticalyMerged:
                                    if position in i:
                                        verticalyTargets.append(i)
                                        verticalyMerged.remove(i)
                                        cellsMerged = len(i)
                                clineHelper.append([column + 1])
                                clineCounter.append(cellsMerged)
                                cellContent = self.generateMultiRow(cellsMerged, table.getContent()[line][column])
                                self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])
                                for merged in verticalyTargets:
                                    if position in merged:
                                        merged.remove(position)

                            elif position in firstPosHoriMerged:
                                for i in mergedCells:
                                    if position in i:
                                        targetCellHorizontally = i
                                mergedCells.remove(targetCellHorizontally)
                                cellContent = self.generateMultiCol(targetCellHorizontally,
                                                                    table.getContent()[line][column])
                                self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])
                                targetCellHorizontally.pop()
                            else:
                                if targetCellHorizontally:
                                    targetCellHorizontally.pop()
                                    self.body += self.basicSigns['tab']
                                    continue
                                else:
                                    if firstColumnsToSkipInNextRows:
                                        added = False
                                        toPop = False
                                        indicator = 0
                                        for i in range(len(firstColumnsToSkipInNextRows)):
                                            if position in firstColumnsToSkipInNextRows[i]:
                                                colToSkip = colSkipper[i]
                                                self.body += "{}{}{}{}".format(self.basicCommnads['multi'],
                                                                               self.basicSigns['open'],
                                                                               colToSkip, self.basicSigns['close'])
                                                self.body += "{}{}{}".format(self.basicSigns['open'],
                                                                             "|c|", self.basicSigns['close'])

                                                self.body += "{}{}{}".format(self.basicSigns['open'],
                                                                           self.basicSigns['close'],
                                                                           self.basicSigns['newCellWithSpace'])

                                                if len(firstColumnsToSkipInNextRows[i]) > 1:
                                                    firstColumnsToSkipInNextRows[i].remove(position)
                                                else:
                                                    indicator = i
                                                    colSkipper.pop(0)
                                                    toPop = True
                                                added = True
                                        if added:
                                            if toPop:
                                                firstColumnsToSkipInNextRows.pop(indicator)
                                            continue
                                        else:
                                            skip = False
                                            for merged in boxTargets:
                                                if position in merged:
                                                    merged.remove(position)
                                                    self.body += self.basicSigns['tab']
                                                    skip = True
                                                    break
                                            if skip:
                                                continue
                                            else:
                                                if targetCellHorizontally:  # ewentualny blad
                                                    targetCellHorizontally.pop()
                                                    self.body += self.basicSigns['tab']
                                                    continue
                                                else:
                                                    if verticalyTargets:
                                                        added = False
                                                        for i in verticalyTargets:
                                                            if position in i:
                                                                self.body += "{}{}".format(self.basicSigns['tab'],
                                                                                           self.basicSigns[
                                                                                               'newCellWithSpace'])
                                                                i.remove(position)
                                                                added = True
                                                        if added:
                                                            continue
                                                        else:
                                                            valueOfCell = table.getContent()[line][column].getValue()
                                                            if self.checkAnyStyle(table.getContent()[line][column]):
                                                                valueOfCell = self.genereteCellContentWithStyle(
                                                                    table.getContent()[line][column])

                                                            self.body += "{} {} ".format(valueOfCell,
                                                                                         self.basicSigns[
                                                                                             'newCellWithSpace'])

                                                    else:
                                                        valueOfCell = table.getContent()[line][column].getValue()
                                                        if self.checkAnyStyle(table.getContent()[line][column]):
                                                            valueOfCell = self.genereteCellContentWithStyle(
                                                                table.getContent()[line][column])

                                                        self.body += "{} {} ".format(valueOfCell, self.basicSigns[
                                                            'newCellWithSpace'])
                                    else:
                                        if targetCellHorizontally:  # ewentualny blad
                                            targetCellHorizontally.pop()
                                            self.body += self.basicSigns['tab']
                                            continue
                                        else:
                                            if boxTargets:
                                                skip = False
                                                for merged in boxTargets:
                                                    if position in merged:
                                                        merged.remove(position)
                                                        self.body += self.basicSigns['tab']
                                                        skip = True
                                                        break
                                                if skip:
                                                    continue
                                                else:
                                                    if verticalyTargets:
                                                        added = False
                                                        for i in verticalyTargets:
                                                            if position in i:
                                                                self.body += "{}{}".format(self.basicSigns['tab'],
                                                                                           self.basicSigns[
                                                                                               'newCellWithSpace'])
                                                                i.remove(position)
                                                                added = True
                                                        if added:
                                                            continue
                                                        else:
                                                            valueOfCell = table.getContent()[line][column].getValue()
                                                            if self.checkAnyStyle(table.getContent()[line][column]):
                                                                valueOfCell = self.genereteCellContentWithStyle(
                                                                    table.getContent()[line][column])

                                                            self.body += "{} {} ".format(valueOfCell,
                                                                                         self.basicSigns[
                                                                                             'newCellWithSpace'])

                                                    else:
                                                        valueOfCell = table.getContent()[line][column].getValue()
                                                        if self.checkAnyStyle(table.getContent()[line][column]):
                                                            valueOfCell = self.genereteCellContentWithStyle(
                                                                table.getContent()[line][column])

                                                        self.body += "{} {} ".format(valueOfCell, self.basicSigns[
                                                            'newCellWithSpace'])

                                            elif verticalyTargets:
                                                added = False
                                                for i in verticalyTargets:
                                                    if position in i:
                                                        self.body += "{}{}".format(self.basicSigns['tab'],
                                                                                   self.basicSigns['newCellWithSpace'])
                                                        i.remove(position)
                                                        added = True
                                                if added:
                                                    continue
                                                else:
                                                    valueOfCell = table.getContent()[line][column].getValue()
                                                    if self.checkAnyStyle(table.getContent()[line][column]):
                                                        valueOfCell = self.genereteCellContentWithStyle(
                                                            table.getContent()[line][column])

                                                    self.body += "{} {} ".format(valueOfCell,
                                                                                 self.basicSigns['newCellWithSpace'])

                                            else:
                                                valueOfCell = table.getContent()[line][column].getValue()
                                                if self.checkAnyStyle(table.getContent()[line][column]):
                                                    valueOfCell = self.genereteCellContentWithStyle(
                                                        table.getContent()[line][column])

                                                self.body += "{} {} ".format(valueOfCell,
                                                                             self.basicSigns['newCellWithSpace'])
                print(clineHelper)
                print("OK")

            else:
                if firstPosVertMerged:
                    verticalyMerged = []
                    for i in range(len(mergedCells)):
                        if mergedCells[i][1] - mergedCells[i][0] == width:
                            verticalyMerged.append(mergedCells[i])

                    verticalyTargets = []
                    clineHelper = []
                    ''' clineHelper - podaje pozycje(ale w poszczegolnym wierszu, nie ogolna, czyli w zakresie petli)
                        scalonych komorek'''
                    clineCounter = []
                    for line in range(height):
                        # clineHelper = []
                        targetCellHorizontally = []  # zmienna pomocnicza wyznaczajaca obecnie scalane komorki
                        for column in range(width):
                            position = table.getContent()[line][column].getPosition()
                            if column == width - 1:
                                if position in firstPosVertMerged:  # dla pierwszej pozycji scalonej wertykalnie
                                    cellsMerged = 1
                                    for i in verticalyMerged:
                                        if position in i:
                                            verticalyTargets.append(i)
                                            verticalyMerged.remove(i)
                                            cellsMerged = len(i)
                                    clineHelper.append([column + 1])
                                    clineCounter.append(cellsMerged)
                                    cellContent = self.generateMultiRow(cellsMerged, table.getContent()[line][column])
                                    rowSign = self.basicSigns['hline']
                                    if clineCounter:
                                        rowSign, clineCounter, clineHelper = self.generateCLine(clineCounter,
                                                                                                clineHelper, width)
                                        self.body += "{} {}{}{}{}".format(cellContent, self.basicSigns['newLine'],
                                                                          self.basicSigns['enter'], rowSign,
                                                                          self.basicSigns['enter'])
                                    else:
                                        self.body += "{} {}{}{}{}".format(cellContent, self.basicSigns['newLine'],
                                                                          self.basicSigns['enter'], rowSign,
                                                                          self.basicSigns['enter'])
                                    for merged in verticalyTargets:
                                        if position in merged:
                                            merged.remove(position)
                                else:
                                    if targetCellHorizontally:
                                        targetCellHorizontally.pop()
                                        self.body += "{} {}".format(self.basicSigns['hline'], self.basicSigns['enter'])
                                        continue
                                    else:
                                        if verticalyTargets:
                                            added = False
                                            for i in verticalyTargets:
                                                if position in i:
                                                    rowSign = self.basicSigns['hline']
                                                    if clineCounter:
                                                        rowSign, clineCounter, clineHelper = self.generateCLine(
                                                            clineCounter,
                                                            clineHelper,
                                                            width)
                                                        self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                        self.basicSigns['enter'],
                                                                                        rowSign,
                                                                                        self.basicSigns['enter'])
                                                    else:
                                                        self.body += " {}{}{}{}".format(self.basicSigns['newLine'],
                                                                                        self.basicSigns['enter'],
                                                                                        rowSign,
                                                                                        self.basicSigns['enter'])
                                                    i.remove(position)
                                                    added = True
                                            if added:
                                                continue
                                            else:
                                                valueOfCell = table.getContent()[line][column].getValue()
                                                if self.checkAnyStyle(table.getContent()[line][column]):
                                                    valueOfCell = self.genereteCellContentWithStyle(
                                                        table.getContent()[line][column])

                                                rowSign = self.basicSigns['hline']

                                                if clineCounter:
                                                    rowSign, clineCounter, clineHelper = self.generateCLine(
                                                        clineCounter,
                                                        clineHelper,
                                                        width)
                                                    self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                      self.basicSigns['newLine'],
                                                                                      self.basicSigns['enter'], rowSign,
                                                                                      self.basicSigns['enter'])
                                                else:
                                                    self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                                      self.basicSigns['newLine'],
                                                                                      self.basicSigns['enter'], rowSign,
                                                                                      self.basicSigns['enter'])

                                        else:
                                            valueOfCell = table.getContent()[line][column].getValue()
                                            if self.checkAnyStyle(table.getContent()[line][column]):
                                                valueOfCell = self.genereteCellContentWithStyle(
                                                    table.getContent()[line][column])

                                            self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                              self.basicSigns['newLine'],
                                                                              self.basicSigns['enter'],
                                                                              self.basicSigns['hline'],
                                                                              self.basicSigns['enter'])

                            else:
                                if position in firstPosVertMerged:  # dla pierwszej pozycji scalonej wertykalnie
                                    cellsMerged = 1
                                    for i in verticalyMerged:
                                        if position in i:
                                            verticalyTargets.append(i)
                                            verticalyMerged.remove(i)
                                            cellsMerged = len(i)
                                    clineHelper.append([column + 1])
                                    clineCounter.append(cellsMerged)
                                    cellContent = self.generateMultiRow(cellsMerged, table.getContent()[line][column])
                                    self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])
                                    for merged in verticalyTargets:
                                        if position in merged:
                                            merged.remove(position)
                                elif position in firstPosHoriMerged:  # dla pierwszej pozycji scalonej horyzontalnie
                                    for i in mergedCells:
                                        if position in i:
                                            targetCellHorizontally = i
                                    mergedCells.remove(targetCellHorizontally)
                                    cellContent = self.generateMultiCol(targetCellHorizontally,
                                                                        table.getContent()[line][column])
                                    self.body += "{} {}".format(cellContent, self.basicSigns['newCellWithSpace'])
                                    targetCellHorizontally.pop()
                                else:
                                    if targetCellHorizontally:  # ewentualny blad
                                        targetCellHorizontally.pop()
                                        self.body += self.basicSigns['tab']
                                        continue
                                    else:
                                        if verticalyTargets:
                                            added = False
                                            for i in verticalyTargets:
                                                if position in i:
                                                    self.body += "{}{}".format(self.basicSigns['tab'],
                                                                               self.basicSigns['newCellWithSpace'])
                                                    i.remove(position)
                                                    added = True
                                            if added:
                                                continue
                                            else:
                                                valueOfCell = table.getContent()[line][column].getValue()
                                                if self.checkAnyStyle(table.getContent()[line][column]):
                                                    valueOfCell = self.genereteCellContentWithStyle(
                                                        table.getContent()[line][column])

                                                self.body += "{} {} ".format(valueOfCell,
                                                                             self.basicSigns['newCellWithSpace'])

                                        else:
                                            valueOfCell = table.getContent()[line][column].getValue()
                                            if self.checkAnyStyle(table.getContent()[line][column]):
                                                valueOfCell = self.genereteCellContentWithStyle(
                                                    table.getContent()[line][column])

                                            self.body += "{} {} ".format(valueOfCell,
                                                                         self.basicSigns['newCellWithSpace'])

                else:
                    self.hasOnlyHorizontally(table, height, width)
        else:
            '''
            to jest na razie taki standard przy generowaniu tabeli, bez zadnych wyjustowanych tekstow w komorkach 
            oraz bez zadnych scalonych komorek. Bedzie to zmienione tak, zeby kazda
            komorka byla sprawdzona pod wzgledem wyjustowania.
            '''
            for line in range(height):
                for column in range(width):
                    valueOfCell = table.getContent()[line][column].getValue()
                    if self.checkAnyStyle(table.getContent()[line][column]):
                        valueOfCell = self.genereteCellContentWithStyle(table.getContent()[line][column])
                    if line == height - 1:
                        if column == width - 1:
                            self.body += "{} {}{}{}{}".format(valueOfCell,
                                                              self.basicSigns['newLine'], self.basicSigns['enter'],
                                                              self.basicSigns['hline'],
                                                              self.basicSigns['enter'])
                        else:
                            self.body += "{} {} ".format(valueOfCell,
                                                         self.basicSigns['newCellWithSpace'])
                    else:
                        if column == width - 1:
                            self.body += "{} {} {} {}".format(valueOfCell,
                                                           self.basicSigns['newLine'], self.basicSigns['hline'],
                                                           self.basicSigns['enter'])
                        else:
                            self.body += "{} {} ".format(valueOfCell,
                                                         self.basicSigns['newCellWithSpace'])




    def addEnding(self):
        '''
        Zamyka całość
        '''
        self.ending += "{}{}{}{}{}".format(self.basicCommnads['end'], self.basicSigns['open'],
                                           self.basicCommnads['table'], self.basicSigns['close'],
                                           self.basicSigns['enter'])
        self.ending += "{}{}{}{}{}".format(self.basicCommnads['end'], self.basicSigns['open'],
                                           self.basicCommnads['cen'], self.basicSigns['close'],
                                           self.basicSigns['enter'])

    def generateCode(self, table):
        self.addHeader(table, None)
        self.addToBody(table)
        self.addEnding()
        with open('eksport.txt', 'wb') as f:
            f.write(self.header.encode('UTF8'))
            f.write(self.body.encode('UTF8'))
            f.write(self.ending.encode('UTF8'))
        # wyczszczenie stringow
        self.header = ""
        self.body = ""
        self.ending = ""


test_table = Table(6, 6)
# test_table.getContent()[0][0].setStyle('right-justified')
# test_table.getContent()[0][0].setStyle('bold')
# test_table.getContent()[0][0].setStyle('cursive')
# test_table.getContent()[3][3].setValue("jakis przykladowy tekst")
# test_table.getContent()[3][3].setStyle('bold')
# test_table.mergeCells(['F4', 'F5'])
# test_table.mergeCells(['E4', 'E5'])
# test_table.mergeCells(['F3', 'F4', 'F5'])
# test_table.mergeCells(['A0', 'A1'])
# test_table.mergeCells(['A5', 'B5'])
# test_table.mergeCells(['B4', 'B5'])
# test_table.mergeCells(['A0', 'A1', 'A2', 'A3'])
# test_table.mergeCells(['C2', 'D2', 'E2'])
# test_table.mergeCells(['C5', 'D5', 'E5', 'F5'])
# test_table.mergeCells(['C0', 'D0', 'C1', 'D1', 'C2', 'D2'])
# test_table.mergeCells(['A0', 'B0', 'C0', 'D0', 'E0'])
# test_table.mergeCells(['B1', 'C1'])
# test_table.mergeCells(['E0', 'F0', 'E1', 'F1'])
# print(test_table.getWidth())
# print(test_table.getHeight())


print("_________________")

#test = [0, 1, 2, 6, 7, 8, 12, 13, 14]  # <-przyklad z 6x6 scalenie trzech kolumn i trzech wierszy


# test_table.getContent()[0][0].setStyle('right-justified')
# test_table.getContent()[0][0].setStyle('bold')
# test_table.getContent()[0][0].setStyle('cursive')

# test_table.getContent()[3][3].setValue("jakis przykladowy tekst")
# test_table.getContent()[3][3].setStyle('bold')

export_test = Export()
mergedCells = test_table.getMergedCells()
height = test_table.getHeight()
width = test_table.getWidth()
firstPosVertMerged, firstPosHoriMerged, firstPosBoxMerged = export_test.howMerged(mergedCells, height, width)
#print(mergedCells)

# result = export_test.verticalyMerged(test_table.getMergedCells(), test_table.getWidth())
# print(result)
export_test.generateCode(test_table)
#print(firstPosVertMerged, firstPosHoriMerged, firstPosBoxMerged)

#cellBody, rowsToSkip, columnsToSkip, cos = export_test.generateMultiBox(test, test_table.getContent()[0][0])
#print(cellBody)
#print(rowsToSkip)

# print(export_test.basicSigns['newLine'])
