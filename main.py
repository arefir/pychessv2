from array import *
import sys
import os


def parseCoords(row, col):

    # print(f"row: {row} col: {col}")

    try:
        row = 8 - int(row)
        col = ord(col)
    except:
        return 1

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


def finish():
    x = input("Please press Enter to continue")
    os.system("cls")


rows, cols = (8, 8)


class ChessBoard:
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

                        king = self.findKing(team)
                        if king == 1:
                            print("king not found")
                            os.system("exit")

                        check = piece.checkvalid(king.row, king.col)
                        # print(f"isCheck {piece.identifier} {src} {dest} {check}")
                        if check:
                            # print("if check? break")
                            return check

        # print(check)
        return check

    # CHECK FOR CHECKMATE
    def isCheckmate(self):

        if not self.isCheck():
            return False
        else:

            team = self.turn

            check = True
            for i in range(8):
                for j in range(8):

                    piece = self.board[i][j]
                    if piece != 0:
                        if piece.team == team:

                            for r in range(8):
                                for c in range(8):

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

                                        # print("TEMPBOARD\n")
                                        # self.printBoard()
                                        check = self.isCheck()
                                        # print(
                                        #     f"isCheckmate {piece.identifier} src:{piece.row} {piece.col} des:{r} {c} {check}"
                                        # )

                                        piece = self.board[r][c]
                                        piece.move(i, j)
                                        self.board[r][c] = temp

                                        if not check:
                                            return False

            if check == False:
                return False
            else:
                return True

    # CHECK DRAW
    def isDraw(self):

        white, black = False, False
        wKnight, wBishop, wOthers = 0, 0, 0
        bKnight, bBishop, bOthers = 0, 0, 0
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]

                if piece != 0:
                    if piece.identifier == "knight":
                        if piece.team == "white":
                            wKnight += 1
                        else:
                            bKnight += 1
                    elif piece.identifier == "bishop":
                        if piece.team == "white":
                            wBishop += 1
                        else:
                            bBishop += 1
                    elif piece.identifier == "king":
                        continue
                    else:
                        if piece.team == "white":
                            wOthers += 1
                        else:
                            bOthers += 1

        if (
            (wKnight == 1 and wOthers == 0 and wBishop == 0)
            or (wKnight == 0 and wOthers == 0 and wBishop == 1)
            or (wKnight == 0 and wOthers == 0 and wBishop == 0)
        ):
            white = True
        if (
            (bKnight == 1 and bOthers == 0 and bBishop == 0)
            or (bKnight == 0 and bOthers == 0 and bBishop == 1)
            or (bKnight == 0 and bOthers == 0 and bBishop == 0)
        ):
            black = True

        if white and black:
            return True

        if self.isCheck():
            return False
        else:
            team = self.turn

            for i in range(8):

                for j in range(8):

                    piece = self.board[i][j]
                    if piece != 0:
                        if piece.team == team:

                            for r in range(8):
                                for c in range(8):

                                    if self.board[r][c] != 0:
                                        if self.board[r][c].team == team:
                                            continue

                                    if r == i and c == j:
                                        continue

                                    valid = piece.checkvalid(r, c)

                                    if valid:
                                        temp = self.board[r][c]
                                        piece.move(r, c)

                                        # print("TEMPBOARD\n")
                                        # self.printBoard()
                                        check = self.isCheck()
                                        # print(
                                        #     f"isDraw {piece.identifier} src:{piece.row} {piece.col} des:{r} {c} {check}"
                                        # )

                                        piece = self.board[r][c]
                                        piece.move(i, j)
                                        self.board[r][c] = temp

                                        if not check:
                                            return False

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

                try:
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
                        try:
                            coords = parseCoords(coords[1], coords[0])
                        except:
                            os.system("cls")
                            print(
                                "This file could not be loaded, Please make sure it is a valid save file"
                            )
                            return 1

                        if coords == 1:
                            os.system("cls")
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
                            try:
                                coords = parseCoords(coords[1], coords[0])
                            except:
                                coords = 1

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

                                temp = self.board[mr][mc]
                                pc.move(mr, mc)
                                pc = self.board[mr][mc]
                                isCheck = self.isCheck()

                                if isCheck:
                                    # print("Checked");
                                    pc.move(r, c)
                                    self.board[mr][mc] = temp
                                    os.system("cls")
                                    print("Checked!")
                                    continue

                                if self.board[mr][mc].identifier == "pawn":
                                    if self.board[mr][mc].enPassant != "":
                                        self.board[mr][mc].enPassant = ""
                                        if turn == "white":
                                            self.board[mr + 1][mc] = 0
                                        if turn == "black":
                                            self.board[mr - 1][mc] = 0

                                pc.counter += 1
                                self.count += 1

                                if self.turn == "white":
                                    self.turn = "black"
                                else:
                                    self.turn = "white"

                                if turn == "white":
                                    self.moveW.append(f"{piece} {move}")
                                else:
                                    self.moveB.append(f"{piece} {move}")
                                os.system("cls")
                            else:
                                os.system("cls")
                                print(
                                    "Invalid move for selected piece. Please try again"
                                )

                    f.flush()
                    f.close()
                    sys.stdout.flush()
                    break
                except:
                    print(
                        "This file could not be loaded, Please make sure it is a valid save file"
                    )
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
            try:
                coords = parseCoords(coords[1], coords[0])
            except:
                coords = 1

            if coords == 1:
                os.system("cls")
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
                try:
                    coords = parseCoords(coords[1], coords[0])
                except:
                    coords = 1

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

                    temp = self.board[mr][mc]
                    pc.move(mr, mc)
                    pc = self.board[mr][mc]
                    isCheck = self.isCheck()

                    if isCheck:
                        # print("Checked");

                        pc.move(r, c)
                        self.board[mr][mc] = temp
                        os.system("cls")
                        print("Checked!")
                        continue

                    if self.board[mr][mc].identifier == "pawn":
                        if self.board[mr][mc].enPassant != "":
                            self.board[mr][mc].enPassant = ""
                            if turn == "white":
                                self.board[mr + 1][mc] = 0
                            if turn == "black":
                                self.board[mr - 1][mc] = 0
                    pc.counter += 1
                    self.count += 1

                    if self.turn == "white":
                        self.turn = "black"
                    else:
                        self.turn = "white"

                    if turn == "white":
                        self.moveW.append(f"{piece} {move}")
                    else:
                        self.moveB.append(f"{piece} {move}")

                    f.write(f"{piece} {move}\n")
                    f.close()
                    os.system("cls")
                else:
                    os.system("cls")
                    print("Invalid move for selected piece. Please try again")


