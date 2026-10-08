import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8000


def atender_cliente(conexao, endereco):
    print("Cliente conectado:", endereco)

    pedido = conexao.recv(1024).decode()

    print("Pedido recebido:", pedido)

    horario = datetime.now().strftime("%H:%M:%S")

    conexao.send(horario.encode())

    conexao.close()

    print("Cliente desconectado:", endereco)


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))

servidor.listen()

print(f"Servidor rodando em {HOST}:{PORT}")

while True:

    conexao, endereco = servidor.accept()

    thread = threading.Thread(
        target=atender_cliente,
        args=(conexao, endereco)
    )

    thread.start()