import socket
import pickle
import json

tcpPort = 4000
udpPort = 5000
tcpServer = None
udpServer = None
connectedDevices = {}
connections = {}

# Função responsável por salvar uma conexão ao dicionário de conexões.
def save_device(connection, address):
    global connectedDevices
    
    connection.sendto(str("Dispositivo conectado o broker com sucesso!").encode(), (address[0], tcpPort))
    connectedDevices[address[0]] = {"addressInfo": address, "sentMessages": {}}
    connections[address[0]] = connection
        
    print(f"Um novo dispositivo foi conectado: {address[0]}")

def change_device_mode(ip_address, mode):
    try:
        connections[ip_address].sendall(str(mode).encode())
    except e:
        print(e)
        
def change_device_temperature(ip_address, temperature):
    try:
        connections[ip_address].sendall(str(temperature).encode())
    except e:
        print(e)

# Função responsável por receber as mensagens UDP e salvar no dicionário.
def receive_udp_message(udpServer):
    global connectedDevices
    
    message, address = udpServer.recvfrom(1024)
        
    if address[0] in connectedDevices:
        connectedDevices[address[0]]['sentMessages'] = json.loads(message.decode())

        print(f"Sucesso: Mensagem UDP recebida de {address[0]}!")

# Função responsável por receber as conexões.
def receive_connections(tcpServer):
    connection, address = tcpServer.accept()
    
    save_device(connection, address)
    
# Função responsável por iniciar o Broker e escutar as conexões.
def start_broker_server():
    global tcpServer
    global udpServer
    
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.bind(('localhost', tcpPort))
    tcpServer.listen(1)
    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServer.bind(('localhost', udpPort))
    
    print(f"TCP Server is listening on port {tcpPort}")
    print(f"UDP Server is listening on port {udpPort}")
    
    receive_connections(tcpServer)
    
    while (True):
        receive_udp_message(udpServer)