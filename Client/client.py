import pickle
import enum
import select
import socket
import sys


buffer_size = 2048


class ServerResponse(enum.Enum):
    OK = "OK"
    ERROR1 = "file does not exist"
    ERROR2 = "invalid offset"


def wait_for_reply(u_socket):
    rx, tx, er = select.select([u_socket], [], [], 1)
    if rx == []:
        return False
    return True


def execute_request(cl_socket, server_address_port, fileName, chunkSize):
    file = open(fileName, "w")
    offset = 0
    while True:
        request = (fileName, offset, chunkSize)
        req = pickle.dumps(request)
        cl_socket.sendto(req, server_address_port)
        print("wait for reply")
        if wait_for_reply(cl_socket):
            message, _ = cl_socket.recvfrom(buffer_size)
            status, n_bytes, content = pickle.loads(message)
            if status == ServerResponse.OK.value:
                print("ok")
                print(offset)
                print(n_bytes)
                print(content)
                file.write(content)
                if n_bytes < chunkSize:
                    file.close()
                    cl_socket.close()
                    break
                offset += chunkSize
            elif status == ServerResponse.ERROR1.value:
                print(ServerResponse.ERROR1.value + "\n")
                sys.exit(-1)
            else:
                print(ServerResponse.ERROR2.value + "\n")
                sys.exit(-1)


def main():
    n = len(sys.argv) - 1

    if n != 4:
        print("Invalid number of arguments!")
        sys.exit(-1)

    server_address_port = (sys.argv[1], int(sys.argv[2]))
    udp_socket_cl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    execute_request(udp_socket_cl, server_address_port, sys.argv[3], int(sys.argv[4]))

main()