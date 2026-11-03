
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

# Armazena os clientes conectados
clientes = []
lock = threading.Lock()


# Envia uma mensagem para todos os clientes conectados
def transmitir(mensagem, remetente=None):
    with lock:
        for cliente in clientes[:]:
            if cliente != remetente:
                try:
                    cliente.sendall(mensagem.encode("utf-8"))
                except:
                    clientes.remove(cliente)
                    cliente.close()


# Atende individualmente cada cliente
def atender_cliente(conexao, endereco):
    try:
        arquivo = conexao.makefile("r", encoding="utf-8")

        nome = arquivo.readline().strip()

        if not nome:
            return

        with lock:
            clientes.append(conexao)

        print(f"{nome} entrou no chat.")

        transmitir(f"[SERVIDOR] {nome} entrou no chat.\n",
                   remetente=conexao)

        # Recebe mensagens continuamente
        for mensagem in arquivo:
            mensagem = mensagem.strip()

            if mensagem == "/sair":
                break

            if mensagem:
                texto = f"{nome}: {mensagem}\n"

                print(texto.strip())

                transmitir(texto, remetente=conexao)

    except (ConnectionError, OSError):
        pass

    finally:
        with lock:
            if conexao in clientes:
                clientes.remove(conexao)

        arquivo.close() if 'arquivo' in locals() else None
        conexao.close()

        if 'nome' in locals() and nome:
            print(f"{nome} saiu do chat.")

            transmitir(f"[SERVIDOR] {nome} saiu do chat.\n")


# Criação do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor.bind((HOST, PORT))

servidor.listen()

print(f"Servidor iniciado em {HOST}:{PORT}")
print("Aguardando clientes...")

# Aceita novos clientes continuamente
while True:
    conexao, endereco = servidor.accept()

    thread = threading.Thread(
        target=atender_cliente,
        args=(conexao, endereco)
    )

    thread.start()
