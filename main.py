from array import *
import sys
import os


def getTrueCoords(coords):

    if isinstance(coords[0], str):
        coords[0] = ord(coords[0])
        coords[1] = 8 - int(coords[1])

    else:
        coords[1] = 8 - coords[1]

    if coords[0] >= 65 and coords[0] <= 72:
        coords[0] = coords[0] - 65
    elif coords[0] >= 97 and coords[0] <= 104:
        coords[0] = coords[0] - 97
    else:
        print("Invalid coordinates")
        return 1


def finish():
    x = input("Please press Enter to continue")
    os.system("cls")


class ChessBoard:

    rows, cols = (8, 8)

    board = []
    board = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(rows)]
    count = 0
    kingB = [4, 0]
    kingW = [4, 7]
    turn = "white"
    moveW = []
    moveB = []

    def __init__(self):

        board = self.board

        for i in range(8):
            board[1][i] = Pawn("black", 1, i)

        for i in range(8):
            board[6][i] = Pawn("white", 6, i)

        board[0][0], board[0][7] = (Rook("black", 0, 0), Rook("black", 0, 7))
        board[7][0], board[7][7] = (Rook("white", 7, 0), Rook("white", 7, 7))

        board[0][1], board[0][6] = (Knight("black", 0, 1), Knight("black", 0, 6))
        board[7][1], board[7][6] = (Knight("white", 7, 1), Knight("white", 7, 6))

        board[0][2], board[0][5] = (Bishop("black", 0, 2), Bishop("black", 0, 5))
        board[7][2], board[7][5] = (Bishop("white", 7, 2), Bishop("white", 7, 5))

        board[0][3], board[0][4] = (Queen("black", 0, 3), King("black", 0, 4))
        board[7][3], board[7][4] = (Queen("white", 7, 3), King("white", 7, 4))

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
                        coords = [j, i]
                        src = [piece.col + 65, 8 - piece.row]
                        # print(f"{piece.identifier} {src}")
                        if team == "white":
                            dest = [self.kingW[0] + 65, 8 - self.kingW[1]]
                            # print(dest)
                            check = piece.checkvalid(src, dest, coords, self.kingW)
                            # print(f"isCheck {piece.identifier} {src} {dest} {check}")
                            if check:
                                # print("if check? break")
                                break
                        if team == "black":
                            dest = [self.kingB[0] + 65, 8 - self.kingB[1]]
                            # print(f"isCheck {piece.identifier} {src} {dest} {check}")
                            check = piece.checkvalid(src, dest, coords, self.kingB)
                if check:
                    # print("if check? break")
                    break
        # print(check)
        return check

    def isCheckmate(self):

        if not self.isCheck():
            return False
        else:

            team = self.turn
            king = [0, 0]

            if team == "white":
                king = self.kingW.copy()
            else:
                king = self.kingB.copy()

            # kingPc = self.board[king[1]][king[0]]

            # sq2 = [king[0] + 1, king[1]]
            # sq3 = [king[0] - 1, king[1]]
            # sq4 = [king[0], king[1] + 1]
            # sq5 = [king[0], king[1] - 1]
            # sq6 = [king[0] + 1, king[1] + 1]
            # sq7 = [king[0] + 1, king[1] - 1]
            # sq8 = [king[0] - 1, king[1] + 1]
            # sq9 = [king[0] - 1, king[1] - 1]

            # squares = [sq2, sq3, sq4, sq5, sq6, sq7, sq8, sq9]
            # squares[:] = filterfalse(
            #     lambda i: (i[0] < 0 or i[0] > 7 or i[1] < 0 or i[1] > 7)
            #     or self.board[i[1]][i[0]] != 0,
            #     squares,
            # )

            # print(squares)
            check = True
            for i in range(8):
                if not check:
                    break
                for j in range(8):
                    if not check:
                        break
                    piece = self.board[i][j]
                    if piece != 0:
                        if piece.team == team:

                            for c in range(8):
                                if not check:
                                    break
                                for r in range(8):
                                    coords = [j, i]
                                    dest = [c + 65, 8 - r]
                                    src = [piece.col + 65, 8 - piece.row]

                                    if self.board[r][c] != 0:
                                        if self.board[r][c].team == team:
                                            continue

                                    if coords[0] == c and coords[1] == r:
                                        continue

                                    valid = piece.checkvalid(src, dest, coords, [c, r])

                                    if valid:
                                        temp = board1.board[r][c]
                                        board1.board[r][c] = board1.board[coords[1]][
                                            coords[0]
                                        ]
                                        board1.board[coords[1]][coords[0]] = 0
                                        if board1.board[r][c].identifier == "king":
                                            if board1.board[r][c].team == "white":
                                                board1.kingW = [c, r]
                                            else:
                                                board1.kingB = [c, r]
                                        # self.printBoard()
                                        check = board1.isCheck()
                                        # print(
                                        #     f"isCheckmate {piece.identifier} {src} {dest} {check}"
                                        # )
                                        board1.board[coords[1]][
                                            coords[0]
                                        ] = board1.board[r][c]
                                        board1.board[r][c] = temp

                                        if board1.board[coords[1]][coords[0]] != 0:
                                            if (
                                                board1.board[coords[1]][
                                                    coords[0]
                                                ].identifier
                                                == "king"
                                            ):
                                                if (
                                                    board1.board[coords[1]][
                                                        coords[0]
                                                    ].team
                                                    == "white"
                                                ):
                                                    board1.kingW = king
                                                else:
                                                    board1.kingB = king

                                        if not check:
                                            break

            if check == False:
                return False
            else:
                return True

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


