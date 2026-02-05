###########################################################################
# Concurrent server - webserver3d.py                                      #
#                                                                         #
###########################################################################
import socket
import os

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    request = client_connection.recv(1024)
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)

def server_forever():
    listen_socekt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socekt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socekt.bind(SERVER_ADDRESS)
    listen_socekt.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP port {port} ...'.format(port=PORT))

    clients = []

    while True:
        client_connection, client_address = listen_socekt.accept()
        # store the reference otherwise it's garbage collected
        # on the next loop run
        clients.append(client_connection)
        pid = os.fork()
        if pid == 0: # child
            listen_socekt.close() # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0) # child exits here
        else: # parent
            # client_connection.close()
            print(len(clients))

if __name__ == '__main__':
    server_forever()