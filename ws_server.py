import asyncio
import websockets
import json
from game_logic import crear_juego, resolver_juego, actualizar_progreso, obtener_estado_juego, obtener_estadisticas
from data_storage import storage

HOST = "localhost"
PORT = 5000

# ArrayList para almacenar sesiones activas
sesiones_activas = []

class Sesion:
    """Representa una sesión de cliente conectado"""
    def __init__(self, websocket):
        self.websocket = websocket
        self.cliente_id = id(websocket)
        self.juego_id = None
        self.tablero_id = None
    
    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "juego_id": self.juego_id,
            "tablero_id": self.tablero_id
        }

def buscar_sesion(websocket):
    """Busca una sesión en el ArrayList"""
    cliente_id = id(websocket)
    for sesion in sesiones_activas:
        if sesion.cliente_id == cliente_id:
            return sesion
    return None

def agregar_sesion(websocket):
    """Agrega una nueva sesión al ArrayList"""
    sesion = Sesion(websocket)
    sesiones_activas.append(sesion)
    return sesion

def eliminar_sesion(websocket):
    """Elimina una sesión del ArrayList"""
    sesion = buscar_sesion(websocket)
    if sesion:
        sesiones_activas.remove(sesion)

async def handler(websocket):
    """Maneja las conexiones WebSocket"""
    sesion = agregar_sesion(websocket)
    print(f"✓ Cliente {sesion.cliente_id} conectado")
    print(f"  Total sesiones activas: {len(sesiones_activas)}")
    
    try:
        async for message in websocket:
            print(f"📨 Mensaje de cliente {sesion.cliente_id}: {message}")
            
            try:
                # Intentar parsear como JSON
                datos = json.loads(message)
                comando = datos.get("comando", "").upper()
                
                if comando == "START":
                    # Crear nuevo juego
                    paquete = crear_juego()
                    datos_juego = json.loads(paquete)
                    
                    # Actualizar sesión con datos del juego
                    sesion.juego_id = datos_juego.get("juego_id")
                    sesion.tablero_id = datos_juego.get("tablero_id")
                    
                    await websocket.send(paquete)
                    print(f"✓ Juego {sesion.juego_id} creado para cliente {sesion.cliente_id}")
                
                elif comando == "RESOLVER":
                    # Resolver el juego actual
                    if sesion.juego_id and sesion.tablero_id:
                        respuesta = resolver_juego(sesion.juego_id, sesion.tablero_id)
                        await websocket.send(respuesta)
                        print(f"✓ Solución enviada a cliente {sesion.cliente_id}")
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo. Envía START primero."
                        }))
                
                elif comando == "ENCONTRAR":
                    # Jugador encontró una palabra
                    if sesion.juego_id:
                        palabra = datos.get("palabra", "").upper()
                        respuesta = actualizar_progreso(sesion.juego_id, palabra)
                        await websocket.send(respuesta)
                        print(f"✓ Palabra '{palabra}' marcada como encontrada")
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo"
                        }))
                
                elif comando == "ESTADO":
                    # Obtener estado del juego actual
                    if sesion.juego_id:
                        respuesta = obtener_estado_juego(sesion.juego_id)
                        await websocket.send(respuesta)
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo"
                        }))
                
                elif comando == "ESTADISTICAS":
                    # Obtener estadísticas generales
                    respuesta = obtener_estadisticas()
                    await websocket.send(respuesta)
                
                else:
                    await websocket.send(json.dumps({
                        "error": f"Comando desconocido: {comando}",
                        "comandos_disponibles": ["START", "RESOLVER", "ENCONTRAR", "ESTADO", "ESTADISTICAS"]
                    }))
                    
            except json.JSONDecodeError:
                # Compatibilidad con mensajes de texto plano
                message = message.strip().upper()
                
                if message == "START":
                    paquete = crear_juego()
                    datos_juego = json.loads(paquete)
                    
                    sesion.juego_id = datos_juego.get("juego_id")
                    sesion.tablero_id = datos_juego.get("tablero_id")
                    
                    await websocket.send(paquete)
                
                elif message == "RESOLVER":
                    if sesion.juego_id and sesion.tablero_id:
                        respuesta = resolver_juego(sesion.juego_id, sesion.tablero_id)
                        await websocket.send(respuesta)
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo"
                        }))
                
                else:
                    await websocket.send(json.dumps({
                        "error": "Formato de mensaje inválido. Usa JSON o comandos: START, RESOLVER"
                    }))
    
    except websockets.exceptions.ConnectionClosed:
        print(f"✗ Cliente {sesion.cliente_id} desconectado")
    
    except Exception as e:
        print(f"❌ Error en handler: {e}")
    
    finally:
        # Limpiar sesión del ArrayList
        eliminar_sesion(websocket)
        print(f"  Total sesiones activas: {len(sesiones_activas)}")

async def main():
    """Inicia el servidor WebSocket"""
    print("=" * 60)
    print("🎮 SERVIDOR DE SOPA DE LETRAS")
    print("=" * 60)
    print(f"📊 Storage inicializado con {len(storage.palabras)} palabras")
    print(f"🚀 Servidor WebSocket escuchando en ws://{HOST}:{PORT}")
    print("=" * 60)
    print("\nComandos disponibles para clientes:")
    print("  - START: Iniciar nuevo juego")
    print("  - RESOLVER: Obtener solución")
    print("  - ENCONTRAR: Marcar palabra encontrada")
    print("  - ESTADO: Ver estado del juego")
    print("  - ESTADISTICAS: Ver estadísticas generales")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    try:
        async with websockets.serve(handler, HOST, PORT):
            await asyncio.Future()  # Mantener vivo
    except KeyboardInterrupt:
        print("\n⏹ Deteniendo servidor...")
        print(f"📈 Estadísticas finales: {storage.obtener_estadisticas()}")
        
        # Opcional: Exportar datos antes de cerrar
        storage.exportar_datos()

if __name__ == "__main__":
    asyncio.run(main())