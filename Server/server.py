import enum
import socket
import pickle
import os.path
import sys
import random


class ServerResponse(enum.Enum):
    OK = 0
    ERROR1 = 1
    ERROR2 = 2


localIP = "127.0.0.1"
buffer_size = 2048


def server_reply(message, udp_socket_sv, client_address):
    rand = random.randint(0, 9)
    if rand > 2:
        udp_socket_sv.sendto(message, client_address)
    return


def send_file(udp_socket_sv, client_address, fileName, offset, nBytes):
    file = open(fileName, 'rb')
    file.seek(offset)
    message = file.read(nBytes)
    file.close()
    request = (ServerResponse.OK.value, len(message), message)
    req = pickle.dumps(request)
    server_reply(req, udp_socket_sv, client_address)


def wait_for_connection(udp_socket_sv):
    print("Server waiting for client request.\n")
    while True:
        message, client_address = udp_socket_sv.recvfrom(buffer_size)
        request = pickle.loads(message)
        fileName = request[0]
        offset = request[1]
        nBytes = request[2]
        if not os.path.isfile(fileName):
            request = (ServerResponse.ERROR1.value, 0, 0)
            req = pickle.dumps(request)
            server_reply(req, udp_socket_sv, client_address)
        elif 0 > offset > os.path.getsize(fileName):
            request = (ServerResponse.ERROR2.value, 0, 0)
            req = pickle.dumps(request)
            server_reply(req, udp_socket_sv, client_address)
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
