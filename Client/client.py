import socket
import sys

def execute_request(socket, server_address_port, fileName, chunkSize):
    

def main():
    n = len(sys.argv) - 1

    if n != 4:
        print("Invalid number of arguments!")
        sys.exit(-1)

    server_address_port = (sys.argv[1], int(sys.argv[2]))
    udp_socket_cl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    execute_request(udp_socket_cl, server_address_port, sys.argv[3], sys.argv[4])

main()