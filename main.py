"""
Este es el archivo principal, es el encargado de manejar los input del usuario y mostrar el estado actual del juego
"""

import pygame as p
import ChessEngine
from suplement import *
import time
import BrainV0 as bcero
import BrainV1 as bone

p.init()
width = 800  # 712
height = 600  # 512
dimension = 8  # por el 8x8 del tablero
sq_size = height // dimension
max_fps = 15  # para la animacion
images = [None, None, None, None, None, None, None, None, None, None, None, None]

"""
metodo complementario para cargar las imagenes
"""


def code(str):
    result = ""
    for char in str:
        result += ord(char)
    return


"""
inicializar un dicionario global de imagenes. esto sera llamado una sola vez en el main
"""


def loadImages():
    pieces = ["bP", "wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[convertToInt(piece)] = p.transform.scale((p.image.load("images/" + piece + ".png")), (sq_size, sq_size))
    # Nota: accedemos a la imagen de la pieza usando como indice la misma pieza


"""
metodo para ver las matrices en la consola
"""


def printM(m):
    for i in range(len(m)):
        print(m[i])


"""
el controlador principal para nuestro codigo
controla el input del usuario y actualiza la GUI
"""


def main():
    colors = [
        [p.Color("burly wood1"), p.Color("burlywood4")],
        [p.Color("gray90"), p.Color("gray39")],
        [p.Color("aquamarine"), p.Color("aquamarine3")],
        [p.Color("indianred"), p.Color("indianred4")],

    ]
    color = [colors[0], 0, len(colors)]
    screen = p.display.set_mode((width, height))
    p.display.set_caption('NemoChessBot v0.1')
    clock = p.time.Clock()
    screen.fill("white")
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    loadImages()  # esto se hace una sola vez antes del ciclo ya que es muy costoso
    running = True
    p.draw.rect(screen, p.Color("azure3"), p.Rect(sq_size * 8, 0, 200, sq_size * 8))
    playerIsWhite = True

    # Boton start
    restetNewGameBtn(screen)
    undoMoveBtn(screen)
    setColorBoard(screen)
    selectColorPlayer(screen, playerIsWhite)

    sqSelected = ()  # no se inicia con ningun cuadrado seleccionado, recuerda el ultimo click del usuario (row, col)
    playerClicks = []  # recuerda los clicks del usuario ( dos tuplas [(6,4), (4,4)] )

    while running:

        # Bot plays
        if playerIsWhite != gameState.whiteToMove:
            move = playBot(gameState, 'bone', 4, True)
            if move is not None:
                gameState.makeMove(move)
                moveMade = True
            else:
                if gameState.staleMate:
                    pass
                elif gameState.checkMate:
                    pass

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False



            elif e.type == p.MOUSEBUTTONDOWN:  # [UPGRADE] hay q hacerlo click and drag para q sea mas lindo
                location = p.mouse.get_pos()  # esta es la ubicacion (x,y) del mouse
                col = location[0] // sq_size
                row = location[1] // sq_size
                if sqSelected == (row, col) and inBoard(row, col):  # cuando se clickea dos veces el mismo casillero
                    sqSelected = ()
                    playerClicks = []  # reseteamos los clicks
                elif inBoard(row, col):
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                # Funcion para nuevo juego (BTN)
                mouse = p.mouse.get_pos()
                if (sq_size * 8) + 20 <= mouse[0] <= (sq_size * 8) + 180 and 20 <= mouse[1] <= (sq_size // 2) + 20:
                    p.draw.rect(screen, p.Color("gray"), [sq_size * 8 + 20, 20, 160, sq_size // 2])
                    text = p.font.SysFont('Corbel', 24).render('New Game', True, "black")
                    screen.blit(text, ((sq_size * 8) + 25, 25))
                    gameState = ChessEngine.GameState()
                    playerIsWhite = True
                    moveMade = True
                else:
                    restetNewGameBtn(screen)

                # Funcion para Undo (BTN)
                if (sq_size * 8) + 20 <= mouse[0] <= (sq_size * 8) + 180 and 60 <= mouse[1] <= (sq_size // 2) + 60:
                    p.draw.rect(screen, p.Color("gray"), [sq_size * 8 + 20, 60, 160, sq_size // 2])
                    text = p.font.SysFont('Corbel', 24).render('Undo', True, "black")
                    screen.blit(text, ((sq_size * 8) + 25, 65))
                    gameState.undoMove()
                    gameState.undoMove() #pq sino le saca el movimiento al bot y automaticamente lo vuelve a hacer
                    moveMade = True
                else:
                    undoMoveBtn(screen)

                # Funcion para cambiar el color del tablero
                if (sq_size * 8) + 20 <= mouse[0] <= (sq_size * 8) + 180 and 100 <= mouse[1] <= (sq_size // 2) + 100:
                    p.draw.rect(screen, p.Color("gray"), [sq_size * 8 + 20, 100, 160, sq_size // 2])
                    text = p.font.SysFont('Corbel', 24).render('Color', True, "black")
                    screen.blit(text, ((sq_size * 8) + 25, 105))
                    if color[1] + 1 >= color[2]:
                        ind = 0
                    else:
                        ind = color[1] + 1
                    color = [colors[ind], ind, len(colors)]
                else:
                    setColorBoard(screen)

                # Funcionalidad para elegir el color de jugar
                if (sq_size * 8) + 20 <= mouse[0] <= (sq_size * 8) + 180 and 140 <= mouse[1] <= (sq_size // 2) + 140:
                    p.draw.rect(screen, p.Color("gray"), [sq_size * 8 + 20, 140, 160, sq_size // 2])
                    playerIsWhite = not playerIsWhite
                    gameState = ChessEngine.GameState()
                    text = 'Player Color: B'
                    if playerIsWhite:
                        text = 'Player Color: W'
                    moveMade = True # Esto es para q cambie de jugador con respecto a los movimientos validos
                    text = p.font.SysFont('Corbel', 24).render(text, True, "black")
                    screen.blit(text, ((sq_size * 8) + 25, 145))
                else:
                    selectColorPlayer(screen, playerIsWhite)

                # Funcion para ejecutar un movimiento
                if len(playerClicks) == 2:  # es decir el usuario clickeo 2 veces
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gameState.makeMove(validMoves[i])
                            sqSelected = ()
                            playerClicks = []
                            moveMade = True

                            # Show last valid move made functionality
                            p.draw.rect(screen, p.Color("gray60"), [sq_size * 8 + 20, 550, 165, sq_size // 2])
                            text = p.font.SysFont('Corbel', 24).render('Last Move: ' + str(move.getChessNotation()),
                                                                       True, "black")
                            screen.blit(text, ((sq_size * 8) + 25, 555))

                    if not moveMade:
                        print('invalid move')
                        playerClicks = [sqSelected]

                    print('move made: ' + move.getChessNotation())

                    # resetear los clicks
                    sqSelected = ()
                    playerClicks = []


            # Shortcuts (key handeler)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:  # cuando apreto r se resetea
                    gameState = ChessEngine.GameState()
                    moveMade = True
                if e.key == p.K_u:  # cuando apreto u se elimina el ultimo movimiento
                    gameState.undoMove()
                    moveMade = True

        # Show who to move functionality (have to implement)
        if (gameState.whiteToMove):
            turn = 'white'
        else:
            turn = 'black'
        p.draw.rect(screen, p.Color("gray60"), [sq_size * 8 + 20, 510, 165, sq_size // 2])
        text = p.font.SysFont('Corbel', 24).render('To Move: ' + turn, True, "black")
        screen.blit(text, ((sq_size * 8) + 25, 515))

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        clock.tick(max_fps)
        p.display.flip()
        drawGameState(screen, gameState, color[0], playerClicks, validMoves)


"""
dibuja los cuadrados en el tablero
responsable de los graficos en un estado de juego
"""


def drawGameState(screen, gameState, color, playerClicks, validMoves):
    drawBoard(screen, color)  # dibuja los cuadrados en el tablero
    # [UPGRADE] aca se pueden dibujar movimientos sugeridos, etc
    drawPieces(screen, gameState.board)  # dibuja las piezas en los cuadrados

    # Funcion para mostrar los movimientos validos de una pieza
    if len(playerClicks) == 1:
        rowSel, colSel = playerClicks[0]

        for move in validMoves:
            if move.startCol == colSel and move.startRow == rowSel:
                p.draw.rect(screen, 'green',
                            p.Rect(move.endCol * sq_size + sq_size / 2 - 5,
                                   move.endRow * sq_size + sq_size / 2 - 5,
                                   10,
                                   10))


def drawBoard(screen, colors):
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":  # una celda q no esta vacia
                screen.blit(images[convertToInt(piece)], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


"""
funcion q chequea que los clicks estend dentro del tablero
"""


def inBoard(row, col):
    if row <= 7 and col <= 7:
        return True
    return False


def restetNewGameBtn(screen):
    p.draw.rect(screen, p.Color("white"), p.Rect((sq_size * 8) + 20, 20, 160, sq_size // 2))
    text = p.font.SysFont('Corbel', 24).render('New Game', True, "black")
    screen.blit(text, ((sq_size * 8) + 25, 25))


def undoMoveBtn(screen):
    p.draw.rect(screen, p.Color("white"), p.Rect((sq_size * 8) + 20, 60, 160, sq_size // 2))
    text = p.font.SysFont('Corbel', 24).render('Undo', True, "black")
    screen.blit(text, ((sq_size * 8) + 25, 65))


def setColorBoard(screen):
    p.draw.rect(screen, p.Color("white"), p.Rect((sq_size * 8) + 20, 100, 160, sq_size // 2))
    text = p.font.SysFont('Corbel', 24).render('Color', True, "black")
    screen.blit(text, ((sq_size * 8) + 25, 105))


def selectColorPlayer(screen, playerIsWhite):
    p.draw.rect(screen, p.Color("white"), p.Rect((sq_size * 8) + 20, 140, 160, sq_size // 2))
    text = 'Player Color: B'
    if playerIsWhite:
        text = 'Player Color: W'
    text = p.font.SysFont('Corbel', 24).render(text, True, "black")
    screen.blit(text, ((sq_size * 8) + 25, 145))


def playBot(gameState, brain, depth, maximizingPlayer):
    if brain == 'bcero':
        return bcero.chooseMove(gameState)
    elif brain == 'bone':
        return bone.chooseMove(gameState, depth, maximizingPlayer)

main()
