import random
import threading
from config import BOARD_SIZE
from typing import List, Tuple

# Lock para sincronizar acceso al tablero
tablero_lock = threading.Lock()

def crear_tablero_vacio():
    """Crea un tablero lleno de letras aleatorias"""
    return [[random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") 
             for _ in range(BOARD_SIZE)] 
            for _ in range(BOARD_SIZE)]

def puede_colocar_palabra(tablero: List[List[str]], palabra: str, 
                          fila: int, col: int, dir_fila: int, dir_col: int) -> bool:
    """Verifica si se puede colocar una palabra en la posición y dirección dadas"""
    longitud = len(palabra)
    
    # Verificar límites
    fila_fin = fila + dir_fila * (longitud - 1)
    col_fin = col + dir_col * (longitud - 1)
    
    if not (0 <= fila_fin < BOARD_SIZE and 0 <= col_fin < BOARD_SIZE):
        return False
    
    # Verificar que no sobrescriba letras incorrectas
    for i in range(longitud):
        fila_actual = fila + dir_fila * i
        col_actual = col + dir_col * i
        letra_tablero = tablero[fila_actual][col_actual]
        
        # Solo permitir si es letra aleatoria o coincide con la palabra
        if letra_tablero.isalpha() and letra_tablero != palabra[i]:
            # Si ya hay una letra diferente, no se puede colocar
            if letra_tablero in palabra or any(letra_tablero in p for p in TODAS_LAS_PALABRAS):
                return False
    
    return True

def colocar_palabra_segura(tablero: List[List[str]], palabra: str) -> bool:
    """Intenta colocar una palabra en el tablero de forma thread-safe"""
    # Direcciones: horizontal, vertical, diagonales
    direcciones = [
        (0, 1),   # Horizontal derecha
        (1, 0),   # Vertical abajo
        (1, 1),   # Diagonal abajo-derecha
        (1, -1),  # Diagonal abajo-izquierda
    ]
    
    intentos = 0
    max_intentos = 100
    
    with tablero_lock:  # Sincronizar acceso al tablero
        while intentos < max_intentos:
            fila = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            dir_fila, dir_col = random.choice(direcciones)
            
            if puede_colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
                # Colocar la palabra
                for i, letra in enumerate(palabra):
                    tablero[fila + dir_fila * i][col + dir_col * i] = letra
                return True
            
            intentos += 1
        
        return False  # No se pudo colocar

# Variable global temporal para las palabras
TODAS_LAS_PALABRAS = []

def generar_tablero_con_palabras(palabras: List[str]) -> Tuple[List[List[str]], List[str]]:
    """Genera un tablero con las palabras dadas usando hilos"""
    global TODAS_LAS_PALABRAS
    TODAS_LAS_PALABRAS = palabras
    
    tablero = crear_tablero_vacio()
    palabras_colocadas = []
    lock_colocadas = threading.Lock()
    
    def intentar_colocar(palabra: str):
        if colocar_palabra_segura(tablero, palabra):
            with lock_colocadas:
                palabras_colocadas.append(palabra)
    
    # Crear e iniciar hilos
    hilos = []
    for palabra in palabras:
        hilo = threading.Thread(target=intentar_colocar, args=(palabra,))
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    # Si algunas palabras no se colocaron, intentar secuencialmente
    for palabra in palabras:
        if palabra not in palabras_colocadas:
            if colocar_palabra_segura(tablero, palabra):
                palabras_colocadas.append(palabra)
    
    return tablero, palabras_colocadas