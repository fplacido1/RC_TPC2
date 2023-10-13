import pickle
import enum
import select
import socket
import sys
import time

buffer_size = 0
server_response_size = 29


class ServerResponse(enum.Enum):
    OK = 0
    ERROR1 = 1
    ERROR2 = 2


def wait_for_reply(u_socket):
    rx, tx, er = select.select([u_socket], [], [], 1)
    if rx == []:
        return False
    return True


def getTime():
    return round(time.time() * 1000)


def execute_request(cl_socket, server_address_port, fileName, chunkSize):
    file = open(fileName, "wb")
    offset = 0
    start = getTime()
    while True:
        request = (fileName, offset, chunkSize)
        req = pickle.dumps(request)
        cl_socket.sendto(req, server_address_port)
        if wait_for_reply(cl_socket):
            message, _ = cl_socket.recvfrom(buffer_size)
            status, n_bytes, content = pickle.loads(message)
            if status == ServerResponse.OK.value:
                file.write(content)
                if n_bytes < chunkSize:
                    file.close()
                    cl_socket.close()
                    break
                offset += chunkSize
            elif status == ServerResponse.ERROR1.value:
                print("File does not exist on server.\n")
                sys.exit(-1)
            elif status == ServerResponse.ERROR2.value:
                print("Invalid offset.\n")
                sys.exit(-1)
        else:
            print("Server did not answer, resending request.\n")
            sys.stdout.flush()
    totalTime = getTime() - start
    print("Time to transfer " + str(totalTime) + "ms.")


def main():
    n = len(sys.argv) - 1

    if n != 4:
        print("Invalid number of arguments!")
        sys.exit(-1)

    server_address_port = (sys.argv[1], int(sys.argv[2]))
    udp_socket_cl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global buffer_size
    buffer_size = int(sys.argv[4]) + server_response_size
    execute_request(udp_socket_cl, server_address_port, sys.argv[3], int(sys.argv[4]))


main()
