from board_generator import generar_tablero_con_palabras
from data_storage import storage
import json

def crear_juego():
    """Crea un nuevo juego con tablero y palabras desde storage"""
    # Obtener palabras del storage (ArrayList)
    palabras = storage.obtener_palabras("PROFESIONES")
    
    if not palabras:
        return json.dumps({
            "error": "No hay palabras disponibles"
        })
    
    # Generar tablero con threading
    tablero, palabras_colocadas = generar_tablero_con_palabras(palabras)
    
    # Guardar tablero en storage (ArrayList)
    tablero_id = storage.guardar_tablero(tablero, palabras_colocadas)
    
    # Crear sesión de juego en storage (ArrayList)
    juego_id = storage.crear_juego(tablero_id)
    
    paquete = {
        "juego_id": juego_id,
        "tablero_id": tablero_id,
        "tablero": tablero,
        "palabras": palabras_colocadas,
        "total_palabras": len(palabras_colocadas)
    }
    
    return json.dumps(paquete)

def resolver_juego(juego_id, tablero_id):
    """Encuentra las posiciones de todas las palabras en el tablero"""
    # Obtener tablero del storage (ArrayList)
    tablero_obj = storage.obtener_tablero(tablero_id)
    
    if not tablero_obj:
        return json.dumps({
            "error": "Tablero no encontrado"
        })
    
    tablero = tablero_obj.matriz
    palabras = tablero_obj.palabras
    soluciones = []
    
    # Buscar cada palabra en el tablero
    for palabra in palabras:
        posiciones = encontrar_palabra_en_tablero(tablero, palabra)
        if posiciones:
            soluciones.append({
                "palabra": palabra,
                "posiciones": posiciones
            })
    
    # Marcar juego como completado en storage
    storage.actualizar_juego(juego_id, finalizar=True)
    
    return json.dumps({
        "soluciones": soluciones,
        "mensaje": "Juego resuelto",
        "total_palabras": len(soluciones)
    })

def encontrar_palabra_en_tablero(tablero, palabra):
    """Encuentra una palabra en el tablero y retorna sus posiciones"""
    direcciones = [
        (0, 1),   # Horizontal derecha
        (1, 0),   # Vertical abajo
        (1, 1),   # Diagonal abajo-derecha
        (1, -1),  # Diagonal abajo-izquierda
    ]
    
    size = len(tablero)
    
    for fila in range(size):
        for col in range(size):
            for dir_fila, dir_col in direcciones:
                posiciones = []
                encontrada = True
                
                for i, letra in enumerate(palabra):
                    nueva_fila = fila + dir_fila * i
                    nueva_col = col + dir_col * i
                    
                    # Verificar límites
                    if not (0 <= nueva_fila < size and 0 <= nueva_col < size):
                        encontrada = False
                        break
                    
                    # Verificar letra
                    if tablero[nueva_fila][nueva_col] != letra:
                        encontrada = False
                        break
                    
                    posiciones.append([nueva_fila, nueva_col])
                
                if encontrada:
                    return posiciones
    
    return None

def actualizar_progreso(juego_id, palabra_encontrada):
    """Actualiza el progreso del jugador cuando encuentra una palabra"""
    juego = storage.obtener_juego(juego_id)
    
    if not juego:
        return json.dumps({
            "error": "Juego no encontrado"
        })
    
    # Agregar palabra al ArrayList de palabras encontradas
    storage.actualizar_juego(juego_id, palabra_encontrada=palabra_encontrada)
    
    # Verificar si completó todas las palabras
    tablero = storage.obtener_tablero(juego.tablero_id)
    total_palabras = len(tablero.palabras)
    palabras_encontradas = len(juego.palabras_encontradas)
    
    completado = palabras_encontradas >= total_palabras
    if completado:
        storage.actualizar_juego(juego_id, finalizar=True)
    
    return json.dumps({
        "mensaje": "Progreso guardado",
        "palabras_encontradas": juego.palabras_encontradas,
        "total_encontradas": palabras_encontradas,
        "total_palabras": total_palabras,
        "completado": completado,
        "tiempo_transcurrido": juego.get_tiempo_transcurrido()
    })

def obtener_estado_juego(juego_id):
    """Obtiene el estado actual de un juego"""
    juego = storage.obtener_juego(juego_id)
    
    if not juego:
        return json.dumps({
            "error": "Juego no encontrado"
        })
    
    tablero = storage.obtener_tablero(juego.tablero_id)
    
    return json.dumps({
        "juego": juego.to_dict(),
        "tablero": tablero.to_dict() if tablero else None,
        "progreso": len(juego.palabras_encontradas),
        "total": len(tablero.palabras) if tablero else 0
    })

def obtener_estadisticas():
    """Obtiene estadísticas generales del storage"""
    return json.dumps(storage.obtener_estadisticas())