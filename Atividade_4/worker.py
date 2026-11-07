
import socket
import time

HOST = "127.0.0.1"
PORT = 8000

INTERVALO = 3

# Identificação do Worker
worker_id = input("Digite o ID do Worker: ").strip()

if not worker_id:
    print("O ID do Worker não pode ser vazio.")
    raise SystemExit

# Cria a conexão com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORT))

    print(f"{worker_id} conectado ao Servidor Monitor!")

    while True:
        # Monta a mensagem de Heartbeat
        mensagem = f"PING {worker_id}\n"

        # Envia o sinal ao servidor
        cliente.sendall(mensagem.encode("utf-8"))

        print(f"[ENVIADO] {mensagem.strip()}")

        # Aguarda 3 segundos
        time.sleep(INTERVALO)

except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")

except KeyboardInterrupt:
    print(f"\n{worker_id} encerrado pelo usuário.")

except (ConnectionError, OSError):
    print("Conexão com o servidor perdida.")

finally:
    cliente.close()
