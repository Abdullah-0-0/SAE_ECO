# classe.py
from random import randint

class Plante:
    '''
    Une plante peut être mise dans le jardin. 
    Elle a un niveau (maturité 0 à 3) et une qualité (0 à 3).
    '''
    def __init__(self, type_plante, injectee=False):
        self.type = type_plante
        self.niveau = 0
        self.qualité = 1
        self.infecté = False
        self.engrais = False
        self.injectee = injectee

    def __str__(self):
        return f"Plante(type={self.type}, niveau={self.niveau}, qualite={self.qualité}, infecte={self.infecté})"
    
    def grandir(self):
        if self.niveau < 3 and not self.infecté:
            self.niveau += 1
        
    def abimé(self):
        self.qualité -= 1
            
    def insect(self):
        if self.infecté:
            self.qualité -= 1
        self.infecté = True
        
    def soin(self):
        self.qualité += 1


class Jardin:
    """
    Le Jardin contient les plantes sous forme de grille.
    """
    def __init__(self, taille):
        self.taille = taille
        self.jardin = [[None]*taille for _ in range(taille)]
        self.recoltes = [] 
        self.investissements = []
        self.employés = []

    def ajout_Plante(self, Plante, pos):
        """Ajoute une plante à la position donnée (ligne, col)."""
        if self.jardin[pos[0]][pos[1]] is not None:
            print(f'Impossible : la position {pos} est déjà occupée.')
            return False
        self.jardin[pos[0]][pos[1]] = Plante
        print(f'La Plante {Plante.type} plantée en position {pos}')
        return True
        
    def suprime_Plante(self, pos):
        """Supprime une plante."""
        if self.jardin[pos[0]][pos[1]] is None:
            print(f'Impossible : la position {pos} est déjà vide.')
            return False
        self.jardin[pos[0]][pos[1]] = None
        print(f'La Plante en position {pos} a été supprimée')
        return True
     
    def arroser_plante(self, pos): 
        try:
            plante = self.jardin[pos[0]][pos[1]]
        except Exception:
            return False
        if plante is None:
            return False
        # Appel direct de la méthode de l'instance
        plante.grandir()
        if plante.engrais:
            plante.grandir()
        return True

    def recolter(self, pos):
        plante = self.jardin[pos[0]][pos[1]]
        nouvelle_recolte = {"type": plante.type, "qualite": plante.qualité}
        self.recoltes.append(nouvelle_recolte)
        self.jardin[pos[0]][pos[1]] = None 
        return True
    
    def engrais(self, pos):
        plante = self.jardin[pos[0]][pos[1]]
        plante.engrais=True
        return True