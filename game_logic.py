from board_generator import generar_tablero_con_palabras
from data_storage import storage
import json

def crear_juego():
    """Crea un nuevo juego con tablero y palabras desde storage"""
    
    palabras = storage.obtener_palabras("PROFESIONES")
    
    if not palabras:
        return json.dumps({
            "error": "No hay palabras disponibles"
        })
    
  
    from board_generator import generar_tablero_garantizado
    tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=20)
    
  
    tablero_id = storage.guardar_tablero(tablero, palabras_colocadas)
    

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
   
    tablero_obj = storage.obtener_tablero(tablero_id)
    
    if not tablero_obj:
        return json.dumps({
            "error": "Tablero no encontrado"
        })
    
    tablero = tablero_obj.matriz
    palabras = tablero_obj.palabras
    soluciones = []
    
    print(f"\n{'='*60}")
    print(f"🔍 RESOLVIENDO JUEGO #{juego_id}")
    print(f"{'='*60}")
    print(f"Total de palabras a buscar: {len(palabras)}")
    print(f"Palabras: {palabras}")
    print(f"{'='*60}\n")
    

    for i, palabra in enumerate(palabras, 1):
        print(f"Buscando palabra {i}/{len(palabras)}: {palabra}")
        posiciones = encontrar_palabra_en_tablero(tablero, palabra)
        
        if posiciones:
            print(f"  ✓ Encontrada en posiciones: {posiciones}")
            soluciones.append({
                "palabra": palabra,
                "posiciones": posiciones
            })
        else:
            print(f"  ✗ NO ENCONTRADA - Esto es un ERROR")
    
    print(f"\n{'='*60}")
    print(f"✓ RESULTADO: {len(soluciones)}/{len(palabras)} palabras encontradas")
    print(f"{'='*60}\n")
    
 
    storage.actualizar_juego(juego_id, finalizar=True)
    
    return json.dumps({
        "soluciones": soluciones,
        "mensaje": f"Juego resuelto: {len(soluciones)}/{len(palabras)} palabras encontradas",
        "total_palabras": len(soluciones),
        "palabras_faltantes": [p for p in palabras if p not in [s["palabra"] for s in soluciones]]
    })

def encontrar_palabra_en_tablero(tablero, palabra):
    """Encuentra una palabra en el tablero y retorna sus posiciones"""
    
    direcciones = [
        (0, 1),   
        (1, 0),   
        (1, 1),  
        (1, -1), 
        (0, -1),  
        (-1, 0),  
        (-1, -1), 
        (-1, 1),  
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
                    
                   
                    if not (0 <= nueva_fila < size and 0 <= nueva_col < size):
                        encontrada = False
                        break
                    
                    
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
    
   
    storage.actualizar_juego(juego_id, palabra_encontrada=palabra_encontrada)
    
 
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