"""
debido a q python no nos deja usar str como indices en listas tuve q
imporvisar y hacer una funcion transparente q convierta a int los strings usados para las piezas
"""

def convertToInt(str):
    if str == "bP":
        return 0
    if str == "wR":
        return 1
    if str == "wN":
        return 2
    if str == "wB":
        return 3
    if str == "wQ":
        return 4
    if str == "wK":
        return 5
    if str == "wP":
        return 6
    if str == "bR":
        return 7
    if str == "bN":
        return 8
    if str == "bB":
        return 9
    if str == "bQ":
        return 10
    if str == "bK":
        return 11


def convertTostring (int):
    if int == 0:
        return "bP"
    if int == 1:
        return "wR"
    if int == 2:
        return "wN"
    if int == 3:
        return "wB"
    if int == 4:
        return "wQ"
    if int == 5:
        return "wK"
    if int == 6:
        return "wP"
    if int == 7:
        return "bR"
    if int == 8:
        return "bN"
    if int == 9:
        return "bB"
    if int == 10:
        return "bQ"
    if int == 11:
        return "bK"





