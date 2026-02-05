######################################
# Concurrent server - webserver3g.py #
#                                    #
#   Tested with Python 3.12.3        #
######################################

import errno
import os
import signal
import socket

SERVER_ADDERESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,         # Wait for any child process
                os.WNOHANG  # DO not blobk and return EWOULDBLOCK error
            )
        except OSError:
            return
        
        if pid == 0: # no more zombies
            return
        
def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_reponse = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_reponse)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDERESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            # restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0: # child
            listen_socket.close() # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            client_connection.close() # close parent copy and loop over 

if __name__ == '__main__':
    serve_forever()