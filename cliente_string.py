import socket

HOST = "127.0.0.1"
PORT = 8000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORT))

mensagem = "Olá, Mundo Distribuído"

cliente.send(mensagem.encode())

resposta = cliente.recv(1024).decode()

print("Mensagem enviada:", mensagem)

print("Resposta do servidor:", resposta)

cliente.close()