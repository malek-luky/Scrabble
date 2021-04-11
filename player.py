import base
import random
import copy
import itertools
import time


class Player(base.BasePlayer):

    def __init__(self, name, dictionary, board, bag, bigBagSize):
        base.BasePlayer.__init__(self, name, dictionary, board, bag, bigBagSize) #always keep this line and DON't change it
        self.text = "PrayForAustralia" #fill the name of your awesome player!
        #bellow you can define your own variables. Don't forget to use 'self.' to adress them correctly

    def move(self):
        wordlist = [frozenset()]
        one_letter = set() #souradnice kam lze dat pismeno
        value_list = list()
        row_list = list()
        col_list = list()
        letter_list = list()
        final_output = list()
        row_square_R = list()
        col_square_R = list()
        number_R = list()
        row_square_L = list()
        col_square_L = list()
        number_L = list()
        row_square_D = list()
        col_square_D = list()
        number_D = list()
        row_square_U = list()
        col_square_U = list()
        number_U = list()
        row_temp_list = list()
        col_temp_list = list()
        letter_temp_list = list()

        def one_letter_move(row,col):
            if self.isEmpty(row,col) is False:
                if row >0 and self.isEmpty(row-1,col) is True:
                    one_letter.add((row-1,col))
                if row <14 and self.isEmpty(row+1,col) is True:
                    one_letter.add((row+1,col))
                if col >0 and self.isEmpty(row,col-1) is True:
                    one_letter.add((row,col-1))
                if col <14 and self.isEmpty(row,col+1) is True:
                    one_letter.add((row,col+1))

        def value_row(row,col):
            i=0
            value = 0
            while (col+i)<15 and self.isEmpty(row,col+i) is False:
                value += self.cellValue(row, col+i) * self.letterValue(self.board[row][col+i])
                i+=1
            if i == 1:
                value = 0
            return value

        def value_col(row,col):
            i=0
            value = 0
            while (row+i)<15 and self.isEmpty(row+i,col) is False:
                value += self.cellValue(row+i, col) * self.letterValue(self.board[row+i][col])
                i+=1
            if i == 1:
                value = 0
            return value

        if self.tournament is False:

            for row in range (15):
                for col in range (15):
                    one_letter_move(row,col) #najde souradnice kam lze dat jedno pismeno

            for item in one_letter:
                row = item[0]
                col = item[1]

                for letter in set(self.bag):
                    self.board[row][col] = letter #polozim na desku pismeno kvuli pocitani value

                    #NAJDE SLOVO V RADKU
                    word1 = letter
                    i = 1 #nutno dat do vnejsiho scopu
                    for i in range(1,col+1):
                        if self.isEmpty(row, col-i) is False:
                            word1 = self.board[row][col-i] + word1
                        else:
                            break
                    if col-i == 0 and self.isEmpty(row, col-i) is False:
                                i+=1
                    for x in range(col+1,15):
                        if self.isEmpty(row, x) is False:
                            word1 = word1 + self.board[row][x]
                        else:
                            break

                    #NAJDE SLOVO VE SLOUPCI
                    word2 = letter
                    z = 1 #nutno dat do vnejsiho scopu
                    for z in range(1,row+1):
                        if self.isEmpty(row-z, col) is False:
                            word2 = self.board[row-z][col] + word2
                        else:
                            break
                    if row-z == 0 and self.isEmpty(row-z, col) is False:
                        z+=1
                    for y in range(row+1,15):
                        if self.isEmpty(y, col) is False:
                            word2 = word2 + self.board[y][col]
                        else:
                            break

                    #SPOCITA VALUE
                    if (len(word1) == 1 or word1 in self.dictionary) and (len(word2) == 1 or word2 in self.dictionary):
                        value1 = value_row(row, col-i+1)
                        value2 = value_col(row-z+1, col)
                        value_list.append(value1+value2)
                        row_list.append(row)
                        col_list.append(col)
                        letter_list.append(letter)
                    self.board[row][col] = "" #smazu pismeno

            #for i in range(len(value_list)):
                #print(row_list[i], col_list[i], letter_list[i], "-", value_list[i], "(index)", i)

            #NENASEL JSEM ZADNE SLOVO
            if len(value_list) == 0:
                seen = set()
                duplicates = set(x for x in self.bag if x in seen or seen.add(x))
                if len(duplicates) == 0:
                    if len(self.bag) == 0:
                        return None
                    else:
                        return ''.join(self.bag)
                else:
                    return ''.join(duplicates)

            #NASEL JSEM SLOVO
            else:
                maximum = 0
                for i in range (len(value_list)):
                    if value_list[i] > maximum:
                        index_list=list()
                        index_list.append(i)
                        maximum = value_list[i]
                    elif value_list[i] == maximum:
                        index_list.append(i)

                #NEJLEPE POLOZIM JENOPISMENNE MAXIMUM
                k = 1
                for index in index_list:
                    if type(row_list[index]) == int:
                        k = 0

                #POKUD NEEXISTUJE JEDNOPISMENNE, POLOZIM NEJKRATSI
                final_index=-1
                if k == 1:
                    for cislo,index in enumerate(index_list):
                        maxx = 100
                        if len(row_list[index]) < maxx:
                            maxx = len(row_list[index])
                            final_index = cislo
                    for i in range (len(row_list[final_index])):
                        final_output.append([row_list[index][i], col_list[index][i], letter_list[index][i]])
                    return final_output

                #ZKUSIME JEDNOPISMENNE
                else:
                    for index in index_list:
                        if type(row_list[index]) == int:
                            #TAH BEZ DOUBLU A TRIPLU
                            if ((row_list[index] >0 and self.cellValue(row_list[index]-1,col_list[index])== 1) and (row_list[index] <14 and self.cellValue(row_list[index]+1,col_list[index]) == 1)  and (col_list[index] >0 and self.cellValue(row_list[index],col_list[index]-1) == 1) and (col_list[index] <14 and self.cellValue(row_list[index],col_list[index]+1) == 1)):
                                return [[row_list[index],col_list[index],letter_list[index]]]
                            #POKUD NENAJDU JEDNOSPIMENNY TAH BEZ DOUBLE A TRIPLE POLI, ZKUSIM JEN DOBULE
                            elif ((row_list[index] >0 and self.cellValue(row_list[index]-1,col_list[index])<=2) and (row_list[index] <14 and self.cellValue(row_list[index]+1,col_list[index]) <=2)  and (col_list[index] >0 and self.cellValue(row_list[index],col_list[index]-1) <=2) and (col_list[index] <14 and self.cellValue(row_list[index],col_list[index]+1) <=2)):
                                return [[row_list[index],col_list[index],letter_list[index]]]

                #KDYZ NEVYJDE ANI TO, ZKUSIM COKOLI JEDNOPISMENNEHO
                for index in index_list:
                    if type(row_list[index]) == int:
                        return [[row_list[index],col_list[index],letter_list[index]]]

        if self.tournament is True:

            for row in range (15):
                for col in range (15):
                    one_letter_move(row,col) #najde souradnice kam lze dat jedno pismeno

                    #NAJDU VOLNE OBDELNIKY
                    if self.isEmpty(row,col) is False:

                        #RIGHT
                        i=1
                        temp=0
                        while (self.inBoard(row, col+i) is True and self.isEmpty(row,col+i) is True) and (self.inBoard(row-1, col+i) is False or self.isEmpty(row-1,col+i) is True) and (self.inBoard(row+1, col+i) is False or self.isEmpty(row+1,col+i) is True) and temp <7:
                            i+=1
                            temp+=1
                        if self.inBoard(row,col+i) is True and self.isEmpty(row,col+i) is False:
                            temp-=1
                        if temp > 1:
                            row_square_R.append(row)
                            col_square_R.append(col)
                            number_R.append(temp)

                        #LEFT
                        i=-1
                        temp=0
                        while (self.inBoard(row, col+i) is True and self.isEmpty(row,col+i) is True) and (self.inBoard(row-1, col+i) is False or self.isEmpty(row-1,col+i) is True) and (self.inBoard(row+1, col+i) is False or self.isEmpty(row+1,col+i) is True) and temp <7:
                            i-=1
                            temp+=1
                        if self.inBoard(row,col+i) is True and self.isEmpty(row,col+i) is False:
                            temp-=1
                        if temp > 1:
                            row_square_L.append(row)
                            col_square_L.append(col)
                            number_L.append(temp)

                        #DOWN
                        i=1
                        temp=0
                        while (self.inBoard(row+i, col) is True and self.isEmpty(row+i,col) is True) and (self.inBoard(row+i, col-1) is False or self.isEmpty(row+i,col-1) is True) and (self.inBoard(row+i, col+1) is False or self.isEmpty(row+i,col+1) is True) and temp <7:
                            i+=1
                            temp+=1
                        if self.inBoard(row+i,col) is True and self.isEmpty(row+i,col) is False:
                            temp-=1
                        if temp > 1:
                            row_square_D.append(row)
                            col_square_D.append(col)
                            number_D.append(temp)

                        #UP
                        i=-1
                        temp=0
                        while (self.inBoard(row+i, col) is True and self.isEmpty(row+i,col) is True) and (self.inBoard(row+i, col-1) is False or self.isEmpty(row+i,col-1) is True) and (self.inBoard(row+i, col+1) is False or self.isEmpty(row+i,col+1) is True) and temp <7:
                            i-=1
                            temp+=1
                        if self.inBoard(row+i,col) is True and self.isEmpty(row+i,col) is False:
                            temp-=1
                        if temp > 1:
                            row_square_U.append(row)
                            col_square_U.append(col)
                            number_U.append(temp)


            #GENERACE KOMBINACE
            for i in range(1,8):
                wordlist.append(frozenset(itertools.permutations(self.bag, i)))

            #JEDNOPISMENNY TAH
            for item in one_letter:
                row = item[0]
                col = item[1]

                for letter in set(self.bag):
                    self.board[row][col] = letter #polozim na desku pismeno kvuli pocitani value

                    #NAJDE SLOVO V RADKU
                    word1 = letter
                    i = 1 #nutno dat do vnejsiho scopu
                    for i in range(1,col+1):
                        if self.isEmpty(row, col-i) is False:
                            word1 = self.board[row][col-i] + word1
                        else:
                            break
                    if col-i == 0 and self.isEmpty(row, col-i) is False:
                        i+=1
                    for x in range(col+1,15):
                        if self.isEmpty(row, x) is False:
                            word1 = word1 + self.board[row][x]
                        else:
                            break

                    #NAJDE SLOVO VE SLOUPCI
                    word2 = letter
                    z = 1 #nutno dat do vnejsiho scopu
                    for z in range(1,row+1):
                        if self.isEmpty(row-z, col) is False:
                            word2 = self.board[row-z][col] + word2
                        else:
                            break
                    if row-z == 0 and self.isEmpty(row-z, col) is False:
                        z+=1
                    for y in range(row+1,15):
                        if self.isEmpty(y, col) is False:
                            word2 = word2 + self.board[y][col]
                        else:
                            break

                    #SPOCITA VALUE
                    if (len(word1) == 1 or word1 in self.dictionary) and (len(word2) == 1 or word2 in self.dictionary):
                        value1 = value_row(row, col-i+1)
                        value2 = value_col(row-z+1, col)
                        value_list.append(value1+value2)
                        row_list.append(row)
                        col_list.append(col)
                        letter_list.append(letter)

                    self.board[row][col] = "" #smazu pismeno

            #DVOUPISMENNY TAH
            for item in one_letter:
                row = item[0]
                col = item[1]
                for elem in wordlist[2]: #vezme vsechny kombinace dvoupismennych tahu
                    for smer in [-1,1]:

                        #HORIZONTALNE
                        if self.inBoard(row, col+smer) is True and self.isEmpty(row, col+smer) is True:
                            self.board[row][col] = elem[0] # 1.pismeno
                            self.board[row][col+smer] = elem[1] # 2.pismeno

                            #NACTU POD WORD SLOVO V RADKU
                            word = ""
                            sloupec = 1 #nutno dat do vnejsiho scopu
                            for sloupec in range(1,col+1): #jdu nejvic doleva
                                if self.isEmpty(row, col-sloupec) is False:
                                    word = self.board[row][col-sloupec] + word
                                else:
                                    break
                            if col-sloupec == 0 and self.isEmpty(row, col-sloupec) is False: #kdyz jsem nejvic vlevo, prictu jedna, jinak tam to +1 chybi
                                sloupec+=1
                            for x in range(col,15):
                                if self.isEmpty(row, x) is False:
                                    word = word + self.board[row][x]
                                else:
                                    break

                            #POKUD JE V DICT POKRACUJI ZJISTOVANIM SLOV V SLOUPCICH
                            if word in self.dictionary:

                                #PRVNI PISMENO
                                word2 = ""
                                sloupec1 = 1 #nutno dat do vnejsiho scopu
                                for sloupec1 in range(1,row+1):
                                    if self.isEmpty(row-sloupec1, col) is False:
                                        word2 = self.board[row-sloupec1][col] + word2
                                    else:
                                        break
                                if row-sloupec1 == 0 and self.isEmpty(row-sloupec1, col) is False:
                                    sloupec1+=1
                                for y in range(row,15):
                                    if self.isEmpty(y, col) is False:
                                        word2 = word2 + self.board[y][col]
                                    else:
                                        break

                                #POKUD JE V DICT POKRACUJI ZJISTOVANIM SLOV V DRUHEM SLOUPCE
                                if (len(word2) == 1) or (word2 in self.dictionary):
                                    #DRUHE PISMENO
                                    word3 = ""
                                    sloupec2 = 1 #nutno dat do vnejsiho scopu
                                    for sloupec2 in range(1,row+1):
                                        if self.isEmpty(row-sloupec2, col+smer) is False:
                                            word3 = self.board[row-sloupec2][col+smer] + word3
                                        else:
                                            break
                                    if row-sloupec2 == 0 and self.isEmpty(row-sloupec2, col+smer) is False:
                                        sloupec2+=1
                                    for y in range(row,15):
                                        if self.isEmpty(y, col+smer) is False:
                                            word3 = word3 + self.board[y][col+smer]
                                        else:
                                            break

                                    #FINALLY JE VSECHNO V PORADKU A MOHU TENTO TAH POUZIT
                                    if (len(word3) == 1) or (word3 in self.dictionary):

                                        #SPOCITA VALUE
                                        value1 = value_row(row, col-sloupec+1)
                                        value2 = value_col(row-sloupec1+1, col)
                                        value3 = value_col(row-sloupec2+1, col+smer)
                                        value_list.append(value1+value2+value3)
                                        row_list.append([row,row])
                                        col_list.append([col,col+smer])
                                        letter_list.append([elem[0],elem[1]])
                                        self.board[row][col] = "" #smazu 1.pismeno
                                        self.board[row][col+smer] = "" #smazu 2.pismeno
                                    else:
                                        self.board[row][col] = "" #smazu 1.pismeno
                                        self.board[row][col+smer] = "" #smazu 2.pismeno
                                else:
                                    self.board[row][col] = "" #smazu 1.pismeno
                                    self.board[row][col+smer] = "" #smazu 2.pismeno
                            else:
                                self.board[row][col] = "" #smazu 1.pismeno
                                self.board[row][col+smer] = "" #smazu 2.pismeno

                        #VERTIKALNE
                        if self.inBoard(row+smer, col) is True and self.isEmpty(row+smer, col) is True:
                            self.board[row][col] = elem[0] # 1.pismeno
                            self.board[row+smer][col] = elem[1] # 2.pismeno

                            #NACTU POD WORD SLOVO V SLOUPCI
                            word = ""
                            radek = 1 #nutno dat do vnejsiho scopu
                            for radek in range(1,row+1): #jdu nejvic nahoru
                                if self.isEmpty(row-radek, col) is False:
                                    word = self.board[row-radek][col] + word
                                else:
                                    break
                            if row-radek == 0 and self.isEmpty(row-radek, col) is False: #kdyz jsem nejvic vlevo, prictu jedna, jinak tam to +1 chybi
                                radek+=1
                            for x in range(row,15):
                                if self.isEmpty(x, col) is False:
                                    word = word + self.board[x][col]
                                else:
                                    break

                            #POKUD JE V DICT POKRACUJI ZJISTOVANIM SLOV V SLOUPCICH
                            if word in self.dictionary:

                                #PRVNI PISMENO
                                word2 = ""
                                radek1 = 1 #nutno dat do vnejsiho scopu
                                for radek1 in range(1,col+1): #jdu doleva
                                    if self.isEmpty(row, col-radek1) is False:
                                        word2 = self.board[row][col-radek1] + word2
                                    else:
                                        break
                                if col-radek1 == 0 and self.isEmpty(row, col-radek1) is False:
                                    radek1+=1
                                for y in range(col,15):
                                    if self.isEmpty(row, y) is False:
                                        word2 = word2 + self.board[row][y]
                                    else:
                                        break

                                #POKUD JE V DICT POKRACUJI ZJISTOVANIM SLOV V DRUHEM SLOUPCE
                                if (len(word2) == 1) or (word2 in self.dictionary):
                                    #DRUHE PISMENO
                                    word3 = ""
                                    radek2 = 1 #nutno dat do vnejsiho scopu
                                    for radek2 in range(1,col+1):
                                        if self.isEmpty(row+smer, col-radek2) is False:
                                            word3 = self.board[row+smer][col-radek2] + word3
                                        else:
                                            break
                                    if row-radek2 == 0 and self.isEmpty(row+smer, col-radek2) is False:
                                        radek2+=1
                                    for y in range(col,15):
                                        if self.isEmpty(row+smer, y) is False:
                                            word3 = word3 + self.board[row+smer][y]
                                        else:
                                            break

                                    #FINALLY JE VSECHNO V PORADKU A MOHU TENTO TAH POUZIT
                                    if (len(word3) == 1) or (word3 in self.dictionary):

                                        #SPOCITA VALUE
                                        value1 = value_col(row-radek+1, col)
                                        value2 = value_row(row, col-radek1+1)
                                        value3 = value_row(row+smer, col-radek2+1)
                                        value_list.append(value1+value2+value3)
                                        row_list.append([row,row+smer])
                                        col_list.append([col,col])
                                        letter_list.append([elem[0],elem[1]])
                                        self.board[row][col] = "" #smazu 1.pismeno
                                        self.board[row+smer][col] = "" #smazu 2.pismeno
                                    else:
                                        self.board[row][col] = "" #smazu 1.pismeno
                                        self.board[row+smer][col] = "" #smazu 2.pismeno
                                else:
                                    self.board[row][col] = "" #smazu 1.pismeno
                                    self.board[row+smer][col] = "" #smazu 2.pismeno
                            else:
                                self.board[row][col] = "" #smazu 1.pismeno
                                self.board[row+smer][col] = "" #smazu 2.pismeno



            #WOMBO KOMBO DOLU
            for i in range (len(row_square_D)):
                row = row_square_D[i]
                col = col_square_D[i]
                delka = number_D[i]
                for delka2 in range (2,delka+1):
                    z = 0
                    word = ""
                    for z in range(0,row+1):
                        if self.isEmpty(row-z, col) is False:
                            word = self.board[row-z][col] + word
                        else:
                            break
                    if row-z == 0 and self.isEmpty(row-z, col) is False:
                        z+=1
                    for elem in wordlist[delka2]:
                        if (word+''.join(elem)) in self.dictionary:
                            #print()
                            #print()
                            #print(word+''.join(elem))
                            i=0
                            value = 0
                            x = 0
                            for i in range (len(word+''.join(elem))): #zjistuji hodnotu
                                if (row-z+1+i)<15 and self.isEmpty(row-z+1+i, col) is True and (self.inBoard(row-z+1+i, col+1) and self.isEmpty(row-z+1+i, col+1) is True) and (self.inBoard(row-z+1+i, col-1) and self.isEmpty(row-z+1+i, col-1) is True):
                                    #print(value, "+=", self.cellValue(row-z+1+i, col), "*", elem[x], self.letterValue(elem[x]))
                                    value += self.cellValue(row-z+1+i, col) * self.letterValue(elem[x])
                                    i+=1
                                    x+=1
                                elif (row-z+1+i)<15 and self.isEmpty(row-z+1+i, col) is False:
                                    #print(value, "+=", self.cellValue(row-z+1+i, col), "*", self.board[row-z+1+i][col], self.letterValue(self.board[row-z+1+i][col]))
                                    value += self.cellValue(row-z+1+i, col) * self.letterValue(self.board[row-z+1+i][col])
                                    i+=1
                            for i in range(1,delka2+1):
                                row_temp_list.append(row+i)
                                col_temp_list.append(col) #lze optimalizovat
                                letter_temp_list.append(elem[i-1])
                            row_list.append((row_temp_list))
                            row_temp_list = list()
                            col_list.append((col_temp_list))
                            col_temp_list = list()
                            letter_list.append((letter_temp_list))
                            letter_temp_list = list()
                            value_list.append(value)

            #WOMBO KOMBO NAHORU
            for i in range (len(row_square_U)):
                row = row_square_U[i]
                col = col_square_U[i]
                delka = number_U[i]
                for delka2 in range (2,delka+1):
                    #z = 0
                    word = ""
                    for z in range(row,15):
                        if self.isEmpty(z, col) is False:
                            word = word + self.board[z][col]
                        else:
                            break
                    for elem in wordlist[delka2]:
                        if (''.join(elem)+word) in self.dictionary:
                            #print(''.join(elem)+word)
                            x=0
                            value = 0
                            for i in range (len(''.join(elem)),0,-1): #zjistuji hodnotu
                                #print(value, "+=", self.cellValue(row-i, col), "*", elem[x], self.letterValue(elem[x]))
                                value += self.cellValue(row-i, col) * self.letterValue(elem[x])
                                x+=1
                            for i in range (len(word)):
                                #print(value, "+=", self.cellValue(row+i, col), "*", self.board[row+i][col], self.letterValue(self.board[row+i][col]))
                                value += self.cellValue(row+i, col) * self.letterValue(self.board[row+i][col])
                            x = 0
                            for i in range(delka2,0,-1):
                                row_temp_list.append(row-i)
                                col_temp_list.append(col)
                                letter_temp_list.append(elem[x])
                                x+=1
                            row_list.append((row_temp_list))
                            row_temp_list = list()
                            col_list.append((col_temp_list))
                            col_temp_list = list()
                            letter_list.append((letter_temp_list))
                            letter_temp_list = list()
                            value_list.append(value)

            #WOMBO KOMBO DOPRAVA
            for i in range (len(row_square_R)):
                row = row_square_R[i]
                col = col_square_R[i]
                delka = number_R[i]
                for delka2 in range (2,delka+1):
                    word = ""
                    for z in range(col,-1,-1):
                        if self.isEmpty(row, z) is False:
                            word = self.board[row][z] + word
                        else:
                            break
                    for elem in wordlist[delka2]:
                        if (word+''.join(elem)) in self.dictionary:
                            #print(word + ''.join(elem))
                            x=0
                            value = 0
                            for i in range (1,len(''.join(elem))+1): #zjistuji hodnotu
                                #print(value, "+=", self.cellValue(row-i, col), "*", elem[x], self.letterValue(elem[x]))
                                value += self.cellValue(row, col+i) * self.letterValue(elem[x])
                                x+=1
                            for i in range (len(word)):
                                #print(value, "+=", self.cellValue(row+i, col), "*", self.board[row+i][col], self.letterValue(self.board[row+i][col]))
                                value += self.cellValue(row, col-i) * self.letterValue(self.board[row][col-i])
                            for i in range(0,delka2):
                                row_temp_list.append(row)
                                col_temp_list.append(col+i+1)
                                letter_temp_list.append(elem[i])
                            row_list.append((row_temp_list))
                            row_temp_list = list()
                            col_list.append((col_temp_list))
                            col_temp_list = list()
                            letter_list.append((letter_temp_list))
                            letter_temp_list = list()
                            value_list.append(value)

            #WOMBO KOMBO DOLEVA
            for i in range (len(row_square_L)):
                row = row_square_L[i]
                col = col_square_L[i]
                delka = number_L[i]
                for delka2 in range (2,delka+1):
                    word = ""
                    for z in range(col,15):
                        if self.isEmpty(row, z) is False:
                            word = word + self.board[row][z]
                        else:
                            break
                    for elem in wordlist[delka2]:
                        if (''.join(elem) + word) in self.dictionary:
                            #print(word + ''.join(elem))
                            x=0
                            value = 0
                            for i in range (len(''.join(elem)),0,-1): #zjistuji hodnotu
                                #print(value, "+=", self.cellValue(row-i, col), "*", elem[x], self.letterValue(elem[x]))
                                value += self.cellValue(row, col-i) * self.letterValue(elem[x])
                                x+=1
                            for i in range (len(word)):
                                #print(value, "+=", self.cellValue(row+i, col), "*", self.board[row+i][col], self.letterValue(self.board[row+i][col]))
                                value += self.cellValue(row, col+i) * self.letterValue(self.board[row][col+i])
                            x=0
                            for i in range(delka2,0,-1):
                                row_temp_list.append(row)
                                col_temp_list.append(col-i)
                                letter_temp_list.append(elem[x])
                                x+=1
                            row_list.append((row_temp_list))
                            row_temp_list = list()
                            col_list.append((col_temp_list))
                            col_temp_list = list()
                            letter_list.append((letter_temp_list))
                            letter_temp_list = list()
                            value_list.append(value)


            # for i in range(len(value_list)):
            #     print(row_list[i], col_list[i], letter_list[i], "-", value_list[i], "(index)", i)

            #NENASEL JSEM ZADNE SLOVO
            if len(value_list) == 0:
                seen = set()
                duplicates = set(x for x in self.bag if x in seen or seen.add(x))
                if len(duplicates) == 0:
                    if len(self.bag) == 0:
                        return None
                    else:
                        return ''.join(self.bag)
                else:
                    return ''.join(duplicates)

            #NASEL JSEM SLOVO
            else:
                maximum = 0
                for i in range (len(value_list)):
                    if value_list[i] > maximum:
                        index_list=list()
                        index_list.append(i)
                        maximum = value_list[i]
                    elif value_list[i] == maximum:
                        index_list.append(i)

                #print(index_list)

                #NEJLEPE POLOZIM JENOPISMENNE MAXIMUM
                k = 1
                for index in index_list:
                    if type(row_list[index]) == int:
                        k = 0

                #POKUD NEEXISTUJE JEDNOPISMENNE, POLOZIM NEJKRATSI
                final_index = index_list[0]
                if k == 1:
                    if len(index_list)==1:
                        for i in range (len(row_list[final_index])):
                            final_output.append([row_list[final_index][i], col_list[final_index][i], letter_list[final_index][i]])
                        return final_output
                    else:
                        for index in index_list:
                            maxx = 100
                            if len(row_list[index]) < maxx:
                                maxx = len(row_list[index])
                                final_index = index
                        for i in range (len(row_list[final_index])):
                            final_output.append([row_list[final_index][i], col_list[final_index][i], letter_list[final_index][i]])
                        return final_output

                #ZKUSIME JEDNOPISMENNE
                else:
                    for index in index_list:
                        if type(row_list[index]) == int:
                            #TAH BEZ DOUBLU A TRIPLU
                            if ((row_list[index] >0 and self.cellValue(row_list[index]-1,col_list[index])== 1) and (row_list[index] <14 and self.cellValue(row_list[index]+1,col_list[index]) == 1)  and (col_list[index] >0 and self.cellValue(row_list[index],col_list[index]-1) == 1) and (col_list[index] <14 and self.cellValue(row_list[index],col_list[index]+1) == 1)):
                                return [[row_list[index],col_list[index],letter_list[index]]]
                            #POKUD NENAJDU JEDNOSPIMENNY TAH BEZ DOUBLE A TRIPLE POLI, ZKUSIM JEN DOBULE
                            elif ((row_list[index] >0 and self.cellValue(row_list[index]-1,col_list[index])<=2) and (row_list[index] <14 and self.cellValue(row_list[index]+1,col_list[index]) <=2)  and (col_list[index] >0 and self.cellValue(row_list[index],col_list[index]-1) <=2) and (col_list[index] <14 and self.cellValue(row_list[index],col_list[index]+1) <=2)):
                                return [[row_list[index],col_list[index],letter_list[index]]]

                #KDYZ NEVYJDE ANI TO, ZKUSIM COKOLI JEDNOPISMENNEHO
                for index in index_list:
                    if type(row_list[index]) == int:
                        return [[row_list[index],col_list[index],letter_list[index]]]






