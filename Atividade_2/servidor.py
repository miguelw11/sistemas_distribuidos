import rpyc
from datetime import datetime

# Cria uma classe de serviço RPYC
class ServicoHorario(rpyc.Service):

    # Cria função para obter o horário atual e a retona
    def exposed_obter_horario(self):
        horario = datetime.now().strftime("%H:%M:%S")
        return horario

#Importa a classe OneShotServer devido fechar a conexão após o cliente receber o horário
from rpyc.utils.server import OneShotServer

#Realiza a execução do servidor
if __name__ == "__main__":
    servidor = OneShotServer(
        ServicoHorario,
        hostname="127.0.0.1",
        port=8000
    )

    print("Servidor aguardando uma conexão...")
    servidor.start()
