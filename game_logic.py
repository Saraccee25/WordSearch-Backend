from board_generator import generar_tablero_con_palabras
import json

def crear_juego(palabras):
    tablero = generar_tablero_con_palabras(palabras)
    paquete = {
        "tablero": tablero,
        "palabras": palabras
    }
    return json.dumps(paquete)

def resolver_juego(palabras):
    # Por ahora respuesta básica
    # Luego podemos guardar coordenadas reales
    return json.dumps({
        "mensaje": "Resolver no implementado aún",
        "palabras": palabras
    })
