import socket
import pickle
import os.path
import sys
import random

class serverResponse(enum.Enum):
    ERROR0 = "OK"
    ERROR1 = "file does not exist"
    ERROR2 = "invalid offset"

localIP = "127.0.0.1"
buffer_size = 2048

def serverReply(message, udp_socket_sv, client_address):
    rand = random.randint(0, 10)
    if rand > 2:
        udp_socket_sv.sendTo(message, client_address) #! possibilidade de faltar um return
    
def send_file(udp_socket_sv, client_address, fileName, offset, nBytes):
    file = open(fileName, 'r')
    file.seek(offset)
    message = file.read(nBytes) 
    file.close()
    request = (serverResponse.ERROR0.value, nBytes, message)
    req = pickle.dumps(request)
    serverReply(req, udp_socket_sv, client_address)

def wait_for_connection(udp_socket_sv):
    while True:
        message, client_address = udp_socket_sv.recvfrom(buffer_size)
        request = pickle.loads(message)
        fileName = request[0]
        offset = request[1]
        nBytes = request[2]
        if not os.path.isfile(fileName):
            request = (serverResponse.ERROR1.value, 0, 0)
            req = pickle.dumps(request)
            serverReply(req, udp_socket_sv, client_address)
        elif offset < 0 and offset > os.path.filesize(fileName):
            request = (serverResponse.ERROR2.value, 0, 0)
            req = pickle.dumps(request)
            serverReply(req, udp_socket_sv, client_address)
        else:
          send_file(udp_socket_sv, client_address, fileName, offset, nBytes)

 
def main():
    n = len(sys.argv) - 1

    if n != 1:
        print("Invalid number of arguments!\n")
        sys.exit(-1)

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, int(sys.argv[1])))
    wait_for_connection(UDPServerSocket)


main()