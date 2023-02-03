import random

def chooseMove(gameState):
    moves = gameState.getValidMoves()
    if len(moves) == 0:
        return None
    return random.choice(moves)