class Piece:

    identifier = "piece"
    team = ""
    symbolB = ""
    symbolW = ""
    counter = 0
    row = 0
    col = 0
    srcC = [0, 0]
    destC = [0, 0]

    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col

    def initCoords(self, src, dest):
        srcC = []
        destC = []
        if not isinstance(src, list):
            srcC = list(src)
        else:
            srcC = src

        if not isinstance(dest, list):
            destC = list(dest)
        else:
            destC = dest

        # print(f"init {srcC} {destC}")
        # print(srcC);
        # print(destC);
        if isinstance(srcC[0], str):
            self.srcC[0] = ord(srcC[0])
        else:
            self.srcC[0] = srcC[0]
        self.srcC[1] = int(srcC[1])
        if isinstance(destC[0], str):
            self.destC[0] = ord(destC[0])
        else:
            self.destC[0] = destC[0]
        self.destC[1] = int(destC[1])
        # print(f"init {self.srcC} {self.destC}")
        # print(self.srcC);
        # print(self.destC);


class Pawn(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "pawn"
        self.symbolB = "♙"
        self.symbolW = "♟"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC

        team = self.team

        if team == "white":
            if self.counter > 0:
                if (destC[1] - srcC[1]) != 1:
                    return False
            elif (destC[1] - srcC[1]) > 2 or (destC[1] - srcC[1]) < 1:
                return False

        if team == "black":
            if self.counter > 0:
                if (destC[1] - srcC[1]) != -1:
                    return False
            elif (destC[1] - srcC[1]) < -2 or (destC[1] - srcC[1]) > -1:
                return False

        if srcC[0] != destC[0]:
            if abs(destC[0] - srcC[0]) != 1 or abs(destC[1] - srcC[1]) != 1:
                return False
            elif board1.board[mCoords[1]][mCoords[0]] == 0:
                return False
        elif board1.board[mCoords[1]][mCoords[0]] != 0:
            return False

        return True


class Rook(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "rook"
        self.symbolB = "♖"
        self.symbolW = "♜"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC
        c = coords[0]
        r = coords[1]
        mc = mCoords[0]
        mr = mCoords[1]

        team = self.team

        if (srcC[0] != destC[0]) and (srcC[1] != destC[1]):
            return False

        if (c != mc) and (abs(mc - c) > 1):
            if mc > c:
                for i in range(c + 1, mc):
                    if board1.board[r][i] != 0:
                        return False
            else:
                for i in range(mc + 1, c):
                    if board1.board[r][i] != 0:
                        return False

        if (r != mr) and (abs(mr - r) > 1):
            if mr > r:
                for i in range(r + 1, mr):
                    if board1.board[i][c] != 0:
                        return False
            else:
                for i in range(mr + 1, r):
                    if board1.board[i][c] != 0:
                        return False

        return True


class Knight(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "knight"
        self.symbolB = "♘"
        self.symbolW = "♞"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC
        c = coords[0]
        r = coords[1]
        mc = mCoords[0]
        mr = mCoords[1]

        team = self.team

        if abs(destC[0] - srcC[0]) == 2:
            if abs(destC[1] - srcC[1]) == 1:
                return True

        if abs(destC[0] - srcC[0]) == 1:
            if abs(destC[1] - srcC[1]) == 2:
                return True

        return False


class Bishop(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "bishop"
        self.symbolB = "♗"
        self.symbolW = "♝"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC

        c = coords[0]
        r = coords[1]
        mc = mCoords[0]
        mr = mCoords[1]

        team = self.team

        # print(srcC, destC)

        if abs(destC[0] - srcC[0]) != abs(destC[1] - srcC[1]):
            # print("287")
            return False

        cd = 0
        rd = 0

        if destC[0] > srcC[0]:
            cd = 1
        else:
            cd = -1

        if destC[1] > srcC[1]:
            rd = 1
        else:
            rd = -1

        srcC[0] += cd
        srcC[1] += rd

        while srcC[0] != destC[0]:
            srcTC = srcC.copy()
            getTrueCoords(srcTC)
            # print(f"srcC: {srcC}, srcTC: {srcTC}, destC: {destC}")
            # print(f"srcCol = {srcC[0]}, srcRow = {srcC[1]}, destCol = {destC[0]}, destRow = {destC[1]}")
            # print(f"srcTCol = {srcTC[0]}, srcTRow = {srcTC[1]}")
            # print(board1.board[srcTC[1]][srcTC[0]])
            if board1.board[srcTC[1]][srcTC[0]] != 0:
                # print("314")
                return False
            srcC[0] += cd
            srcC[1] += rd

        return True


class Queen(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "queen"
        self.symbolB = "♕"
        self.symbolW = "♛"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC
        c = coords[0]
        r = coords[1]
        mc = mCoords[0]
        mr = mCoords[1]

        team = self.team

        if (srcC[0] != destC[0]) and (srcC[1] != destC[1]):
            if abs(destC[0] - srcC[0]) != abs(destC[1] - srcC[1]):
                return False

            cd = 0
            rd = 0

            if destC[0] > srcC[0]:
                cd = 1
            else:
                cd = -1

            if destC[1] > srcC[1]:
                rd = 1
            else:
                rd = -1

            srcC[0] += cd
            srcC[1] += rd

            while srcC[0] != destC[0]:
                srcTC = srcC.copy()
                getTrueCoords(srcTC)
                # print(f"srcCol = {srcC[0]}, srcRow = {srcC[1]}, destCol = {destC[0]}, destRow = {destC[1]}")
                # print(f"srcTCol = {srcTC[0]}, srcTRow = {srcTC[1]}")
                # print(board1.board[srcTC[1]][srcTC[0]])
                if board1.board[srcTC[1]][srcTC[0]] != 0:
                    return False
                srcC[0] += cd
                srcC[1] += rd

            return True

        if (c != mc) and (abs(mc - c) > 1):
            if mc > c:
                for i in range(c + 1, mc):
                    if board1.board[r][i] != 0:
                        return False
            else:
                for i in range(mc + 1, c):
                    if board1.board[r][i] != 0:
                        return False

        if (r != mr) and (abs(mr - r) > 1):
            if mr > r:
                for i in range(r + 1, mr):
                    if board1.board[i][c] != 0:
                        return False
            else:
                for i in range(mr + 1, r):
                    if board1.board[i][c] != 0:
                        return False

        return True


class King(Piece):
    def __init__(self, team, row, col):
        Piece.__init__(self, team, row, col)
        self.identifier = "king"
        self.symbolB = "♔"
        self.symbolW = "♚"

    def checkvalid(self, src, dest, coords, mCoords):

        self.initCoords(src, dest)

        srcC = self.srcC
        destC = self.destC
        c = coords[0]
        r = coords[1]
        mc = mCoords[0]
        mr = mCoords[1]

        team = self.team

        if (abs(destC[0] - srcC[0])) > 1 or (abs(destC[1] - srcC[1])) > 1:
            return False

        return True


###########################################################################

board1 = ChessBoard()

while True:

    print("MAIN MENU\n")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = int(input("Input number to select: "))

    if choice == 1:

        board1 = ChessBoard()

        x = 1
        while True:
            if not os.path.isfile(f"game-{x}.txt"):
                break
            else:
                x += 1

        f = open(f"game-{x}.txt", "w")

        while True:

            board1.printBoard()

            turn = board1.turn

            f = open(f"game-{x}.txt", "a")

            if board1.isCheckmate():
                print("Checkmate!")
                if turn == "white":
                    print("Black Wins!\n")
                else:
                    print("White Wins!\n")

                board1.printMoves()
                break
            # print(f"KingW: {board1.kingW}, KingB: {board1.kingB}")
            print(f"{turn} to move")

            piece = input("Choose piece (eg; d2 | to exit input 'exit'): ")
            if piece == "exit":
                break

            coords = list(piece)

            abort = getTrueCoords(coords)

            if abort == 1:
                os.system("cls")
                print("Invalid input")
                continue

            c = coords[0]
            r = coords[1]

            # c = ord(coords[0]);
            # r = 8 - int(coords[1]);

            # if c >= 65 and c <= 72:
            #     c = 8 - (c - 64);
            # elif c >= 97 and c <= 104:
            #     c = c - 97;
            # else:
            #     print("Invalid coordinates");

            move = ""

            if board1.board[r][c] != 0:
                if board1.board[r][c].team == turn:
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
                mCoords = list(move)

                abort = getTrueCoords(mCoords)

                if abort == 1:
                    print("Invalid input")
                    continue

                mc = mCoords[0]
                mr = mCoords[1]

                pc = board1.board[r][c]

                # enemy = False
                if board1.board[mr][mc] != 0:
                    # if board1.board[mr][mc].team != pc.team:
                    # enemy = True
                    if board1.board[mr][mc].team == pc.team:
                        os.system("cls")
                        print("Destination Square Occupied")
                        continue

                valid = pc.checkvalid(piece, move, coords, mCoords)

                if valid:

                    king = [0, 0]

                    if pc.identifier == "king":
                        if turn == "white":
                            king = board1.kingW.copy()
                            board1.kingW = [mc, mr]
                        else:
                            king = board1.kingB.copy()
                            board1.kingB = [mc, mr]

                    temp = board1.board[mr][mc]
                    board1.board[mr][mc] = board1.board[r][c]
                    board1.board[r][c] = 0
                    isCheck = board1.isCheck()

                    if pc.identifier == "king":
                        if turn == "white":
                            board1.kingW = king
                        else:
                            board1.kingB = king
                    # board1.printBoard()
                    # x = input()
                    # if x == 1:
                    #     break
                    # print(isCheck)
                    if isCheck:
                        # print("Checked");
                        board1.board[r][c] = board1.board[mr][mc]
                        board1.board[mr][mc] = temp
                        os.system("cls")
                        print("Checked!")
                        continue

                    board1.board[mr][mc].col = mc
                    board1.board[mr][mc].row = mr
                    board1.board[mr][mc].counter += 1
                    board1.count += 1

                    if board1.turn == "white":
                        board1.turn = "black"
                    else:
                        board1.turn = "white"

                    if board1.board[mr][mc].identifier == "king":
                        if board1.board[mr][mc].team == "white":
                            board1.kingW = [mc, mr]
                        else:
                            board1.kingB = [mc, mr]

                    if turn == "white":
                        board1.moveW.append(f"{piece} {move}")
                    else:
                        board1.moveB.append(f"{piece} {move}")

                    f.write(f"{piece} {move}\n")
                    f.close()
                    os.system("cls")
                else:
                    os.system("cls")
                    print("Invalid move for selected piece. Please try again")
    elif choice == 2:
        os.system("cls")
        path = os.getcwd()
        onlyfiles = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]
        onlyfiles.remove("main.py")
        onlyfiles.remove(".gitignore")
        onlyfiles.remove("LICENSE")
        onlyfiles.remove("README.md")

        print("List of available files:\n")
        for file in onlyfiles:
            print(file)

        while True:
            filename = input(
                "\nInput file name to load the desired file(eg: game-1.txt): "
            )

            if os.path.isfile(filename):

                board1 = ChessBoard()

                f = open(filename, "r")
                lines = f.readlines()

                for line in lines:
                    board1.printBoard()

                    steps = line.split()

                    turn = board1.turn

                    if board1.isCheckmate():
                        print("Checkmate!")
                        if turn == "white":
                            print("Black Wins!\n")
                        else:
                            print("White Wins!\n")

                        board1.printMoves()
                        break

                    # print(f"KingW: {board1.kingW}, KingB: {board1.kingB}")
                    # print(f"{turn} to move")

                    piece = steps[0]
                    if piece == "exit":
                        os.system("cls")
                        break

                    coords = list(piece)

                    abort = getTrueCoords(coords)

                    if abort == 1:
                        os.system("cls")
                        print("Invalid input")
                        break

                    c = coords[0]
                    r = coords[1]

                    # c = ord(coords[0]);
                    # r = 8 - int(coords[1]);

                    # if c >= 65 and c <= 72:
                    #     c = 8 - (c - 64);
                    # elif c >= 97 and c <= 104:
                    #     c = c - 97;
                    # else:
                    #     print("Invalid coordinates");

                    move = ""

                    if board1.board[r][c] != 0:
                        if board1.board[r][c].team == turn:
                            move = steps[1]
                        else:
                            os.system("cls")
                            print("You cannot move your opponent's pieces")
                            break
                    else:
                        os.system("cls")
                        print(
                            "There is no chess piece on the selected coordinate. Please try again"
                        )
                        break

                    if (move) != "":
                        mCoords = list(move)

                        abort = getTrueCoords(mCoords)

                        if abort == 1:
                            print("Invalid input")
                            break

                        mc = mCoords[0]
                        mr = mCoords[1]

                        pc = board1.board[r][c]

                        # enemy = False
                        if board1.board[mr][mc] != 0:
                            # if board1.board[mr][mc].team != pc.team:
                            # enemy = True
                            if board1.board[mr][mc].team == pc.team:
                                os.system("cls")
                                print("Destination Square Occupied")
                                break

                        valid = pc.checkvalid(piece, move, coords, mCoords)

                        if valid:

                            king = [0, 0]

                            if pc.identifier == "king":
                                if turn == "white":
                                    king = board1.kingW.copy()
                                    board1.kingW = [mc, mr]
                                else:
                                    king = board1.kingB.copy()
                                    board1.kingB = [mc, mr]

                            temp = board1.board[mr][mc]
                            board1.board[mr][mc] = board1.board[r][c]
                            board1.board[r][c] = 0
                            isCheck = board1.isCheck()

                            if pc.identifier == "king":
                                if turn == "white":
                                    board1.kingW = king
                                else:
                                    board1.kingB = king
                            # board1.printBoard()
                            # x = input()
                            # if x == 1:
                            #     break
                            # print(isCheck)
                            if isCheck:
                                # print("Checked");
                                board1.board[r][c] = board1.board[mr][mc]
                                board1.board[mr][mc] = temp
                                os.system("cls")
                                print("Checked!")
                                break

                            board1.board[mr][mc].col = mc
                            board1.board[mr][mc].row = mr
                            board1.board[mr][mc].counter += 1
                            board1.count += 1

                            if board1.turn == "white":
                                board1.turn = "black"
                            else:
                                board1.turn = "white"

                            if board1.board[mr][mc].identifier == "king":
                                if board1.board[mr][mc].team == "white":
                                    board1.kingW = [mc, mr]
                                else:
                                    board1.kingB = [mc, mr]

                            if turn == "white":
                                board1.moveW.append(f"{piece} {move}")
                            else:
                                board1.moveB.append(f"{piece} {move}")
                            os.system("cls")
                        else:
                            os.system("cls")
                            print("Invalid move for selected piece. Please try again")

                f.flush()
                f.close()
                sys.stdout.flush()

                while True:

                    board1.printBoard()

                    turn = board1.turn

                    f = open(filename, "a")

                    if board1.isCheckmate():
                        print("Checkmate!")
                        if turn == "white":
                            print("Black Wins!\n")
                        else:
                            print("White Wins!\n")

                        board1.printMoves()
                        break
                    # print(f"KingW: {board1.kingW}, KingB: {board1.kingB}")
                    print(f"{turn} to move")

                    piece = input("Choose piece (eg; d2 | to exit input 'exit'): ")
                    if piece == "exit":
                        os.system("cls")
                        break

                    coords = list(piece)

                    abort = getTrueCoords(coords)

                    if abort == 1:
                        os.system("cls")
                        print("Invalid input")
                        continue

                    c = coords[0]
                    r = coords[1]

                    # c = ord(coords[0]);
                    # r = 8 - int(coords[1]);

                    # if c >= 65 and c <= 72:
                    #     c = 8 - (c - 64);
                    # elif c >= 97 and c <= 104:
                    #     c = c - 97;
                    # else:
                    #     print("Invalid coordinates");

                    move = ""

                    if board1.board[r][c] != 0:
                        if board1.board[r][c].team == turn:
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
                        mCoords = list(move)

                        abort = getTrueCoords(mCoords)

                        if abort == 1:
                            print("Invalid input")
                            continue

                        mc = mCoords[0]
                        mr = mCoords[1]

                        pc = board1.board[r][c]

                        # enemy = False
                        if board1.board[mr][mc] != 0:
                            # if board1.board[mr][mc].team != pc.team:
                            # enemy = True
                            if board1.board[mr][mc].team == pc.team:
                                os.system("cls")
                                print("Destination Square Occupied")
                                continue

                        valid = pc.checkvalid(piece, move, coords, mCoords)

                        if valid:

                            king = [0, 0]

                            if pc.identifier == "king":
                                if turn == "white":
                                    king = board1.kingW.copy()
                                    board1.kingW = [mc, mr]
                                else:
                                    king = board1.kingB.copy()
                                    board1.kingB = [mc, mr]

                            temp = board1.board[mr][mc]
                            board1.board[mr][mc] = board1.board[r][c]
                            board1.board[r][c] = 0
                            isCheck = board1.isCheck()

                            if pc.identifier == "king":
                                if turn == "white":
                                    board1.kingW = king
                                else:
                                    board1.kingB = king
                            # board1.printBoard()
                            # x = input()
                            # if x == 1:
                            #     break
                            # print(isCheck)
                            if isCheck:
                                # print("Checked");
                                board1.board[r][c] = board1.board[mr][mc]
                                board1.board[mr][mc] = temp
                                os.system("cls")
                                print("Checked!")
                                continue

                            board1.board[mr][mc].col = mc
                            board1.board[mr][mc].row = mr
                            board1.board[mr][mc].counter += 1
                            board1.count += 1

                            if board1.turn == "white":
                                board1.turn = "black"
                            else:
                                board1.turn = "white"

                            if board1.board[mr][mc].identifier == "king":
                                if board1.board[mr][mc].team == "white":
                                    board1.kingW = [mc, mr]
                                else:
                                    board1.kingB = [mc, mr]

                            if turn == "white":
                                board1.moveW.append(f"{piece} {move}")
                            else:
                                board1.moveB.append(f"{piece} {move}")

                            f.write(f"{piece} {move}\n")
                            f.close()
                            os.system("cls")
                        else:
                            os.system("cls")
                            print("Invalid move for selected piece. Please try again")
                f.flush()
                f.close()
                sys.stdout.flush()
                f.close()
                break
            else:
                print("File with that name does not exist. Please try again")
    elif choice == 3:
        break
    else:
        os.system("cls")
        print("Invalid input. Please enter a number between 1 and 3")
