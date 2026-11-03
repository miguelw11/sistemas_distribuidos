import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))

servidor.listen()

print(f"Servidor iniciado em {HOST}:{PORT}")
print("Aguardando clientes...")
