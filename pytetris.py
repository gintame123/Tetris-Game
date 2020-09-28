import modele
import vue
import time

class Controleur:
    def __init__(self,ModeleTetris):
        self.__modele = ModeleTetris
        self.__vue = vue.VueTetris(ModeleTetris)
        self.__fen = self.__vue.fenetre()
        
        self.__fen.bind("<Key-Left>",self.forme_a_gauche)
        self.__fen.bind("<Key-Right>",self.forme_a_droite)
        self.__fen.bind("<Key-Down>",self.forme_tombe)
        self.__fen.bind("<Key-Up>",self.forme_tourne)
        
        self.__delai = 320
        self.joue()
        self.__fen.mainloop()
    
    def joue(self) :
        '''Controleur -> None
        boucle principale du jeu. Fait tomber une forme d’une ligne.
        '''
        if not self.__modele.fini():
            self.affichage()
            self.__fen.after(self.__delai,self.joue)

    def affichage(self):
        '''Controleur -> None
        le contrôleur indique au module qu’il doit faire tomber la forme, puis il demande à la vue de redessiner son terrain, puis de redessiner la forme.
        '''
        if self.__modele.forme_tombe():
            self.__delai = 320
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__modele.get_coords_forme(),self.__modele.get_couleur_forme())
        self.__vue.dessine_forme_suivante(self.__modele.get_coords_suivante(),self.__modele.get_couleur_suivante())
        score = self.__modele.get_score()
        self.__vue.met_a_jour_score(score)

    def forme_a_gauche(self,event):
        '''Controleur, event -> None
        demande au modèle de déplacer la forme à gauche.
        '''
        self.__modele.forme_a_gauche()

    def forme_a_droite(self,event):
        '''Controleur, event -> None
        demande au modèle de déplacer la forme à droite.
        '''
        self.__modele.forme_a_droite()

    def forme_tombe(self,event):
        '''Controleur, event -> None
        demande au modèle de faire tomber la forme plus vite.
        '''
        self.__delai = 60

    def forme_tourne(self,event):
        '''Controleur, event -> None
        demande au modèle de déplacer faire tourner la forme.
        '''
        self.__modele.forme_tourne()
        
        
if __name__ == "__main__" :
    # création du modèle
    tetris = modele.ModeleTetris()
    # création du contrˆoleur. c’est lui qui créé la vue et lance la boucle d’écoute des évts
    ctrl = Controleur(tetris)

