import sys
import copy
import time


def chooseMove(board, depth, maximizingPlayer, playerIsWhite):
    alpha = float('-inf')
    beta = float('inf')
    log = []
    start = time.time()
    bestValue, bestMove = minimaxAB(board, depth, alpha, beta, maximizingPlayer, log, playerIsWhite)
    log.sort(key=lambda tup: tup[1], reverse=True)
    chessNotation = 'Finished'
    if bestMove is not None:
        chessNotation = bestMove.getChessNotation()
    print('='*20)
    print('Best Move: ', chessNotation)
    print('Best Value: ', bestValue)
    print('Moves taken into account: ', len(log))
    print('Decision time: ' + str(round(time.time()-start,2)) + 's')
    print('=' * 20)
    return bestMove


# MinMax with alpha beta pruning
def minimaxAB(gameState, depth, alpha, beta, maximizingPlayer, log, playerIsWhite):
    if depth == 0 or gameState.staleMate or gameState.checkMate:
        return evaluate(gameState, playerIsWhite), None

    bestMove = None
    if maximizingPlayer:
        bestValue = -sys.maxsize
        for move in gameState.getValidMoves():
            newBoard = copy.deepcopy(gameState)
            newBoard.makeMove(move)
            value, _ = minimaxAB(newBoard, depth - 1, alpha, beta, not maximizingPlayer, log, playerIsWhite)
            if value > bestValue:
                bestValue = value
                bestMove = move
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break
        log.append((bestMove, bestValue))
        return bestValue, bestMove
    else:
        bestValue = sys.maxsize
        for move in gameState.getValidMoves():
            newBoard = copy.deepcopy(gameState)
            newBoard.makeMove(move)
            value, _ = minimaxAB(newBoard, depth - 1, alpha, beta, not maximizingPlayer, log, playerIsWhite)
            if value < bestValue:
                bestValue = value
                bestMove = move
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
        log.append((bestMove, bestValue))
        return bestValue, bestMove


PIECE_VALUES = {
    "P": 100,  # pawn
    "N": 320,  # knight
    "B": 330,  # bishop
    "R": 500,  # rook
    "Q": 900,  # queen
    "K": 20000  # king
}


def evaluate(gameState, botIsBlack):
    material_balance = 0
    piece_mobility = 0
    king_safety = 0
    pawn_structure = 0
    control_of_center = 0
    piece_coordination = 0
    tempo = 0

    # Sum the values of all pieces on the board

    fromBot = 'w'
    if botIsBlack:
        fromBot = 'b'


    for row in gameState.board:
        for piece in row:
            if piece[1] != "-":
                if piece[0] == fromBot:
                    material_balance += PIECE_VALUES[piece[1]]
                else:
                    material_balance -= PIECE_VALUES[piece[1]]

    return material_balance