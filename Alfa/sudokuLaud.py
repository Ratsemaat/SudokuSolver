from tkinter import *

grid = [["3", "", "", "", "", "9", "", "4", ""],
        ["", "", "", "", "", "1", "", "", ""],
        ["", "7", "1", "", "", "", "3", "", "5"],
        ["", "", "", "3", "", "2", "", "", "9"],
        ["5", "8", "", "7", "", "", "", "", ""],
        ["4", "", "3", "1", "", "6", "", "", ""],
        ["", "", "", "", "", "", "6", "", "4"],
        ["", "", "", "", "6", "", "", "", ""],
        ["9", "", "", "2", "", "", "", "5", "3"]
        ]
completeSet = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def RowCandidateNumberFinder(row_number,sudoku_table):
    # funktsioon võtab sisse rea numbri ja tagastab nimekirja arvudest, mis reast puuduvad
    row_candidate_numbers = completeSet.copy()
    for number in sudoku_table[row_number - 1]:
        if number != "":
            row_candidate_numbers.remove(number)
    return row_candidate_numbers


def ColumnCandidateNumberFinder(column_number,sudoku_table):
    # funktsioon võtab sisse kolonni numbri ja tagastab nimekirja arvudest, mis kolonnist puuduvad
    column_candidate_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for number in range(9):
        if sudoku_table[number][column_number - 1] != "":
            column_candidate_numbers.remove(sudoku_table[number][column_number - 1])
    return column_candidate_numbers


def BoxCandidateNumberFinder(row_number,column_number,sudoku_table):
    # Määrab rea ja kolonni põhjal ära 3x3 kasti numbri.
    box = 0
    if row_number < 4:
        box += 1
    elif row_number < 7:
        box += 4
    elif row_number < 10:
        box += 7
    if column_number < 4:
        box += 0
    elif column_number < 7:
        box += 1
    elif column_number < 10:
        box += 2

    # Määrab 3x3 kasti numbri järgi ära nimekirja arvudest, mis on kastist puudu
    x = (box - 1) // 3
    y = (box - 1) % 3
    box_candidate_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(3):
        for j in range(3):
            if sudoku_table[3 * x + i][3 * y + j] != "":
                box_candidate_numbers.remove(sudoku_table[(3 * x + i)][(3 * y + j)])
    return box_candidate_numbers



def CandidateNumberFinder(row_number, column_number,sudoku_table):
    # Leiab konkreetsesse ruutu sobivad numbrid
    candidate_numbers = list(set(RowCandidateNumberFinder(row_number, sudoku_table)) \
                             .intersection(ColumnCandidateNumberFinder(column_number, sudoku_table)) \
                             .intersection(BoxCandidateNumberFinder(row_number,column_number, sudoku_table)))
    return candidate_numbers


def TableShower(sudoku_table):
    # funktsioon joonistab gridi baasil tabeli
    window_height = 600
    window_width = 600
    master = Tk()
    laud = Canvas(height=window_height, width=window_width)
    for i in range(9):
        for j in range(9):
            if sudoku_table[i][j] != "":
                w = Label(laud, text=sudoku_table[i][j], width=2, height=1, font=("Ariel", 20),
                          borderwidth=1, relief="raised")
            else:
                w = Label(laud, width=2, height=1, font=("Ariel", 20),
                          borderwidth=1, relief="raised")
            w.grid(row=i, column=j)
    laud.pack()
    master.mainloop()

#Järgnev lõik otsib ja täidab kohad, kuhu saab minna ainult üks arv
def PreProcessor(sudoku_table):
    #VIGANE PROGRAMMILÕIK
    MakingProgress = True
    while MakingProgress == True:
        MakingProgress = False
        for i in range(9):
            for j in range(9):
                if grid[i][j] == "" and len(CandidateNumberFinder(i + 1, j + 1,sudoku_table)) == 1:
                    for number in CandidateNumberFinder(i + 1, j + 1,sudoku_table):
                        sudoku_table[i][j] = number
                        MakingProgress = True
    return sudoku_table


def RandomFiller(row_number, column_number, sudoku_table, Master=True):
    # muutuja, millega saaks termineerida kogu protsessi nii pea, kui lahendus on leitud
    global isFinished
    isFinished = False
    candidate_numbers = CandidateNumberFinder(row_number, column_number,sudoku_table)
    algpos=(row_number,column_number)
    # Kuniks lahendust pole leitud jätkab otsinguid
    while not isFinished:
        row_number = algpos[0]
        column_number = algpos[1]
        if candidate_numbers == []:  # Kui ühtki sobivat varianti enam pole
            # siis on kuskil eelnevate ruutude juures midagi valesti läinud. Paneme haru kinni.
            sudoku_table[row_number- 1][column_number-1] = ""
            return
        sudoku_table[row_number-1][column_number-1] = candidate_numbers[0]
        # Otsib järgmise täitmata lahtri
        while sudoku_table[row_number - 1][column_number - 1] != "":
            if column_number < 9:
                column_number += 1
            elif column_number == 9:
                if row_number < 9:
                    row_number += 1
                    column_number = 1
                elif row_number == 9 and column_number == 9:
                    isFinished = True
                    return
        # Sama funktsioon uue lahtri peal
        RandomFiller(row_number, column_number,sudoku_table, Master=False)
        # Kui rekursiivne funktsioon on tagasi välimiste kihtide juures, siis järelikult on programm lõpetanud
        if isFinished == True:
            break
        # või on kuskil tehtud viga. Annab veast teada ja eemaldab praegu proovitud elemendi
        else:
            candidate_numbers = candidate_numbers[1:]

    #Kui on originaalse funktsiooiga tegemist siis tagastab lahendatud sudoku.
    if isFinished == True and Master == True:
        return sudoku_table
    return


def lahendaja(sudoku_table):
    #PreProcessor(sudoku_table)
    #Otsib esimese koha sudokus, kus on tühi koht
    found=False
    for i in range(len(sudoku_table)):
        if found==True:
            break
        for j in range(len(sudoku_table)):
            if sudoku_table[i][j] == "":
                row_number = i+1
                column_number = j+1
                found=True
                break
    TableShower(RandomFiller(row_number,column_number,sudoku_table))





