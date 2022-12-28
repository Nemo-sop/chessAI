"""
Esta clase es responsable de almacenar toda la informacion del estado de un juego.
Tambien determina los movimientos validos en cada estado.
Guarda un historial de movimientos
"""


class GameState():
    def __init__(self):
        # TODO [UPGRADE] para hacerlo mas rapido podriamos usar numpy arrays
        # el tablero es de 8x8 representado en un arreglo 2d
        # cada pieza esta representada con dos caracteres, el primero determina el color y el segundo la pieza
        # el "--" representa un espacio vacio
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {
            'P': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves,
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

    '''
    Toma un movimiento como parametro y lo ejecuta, no sirve para algunos movimientos
    como el enroque, promociones, etc
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # update kings location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog[-1]
            self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove  # Switch turns back
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

        else:
            print('Error: No move in the move log!')

    '''
    Funciones para aplicar los movimientos validos
    '''

    # Sin considerar jaques, es decir todos los movimientos que puedo hacer
    # segun las reglas
    def getAllPossibleMoves(self):
        moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                color = self.board[row][col][0]
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]

                    self.moveFunctions[piece](col, row, moves)
                    # if piece == 'P':
                    #     self.getPawnMoves(row, col, moves, color)
                    # if piece == 'R':
                    #     self.getRookMoves(row, col, moves)
                    # if piece == 'N':
                    #     self.getKnightMoves(row, col, moves)
                    # if piece == 'B':
                    #     self.getBishopMoves(row, col, moves)
                    # if piece == 'K':
                    #     self.getKingMoves(row, col, moves)
                    # if piece == 'Q':
                    #     self.getQueenMoves(row, col, moves)

        print('-' * 20)
        for i in moves:
            print(i.getChessNotation())
        print('-' * 20)

        return moves

    # Considerando jaques, es decir toma los movimientos validos y los filtra
    # segun si terminan en un jaque para la persona que esta por mover

    def getValidMoves(self):

        # NAIVE ALGORITHM
        # 1 generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2 for each move, make the move

        # 3 generate all opponents moves
        # 4 for each of your opponents moves, see if they attack your king
        # 5 if they do attack your king, is not a valid move





        return moves



    '''
    moves getters
    '''

    def getPawnMoves(self, col, row, moves):
        limitColLeft = False
        limitColRight = False
        color = self.board[row][col][0]
        if color == 'w':
            if self.board[row - 1][col] == '--':
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--':
                    moves.append(Move((row, col), (row - 2, col), self.board))

            if col == 7:
                limitColRight = True
            elif col == 0:
                limitColLeft = True

            if not limitColLeft and self.board[row - 1][col - 1][0] == 'b':
                moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if not limitColRight and self.board[row - 1][col + 1][0] == 'b':
                moves.append(Move((row, col), (row - 1, col + 1), self.board))



        elif color == 'b':
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col == 7:
                limitColRight = True
            elif col == 0:
                limitColLeft = True

            if not limitColLeft and self.board[row + 1][col - 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col - 1), self.board))

            if not limitColRight and self.board[row + 1][col + 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def getRookMoves(self, col, row, moves):
        color = self.board[row][col][0]

        for i in range(row + 1, 8, 1):
            # osea para abajo
            if self.board[i][col] == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif self.board[i][col][0] != color:
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif self.board[i][col][0] == color:
                break

        for i in range(row - 1, -1, -1):
            # osea para arriba
            if self.board[i][col] == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif self.board[i][col][0] != color:
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif self.board[i][col][0] == color:
                break

        for i in range(col + 1, 8, 1):
            # osea para la derecha
            if self.board[row][i] == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif self.board[row][i][0] != color:
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif self.board[row][i][0] == color:
                break

        for i in range(col - 1, -1, -1):
            # osea para la izquierda
            if self.board[row][i] == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif self.board[row][i][0] != color:
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif self.board[row][i][0] == color:
                break

    def getKnightMoves(self, col, row, moves):
        newpos = [
            # Ls para abajo
            [row + 2, col + 1],
            [row + 2, col - 1],
            # Ls para arriba
            [row - 2, col + 1],
            [row - 2, col - 1],
            # Ls para la derecha
            [row - 1, col + 2],
            [row + 1, col + 2],
            # Ls para la izquierda
            [row - 1, col - 2],
            [row + 1, col - 2],
        ]

        color = self.board[row][col][0]

        for pos in newpos:
            if (7 >= pos[0] >= 0) and (7 >= pos[1] >= 0):
                if self.board[pos[0]][pos[1]] == '--' or self.board[pos[0]][pos[1]][0] != color:
                    moves.append(Move((row, col), (pos[0], pos[1]), self.board))

    def getBishopMoves(self, col, row, moves):
        color = self.board[row][col][0]

        tempCol = col
        end = False
        for i in range(row + 1, 8, 1):
            # osea para abajo y derecha
            for j in range(tempCol + 1, 8, 1):
                if self.board[i][j] == '--' and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    tempCol += 1
                    break
                elif self.board[i][j][0] != color and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    end = True
                    break
                elif self.board[i][j][0] == color and not end:
                    end = True
                    break

        tempCol = col
        end = False
        for i in range(row + 1, 8, 1):
            # osea para abajo y izquierda
            for j in range(tempCol - 1, -1, -1):
                if self.board[i][j] == '--' and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    tempCol -= 1
                    break
                elif self.board[i][j][0] != color and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    end = True
                    break
                elif self.board[i][j][0] == color and not end:
                    end = True
                    break

        tempCol = col
        end = False
        for i in range(row - 1, -1, -1):
            # osea para arriba y derecha
            for j in range(tempCol + 1, 8, 1):
                if self.board[i][j] == '--' and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    tempCol += 1
                    break
                elif self.board[i][j][0] != color and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    end = True
                    break
                elif self.board[i][j][0] == color and not end:
                    end = True
                    break

        tempCol = col
        end = False
        for i in range(row - 1, -1, -1):
            # osea para arriba y izquierda
            for j in range(tempCol - 1, -1, -1):
                if self.board[i][j] == '--' and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    tempCol -= 1
                    break
                elif self.board[i][j][0] != color and not end:
                    moves.append(Move((row, col), (i, j), self.board))
                    end = True
                    break
                elif self.board[i][j][0] == color and not end:
                    end = True
                    break

    def getKingMoves(self, col, row, moves):
        color = self.board[row][col][0]
        newpos = [
            # para abajo
            [row + 1, col + 1],
            [row + 1, col - 1],
            [row + 1, col],
            # para arriba
            [row - 1, col + 1],
            [row - 1, col - 1],
            [row - 1, col],
            # derecha
            [row, col + 1],
            # izquierda
            [row, col - 1],
        ]
        for pos in newpos:
            if (7 >= pos[0] >= 0) and (7 >= pos[1] >= 0):
                if self.board[pos[0]][pos[1]] == '--' or self.board[pos[0]][pos[1]][0] != color:
                    moves.append(Move((row, col), (pos[0], pos[1]), self.board))

    def getQueenMoves(self, col, row, moves):
        self.getRookMoves(col, row, moves)
        self.getBishopMoves(col, row, moves)


class Move():
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def toString(self):
        return
