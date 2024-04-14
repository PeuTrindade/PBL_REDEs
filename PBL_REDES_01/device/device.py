import socket
import json
import time
import threading

clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

brokerIPAdress = None
brokerPortTCP = None
brokerPortUDP = None

device_state = {"on": False, "temperature": 25}

# Função responsável por enviar estado do dispositivo a cada 3 segundos em UDP.
def send_device_state_to_server():
    global brokerPortUDP, brokerIPAdress
    
    clientUDP.sendto(json.dumps(device_state).encode(), (brokerIPAdress, int(brokerPortUDP)))
    
    threading.Timer(3, send_device_state_to_server).start()

# Função responsável por printar o menu.
def print_menu():
    print("\033[34m" + "===================================\nMenu:\n")
    print("[1] -> Ligar dispositivo")
    print("[2] -> Alterar temperatura")
    print("[3] -> Desligar dispositivo")
    print("===================================" + "\033[0m")
    
    selected_option = input("Escolha uma opção: ")
    
    return selected_option

# Função responsável por gerenciar o menu e escolhas do usuário.
def start_menu():
    selected_option = print_menu()
    
    while (selected_option != '3'):
        if selected_option == '1':
            device_state['on'] = True

            print("\033[32m" + "Sucesso: Ar condicionado ligado com sucesso!" + "\033[0m")
            
        elif selected_option == '2':
            if device_state['on']:
                temperature = input("Insira uma temperatura (Valor inteiro): ")
                
                if temperature and temperature.isdigit():
                    device_state['temperature'] = int(temperature)
                    
                    print("\033[32m" + f"Sucesso: Temperatura alterada com sucesso para {temperature} graus!" + "\033[0m")
                else:
                    print("\033[31m" + "Erro: Por favor, insira uma temperatura válida!" + "\033[0m")
            else:
                print("\033[31m" + "Erro: Por favor, ligue o dispositivo!" + "\033[0m")
            
        selected_option = print_menu()

# Função responsável por enviar a primeira mensagem ao usuário.
def send_greeting_messages():
    global brokerPortTCP, brokerPortUDP, brokerIPAdress
    
    print("\033[36m" + "===================================\nAr condicionado iniciado!\n===================================" + "\033[0m")

    print("\033[34m" + "===================================\nConfigure o seu dispositivo\n")

    brokerIPAdress = input("Insira o endereço IP do broker: ")
    brokerPortTCP = input("Insira a porta do servidor TCP: ")
    brokerPortUDP = input("Insira a porta do servidor UDP: ")

    print("==================================="  + "\033[0m")

    clientTCP.connect((brokerIPAdress, int(brokerPortTCP)))
    clientUDP.connect((brokerIPAdress, int(brokerPortUDP)))

    message = clientTCP.recv(1024).decode()

    while (message == ''):
        message = clientTCP.recv(1024).decode()
    
    print("\033[32m" + f"Mensagem do servidor: {message}" + "\033[0m")
    
    send_device_state_to_server()
    
    start_menu()

if __name__ == "__main__":
    send_greeting_messages()