import asyncio
import websockets
from config import WORDS
from game_logic import crear_juego, resolver_juego

HOST = "localhost"
PORT = 5000

async def handler(websocket):   # ← YA NO LLEVA path
    print("Cliente conectado por WebSocket")

    async for message in websocket:

        if message == "START":
            paquete = crear_juego(WORDS)
            await websocket.send(paquete)

        elif message == "RESOLVER":
            respuesta = resolver_juego(WORDS)
            await websocket.send(respuesta)

async def main():
    print(f"Servidor WebSocket escuchando en ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # Mantener vivo

asyncio.run(main())
