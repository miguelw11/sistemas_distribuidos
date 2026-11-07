
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 8000

INTERVALO_VERIFICACAO = 1
TEMPO_LIMITE = 8

# Armazena o último sinal recebido de cada Worker
workers = {}

# Protege o registro contra acessos simultâneos
lock = threading.Lock()


# Recebe os sinais de cada Worker
def atender_worker(conexao, endereco):
    arquivo = conexao.makefile("r", encoding="utf-8")

    try:
        for mensagem in arquivo:
            mensagem = mensagem.strip()

            if mensagem.startswith("PING "):
                worker_id = mensagem[5:].strip()

                if not worker_id:
                    continue

                agora = time.monotonic()

                with lock:
                    estava_offline = (
                        worker_id in workers
                        and not workers[worker_id]["online"]
                    )

                    workers[worker_id] = {
                        "ultimo_sinal": agora,
                        "online": True
                    }

                if estava_offline:
                    print(f"[ONLINE] O Nó {worker_id} voltou a funcionar!")

                else:
                    print(f"[HEARTBEAT] Sinal recebido de {worker_id}")

    except (ConnectionError, OSError):
        pass

    finally:
        arquivo.close()
        conexao.close()


# Verifica periodicamente os Workers
def monitorar_workers():
    while True:
        time.sleep(INTERVALO_VERIFICACAO)

        agora = time.monotonic()

        with lock:
            for worker_id, dados in workers.items():

                tempo_sem_sinal = agora - dados["ultimo_sinal"]

                if tempo_sem_sinal > TEMPO_LIMITE and dados["online"]:
                    dados["online"] = False

                    print(
                        f"[ALERTA] O Nó {worker_id} está OFFLINE!"
                    )


# Criação do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor.bind((HOST, PORT))

servidor.listen()

print(f"Servidor Monitor iniciado em {HOST}:{PORT}")
print("Aguardando Workers...")


# Thread responsável por verificar os sinais
thread_monitor = threading.Thread(
    target=monitorar_workers,
    daemon=True
)

thread_monitor.start()


# Aceita vários Workers
while True:
    conexao, endereco = servidor.accept()

    print(f"Novo Worker conectado: {endereco}")

    thread = threading.Thread(
        target=atender_worker,
        args=(conexao, endereco),
        daemon=True
    )

    thread.start()
