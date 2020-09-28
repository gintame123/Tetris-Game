from tkinter import *
import modele

DIM = 30
COULEURS = ["red","blue","green","yellow","orange","purple","pink",
            "dark grey","black"]
SUIVANT = 6
x1= modele.ModeleTetris()

class VueTetris:
    def __init__(self, ModeleTetris):
        self.__modele = ModeleTetris
        self.__fenetre= Tk()
        self.__fenetre.title("Tetris")
        
        self.__can_terrain = Canvas(self.__fenetre, width =self.__modele.get_largeur()*DIM, height =self.__modele.get_hauteur()*DIM)
        self.__can_terrain.pack(side ='left')
        
        frame = Frame(self.__fenetre)
        Label(frame,text="Forme suivante :").pack()
        self.__can_fsuivante = Canvas(frame, width = SUIVANT*DIM, height = SUIVANT*DIM)
        self.__can_fsuivante.pack()
        
        self.__lbl_score = Label(frame,text="Score : 0")
        self.__lbl_score.pack()
        btn_quitter = Button(frame, text="quitter" , command = self.__fenetre.destroy)
        btn_quitter.pack()
        frame.pack(side ='right')
        
        self.__les_cases = []
        for i in range(self.__modele.get_hauteur()):
            liste =[]
            for j in range( self.__modele.get_largeur()):
                liste.append(self.__can_terrain.create_rectangle(j*DIM,i*DIM,DIM*self.__modele.get_largeur(),DIM*self.__modele.get_hauteur(),outline ="grey", fill= COULEURS[self.__modele.get_valeur(i,j)]))
            self.__les_cases.append(liste)
            
        self.__les_suivants = []
        for i in range(SUIVANT):
            liste =[]
            for j in range(SUIVANT):
                liste.append(self.__can_fsuivante.create_rectangle(j*DIM,i*DIM,DIM*SUIVANT,DIM*SUIVANT,outline ="grey", fill= COULEURS[self.__modele.get_valeur(i+self.__modele.get_base(),j)]))
            self.__les_suivants.append(liste)
        
    def fenetre(self):
        '''VueTetris -> Tk
        retourne l’instance de Tk de l’application.
        '''
        return self.__fenetre

    def dessine_case(self,i,j,coul):
        '''VueTetris,int,int,str -> None
        remplit la case en ligne i et en colonne j de la couleur à l’indice coul. 
        '''
        self.__can_terrain.itemconfigure(self.__les_cases[i][j],fill = COULEURS[coul])

    def dessine_terrain(self):
        '''VueTetris -> None
        met à jour la couleur de tout le terrain en fonction des valeurs du modèle. 
        '''
        for i in range(0,self.__modele.get_hauteur()):
            ligne =[]
            for j in range(0,self.__modele.get_largeur()):
                self.dessine_case(i,j,self.__modele.get_valeur(i,j))

    def dessine_forme(self, coords, couleur):
        '''VueTetris,(int,int),str -> None
        remplit de couleur les cases dont les coordonnées sont données dans coords. 
        '''
        for i in coords :
            self.dessine_case(i[1],i[0], couleur)
            
    def met_a_jour_score(self,val):
        self.__lbl_score.config(text="Score : "+str(val))
        
    def dessine_case_suivante(self,i,j,coul):
        self.__can_fsuivante.itemconfigure(self.__les_suivants[i][j],fill = COULEURS[coul])

    def nettoie_forme_suivante(self):
        for ligne in range(SUIVANT):
            for colonne in range(SUIVANT):
                self.dessine_case_suivante(ligne,colonne,-1)

    def dessine_forme_suivante(self,coords,coul):
        self.nettoie_forme_suivante()
        for i in coords:
            self.dessine_case_suivante(i[1]+2,i[0]+2,coul)


    
