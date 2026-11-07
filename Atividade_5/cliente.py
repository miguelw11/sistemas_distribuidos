
import rpyc

# Endereço e porta do servidor
HOST = "127.0.0.1"
PORT = 8000


def listar_assentos(conexao):

    # Solicita ao servidor o estado atual dos assentos
    assentos = conexao.root.listar_assentos()

    print("\n========== MAPA DE ASSENTOS ==========")

    # Percorre a lista de tuplas recebida do servidor
    for assento, status in assentos:
        print(f"{assento}: {status}")

    print("======================================\n")


def reservar_assento(conexao, nome_cliente):

    # Solicita o assento desejado
    assento = input("Digite o assento que deseja reservar (ex: A1): ")

    # Remove espaços e padroniza as letras
    assento = assento.strip().upper()

    # Envia a solicitação ao servidor
    resposta = conexao.root.reservar_assento(
        nome_cliente,
        assento
    )

    # Exibe o resultado recebido
    print(f"\n{resposta}\n")


if __name__ == "__main__":

    try:

        # Conecta ao servidor RPyC
        conexao = rpyc.connect(HOST, PORT)

        print("Conectado ao sistema de reservas!")

        # Identifica o cliente
        nome_cliente = input("Digite seu nome: ").strip()

        if not nome_cliente:
            nome_cliente = "Cliente"

        # Menu principal
        while True:

            print("========== SISTEMA DE RESERVAS ==========")
            print("1 - Visualizar assentos")
            print("2 - Reservar assento")
            print("0 - Sair")
            print("=========================================")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":

                listar_assentos(conexao)

            elif opcao == "2":

                reservar_assento(conexao, nome_cliente)

            elif opcao == "0":

                print("Encerrando conexão...")
                break

            else:

                print("Opção inválida! Tente novamente.\n")

        # Encerra a conexão
        conexao.close()

    except ConnectionRefusedError:

        print("Não foi possível conectar ao servidor.")
        print("Verifique se ele está em execução.")

    except (ConnectionError, OSError):

        print("A conexão com o servidor foi encerrada.")
