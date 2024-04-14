import socket
import pickle
import json

tcpPort = 3000
udpPort = 5000
tcpServer = None
udpServer = None

# Função responsável pela verificação se já existe um servidor ativo.
def check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
        except socket.error:
            return True
    return False

# Função responsável por salvar uma conexão ao dicionário de conexões.
def save_device(connection, address):
    try:
        with open('database/connectedDevices.pickle', 'rb') as dic:
            connectedDevices = pickle.load(dic)
    except (FileNotFoundError, EOFError):
        connectedDevices = {}

    connection.sendto(str("Dispositivo conectado o broker com sucesso!").encode(), (address[0], tcpPort))
    connectedDevices[address[0]] = {"addressInfo": address, "sentMessages": []}

    with open('database/connectedDevices.pickle', 'wb') as dicFile:
        pickle.dump(connectedDevices, dicFile)
        
    print(f"Um novo dispositivo foi conectado: {address[0]}")

# Função responsável por receber as mensagens UDP e salvar no dicionário.
def receive_udp_message(udpServer):
    message, address = udpServer.recvfrom(1024)
    
    with open('database/connectedDevices.pickle', 'rb') as dic:
        connectedDevices = pickle.load(dic)
        
    if address[0] in connectedDevices:
        connectedDevices[address[0]]['sentMessages'].append(json.loads(message.decode()))

        with open('database/connectedDevices.pickle', 'wb') as dic:
            pickle.dump(connectedDevices, dic)

        print(f"Sucesso: Mensagem UDP recebida de {address[0]}!")

# Função responsável por receber as conexões.
def receive_connections(tcpServer):
    connection, address = tcpServer.accept()
    
    save_device(connection, address)
    
# Função responsável por iniciar o Broker e escutar as conexões.
def start_broker_server():
    try:
        if not check_port_in_use(tcpPort):
            tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpServer.bind(('localhost', tcpPort))
            tcpServer.listen(1)
            print(f"TCP Server is listening on port {tcpPort}")
        else:
            print(f"Port {tcpPort} is already in use. Skipping TCP server creation.")

        if not check_port_in_use(udpPort):
            udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpServer.bind(('localhost', udpPort))
            print(f"UDP Server is listening on port {udpPort}")
        else:
            print(f"Port {udpPort} is already in use. Skipping UDP server creation.")
        
        receive_connections(tcpServer)
        
        while (True):
            receive_udp_message(udpServer)
    
    except Exception as e:
        print(f"Error: {e}")