class TicTacToe:
    player_one = ''
    player_two = ''
    morpion_symbole = ('X', 'O')
    morpion_grille_3x3 = [['', '', ''], ['', '', ''], ['', '', '']]
    
    def __init__(self, po='', pt=''):
        self.player_one=po
        self.player_two=pt
        
    def Check_winner(self, curr_gamer):
        """ si ya un gagnant """
        b = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(3): 
            for j in range(3): 
                if self.morpion_grille_3x3[i][j] == curr_gamer: 
                    if i == j: # pour diag1
                        b[3+3]+=1
                    if (i == 0 and j == 2) or (i == 1 and j == 1) or (i == 2 and j == 0): # pour diag2
                        b[3+4]+=1
                    b[i]+=1 # represente les lignes
                    b[3+j]+=1 # represente les colonnes
        
        print(b)
                   
        return (3 in b)
        
    def Check_clear_case(self, x, y):
        """ si la case choisi est vide """
        return True if self.morpion_grille_3x3[x][y] == '' else False    
        
    def Print_grille(self, diff=print):
        """ affichage de la grille """
        diff('\n\n\n')
        for i in range(3):
            s = ''
            for j in range(3):
                if self.morpion_grille_3x3[i][j] == '':
                    s += '.\t'
                else:
                    s += self.morpion_grille_3x3[i][j] + '\t'
            s+='\n'
            diff(s)
        diff('\n\n\n')
        
    def Step_player(self, curr_player, xpos, ypos, diff=print):
        x = int(xpos)
        y = int(ypos)
        if int(x) < 0 or int(x) > 2 or int(y) < 0 or int(y) > 2:
            diff('(Selectionner une case valide)')
        elif self.Check_clear_case(x, y):
            self.morpion_grille_3x3[x][y] = self.morpion_symbole[curr_player%2]
            return False
        else:
           diff('(Selectionner une case vide)')
        return True
        
    def Start(self):
        """ lancer le jeux """
        finish = False
        curr_player = 0 # 0: player_one, 1: player_two
        while not finish:
            while self.Step_player(curr_player,
				  input('(Entrer le num de la ligne [0, 1, 2])> '),
				  input('(Entrer le num de la colonne [0, 1, 2])> ')): pass
                    
            if self.Check_winner(self.morpion_symbole[curr_player%2]):
                print('{} Gagne'.format(self.player_one if curr_player%2 == 0 else self.player_two))
                break
            
            self.Print_grille()
            curr_player = curr_player + 1
                
if __name__ == '__main__':
    ttt = TicTacToe('first', 'second')
    ttt.Print_grille()
    ttt.Start()
    ttt.Print_grille()  
