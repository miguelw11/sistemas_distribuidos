
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000


# Recebe e exibe mensagens do servidor
def receber_mensagens(cliente):
    arquivo = cliente.makefile("r", encoding="utf-8")

    try:
        for mensagem in arquivo:
            print(mensagem.strip())

    except (ConnectionError, OSError):
        pass

    finally:
        arquivo.close()


# Cria a conexão com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORT))

    nome = input("Digite seu nome: ")

    # Envia o nome ao servidor
    cliente.sendall((nome + "\n").encode("utf-8"))

    print("\nConectado ao chat!")
    print("Digite /sair para desconectar.\n")

    # Thread responsável por receber mensagens
    thread = threading.Thread(
        target=receber_mensagens,
        args=(cliente,),
        daemon=True
    )

    thread.start()

    # Loop principal para enviar mensagens
    while True:
        mensagem = input()

        cliente.sendall((mensagem + "\n").encode("utf-8"))

        if mensagem.strip() == "/sair":
            break

except ConnectionRefusedError:
    print("Não foi possível conectar. Verifique se o servidor está ligado.")

except (ConnectionError, OSError):
    print("A conexão com o servidor foi encerrada.")

finally:
    cliente.close()
    print("Você saiu do chat.")
