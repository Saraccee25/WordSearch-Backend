import socket
import json

HOST = "localhost"
PORT = 5000

def main():
    cliente = socket.socket()
    cliente.connect((HOST, PORT))
    print("✔ Conectado al servidor")

    # 1. Enviar comando START
    cliente.send("START".encode())

    # 2. Recibir paquete con tablero + palabras
    data = cliente.recv(50000).decode()
    paquete = json.loads(data)

    print("\n🧩 Tablero recibido:\n")
    for fila in paquete["tablero"]:
        print(" ".join(fila))

    print("\n📌 Palabras a encontrar:")
    print(", ".join(paquete["palabras"]))

    cliente.close()

if __name__ == "__main__":
    main()
