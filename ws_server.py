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
    print(f"✓ Cliente conectado (ID: {sesion.cliente_id})")
    print(f"  Total sesiones activas: {len(sesiones_activas)}")
    
    try:
        async for message in websocket:
            try:
                # Parsear mensaje JSON del frontend
                datos = json.loads(message)
                comando = datos.get("comando", "").upper()
                
                if comando == "START":
                    # Botón "Nuevo Juego" presionado
                    print(f"🎮 Nuevo juego iniciado (Cliente: {sesion.cliente_id})")
                    paquete = crear_juego()
                    datos_juego = json.loads(paquete)
                    
                    sesion.juego_id = datos_juego.get("juego_id")
                    sesion.tablero_id = datos_juego.get("tablero_id")
                    
                    await websocket.send(paquete)
                    print(f"   → Palabras: {datos_juego.get('total_palabras')}")
                
                elif comando == "RESOLVER":
                    # Botón "Ver Solución" presionado
                    if sesion.juego_id and sesion.tablero_id:
                        print(f"🔍 Solución solicitada (Cliente: {sesion.cliente_id})")
                        respuesta = resolver_juego(sesion.juego_id, sesion.tablero_id)
                        datos_respuesta = json.loads(respuesta)
                        
                        await websocket.send(respuesta)
                        print(f"   → Soluciones enviadas: {len(datos_respuesta.get('soluciones', []))}")
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo."
                        }))
                
                elif comando == "ENCONTRAR":
                    # Usuario seleccionó una palabra correcta
                    if sesion.juego_id:
                        palabra = datos.get("palabra", "").upper()
                        respuesta = actualizar_progreso(sesion.juego_id, palabra)
                        datos_respuesta = json.loads(respuesta)
                        
                        await websocket.send(respuesta)
                        
                        palabras_encontradas = len(datos_respuesta.get('palabras_encontradas', []))
                        total = datos_respuesta.get('total_palabras', 0)
                        print(f"✓ Palabra encontrada: {palabra} ({palabras_encontradas}/{total})")
                        
                        if datos_respuesta.get('completado', False):
                            print(f"🎉 ¡Juego completado! (Cliente: {sesion.cliente_id})")
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo"
                        }))
                
                elif comando == "ESTADO":
                    if sesion.juego_id:
                        respuesta = obtener_estado_juego(sesion.juego_id)
                        await websocket.send(respuesta)
                    else:
                        await websocket.send(json.dumps({
                            "error": "No hay juego activo"
                        }))
                
                elif comando == "ESTADISTICAS":
                    respuesta = obtener_estadisticas()
                    await websocket.send(respuesta)
                
                else:
                    await websocket.send(json.dumps({
                        "error": f"Comando desconocido: {comando}"
                    }))
                    
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "error": "Formato de mensaje inválido"
                }))
    
    except websockets.exceptions.ConnectionClosed:
        print(f"✗ Cliente desconectado (ID: {sesion.cliente_id})")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        eliminar_sesion(websocket)
        print(f"   Total sesiones activas: {len(sesiones_activas)}")

async def main():
    """Inicia el servidor WebSocket"""
    print("=" * 60)
    print("🎮 SERVIDOR DE SOPA DE LETRAS")
    print("=" * 60)
    print(f"📊 Storage inicializado con {len(storage.palabras)} palabras")
    print(f"🚀 Servidor WebSocket escuchando en ws://{HOST}:{PORT}")
    print("=" * 60)
    print("\n✅ Servidor listo para recibir conexiones del frontend")
    print("   - Los comandos se envían automáticamente desde la interfaz web")
    print("   - No se requiere interacción manual del usuario")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    print("=" * 60)
    
    try:
        async with websockets.serve(handler, HOST, PORT):
            await asyncio.Future()  # Mantener vivo
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹ Deteniendo servidor...")
        print(f"📈 Estadísticas finales: {storage.obtener_estadisticas()}")
        print("=" * 60)
        
        # Opcional: Exportar datos antes de cerrar
        try:
            storage.exportar_datos()
            print("💾 Datos exportados correctamente")
        except Exception as e:
            print(f"⚠️ Error al exportar datos: {e}")

if __name__ == "__main__":
    asyncio.run(main())