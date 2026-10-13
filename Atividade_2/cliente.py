import rpyc

conexao = rpyc.connect("127.0.0.1", 8000)

horario = conexao.root.obter_horario()

print("Horário recebido do servidor:", horario)

conexao.close()
