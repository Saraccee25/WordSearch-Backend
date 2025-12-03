import socket
import threading
from config import HOST, PORT, WORDS
from game_logic import crear_juego, resolver_juego

def manejar_cliente(conn, addr):
    print("Cliente conectado:", addr)

    while True:
        data = conn.recv(4096).decode()
        if not data:
            break

        if data == "START":
            paquete = crear_juego(WORDS)
            conn.send(paquete.encode())

        elif data == "RESOLVER":
            respuesta = resolver_juego(WORDS)
            conn.send(respuesta.encode())

    conn.close()
    print("Cliente desconectado:", addr)

def iniciar_servidor():
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Servidor iniciado en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

iniciar_servidor()
