import socket
import threading

# Porta referente ao servidor TCP.
tcpPort = 3000
# Porta referente ao servidor UDP.
udpPort = 5000
# Criando servidor TCP.
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Criando servidor UDP.
udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Criando um dicionário para armazenar os dispositivos conectados.
connectedDevices = {}

tcpServer.bind(('localhost', tcpPort))
tcpServer.listen(1)

print(f"Servidor TCP está conectado na porta {tcpPort}!")

udpServer.bind(('localhost', udpPort))
print(f"Servidor UDP está conectado na porta {udpPort}")


while (True):
    # Connection -> Objeto do dispositivo conectado.
    # Address -> Endereço do dispositivo conectado.
    connection, address = tcpServer.accept()

    print(f"Um novo dispositivo foi conectado: {address[1]}")

    connectedDevices[address] = connection
    
    message = udpServer.recv(1024).decode()
    
    print(f"Mensagem recebida: {message}")
    
    
    
    

