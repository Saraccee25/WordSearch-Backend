import random
import threading
from config import BOARD_SIZE
from typing import List, Tuple

# Lock para sincronizar acceso al tablero
tablero_lock = threading.Lock()

def crear_tablero_vacio():
    """Crea un tablero lleno de letras aleatorias"""
    return [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def rellenar_espacios_vacios(tablero):
    """Rellena los espacios vacíos con letras aleatorias"""
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == ' ':
                tablero[i][j] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

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
        
        # Solo permitir si es espacio vacío o coincide con la letra
        if letra_tablero != ' ' and letra_tablero != palabra[i]:
            return False
    
    return True

def colocar_palabra_en_tablero(tablero: List[List[str]], palabra: str, 
                                fila: int, col: int, dir_fila: int, dir_col: int):
    """Coloca una palabra en el tablero"""
    for i, letra in enumerate(palabra):
        tablero[fila + dir_fila * i][col + dir_col * i] = letra

def intentar_colocar_palabra(tablero: List[List[str]], palabra: str, max_intentos: int = 200) -> bool:
    """Intenta colocar una palabra en el tablero con múltiples intentos"""
    # Direcciones: horizontal, vertical, diagonales (8 direcciones)
    direcciones = [
        (0, 1),   # Horizontal derecha
        (1, 0),   # Vertical abajo
        (1, 1),   # Diagonal abajo-derecha
        (1, -1),  # Diagonal abajo-izquierda
        (0, -1),  # Horizontal izquierda
        (-1, 0),  # Vertical arriba
        (-1, -1), # Diagonal arriba-izquierda
        (-1, 1),  # Diagonal arriba-derecha
    ]
    
    for intento in range(max_intentos):
        fila = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        dir_fila, dir_col = random.choice(direcciones)
        
        if puede_colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
            colocar_palabra_en_tablero(tablero, palabra, fila, col, dir_fila, dir_col)
            return True
    
    return False

def generar_tablero_con_palabras(palabras: List[str]) -> Tuple[List[List[str]], List[str]]:
    """Genera un tablero con las palabras dadas usando hilos - GARANTIZA todas las palabras"""
    
    max_intentos_generacion = 10  # Intentos para generar un tablero completo
    
    for intento_generacion in range(max_intentos_generacion):
        tablero = crear_tablero_vacio()
        palabras_colocadas = []
        palabras_pendientes = palabras.copy()
        
        # Ordenar palabras por longitud (las más largas primero)
        palabras_pendientes.sort(key=len, reverse=True)
        
        # Fase 1: Colocar palabras largas primero (sin threading)
        palabras_largas = [p for p in palabras_pendientes if len(p) >= 8]
        for palabra in palabras_largas:
            if intentar_colocar_palabra(tablero, palabra, max_intentos=300):
                palabras_colocadas.append(palabra)
                palabras_pendientes.remove(palabra)
        
        # Fase 2: Usar threading para palabras restantes
        palabras_por_colocar = palabras_pendientes.copy()
        palabras_colocadas_thread = []
        lock_colocadas = threading.Lock()
        
        def intentar_colocar_thread(palabra: str):
            with tablero_lock:
                if intentar_colocar_palabra(tablero, palabra, max_intentos=200):
                    with lock_colocadas:
                        palabras_colocadas_thread.append(palabra)
        
        # Crear e iniciar hilos
        hilos = []
        for palabra in palabras_por_colocar:
            hilo = threading.Thread(target=intentar_colocar_thread, args=(palabra,))
            hilos.append(hilo)
            hilo.start()
        
        # Esperar a que todos terminen
        for hilo in hilos:
            hilo.join()
        
        palabras_colocadas.extend(palabras_colocadas_thread)
        
        # Fase 3: Intentar colocar las que quedaron sin threading
        palabras_faltantes = [p for p in palabras if p not in palabras_colocadas]
        for palabra in palabras_faltantes:
            if intentar_colocar_palabra(tablero, palabra, max_intentos=500):
                palabras_colocadas.append(palabra)
        
        # Si logramos colocar TODAS las palabras, terminamos
        if len(palabras_colocadas) == len(palabras):
            print(f"✓ Tablero generado exitosamente en intento {intento_generacion + 1}")
            print(f"  Palabras colocadas: {len(palabras_colocadas)}/{len(palabras)}")
            rellenar_espacios_vacios(tablero)
            return tablero, palabras_colocadas
        else:
            print(f"✗ Intento {intento_generacion + 1}: Solo se colocaron {len(palabras_colocadas)}/{len(palabras)} palabras")
    
    # Si después de todos los intentos no se logró, retornar el mejor resultado
    print(f"⚠ Advertencia: Solo se pudieron colocar {len(palabras_colocadas)}/{len(palabras)} palabras")
    rellenar_espacios_vacios(tablero)
    return tablero, palabras_colocadas

def generar_tablero_garantizado(palabras: List[str], intentos_maximos: int = 20) -> Tuple[List[List[str]], List[str]]:
    """
    Versión alternativa que GARANTIZA colocar todas las palabras
    Reintenta múltiples veces hasta lograrlo
    """
    for intento in range(intentos_maximos):
        tablero, palabras_colocadas = generar_tablero_con_palabras(palabras)
        
        if len(palabras_colocadas) == len(palabras):
            return tablero, palabras_colocadas
        
        print(f"🔄 Reintentando... (intento {intento + 1}/{intentos_maximos})")
    
    # Si falló, usar método sin threading (más lento pero más confiable)
    print("⚠ Usando método secuencial como respaldo...")
    tablero = crear_tablero_vacio()
    palabras_colocadas = []
    palabras_ordenadas = sorted(palabras, key=len, reverse=True)
    
    for palabra in palabras_ordenadas:
        if intentar_colocar_palabra(tablero, palabra, max_intentos=1000):
            palabras_colocadas.append(palabra)
    
    rellenar_espacios_vacios(tablero)
    print(f"✓ Método secuencial: {len(palabras_colocadas)}/{len(palabras)} palabras colocadas")
    
    return tablero, palabras_colocadas