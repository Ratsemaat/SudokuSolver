from tkinter import*


grid=[["3", "x", "x", "x", "x", "9", "x", "4", "x"],
       ["x", "x", "x", "x", "x", "1", "x", "x", "x"],
       ["x", "7", "1", "x", "x", "x", "3", "x", "5"],
       ["x", "x", "x", "3", "x", "2", "x", "x", "9"],
       ["5", "8", "x", "7", "x", "x", "x", "x", "x"],
       ["4", "x", "3", "1", "x", "6", "x", "x", "x"],
       ["x", "x", "x", "x", "x", "x", "6", "x", "4"],
       ["x", "x", "x", "x", "6", "x", "x", "x", "x"],
       ["9", "x", "x", "2", "x", "x", "x", "5", "3"]
       ]
completeSet=["1","2","3","4","5","6","7","8","9"]


def RowCandidateNumberFinder(row_number, sudoku_table=grid):
    #funktsioon võtab sisse rea numbri ja tagastab nimekirja arvudest, mis reast puuduvad
    row_candidate_numbers = completeSet.copy()
    for number in sudoku_table[row_number-1]:
        if number != "x":
            row_candidate_numbers.remove(number)
    return(row_candidate_numbers)


def ColumnCandidateNumberFinder(column_number, sudoku_table = grid):
    #funktsioon võtab sisse kolonni numbri ja tagastab nimekirja arvudest, mis kolonnist puuduvad
    column_candidate_numbers = ["1","2","3","4","5","6","7","8","9"]
    for number in range(9):
        if sudoku_table[number][column_number-1] !=  "x":
            column_candidate_numbers.remove(sudoku_table[number][column_number-1])
    return(column_candidate_numbers)


def BoxCandidateNumberFinder(box_number, sudoku_table = grid):
    #funktsioon võtab sisse 3x3 kasti numbri ja tagastab nimekirja arvudest, mis on kastist puudu
    x=(box_number-1)//3
    y=(box_number-1)%3
    box_candidate_numbers= ["1","2","3","4","5","6","7","8","9"]
    for i in range(3):
        for j in range(3):
            if sudoku_table[3*x+i][3*y+j] != "x":
                box_candidate_numbers.remove(sudoku_table[(3*x+i)][(3*y+j)])
    return box_candidate_numbers


def BoxAssigner(row_number, column_number):
    #Funktsioon määrab rea ja kolonni põhjal ära 3x3 kasti numbri.
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
    return box


def CandidateNumberFinder(row_number,column_number, sudoku_table=grid):
    #Leiab konkreetsesse ruutu sobivad numbrid
    box_number = BoxAssigner(row_number,column_number)
    candidate_numbers = list(set(RowCandidateNumberFinder(row_number, sudoku_table)).intersection(ColumnCandidateNumberFinder(column_number, sudoku_table)).intersection(BoxCandidateNumberFinder(box_number, sudoku_table)))
    return(candidate_numbers)


def TableShower(sudoku_table=grid):
    # funktsioon joonistab gridi baasil tabeli
    window_height=600
    window_width=600
    master=Tk()
    laud = Canvas(height=window_height, width=window_width)
    for i in range(9):
        for j in range(9):
            if sudoku_table[i][j] != "x":
                w = Label(laud, text=sudoku_table[i][j], width=2, height=1, font=("Ariel", 20),
                          borderwidth=1, relief="raised")
            else:
                w = Label(laud, width=2, height=1, font=("Ariel", 20),
                          borderwidth=1, relief="raised")
            w.grid(row=i, column=j)
    laud.pack()
    master.mainloop()



def RandomFiller(row_number, column_number, sudoku_table=grid, isFinished=False ):
#clusterfack aga suht tootab isegi
    print(sudoku_table)
    candidate_numbers = CandidateNumberFinder(row_number,column_number, sudoku_table)
    print(row_number, column_number,candidate_numbers)


    if candidate_numbers==[]:
        return False

    while isFinished == False :

        sudoku_table[row_number-1][column_number-1] = candidate_numbers[0]
        next_column_number = column_number
        next_row_number = row_number
        while sudoku_table[next_row_number-1][next_column_number-1] != "x":
            if next_column_number<9:
                next_column_number+=1
            elif next_column_number == 9:
                if next_row_number<9:
                    next_row_number+=1
                    next_column_number=1
                if next_row_number==9 and next_column_number==9:
                    isFinished=True
                    print("finished")
                    break
        if RandomFiller(next_row_number, next_column_number, sudoku_table) == False and isFinished == False:
            sudoku_table[next_row_number-1][next_column_number-1]="x"
            candidate_numbers = candidate_numbers[1:]
        if candidate_numbers==[]:
            return False
    return


#Järgnev lõik otsib ja täidab kohad, kuhu saab minna ainult üks arv
MakingProgress=True
while MakingProgress==True:
    MakingProgress = False
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "x" and len(CandidateNumberFinder(i+1,j+1)) == 1:
                for number in CandidateNumberFinder(i+1, j+1):
                    grid[i][j] = number

Testing_grid=grid.copy()
RandomFiller(1,2,sudoku_table=Testing_grid)
TableShower(Testing_grid)




