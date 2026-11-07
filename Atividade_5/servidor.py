
import rpyc
import threading
from rpyc.utils.server import ThreadedServer

# Endereço e porta do servidor
HOST = "127.0.0.1"
PORT = 8000

# Estado compartilhado:
# Cada assento começa com None, indicando que está livre.
assentos = {
    f"A{i}": None for i in range(1, 11)
}

# Controla o acesso simultâneo ao estado compartilhado.
lock = threading.Lock()


class ServicoReservas(rpyc.Service):

    # Retorna o estado atual de todos os assentos
    def exposed_listar_assentos(self):

        with lock:
            resultado = []

            for assento, cliente in assentos.items():

                if cliente is None:
                    status = "Livre"
                else:
                    status = f"Reservado por {cliente}"

                # Adiciona uma tupla com o assento e seu status
                resultado.append((assento, status))

            # Retorna a lista para o cliente
            return resultado

    # Recebe o nome do cliente e o assento desejado
    def exposed_reservar_assento(self, nome_cliente, assento):

        # Verifica se o assento existe
        if assento not in assentos:
            return "Assento inválido!"

        # Protege a verificação e a reserva contra concorrência
        with lock:

            # Verifica se já está ocupado
            if assentos[assento] is not None:
                return "Assento já ocupado!"

            # Registra o cliente no assento
            assentos[assento] = nome_cliente

            return (
                f"Reserva realizada com sucesso! "
                f"Assento {assento} reservado para {nome_cliente}."
            )


if __name__ == "__main__":

    # Permite atender vários clientes simultaneamente
    servidor = ThreadedServer(
        ServicoReservas,
        hostname=HOST,
        port=PORT
    )

    print(f"Servidor de reservas iniciado em {HOST}:{PORT}")
    print("Aguardando solicitações dos clientes...")

    servidor.start()
