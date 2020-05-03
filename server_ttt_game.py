import threading
import queue
import tincan_ttt_game
import tictactoe

HOST = tincan_ttt_game.HOST
PORT = tincan_ttt_game.PORT

send_queues = {}
names = []
lock = threading.Lock()
game = tictactoe.TicTacToe()
curr_player = 0
finish = False

def deconnecte_joueur(sock, addr):
    fd = sock.fileno()
    with lock:
        q = send_queues.get(fd, None)
    if q:
        q.put(None)
        del send_queues[fd]
        try:
            addr = sock.getpeername()
            print('joueur {} deconnecte'.format(addr))
        except OSError:
            pass
        sock.close()
        
def recv_step(sock, addr):
    global names
    global game
    global curr_player
    global finish
    
    while not finish:
        try:
            pos_step = tincan_ttt_game.recv_msg(sock)
            name_curr_player = sock.getpeername()
            print(name_curr_player[1])
            print('-> {}'.format(names[curr_player%2].split(':')[-1]))
            if int(name_curr_player[1]) == int(names[curr_player%2].split(':')[-1]):
                print('{} va jouer.'.format(names[curr_player%2]))
                pos = pos_step.split(' ')
                if len(pos) != 2:
                    diffuser_res('{}: veuiller entrer 2 nombre (position)'.format(names[curr_player%2]))
                else:
                    diffuser_res('{} a jouer la case {}:{}'.format(names[curr_player%2], pos[0], pos[1]))
                    
                    r = game.Step_player(curr_player, int(pos[0]), int(pos[1]), diffuser_res)
                    print ('r = {}'.format(r))
                    if game.Check_winner(game.morpion_symbole[curr_player%2]):
                            diffuser_res(')=> {} <=( A GAGNER'.format(names[curr_player%2]))
                            finish = True
                    elif curr_player == 3*3-1:
                            diffuser_res(')=> Personne na gagner <=(')
                            finish = True 
                    if not r:
                        game.Print_grille(diffuser_res)
                        curr_player = curr_player + 1;  
            else:
                print("c'est a {} de jouer.".format(names[curr_player%2]))  
                diffuser_res("c'est a {} de jouer.".format(names[curr_player%2]))   
        except (EOFError, ConnectionError):
            deconnecte_joueur(sock, addr)
            diffuser_res(')=> {} <=( A GAGNER'.format(names[curr_player%2]))
            break
    
    print(tincan_ttt_game.FINISH)       
    diffuser_res(tincan_ttt_game.FINISH)  
    # FINISH... add for more
        

def envoi_grille(sock, q, addr):
    while True:
        grille = q.get()
        if grille == None: break
        try:
            tincan_ttt_game.send_msg(sock, grille)
        except (ConnectionError, BrokenPipeError):
            deconnecte_joueur(sock, addr)
            break
            
def diffuser_res(resultat):
    with lock:
        for q in send_queues.values():
            q.put(resultat)
            
if __name__ == '__main__':
    listen_sock = tincan_ttt_game.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Ecoute on {}'.format(addr))
    count = 0
    while len(send_queues) != 2:
        client_sock, addr = listen_sock.accept()
        q = queue.Queue()
        with lock:
            send_queues[client_sock.fileno()] = q
            
        recv_pos_thread = threading.Thread(target=recv_step, args=[client_sock, addr], daemon=True)
        send_res_thread = threading.Thread(target=envoi_grille, args=[client_sock, q, addr], daemon=True)
        recv_pos_thread.start()
        send_res_thread.start()  
        
        if len(send_queues) == 1:
            names.append('FIRST:{}'.format(str(addr[1])))
            print('FIRST:{}'.format(str(addr[1])))
        else:
            names.append('SECOND:{}'.format(str(addr[1])))  
            print('SECOND:{}'.format(str(addr[1])))
        
        tincan_ttt_game.send_msg(client_sock, 'Ton nom est: {}'.format(names[count]))
        
        count = count + 1
       # thread_step = threading.Thread(target=)
    game.player_one = names[0]
    game.player_two = names[1]
    print(tincan_ttt_game.READY)
    diffuser_res(tincan_ttt_game.READY)
    
    while True: pass
        