def replaceLetters(player, lettersToReplace, bag):
    print("Player ", player.name, " want's to exchange ", len(lettersToReplace), ", bag has " , len(bag) , " letters")

    if (len(lettersToReplace) > 7 or len(lettersToReplace) > len(bag)):
        print("No replacement will be made, as the user either wants to replace >7 letters or more than than letters in the bag")
        return player.bag

    listLetters = list(lettersToReplace)
    newBag = []
    for letter in player.bag:
        if letter not in listLetters:
            newBag.append(letter)
        else:
            listLetters.remove(letter)

    new = ""
    for i in range(len(lettersToReplace)):
        if len(bag) > 0:
            newBag.append(bag.pop())
            new += newBag[-1]
    print("New replacement ", new)
    return newBag



def afterMove(lastPlayer, lastPlayerResult, nextPlayer, board, bag):

    """
        simplifed game handling procedure. We assume here that both player behave correctly, e.g. they do not
        invalide their 'self.bag' etc..

        On Brute/Tournament, this function will also check all return types and validiy of actions
    """

    if (lastPlayerResult is None):
        #player 'pass', no change
        print("Player ", lastPlayer.name, " is passing ")
        return 0

    if isinstance(lastPlayerResult, str):

        newBag = replaceLetters(lastPlayer, lastPlayerResult, bag)
        lastPlayer.update(board,newBag, lastPlayer.myScore, nextPlayer.myScore, len(bag))
        #the second player does not need to be updated, as the board didn't change
        return 0

    if isinstance(lastPlayerResult,list):
        #player is placing some letters to the game
        print("Player ", lastPlayer.name , " is placing stuff .. ", lastPlayerResult)
        lettersToReplace = ""
        changeOfScore = 0
        for item in lastPlayerResult:
            if isinstance(item, list) and len(item) == 3:
                row, col, letter = item
                if (lastPlayer.inBoard(row, col) and board[row][col] == ""):
                    board[row][col] = letter
                    lettersToReplace += letter
                    print("Placing ", letter, "at ", row,col)
                    changeOfScore+=1
            else:
                print("Error when reading result of ", lastPlayer.name, " result should be a list of list (e.g. [ [1,2,'a'] ]")
                print("Player instead returned: ", lastPlayerResult)
                quit()
        newBag = replaceLetters(lastPlayer, lettersToReplace, bag)
        lastPlayer.update(board, newBag, lastPlayer.myScore+1, nextPlayer.myScore, len(bag))
        nextPlayer.update(board, nextPlayer.bag, nextPlayer.myScore, lastPlayer.myScore+1, len(bag))
        return changeOfScore

    print("Wrong result from player.move; exit now")
    quit()
    return 0


if __name__ == "__main__":



    words = base.readDictionary('dic.txt') #words is represented as python-dictionray

    #board = base.createBoard("INVOLVER") #this word should be from the dictionray
    board = base.createBoard(random.choice(list(words))) #random word from the dictionray

    bag = base.createInitialBag()

    player1bag = bag[0:7]   #letters for the player1
    player2bag = bag[7:14]  #letters for the player2
    bag = bag[14:] #remove first 14 letters


    p1 = Player("player1", words, board, player1bag, len(bag))
    p2 = Player("player2", words, board, player2bag, len(bag))
    p1.print()

    noChangeMoves = 0
    while noChangeMoves < 3:

        result = p1.move()
        s1 = afterMove(p1, result, p2, board, bag)

        p1.print()

        result = p2.move()
        s2 = afterMove(p2, result, p1, board, bag)

        p2.print()

        if s1 + s2 == 0:
            noChangeMoves+=1
        else:
            noChangeMoves = 0


    print("Game finished after " , noChangeMoves , " moves without change of score ")