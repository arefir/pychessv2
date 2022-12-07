from array import *
import sys
import os


def parseCoords(row, col):

    # print(f"row: {row} col: {col}")

    row = 8 - int(row)
    col = ord(col)

    # print(f"row: {row} col: {col}")

    if row < 0 or row > 7:
        return 1

    if col < 65 or col > 72:
        if col < 97 or col > 104:
            return 1

    if col >= 97:
        col = col - 97
    else:
        col = col - 65

    return [row, col]
    # if isinstance(coords[0], str):
    #     coords[0] = ord(coords[0])
    #     coords[1] = 8 - int(coords[1])

    # else:
    #     coords[1] = 8 - coords[1]

    # if coords[0] >= 65 and coords[0] <= 72:
    #     coords[0] = coords[0] - 65
    # elif coords[0] >= 97 and coords[0] <= 104:
    #     coords[0] = coords[0] - 97
    # else:
    #     print("Invalid coordinates")
    #     return 1


def finish():
    x = input("Please press Enter to continue")
    os.system("cls")


rows, cols = (8, 8)


class ChessBoard:

    # board = []
    # board = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(rows)]
    # count = 0
    # kingB = [4, 0]
    # kingW = [4, 7]
    # turn = "white"
    # moveW = []
    # moveB = []

    def __init__(self):

        self.board = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(rows)]
        self.count = 0
        # self.kingB = [4, 0]
        # self.kingW = [4, 7]
        self.turn = "white"
        self.moveW = []
        self.moveB = []

        for i in range(8):
            self.board[1][i] = Pawn("black", 1, i, self.board)

        for i in range(8):
            self.board[6][i] = Pawn("white", 6, i, self.board)

        self.board[0][0], self.board[0][7] = (
            Rook("black", 0, 0, self.board),
            Rook("black", 0, 7, self.board),
        )
        self.board[7][0], self.board[7][7] = (
            Rook("white", 7, 0, self.board),
            Rook("white", 7, 7, self.board),
        )

        self.board[0][1], self.board[0][6] = (
            Knight("black", 0, 1, self.board),
            Knight("black", 0, 6, self.board),
        )
        self.board[7][1], self.board[7][6] = (
            Knight("white", 7, 1, self.board),
            Knight("white", 7, 6, self.board),
        )

        self.board[0][2], self.board[0][5] = (
            Bishop("black", 0, 2, self.board),
            Bishop("black", 0, 5, self.board),
        )
        self.board[7][2], self.board[7][5] = (
            Bishop("white", 7, 2, self.board),
            Bishop("white", 7, 5, self.board),
        )

        self.board[0][3], self.board[0][4] = (
            Queen("black", 0, 3, self.board),
            King("black", 0, 4, self.board),
        )
        self.board[7][3], self.board[7][4] = (
            Queen("white", 7, 3, self.board),
            King("white", 7, 4, self.board),
        )

    # PRINT CHESSBOARD
    def printBoard(self):

        c = 8
        print("")
        for i in self.board:
            print(c, end=" ")
            for j in i:
                if j == 0:
                    print("⊡", end=" ")
                else:
                    if j.team == "black":
                        print(j.symbolB, end=" ")
                    else:
                        print(j.symbolW, end=" ")
                    # print(j, end=" ");
            print()
            c -= 1

        print("  a b c d e f g h")
        print("")

    # find KING PIECE
    def findKing(self, team):

        for k in range(8):
            for l in range(8):
                king = self.board[k][l]
                if king != 0:
                    if king.team != team:
                        continue
                    elif king.identifier == "king":
                        return king

        return 1

    # CHECK FOR CHECK
    def isCheck(self):

        team = self.turn

        check = False
        for i in range(8):
            if check:
                # print("if check? break")
                break
            for j in range(8):
                piece = self.board[i][j]
                if piece != 0:
                    # print(piece)
                    if piece.team != team:
                        # coords = [j, i]
                        # src = [piece.col + 65, 8 - piece.row]
                        # print(f"{piece.identifier} {src}")
                        # if team == "white":
                        # dest = [self.kingW[0] + 65, 8 - self.kingW[1]]
                        # print(dest)
                        king = self.findKing(team)
                        if king == 1:
                            print("king not found")
                            os.system("exit")

                        check = piece.checkvalid(king.row, king.col)
                        # print(f"isCheck {piece.identifier} {src} {dest} {check}")
                        if check:
                            # print("if check? break")
                            return check
                        # if team == "black":
                        #     dest = [self.kingB[0] + 65, 8 - self.kingB[1]]
                        #     print(f"isCheck {piece.identifier} {src} {dest} {check}")
                        #     check = piece.checkvalid(src, dest, coords, self.kingB)
                # if check:
                #     # print("if check? break")
                #     break
        # print(check)
        return check

    # CHECK FOR CHECKMATE
    def isCheckmate(self):

        if not self.isCheck():
            return False
        else:

            team = self.turn
            # king = [0, 0]

            # if team == "white":
            #     king = self.kingW.copy()
            # else:
            #     king = self.kingB.copy()

            check = True
            for i in range(8):
                # if not check:
                #     break
                for j in range(8):
                    # if not check:
                    #     break
                    piece = self.board[i][j]
                    if piece != 0:
                        if piece.team == team:

                            for r in range(8):
                                # if not check:
                                #     break
                                for c in range(8):
                                    # coords = [j, i]
                                    # dest = [c + 65, 8 - r]
                                    # src = [piece.col + 65, 8 - piece.row]

                                    if self.board[r][c] != 0:
                                        if self.board[r][c].team == team:
                                            continue

                                    # if coords[0] == c and coords[1] == r:
                                    #     continue
                                    if r == i and c == j:
                                        continue

                                    valid = piece.checkvalid(r, c)

                                    if valid:
                                        temp = self.board[r][c]
                                        piece.move(r, c)
                                        # if self.board[r][c].identifier == "king":
                                        #     if self.board[r][c].team == "white":
                                        #         self.kingW = [c, r]
                                        #     else:
                                        #         self.kingB = [c, r]

                                        # print("TEMPBOARD\n")
                                        # self.printBoard()
                                        check = self.isCheck()
                                        # print(
                                        #     f"isCheckmate {piece.identifier} src:{piece.row} {piece.col} des:{r} {c} {check}"
                                        # )

                                        piece = self.board[r][c]
                                        piece.move(i, j)
                                        self.board[r][c] = temp

                                        # self.printBoard()

                                        # if self.board[coords[1]][coords[0]] != 0:
                                        #     if (
                                        #         self.board[coords[1]][
                                        #             coords[0]
                                        #         ].identifier
                                        #         == "king"
                                        #     ):
                                        #         if (
                                        #             self.board[coords[1]][
                                        #                 coords[0]
                                        #             ].team
                                        #             == "white"
                                        #         ):
                                        #             self.kingW = king
                                        #         else:
                                        #             self.kingB = king

                                        if not check:
                                            return False

            if check == False:
                return False
            else:
                return True

    # CHECK DRAW
    def isDraw(self):

        if self.isCheck():
            return False
        else:
            team = self.turn
            # king = [0, 0]

            # if team == "white":
            #     king = self.kingW.copy()
            # else:
            #     king = self.kingB.copy()

            check = True
            for i in range(8):
                # if not check:
                #     break
                for j in range(8):
                    # if not check:
                    #     break
                    piece = self.board[i][j]
                    if piece != 0:
                        if piece.team == team:

                            for r in range(8):
                                # if not check:
                                #     break
                                for c in range(8):
                                    # coords = [j, i]
                                    # dest = [c + 65, 8 - r]
                                    # src = [piece.col + 65, 8 - piece.row]

                                    if self.board[r][c] != 0:
                                        if self.board[r][c].team == team:
                                            continue

                                    # if coords[0] == c and coords[1] == r:
                                    #     continue
                                    if r == i and c == j:
                                        continue

                                    valid = piece.checkvalid(r, c)

                                    if valid:
                                        temp = self.board[r][c]
                                        piece.move(r, c)
                                        # if self.board[r][c].identifier == "king":
                                        #     if self.board[r][c].team == "white":
                                        #         self.kingW = [c, r]
                                        #     else:
                                        #         self.kingB = [c, r]

                                        # print("TEMPBOARD\n")
                                        # self.printBoard()
                                        check = self.isCheck()
                                        # print(
                                        #     f"isDraw {piece.identifier} src:{piece.row} {piece.col} des:{r} {c} {check}"
                                        # )

                                        piece = self.board[r][c]
                                        piece.move(i, j)
                                        self.board[r][c] = temp

                                        # self.printBoard()

                                        # if self.board[coords[1]][coords[0]] != 0:
                                        #     if (
                                        #         self.board[coords[1]][
                                        #             coords[0]
                                        #         ].identifier
                                        #         == "king"
                                        #     ):
                                        #         if (
                                        #             self.board[coords[1]][
                                        #                 coords[0]
                                        #             ].team
                                        #             == "white"
                                        #         ):
                                        #             self.kingW = king
                                        #         else:
                                        #             self.kingB = king

                                        if not check:
                                            return False

            if check == False:
                return False
            else:
                return True

    # PRINT MOVE LIST
    def printMoves(self):

        print("White\tBlack")

        moveW = self.moveW
        moveB = self.moveB

        for i in range(len(moveB)):
            print(f"{moveW[i]}\t{moveB[i]}")

        if len(moveW) > len(moveB):
            print(f"{moveW[-1]}\n")
        else:
            print()

        finish()

    # NEW GAME
    def new(self):

        x = 1

        while True:
            if not os.path.isfile(f"game-{x}.txt"):
                break
            else:
                x += 1

        f = open(f"game-{x}.txt", "w")
        f.close()

        self.play(x, "")

    #  LOAD GAME
    def load(self):
        turn = self.turn

        os.system("cls")
        path = os.getcwd()
        onlyfiles = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]
        onlyfiles.remove("main.py")

        print("List of available files:\n")
        for file in onlyfiles:
            print(file)

        while True:
            filename = input(
                "\nInput file name to load the desired file(eg: game-1.txt): "
            )

            if os.path.isfile(filename):

                f = open(filename, "r")
                lines = f.readlines()

                for line in lines:
                    self.printBoard()

                    steps = line.split()

                    turn = self.turn

                    if self.isCheckmate():
                        print("Checkmate!")
                        if turn == "white":
                            print("Black Wins!\n")
                        else:
                            print("White Wins!\n")

                        self.printMoves()
                        break

                    print(f"{turn} to move")

                    piece = steps[0]
                    if piece == "exit":
                        os.system("cls")
                        break

                    coords = list(piece)
                    coords = parseCoords(coords[1], coords[0])

                    if coords == 1:
                        # os.system("cls")
                        print("Invalid input")
                        continue

                    r = coords[0]
                    c = coords[1]

                    move = ""

                    if self.board[r][c] != 0:
                        if self.board[r][c].team == turn:
                            move = steps[1]
                        else:
                            os.system("cls")
                            print("You cannot move your opponent's pieces")
                    else:
                        os.system("cls")
                        print(
                            "There is no chess piece on the selected coordinate. Please try again"
                        )
                        continue

                    if (move) != "":
                        coords = list(move)
                        coords = parseCoords(coords[1], coords[0])

                        if coords == 1:
                            os.system("cls")
                            print("Invalid input")
                            continue

                        mr = coords[0]
                        mc = coords[1]

                        pc = self.board[r][c]

                        # enemy = False
                        if self.board[mr][mc] != 0:
                            # if self.board[mr][mc].team != pc.team:
                            # enemy = True
                            if self.board[mr][mc].team == pc.team:
                                os.system("cls")
                                print("Destination Square Occupied")
                                continue

                        valid = pc.checkvalid(mr, mc)

                        if valid:

                            # king = [0, 0]

                            # if pc.identifier == "king":
                            #     if turn == "white":
                            #         king = self.kingW.copy()
                            #         self.kingW = [mc, mr]
                            #     else:
                            #         king = self.kingB.copy()
                            #         self.kingB = [mc, mr]
                            temp = self.board[mr][mc]
                            pc.move(mr, mc)
                            pc = self.board[mr][mc]
                            isCheck = self.isCheck()

                            # if pc.identifier == "king":
                            #     if turn == "white":
                            #         self.kingW = king
                            #     else:
                            #         self.kingB = king
                            # self.printBoard()
                            # x = input()
                            # if x == 1:
                            #     break
                            # print(isCheck)
                            if isCheck:
                                # print("Checked");
                                pc.move(r, c)
                                self.board[mr][mc] = temp
                                os.system("cls")
                                print("Checked!")
                                continue

                            # self.board[mr][mc].col = mc
                            # self.board[mr][mc].row = mr
                            # self.board[mr][mc].counter += 1
                            pc.counter += 1
                            self.count += 1

                            if self.turn == "white":
                                self.turn = "black"
                            else:
                                self.turn = "white"

                            # if self.board[mr][mc].identifier == "king":
                            #     if self.board[mr][mc].team == "white":
                            #         self.kingW = [mc, mr]
                            #     else:
                            #         self.kingB = [mc, mr]

                            if turn == "white":
                                self.moveW.append(f"{piece} {move}")
                            else:
                                self.moveB.append(f"{piece} {move}")
                            # os.system("cls")
                        else:
                            # os.system("cls")
                            print("Invalid move for selected piece. Please try again")

                f.flush()
                f.close()
                sys.stdout.flush()
                break

            else:
                print("File with that name does not exist. Please try again")

        self.play(0, filename)

    # PLAY
    def play(self, x, filename):

        while True:

            self.printBoard()

            turn = self.turn

            if x:
                f = open(f"game-{x}.txt", "a")
            else:
                f = open(filename, "a")

            if self.isCheckmate():
                print("Checkmate!")
                if turn == "white":
                    print("Black Wins!\n")
                else:
                    print("White Wins!\n")

                self.printMoves()
                break

            if self.isDraw():
                print("Draw!")

                self.printMoves()
                break

            print(f"{turn} to move")

            piece = input("Choose piece (eg; d2 | to exit input 'exit'): ")
            if piece == "exit":
                os.system("cls")
                break

            coords = list(piece)
            coords = parseCoords(coords[1], coords[0])

            if coords == 1:
                # os.system("cls")
                print("Invalid input")
                continue

            r = coords[0]
            c = coords[1]

            move = ""

            if self.board[r][c] != 0:
                if self.board[r][c].team == turn:
                    move = input("Choose square to move (eg; d4): ")
                else:
                    os.system("cls")
                    print("You cannot move your opponent's pieces")
            else:
                os.system("cls")
                print(
                    "There is no chess piece on the selected coordinate. Please try again"
                )
                continue

            if (move) != "":
                coords = list(move)
                coords = parseCoords(coords[1], coords[0])

                if coords == 1:
                    os.system("cls")
                    print("Invalid input")
                    continue

                mr = coords[0]
                mc = coords[1]

                pc = self.board[r][c]

                # enemy = False
                if self.board[mr][mc] != 0:
                    # if self.board[mr][mc].team != pc.team:
                    # enemy = True
                    if self.board[mr][mc].team == pc.team:
                        os.system("cls")
                        print("Destination Square Occupied")
                        continue

                valid = pc.checkvalid(mr, mc)

                if valid:

                    # king = [0, 0]

                    # if pc.identifier == "king":
                    #     if turn == "white":
                    #         king = self.kingW.copy()
                    #         self.kingW = [mc, mr]
                    #     else:
                    #         king = self.kingB.copy()
                    #         self.kingB = [mc, mr]
                    temp = self.board[mr][mc]
                    pc.move(mr, mc)
                    pc = self.board[mr][mc]
                    isCheck = self.isCheck()

                    # if pc.identifier == "king":
                    #     if turn == "white":
                    #         self.kingW = king
                    #     else:
                    #         self.kingB = king
                    # self.printBoard()
                    # x = input()
                    # if x == 1:
                    #     break
                    # print(isCheck)
                    if isCheck:
                        # print("Checked");
                        pc.move(r, c)
                        self.board[mr][mr] = temp
                        os.system("cls")
                        print("Checked!")
                        continue

                    # self.board[mr][mc].col = mc
                    # self.board[mr][mc].row = mr
                    # self.board[mr][mc].counter += 1
                    pc.counter += 1
                    self.count += 1

                    if self.turn == "white":
                        self.turn = "black"
                    else:
                        self.turn = "white"

                    # if self.board[mr][mc].identifier == "king":
                    #     if self.board[mr][mc].team == "white":
                    #         self.kingW = [mc, mr]
                    #     else:
                    #         self.kingB = [mc, mr]

                    if turn == "white":
                        self.moveW.append(f"{piece} {move}")
                    else:
                        self.moveB.append(f"{piece} {move}")

                    f.write(f"{piece} {move}\n")
                    f.close()
                    # os.system("cls")
                else:
                    # os.system("cls")
                    print("Invalid move for selected piece. Please try again")


