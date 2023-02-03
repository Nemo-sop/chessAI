import sys
import copy


def chooseMove(board, depth, maximizingPlayer):
    alpha = float('-inf')
    beta = float('inf')
    bestValue, bestMove = minimaxAB(board, depth, alpha, beta, maximizingPlayer)
    print('Best Move: ', bestMove.getChessNotation())
    print('Best Value: ', bestValue)
    return bestMove


# MinMax with alpha beta pruning
def minimaxAB(gameState, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or gameState.staleMate or gameState.checkMate:
        return evaluate(gameState), None

    bestMove = None
    if maximizingPlayer:
        bestValue = -sys.maxsize
        for move in gameState.getValidMoves():
            newBoard = copy.deepcopy(gameState)
            newBoard.makeMove(move)
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
        for move in gameState.getValidMoves():
            newBoard = copy.deepcopy(gameState)
            newBoard.makeMove(move)
            value, _ = minimaxAB(newBoard, depth - 1, alpha, beta, not maximizingPlayer)
            if value < bestValue:
                bestValue = value
                bestMove = move
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
        return bestValue, bestMove


PIECE_VALUES = {
    "P": 100,  # pawn
    "N": 320,  # knight
    "B": 330,  # bishop
    "R": 500,  # rook
    "Q": 900,  # queen
    "K": 20000  # king
}


def evaluate(gameState):
    material_balance = 0
    piece_mobility = 0
    king_safety = 0
    pawn_structure = 0
    control_of_center = 0
    piece_coordination = 0
    tempo = 0

    # Sum the values of all pieces on the board
    for row in gameState.board:
        for piece in row:
            if piece[1] != "-":
                material_balance += PIECE_VALUES[piece[1]]

    # # Consider piece mobility by counting the number of legal moves for each piece
    # for row in range(8):
    #     for col in range(8):
    #         piece = gameState.board[row][col]
    #         if piece != "--":
    #             piece_mobility += len(get_legal_moves(board, row, col))
    #
    # # Consider king safety by counting the number of squares that attack the king
    # for row in range(8):
    #     for col in range(8):
    #         piece = board[row][col]
    #         if piece == "K":
    #             king_row, king_col = row, col
    #             break
    #
    # for row in range(8):
    #     for col in range(8):
    #         if board[row][col] == "Q":
    #             king_safety -= len(get_squares_attacked(board, row, col))
    #
    # # Consider pawn structure by counting the number of pawn chains and doubled pawns
    # pawn_structure = count_pawn_chains(board) + count_doubled_pawns(board)
    #
    # # Consider control of center by counting the number of central squares controlled by each player
    # control_of_center = count_central_squares_controlled(board)
    #
    # # Consider piece coordination by counting the number of pairs of pieces that are working together
    # piece_coordination = count_piece_coordination(board)
    #
    # # Consider tempo by counting the number of turns that have passed
    # tempo = count_turns(board)
    #
    # # Combine the factors to get the final score
    # score = material_balance + piece_mobility + king_safety + pawn_structure + control_of_center + piece_coordination + tempo

    return material_balance
