import socket


def receber_texto(conexao):
    texto = conexao.recv(1024).decode()
    with open('texto_recebido.txt', 'a') as arquivo:  # 'a' para acrescentar ao arquivo existente
        arquivo.write(texto + '\n')

    print("Texto recebido e salvo.")


def receber_arquivo(conexao):
    nome_arquivo = ''
    byte = conexao.recv(1)
    while byte != b'\n':  # Lê até o delimitador de nova linha
        nome_arquivo += byte.decode()
        byte = conexao.recv(1)
    
    with open(nome_arquivo, 'wb') as arquivo:
        while True:
            dados = conexao.recv(1024)
            # Verifica o marcador de fim de arquivo
            if dados.endswith(b'END_OF_FILE\n'):
                dados = dados[:-12]  # Remove o marcador do fluxo de dados
                if dados:
                    arquivo.write(dados)
                break
            arquivo.write(dados)
    print(f"Arquivo {nome_arquivo} recebido e salvo.")


def main():
    servidor_host = 'localhost'
    servidor_porta = 5001 #porta de sua preferencia
    timeout_segundos = 10

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((servidor_host, servidor_porta))
    servidor_socket.listen(1)

    print(f"Servidor rodando na porta {servidor_porta} e ip 127.0.0.1...")
    print("Aguardando cliente...")
    servidor_socket.settimeout(timeout_segundos)  # tempo de espera por conexão

    try:
        conexao, endereco = servidor_socket.accept()

        print(f"Conexão estabelecida com {endereco}")

        while True:
            opcao = conexao.recv(4)
            if opcao == b'TEXT':
                receber_texto(conexao)
            elif opcao == b'FILE':
                receber_arquivo(conexao)
            elif not opcao:  # Caso a conexão seja fechada
                print("Conexão fechada pelo cliente.")
                break
            else:
                print("Opção inválida recebida.")
        conexao.close()
    except TimeoutError as T:
        print(f"Tempo de espera por conexão excedido: {T}")
    finally:
        print("Servidor desconectado.")
        servidor_socket.close()


if __name__ == '__main__':
    main()
