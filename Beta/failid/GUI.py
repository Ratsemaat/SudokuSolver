import easygui
import pildiltTuvastamine as pt
import sudokuLaud as sl
import tkinter as tk
import cv2


def BoardEditor(board=[]):
    data = {}
    master = tk.Tk()
    for i in range(9):
        for j in range(9):
            data[str(i) + str(j)] = tk.StringVar(master)
            if board == []:
                data[str(i) + str(j)].set("")
            else:
                data[str(i) + str(j)].set(board[i][j])
            a = tk.OptionMenu(master, data[str(i) + str(j)], "", "1", "2", "3", "4", "5", "6", "7", "8", "9")
            a.grid(row=i, column=j)
    b = tk.Button(master, text="Sisestatud", command=master.destroy).grid(row=9, columnspan=6)
    master.mainloop()
    board=[]
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(data[str(i) + str(j)].get())
        board.append(temp)
    if sl.kontrollija(board)==False:
        easygui.msgbox(msg="Vigane sudoku",ok_button="Uuesti")
        return(BoardEditor(board))
    return board


reply = easygui.buttonbox("Tere! Kust ma saan Sudoku, mida lahendada?", choices=["Pildilt", "Sisestan ise"])

if reply == "Pildilt":
    f = easygui.fileopenbox()
    laud = (pt.ImageToGrid(f))

    pilt=cv2.resize(cv2.imread(f), (256, 256))
    cv2.imshow("originaalpilt. Vajuta midagi, et edasi minna.",pilt)
    cv2.waitKey(3)
    new_board = BoardEditor(board=laud)
    sl.lahendaja(new_board)

if reply == "Sisestan ise":
    board = BoardEditor()
    sl.lahendaja(board)