class Piece:
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


class Pawn(Piece):
    def __init__(self, team, row, col, board):
        Piece.__init__(self, team, row, col, board)
        self.identifier = "pawn"
        self.symbolB = "♙"
        self.symbolW = "♟"
        self.enPassant = ""

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
                if col + 1 < cols:
                    if self.board[row][col + 1] != 0:
                        if self.board[row][col + 1].identifier == "pawn":
                            self.board[row][col + 1].enPassant = [row + 1, col]
                if col - 1 >= 0:
                    if self.board[row][col - 1] != 0:
                        if self.board[row][col - 1].identifier == "pawn":
                            self.board[row][col - 1].enPassant = [row + 1, col]

        if team == "black":
            if self.counter > 0:
                if (row - self.row) != 1:
                    return False
            elif (row - self.row) > 2 or (row - self.row) < 1:
                return False
            if (row - self.row) == 2:
                if self.board[row - 1][col] != 0:
                    return False
                if col + 1 < cols:
                    if self.board[row][col + 1] != 0:
                        if self.board[row][col + 1].identifier == "pawn":
                            self.board[row][col + 1].enPassant = [row - 1, col]
                if col - 1 >= 0:
                    if self.board[row][col - 1] != 0:
                        if self.board[row][col - 1].identifier == "pawn":
                            self.board[row][col - 1].enPassant = [row - 1, col]

        # print(f"enpassant: {self.enPassant}")
        # print(f"{row} {col}")

        if self.col != col:
            if self.enPassant != 0 and self.enPassant != "":
                if row == self.enPassant[0] and col == self.enPassant[1]:
                    return True
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

        while tempCol != col:

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

            while tempCol != col:

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

        if self.counter < 1:
            if self.team == "white":
                if row == 7 and col == 2:
                    if self.board[7][0] != 0:
                        if (
                            self.board[7][0].identifier == "rook"
                            and self.board[7][0].counter < 1
                        ):
                            for i in range(1, self.col):
                                if self.board[row][i] != 0:
                                    return False
                            self.board[7][0].counter += 1
                            self.board[7][0].move(7, 3)
                            return True
                if row == 7 and col == 6:
                    if self.board[7][7] != 0:
                        if (
                            self.board[7][7].identifier == "rook"
                            and self.board[7][7].counter < 1
                        ):
                            for i in range(self.col + 1, 7):
                                if self.board[row][i] != 0:
                                    return False
                            self.board[7][7].counter += 1
                            self.board[7][7].move(7, 5)
                            return True
            if self.team == "black":
                if row == 0 and col == 2:
                    if self.board[0][0] != 0:
                        if (
                            self.board[0][0].identifier == "rook"
                            and self.board[0][0].counter < 1
                        ):
                            for i in range(1, self.col):
                                if self.board[row][i] != 0:
                                    return False
                            self.board[0][0].counter += 1
                            self.board[0][0].move(0, 3)
                            self.counter += 1
                            return True
                if row == 0 and col == 6:
                    if self.board[0][7] != 0:
                        if (
                            self.board[0][7].identifier == "rook"
                            and self.board[0][7].counter < 1
                        ):
                            for i in range(self.col + 1, 7):
                                if self.board[row][i] != 0:
                                    return False
                            self.board[0][7].counter += 1
                            self.board[0][7].move(0, 5)
                            self.counter += 1
                            return True

        if (abs(row - self.row)) > 1 or (abs(col - self.col)) > 1:
            return False

        self.counter += 1
        return True


###########################################################################


while True:

    print("MAIN MENU\n")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    try:
        choice = int(input("Input number to select: "))
    except:
        choice = 4

    if choice == 1:
        chessboard1 = ChessBoard()
        chessboard1.new()
        del chessboard1

    elif choice == 2:
        chessboard2 = ChessBoard()
        chessboard2.load()
        del chessboard2

    elif choice == 3:
        break
    else:
        os.system("cls")
        print("Invalid input. Please enter a number between 1 and 3")
