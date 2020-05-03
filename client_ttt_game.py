import sys
import threading
import socket
import tincan_ttt_game

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = tincan_ttt_game.PORT

def input_game(sock):
    """ user play """
    print('Entrer la case a jouer [x y], "a" pour abandonner/quitter')
    while True:
        msg = input()
        if msg == 'a':
            sock.shutdown(socket.SHUT_RDWR) 
            sock.close()
            break
        try:
            tincan_ttt_game.send_msg(sock, msg)
        except (BrokenPipeError, ConnectionError):
            break
            
if __name__ == '__main__':
    sock = tincan_ttt_game.create_contact_with_server(HOST, PORT)
    print('Connecte a {}: {}'.format(HOST, PORT))
    print("Attendre un deuxieme joueur...")
    
    start = False
    while not start: 
        try:
            msg = tincan_ttt_game.recv_msg(sock)
            print('message recu: {}'.format(msg))
            if msg == tincan_ttt_game.READY:
                start = True
        except ConnectionError:
            print('1Connection au server ferme')
            sock.close()
            sys.exit(-1)
            
    print('============= La partie commence =============')  
    
    thread = threading.Thread(target=input_game, args=[sock], daemon=True)
    thread.start()
    
    while True:
        try:
            grille_res = tincan_ttt_game.recv_msg(sock)
            print(grille_res)
            if grille_res == tincan_ttt_game.FINISH:
                break
        except ConnectionError:
            print('2Connection au server ferme')
            sock.close()
            break