class Piece:

    # identifier = "piece"
    # team = ""
    # symbolB = ""
    # symbolW = ""
    # counter = 0
    # board = ""
    # row = 0
    # col = 0
    # srcC = [0, 0]
    # destC = [0, 0]

    def __init__(self, team, row, col, board):
        self.indentfier = ""
        self.team = team
        self.board = board
        self.counter = 0
        self.row = row
        self.col = col

    def move(self, row, col):
        self.board[row][col] = self.board[self.row][self.col]
        self.board[self.row][self.col] = 0
        self.row = row
        self.col = col

    # def initCoords(self, src, dest):
    #     self.srcC = []
    #     self.destC = []
    #     if not isinstance(src, list):
    #         self.srcC = list(src)
    #     else:
    #         self.srcC = src

    #     if not isinstance(dest, list):
    #         self.destC = list(dest)
    #     else:
    #         self.destC = dest

    # print(f"init {self.srcC} {destC}")
    # print(self.srcC);
    # print(destC);
    ######################
    # if isinstance(self.srcC[0], str):
    #     self.srcC[0] = ord(self.srcC[0])
    # else:
    #     self.srcC[0] = self.srcC[0]
    # self.srcC[1] = int(self.srcC[1])
    # if isinstance(self.destC[0], str):
    #     self.destC[0] = ord(self.destC[0])
    # else:
    #     self.destC[0] = self.destC[0]
    # self.destC[1] = int(self.destC[1])
    ######################
    # print(f"init {self.srcC} {self.destC}")
    # print(self.srcC);
    # print(self.destC);


