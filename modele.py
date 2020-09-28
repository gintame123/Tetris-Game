from random import randint
LES_FORMES = [[(0,3),(0,0),(0,1),(0,2)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(-1,1)],[(0,0),(-1,0),(0,1),(1,1)],[(-1,1),(-1,0),(0,0),(1,0)],[(0,0),(-1,0),(1,0),(1,1)],[(0,0),(-1,0),(1,0),(0,-1)]]

class ModeleTetris :
    def __init__(self, lig= 14, col= 10):
        self.__haut = lig + 4
        self.__larg = col
        self.__base = 4
        self.__terrain = []
        self.__score = 0
        self.__suivante = Forme(self)
        
        for i in range(self.__haut):
            liste =[]
            for j in range( self.__larg):
                if i < self.__base:
                    liste.append(-2)
                else:
                    liste.append(-1)
            self.__terrain.append(liste)
        self.__forme = Forme(self)

    def get_largeur(self):
        '''ModeleTetris -> int
        retourne la valeur de la largeur.
        '''
        return self.__larg

    def get_hauteur(self):
        '''ModeleTetris -> int
        retourne la valeur de la hauteur.
        '''
        return self.__haut
    
    def get_base(self):
        '''ModeleTetris -> int
        retourne la valeur de la base.
        '''
        return self.__base

    def get_valeur(self, lig,col):
        '''ModeleTetris,int,int -> int
        retourne la valeur du terrain dans la case correspondante à la ligne lig et colonne col données.
        '''
        return self.__terrain[lig][col]

    def get_score(self):
        return self.__score
    
    def est_occupe(self,lig,col):
        '''ModeleTetris,int,int -> Booléen
        retourne True si la case du terrain correspondante à la ligne lig et colonne col données est occupée. Sinon, il return False.
        '''
        if self.get_valeur(lig,col) == -1 or self.get_valeur(lig,col) == -2:
            return False
        else:
            return True

    def fini(self):
        '''ModeleTetris -> Bouléen
        retourne True si la partie est fini. Sinon, il retourne False
        '''
        for i in self.__terrain[self.__base]:
            if i >= 0:
                return True
        return False

    def ajoute_forme(self):
        '''ModeleTetris -> None
        ajoute une forme sur le terrain. 
        '''
        li = self.__forme.get_coords()
        for i in li:
            self.__terrain[i[1]][i[0]] = self.__forme.get_couleur()

    def forme_tombe(self):
        '''ModeleTetris -> Booléen
         retourne True s’il y a eu collision, faux sinon. 
        '''
        if not self.__forme.tombe():
            return False
        else:
            self.ajoute_forme()
            self.__forme = self.__suivante
            self.__suivante = Forme(self)
            self.supprimes_lignes_completes()
            return True

    def get_couleur_forme(self):
        ''''ModeleTetris -> int
        retourne la couleur de la forme. 
        '''
        return self.__forme.get_couleur()

    def get_coords_forme(self):
        '''ModeleTetris -> (int,int)
        retourne les coordonnees absolues  de la forme. 
        '''
        return self.__forme.get_coords()

    def forme_a_gauche(self):
        '''ModeleTetris -> None
        permet de déplacer la forme à gauche
        '''
        self.__forme.a_gauche()

    def forme_a_droite(self):
        '''ModeleTetris -> None
        permet de déplacer la forme à droite
        '''
        self.__forme.a_droite()

    def forme_tourne(self):
        '''ModeleTetris -> None
         demande a la forme de tourner
        '''
        self.__forme.tourne()
        
    def est_ligne_complete(self,lig):
        for i in range(self.get_largeur()):
            if not(self.est_occupe(lig,i)):
                return False
        return True
    
    def supprime_ligne(self,lig):
        for i in range(lig-1,self.__base,-1):
            for j in range(self.get_largeur()):
                self.__terrain[i+1][j] = self.__terrain[i][j]
        for k in range(self.get_largeur()):
            self.__terrain[self.__base][k] = -1
            
    def supprimes_lignes_completes(self):
        for lig in range(self.__base,self.get_hauteur()):
            if self.est_ligne_complete(lig):
                self.supprime_ligne(lig)
                self.__score += 1
                
    def get_coords_suivante(self):
        return self.__suivante.get_coords_relatives()

    def get_couleur_suivante(self):
        return self.__suivante.get_couleur()

class Forme:
    def __init__(self,ModeleTetris):
        self.__modele= ModeleTetris
        ket = randint(0,6)
        self.__couleur = ket
        self.__forme = LES_FORMES[ket]
        self.__x0= randint(2,self.__modele.get_largeur()-2)
        self.__y0= 1

    def get_couleur(self):
        '''Forme -> int
        retourne la couleur de la forme.
        '''
        return self.__couleur

    def get_coords(self):
        '''Forme -> (int,int)
        retourne les coordonnees absolues de la forme sur le terrain du modèle.
        '''
        res= []
        for i in self.__forme:
            res.append((self.__x0+i[0], self.__y0+i[1]))
        return res

    def collision(self):
        '''Forme -> Booléen
        retourne True si la forme doit se poser, False sinon.
        '''
        li = self.get_coords()
        for i in li:
            if i[1]+1 == self.__modele.get_hauteur():
                return True
            if (self.__modele.est_occupe(i[1]+1, i[0])):
                return True
        return False

    def tombe(self):
        '''Forme -> Booléen
        retourne True s’il y a eu collision et que la forme n’a pas bouge, False sinon. 
        '''
        if self.collision() == True:
            return True
        else:
            self.__y0+=1
            return False
        
    def position_valide(self):
        '''Forme -> Booléen
        retourne True si chaque coordonnee absolue (x,y)de la forme est valide. Sinon returne False.
        '''
        for couple_coords in self.get_coords():
            if couple_coords[0] < 0 or couple_coords[0] >= self.__modele.get_largeur():
                return False
            if couple_coords[1] > self.__modele.get_hauteur():
                return False
            if self.__modele.est_occupe(couple_coords[1],couple_coords[0]):
                return False
        return True

    def a_gauche(self):
        '''Forme -> None
        déplace la forme d’une colonne vers la gauche si la position de la forme est valide, sinon la forme reste à sa position initiale.
        '''
        self.__x0 -=1
        if not self.position_valide():
            self.__x0 += 1

    def a_droite(self):
        '''Forme -> None
        déplace la forme d’une colonne vers la droite si la position de la forme est valide, sinon la forme reste à sa position initiale.
        '''
        self.__x0 += 1
        if not self.position_valide():
            self.__x0 -= 1

    def tourne(self):
        '''Forme -> None
        fait pivoter la forme si la position de la forme est valide, sinon la forme reste à sa position initiale.
        '''
        forme_prec = self.__forme
        self.__forme =[]
        
        for couple_coords in forme_prec:
            self.__forme.append((couple_coords[1]*-1,couple_coords[0]))
        if not self.position_valide():
            self.__forme = forme_prec
            
    def get_coords_relatives(self):
        return self.__forme
            
        
        
                                        
                                        

    
                
