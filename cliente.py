import socket
import os


def enviar_texto(cliente_socket):
    texto = input("Digite o texto a ser enviado: ")
    cliente_socket.sendall(b'TEXT')
    cliente_socket.sendall(texto.encode())
    print("Texto enviado com sucesso!")


def enviar_arquivo(cliente_socket):
    caminho_arquivo = input("Digite o caminho do arquivo: ")
    if os.path.exists(caminho_arquivo):
        try:
            if os.access(caminho_arquivo, os.R_OK):
                cliente_socket.sendall(b'FILE')
                nome_arquivo = os.path.basename(caminho_arquivo)
                cliente_socket.sendall(nome_arquivo.encode() + b'\n')
                with open(caminho_arquivo, 'rb') as arquivo:
                    while True:
                        dados = arquivo.read(1024)
                        if not dados:
                            break
                        cliente_socket.sendall(dados)
                # Envio de marcador de fim de arquivo
                cliente_socket.sendall(b'END_OF_FILE\n')
                print(f"Arquivo {nome_arquivo} enviado com sucesso!")
        except PermissionError as P:
            print(f"Permissão de leitura negada para o arquivo: {P}")
            

    else:
        print("Arquivo não encontrado.")


def main():
    servidor_host = 'localhost'
    servidor_porta = 5001  # Porta que funcionou

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((servidor_host, servidor_porta))
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        return

    while True:
        print("\n1. Enviar texto corrido")
        print("2. Enviar arquivo")
        print("3. Sair")
        opcao = input("Escolha uma opção (1, 2 ou 3): ")

        if opcao == '1':
            enviar_texto(cliente_socket)
        elif opcao == '2':
            enviar_arquivo(cliente_socket)
        elif opcao == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

        continuar = input("Deseja enviar mais alguma coisa? (s/n): ")
        if continuar.lower() != 's':
            break

    cliente_socket.close()


if __name__ == '__main__':
    main()