class Pawn(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "pawn"
        self.symbolB = "♙"
        self.symbolW = "♟"

    def checkvalid(self, row, col):

        # self.initCoords(src, dest)
        team = self.team

        # print(f"self row: {self.row} self col: {self.col} row: {row} col: {col}")

        if team == "white":
            if self.counter > 0:
                if (row - self.row) != -1:
                    return False
            elif (row - self.row) < -2 or (row - self.row) > -1:
                return False
            if (row - self.row) == -2:
                if self.board[row + 1][col] != 0:
                    return False

        if team == "black":
            if self.counter > 0:
                if (row - self.row) != 1:
                    return False
            elif (row - self.row) > 2 or (row - self.row) < 1:
                return False
            if (row - self.row) == 2:
                if self.board[row - 1][col] != 0:
                    return False

        if self.col != col:
            if abs(row - self.row) != 1 or abs(col - self.col) != 1:
                return False
            elif self.board[row][col] == 0:
                return False
        elif self.board[row][col] != 0:
            return False

        return True


class Rook(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "rook"
        self.symbolB = "♖"
        self.symbolW = "♜"

    def checkvalid(self, row, col):

        # srcC = self.srcC
        # destC = self.destC
        # c = coords[0]
        # r = coords[1]
        # mc = mCoords[0]
        # mr = mCoords[1]

        team = self.team

        if (row != self.row) and (col != self.col):
            return False

        if (col != self.col) and (abs(col - self.col) > 1):
            if col > self.col:
                for i in range(self.col + 1, col):
                    if self.board[row][i] != 0:
                        return False
            else:
                for i in range(col + 1, self.col):
                    if self.board[row][i] != 0:
                        return False

        if (row != self.row) and (abs(row - self.row) > 1):
            if row > self.row:
                for i in range(self.row + 1, row):
                    if self.board[i][col] != 0:
                        return False
            else:
                for i in range(row + 1, self.row):
                    if self.board[i][col] != 0:
                        return False

        return True


class Knight(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "knight"
        self.symbolB = "♘"
        self.symbolW = "♞"

    def checkvalid(self, row, col):

        # self.initCoords(src, dest)

        # srcC = self.srcC
        # destC = self.destC
        # c = coords[0]
        # r = coords[1]
        # mc = mCoords[0]
        # mr = mCoords[1]

        # team = self.team

        if abs(row - self.row) == 2:
            if abs(col - self.col) == 1:
                return True

        if abs(row - self.row) == 1:
            if abs(col - self.col) == 2:
                return True

        return False


class Bishop(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "bishop"
        self.symbolB = "♗"
        self.symbolW = "♝"

    def checkvalid(self, row, col):

        # print(f"self row: {self.row} self col: {self.col} row: {row} col: {col}")

        # self.initCoords(src, dest)

        # srcC = self.srcC
        # destC = self.destC

        # c = coords[0]
        # r = coords[1]
        # mc = mCoords[0]
        # mr = mCoords[1]

        # team = self.team

        # print(srcC, destC)

        if abs(row - self.row) != abs(col - self.col):
            # print("287")
            return False

        rd = 0
        cd = 0

        if row > self.row:
            rd = 1
        else:
            rd = -1

        if col > self.col:
            cd = 1
        else:
            cd = -1

        tempRow = self.row
        tempCol = self.col
        tempRow += rd
        tempCol += cd

        #  and (
        #     (coords[0] >= 65 and coords[0] <= 72)
        #     or (coords[0] >= 97 and coords[0] <= 104)
        # ):
        while tempCol != col:
            # print(
            #     f"self row: {self.row} self col: {self.col} temprow: {tempRow} tempcol: {tempCol}"
            # )
            # print(f"srcC: {srcC}, srcTC: {srcTC}, destC: {destC}")
            # print(f"srcCol = {srcC[0]}, srcRow = {srcC[1]}, destCol = {destC[0]}, destRow = {destC[1]}")
            # print(f"srcTCol = {srcTC[0]}, srcTRow = {srcTC[1]}")
            # print(self.board[srcTC[1]][srcTC[0]])
            if self.board[tempRow][tempCol] != 0:
                # print("314")
                return False
            tempRow += rd
            tempCol += cd

        return True


class Queen(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "queen"
        self.symbolB = "♕"
        self.symbolW = "♛"

    def checkvalid(self, row, col):

        # self.initCoords(src, dest)

        # srcC = self.srcC
        # destC = self.destC
        # c = coords[0]
        # r = coords[1]
        # mc = mCoords[0]
        # mr = mCoords[1]

        # team = self.team

        if (row != self.row) and (col != self.col):
            if abs(row - self.row) != abs(col - self.col):
                return False

            rd = 0
            cd = 0

            if row > self.row:
                rd = 1
            else:
                rd = -1

            if col > self.col:
                cd = 1
            else:
                cd = -1

            tempRow = self.row
            tempCol = self.col
            tempRow += rd
            tempCol += cd

            #  and (
            #     (coords[0] >= 65 and coords[0] <= 72)
            #     or (coords[0] >= 97 and coords[0] <= 104)
            # ):
            while tempCol != col:
                # print(f"srcC: {srcC}, srcTC: {srcTC}, destC: {destC}")
                # print(f"srcCol = {srcC[0]}, srcRow = {srcC[1]}, destCol = {destC[0]}, destRow = {destC[1]}")
                # print(f"srcTCol = {srcTC[0]}, srcTRow = {srcTC[1]}")
                # print(self.board[srcTC[1]][srcTC[0]])
                if self.board[tempRow][tempCol] != 0:
                    # print("314")
                    return False
                tempRow += rd
                tempCol += cd

            return True

        if (col != self.col) and (abs(col - self.col) > 1):
            if col > self.col:
                for i in range(self.col + 1, col):
                    if self.board[row][i] != 0:
                        return False
            else:
                for i in range(col + 1, self.col):
                    if self.board[row][i] != 0:
                        return False

        if (row != self.row) and (abs(row - self.row) > 1):
            if row > self.row:
                for i in range(self.row + 1, row):
                    if self.board[i][col] != 0:
                        return False
            else:
                for i in range(row + 1, self.row):
                    if self.board[i][col] != 0:
                        return False

        return True


class King(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "king"
        self.symbolB = "♔"
        self.symbolW = "♚"

    def checkvalid(self, row, col):

        # self.initCoords(src, dest)

        # srcC = self.srcC
        # destC = self.destC
        # c = coords[0]
        # r = coords[1]
        # mc = mCoords[0]
        # mr = mCoords[1]

        # team = self.team

        if (abs(row - self.row)) > 1 or (abs(col - self.col)) > 1:
            return False

        return True


###########################################################################


while True:

    print("MAIN MENU\n")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = int(input("Input number to select: "))

    if choice == 1:
        chessboard1 = ChessBoard()
        chessboard1.new()
        del chessboard1

        # x = 1
        # while True:
        #     if not os.path.isfile(f"game-{x}.txt"):
        #         break
        #     else:
        #         x += 1

        # f = open(f"game-{x}.txt", "w")

    elif choice == 2:
        chessboard2 = ChessBoard()
        chessboard2.load()
        del chessboard2
        # os.system("cls")
        # path = os.getcwd()
        # onlyfiles = [
        #     f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        # ]
        # onlyfiles.remove("main.py")
        # onlyfiles.remove(".gitignore")
        # onlyfiles.remove("LICENSE")
        # onlyfiles.remove("README.md")

        # print("List of available files:\n")
        # for file in onlyfiles:
        #     print(file)

        # while True:
        #     filename = input(
        #         "\nInput file name to load the desired file(eg: game-1.txt): "
        #     )

        #     if os.path.isfile(filename):

        #         board1 = ChessBoard()

        #         f = open(filename, "r")
        #         lines = f.readlines()

        #         for line in lines:
        #             board1.printBoard()

        #             steps = line.split()

        #             turn = board1.turn

        #             if board1.isCheckmate():
        #                 print("Checkmate!")
        #                 if turn == "white":
        #                     print("Black Wins!\n")
        #                 else:
        #                     print("White Wins!\n")

        #                 board1.printMoves()
        #                 break

        #             # print(f"KingW: {board1.kingW}, KingB: {board1.kingB}")
        #             # print(f"{turn} to move")

        #             piece = steps[0]
        #             if piece == "exit":
        #                 os.system("cls")
        #                 break

        #             coords = list(piece)

        #             abort = getTrueCoords(coords)

        #             if abort == 1:
        #                 os.system("cls")
        #                 print("Invalid input")
        #                 break

        #             c = coords[0]
        #             r = coords[1]

        #             # c = ord(coords[0]);
        #             # r = 8 - int(coords[1]);

        #             # if c >= 65 and c <= 72:
        #             #     c = 8 - (c - 64);
        #             # elif c >= 97 and c <= 104:
        #             #     c = c - 97;
        #             # else:
        #             #     print("Invalid coordinates");

        #             move = ""

        #             if board1.board[r][c] != 0:
        #                 if board1.board[r][c].team == turn:
        #                     move = steps[1]
        #                 else:
        #                     os.system("cls")
        #                     print("You cannot move your opponent's pieces")
        #                     break
        #             else:
        #                 os.system("cls")
        #                 print(
        #                     "There is no chess piece on the selected coordinate. Please try again"
        #                 )
        #                 break

        #             if (move) != "":
        #                 mCoords = list(move)

        #                 abort = getTrueCoords(mCoords)

        #                 if abort == 1:
        #                     print("Invalid input")
        #                     break

        #                 mc = mCoords[0]
        #                 mr = mCoords[1]

        #                 pc = board1.board[r][c]

        #                 # enemy = False
        #                 if board1.board[mr][mc] != 0:
        #                     # if board1.board[mr][mc].team != pc.team:
        #                     # enemy = True
        #                     if board1.board[mr][mc].team == pc.team:
        #                         os.system("cls")
        #                         print("Destination Square Occupied")
        #                         break

        #                 valid = pc.checkvalid(piece, move, coords, mCoords)

        #                 if valid:

        #                     king = [0, 0]

        #                     if pc.identifier == "king":
        #                         if turn == "white":
        #                             king = board1.kingW.copy()
        #                             board1.kingW = [mc, mr]
        #                         else:
        #                             king = board1.kingB.copy()
        #                             board1.kingB = [mc, mr]

        #                     temp = board1.board[mr][mc]
        #                     board1.board[mr][mc] = board1.board[r][c]
        #                     board1.board[r][c] = 0
        #                     isCheck = board1.isCheck()

        #                     if pc.identifier == "king":
        #                         if turn == "white":
        #                             board1.kingW = king
        #                         else:
        #                             board1.kingB = king
        #                     # board1.printBoard()
        #                     # x = input()
        #                     # if x == 1:
        #                     #     break
        #                     # print(isCheck)
        #                     if isCheck:
        #                         # print("Checked");
        #                         board1.board[r][c] = board1.board[mr][mc]
        #                         board1.board[mr][mc] = temp
        #                         os.system("cls")
        #                         print("Checked!")
        #                         break

        #                     board1.board[mr][mc].col = mc
        #                     board1.board[mr][mc].row = mr
        #                     board1.board[mr][mc].counter += 1
        #                     board1.count += 1

        #                     if board1.turn == "white":
        #                         board1.turn = "black"
        #                     else:
        #                         board1.turn = "white"

        #                     if board1.board[mr][mc].identifier == "king":
        #                         if board1.board[mr][mc].team == "white":
        #                             board1.kingW = [mc, mr]
        #                         else:
        #                             board1.kingB = [mc, mr]

        #                     if turn == "white":
        #                         board1.moveW.append(f"{piece} {move}")
        #                     else:
        #                         board1.moveB.append(f"{piece} {move}")
        #                     os.system("cls")
        #                 else:
        #                     os.system("cls")
        #                     print("Invalid move for selected piece. Please try again")

        #         f.flush()
        #         f.close()
        #         sys.stdout.flush()

        # while True:

        #     board1.printBoard()

        #     turn = board1.turn

        #     f = open(filename, "a")

        #     if board1.isCheckmate():
        #         print("Checkmate!")
        #         if turn == "white":
        #             print("Black Wins!\n")
        #         else:
        #             print("White Wins!\n")

        #         board1.printMoves()
        #         break
        #     # print(f"KingW: {board1.kingW}, KingB: {board1.kingB}")
        #     print(f"{turn} to move")

        #     piece = input("Choose piece (eg; d2 | to exit input 'exit'): ")
        #     if piece == "exit":
        #         os.system("cls")
        #         break

        #     coords = list(piece)

        #     abort = getTrueCoords(coords)

        #     if abort == 1:
        #         os.system("cls")
        #         print("Invalid input")
        #         continue

        #     c = coords[0]
        #     r = coords[1]

        #     # c = ord(coords[0]);
        #     # r = 8 - int(coords[1]);

        #     # if c >= 65 and c <= 72:
        #     #     c = 8 - (c - 64);
        #     # elif c >= 97 and c <= 104:
        #     #     c = c - 97;
        #     # else:
        #     #     print("Invalid coordinates");

        #     move = ""

        #     if board1.board[r][c] != 0:
        #         if board1.board[r][c].team == turn:
        #             move = input("Choose square to move (eg; d4): ")
        #         else:
        #             os.system("cls")
        #             print("You cannot move your opponent's pieces")
        #     else:
        #         os.system("cls")
        #         print(
        #             "There is no chess piece on the selected coordinate. Please try again"
        #         )
        #         continue

        #     if (move) != "":
        #         mCoords = list(move)

        #         abort = getTrueCoords(mCoords)

        #         if abort == 1:
        #             print("Invalid input")
        #             continue

        #         mc = mCoords[0]
        #         mr = mCoords[1]

        #         pc = board1.board[r][c]

        #         # enemy = False
        #         if board1.board[mr][mc] != 0:
        #             # if board1.board[mr][mc].team != pc.team:
        #             # enemy = True
        #             if board1.board[mr][mc].team == pc.team:
        #                 os.system("cls")
        #                 print("Destination Square Occupied")
        #                 continue

        #         valid = pc.checkvalid(piece, move, coords, mCoords)

        #         if valid:

        #             king = [0, 0]

        #             if pc.identifier == "king":
        #                 if turn == "white":
        #                     king = board1.kingW.copy()
        #                     board1.kingW = [mc, mr]
        #                 else:
        #                     king = board1.kingB.copy()
        #                     board1.kingB = [mc, mr]

        #             temp = board1.board[mr][mc]
        #             board1.board[mr][mc] = board1.board[r][c]
        #             board1.board[r][c] = 0
        #             isCheck = board1.isCheck()

        #             if pc.identifier == "king":
        #                 if turn == "white":
        #                     board1.kingW = king
        #                 else:
        #                     board1.kingB = king
        #             # board1.printBoard()
        #             # x = input()
        #             # if x == 1:
        #             #     break
        #             # print(isCheck)
        #             if isCheck:
        #                 # print("Checked");
        #                 board1.board[r][c] = board1.board[mr][mc]
        #                 board1.board[mr][mc] = temp
        #                 os.system("cls")
        #                 print("Checked!")
        #                 continue

        #             board1.board[mr][mc].col = mc
        #             board1.board[mr][mc].row = mr
        #             board1.board[mr][mc].counter += 1
        #             board1.count += 1

        #             if board1.turn == "white":
        #                 board1.turn = "black"
        #             else:
        #                 board1.turn = "white"

        #             if board1.board[mr][mc].identifier == "king":
        #                 if board1.board[mr][mc].team == "white":
        #                     board1.kingW = [mc, mr]
        #                 else:
        #                     board1.kingB = [mc, mr]

        #             if turn == "white":
        #                 board1.moveW.append(f"{piece} {move}")
        #             else:
        #                 board1.moveB.append(f"{piece} {move}")

        #             f.write(f"{piece} {move}\n")
        #             f.close()
        #             os.system("cls")
        #         else:
        #             os.system("cls")
        #             print("Invalid move for selected piece. Please try again")
        # f.flush()
        # f.close()
        # sys.stdout.flush()
        # f.close()
        # break
        # else:
        #     print("File with that name does not exist. Please try again")
    elif choice == 3:
        break
    else:
        os.system("cls")
        print("Invalid input. Please enter a number between 1 and 3")
