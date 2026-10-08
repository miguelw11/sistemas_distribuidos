import socket

HOST = "127.0.0.1"
PORT = 8000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))

servidor.listen()

print("Servidor aguardando conexão...")

conexao, endereco = servidor.accept()

print("Cliente conectado:", endereco)

mensagem = conexao.recv(1024).decode()

print("Mensagem recebida:", mensagem)

mensagem_invertida = mensagem[::-1]

conexao.send(mensagem_invertida.encode())

conexao.close()

servidor.close()