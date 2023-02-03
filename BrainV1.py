import sys


def chooseMove(board, depth, alpha, beta, maximizingPlayer):

    bestValue, bestMove = minimaxAB(board, depth, alpha, beta, maximizingPlayer)
    print('Best Move: ', bestMove.getChessNotation())
    print('Best Value: ', bestValue)
    return bestMove


# MinMax with alpha beta pruning
def minimaxAB(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.game_over():
        return evaluate(board), None

    bestMove = None
    if maximizingPlayer:
        bestValue = -sys.maxsize
        for move in board.getValidMoves():
            newBoard = board.copy().makeMove(move)
            value, _ = minimaxAB(newBoard, depth - 1, alpha, beta, not maximizingPlayer)
            if value > bestValue:
                bestValue = value
                bestMove = move
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break
        return bestValue, bestMove
    else:
        bestValue = sys.maxsize
        for move in board.getValidMoves():
            newBoard = board.copy().makeMove(move)
            value, _ = minimaxAB(newBoard, depth - 1, alpha, beta, not maximizingPlayer)
            if value < bestValue:
                bestValue = value
                bestMove = move
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
        return bestValue, bestMove


PIECE_VALUES = {
    "P": 100, # pawn
    "N": 320, # knight
    "B": 330, # bishop
    "R": 500, # rook
    "Q": 900, # queen
    "K": 20000 # king
}

def evaluate(board):

    return 0