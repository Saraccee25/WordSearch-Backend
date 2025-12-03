import asyncio
import websockets

HOST = "localhost"
PORT = 5000

async def main():
    uri = f"ws://{HOST}:{PORT}"

    print("Intentando conectar al servidor WebSocket...")

    async with websockets.connect(uri) as websocket:
        print("✔ Conectado al servidor")

        await websocket.send("START")
        paquete = await websocket.recv()
        print("Juego recibido:", paquete)

        await websocket.send("RESOLVER")
        respuesta = await websocket.recv()
        print("Solución:", respuesta)

asyncio.run(main())
