import socket

HOST = "127.0.0.1"
PORT = 8000

#Cria o socket definindo conexão TCP/IP em IPv4
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Realiza a conexão com o servidor através do host e porta definidos
cliente.connect((HOST, PORT))

#Envia o pedido de horário para o servidor com encode para transformar a string em bytes, que é o formato aceito pelo socket
cliente.send("HORARIO".encode())

#Espera a resposta do servidor, que é o horário atual, e decodifica de bytes para string
resposta = cliente.recv(1024).decode()

#Retorna o horário recebido do servidor decodificado para string e imprime na tela
print("Horário recebido do servidor:", resposta)

cliente.close()