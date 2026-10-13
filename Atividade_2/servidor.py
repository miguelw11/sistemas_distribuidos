import rpyc
from datetime import datetime


class ServicoHorario(rpyc.Service):

    def exposed_obter_horario(self):
        horario = datetime.now().strftime("%H:%M:%S")
        return horario

from rpyc.utils.server import OneShotServer


if __name__ == "__main__":
    servidor = OneShotServer(
        ServicoHorario,
        hostname="127.0.0.1",
        port=8000
    )

    print("Servidor aguardando uma conexão...")
    servidor.start()
