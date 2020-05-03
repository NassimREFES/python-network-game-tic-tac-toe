import socket

HOST = ''
PORT = 4040

READY = 'START_GAME'
FINISH = 'FINISH_GAME'

def create_listen_socket(host, port):
    """ configure socket server """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    return sock
    
def recv_msg(sock):
    data = bytearray()
    msg = ''
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            msg = (data.rstrip(b'\0')).decode('utf-8')
    return msg
    
def send_msg(sock, msg):
    msg += '\0' # affirme l'envoi complet du msg
    Sock.sendall(msg.encode('utf-8'))
    
def create_contact_with_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock
    
