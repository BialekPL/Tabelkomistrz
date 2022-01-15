from model import Table

'''
to do:
- zabezpieczenia(1-2h)
- scalanie blokowe(2-3h)
- justowanie pojedynczych komorek, ktore nie sa scalone(15 min)
- dodac do scalania wertykalnego "cline"(max 1h)
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

        # pozycja w srodku bedzie potem zalezec od wyjustowania tekstu
        cellBody += "{}{}{}".format(self.basicSigns['open'], justification,
                                      self.basicSigns['close'])

        # pozycja z content.getValue bedzie potem zamieniona zeby przekazywala wartosc komorki wraz z pogrubieniem lub
        # czyms innym
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

    def howMerged(self, mergedCells, width):  # sprawdza ktore komorki sa scalone wertyklanie
        firstPosVertMerged = []
        firstPosHoriMerged = []
        for i in range(len(mergedCells)):
            if mergedCells[i][1] - mergedCells[i][0] == width:
                firstPosVertMerged.append(mergedCells[i][0])
            else:
                firstPosHoriMerged.append(mergedCells[i][0])
        return firstPosVertMerged, firstPosHoriMerged

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

    # def generateCLine(self, clines):  # to jest do zrobienia(max godzinka)
    #     cline = ''
    #     counter = len(clines)
    #     if counter > 1:
    #     if counter == 1:
    #         if len(clines[0]) > 2:
    #
    #
    #     return cline

    def addToBody(self, table):
        '''
        Ciało tabeli, czyli główna funkcja. Sprawdza czy komórki są scalone itd, po wierszach znaki nawych lini
        Dodaje kolejne komórki do ciała tabeli, dodaje hline itp., sprawdza style (można to robić za pomocą innej funkcji)
        '''

        height = table.getHeight()
        width = table.getWidth()

        if table.getMergedCells():
            mergedCells = table.getMergedCells()
            firstPosVertMerged, firstPosHoriMerged = self.howMerged(mergedCells, width)
            if firstPosVertMerged:
                verticalyMerged = []
                for i in range(len(mergedCells)):
                    if mergedCells[i][1] - mergedCells[i][0] == width:
                        verticalyMerged.append(mergedCells[i])

                verticalyTargets = []
                clineHelper = []
                for line in range(height):
                    #clineHelper = []
                    targetCellHorizontally = []  # zmienna pomocnicza wyznaczajaca obecnie scalane komorki
                    for column in range(width):
                        position = table.getContent()[line][column].getPosition()
                        if column == width - 1:
                            if position in firstPosVertMerged:  # dla pierwszej pozycji scalonej wertykalnie
                                cellsMerged = 1
                                for i in verticalyMerged:
                                    if position in i:
                                        verticalyTargets.append(i)
                                        clineHelper.append(i)
                                        verticalyMerged.remove(i)
                                        cellsMerged = len(i)
                                cellContent = self.generateMultiRow(cellsMerged, table.getContent()[line][column])
                                self.body += "{} {}".format(cellContent, self.basicSigns['newLine'],
                                                            self.basicSigns['enter'], self.basicSigns['hline'], # tu poprawic
                                                            self.basicSigns['enter'])
                                for merged in verticalyTargets:
                                    if position in merged:
                                        verticalyTargets.remove(position)
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

                                            self.body += "{} {}{}{}{}".format(valueOfCell,
                                                                              self.basicSigns['newLine'],
                                                                              self.basicSigns['enter'],
                                                                              self.basicSigns['hline'],
                                                                              # tu dodac cline, zamiast hline
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
                                        clineHelper.append(i)
                                        verticalyMerged.remove(i)
                                        cellsMerged = len(i)
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

                                        self.body += "{} {} ".format(valueOfCell, self.basicSigns['newCellWithSpace'])

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
        #print(self.header)
        #test_string = "working test"
        with open('test.txt', 'w') as f:
            f.write(self.header)
            f.write(self.body)
            f.write(self.ending)


test_table = Table(3, 3)
test_table.mergeCells(['A0', 'A1'])
#test_table.mergeCells(['A0', 'B0', 'C0', 'D0', 'E0', 'F0'])
test_table.mergeCells(['B1', 'C1'])
# print(test_table.getWidth())
# print(test_table.getHeight())


print("_________________")
#test_table.getContent()[0][0].setStyle('right-justified')
#test_table.getContent()[0][0].setStyle('bold')
#test_table.getContent()[0][0].setStyle('cursive')

#test_table.getContent()[3][3].setValue("jakis przykladowy tekst")
#test_table.getContent()[3][3].setStyle('bold')

export_test = Export()
#result = export_test.verticalyMerged(test_table.getMergedCells(), test_table.getWidth())
#print(result)
export_test.generateCode(test_table)
# print(export_test.basicSigns['newLine'])
