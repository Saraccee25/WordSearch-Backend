import random
import threading
from config import BOARD_SIZE

def crear_tablero_vacio():
    return [[random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def colocar_palabra(tablero, palabra):
    fila = random.randint(0, BOARD_SIZE - 1)
    col = random.randint(0, BOARD_SIZE - len(palabra))

    for i, letra in enumerate(palabra):
        tablero[fila][col + i] = letra

def generar_tablero_con_palabras(palabras):
    tablero = crear_tablero_vacio()

    hilos = []
    for palabra in palabras:
        hilo = threading.Thread(target=colocar_palabra, args=(tablero, palabra))
        hilos.append(hilo)
        hilo.start()

    for h in hilos:
        h.join()

    return tablero
