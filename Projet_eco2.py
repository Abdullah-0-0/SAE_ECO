from random import*
from PIL import Image, ImageTk
from accueil import afficher_page_accueil
from fin import afficher_page_fin
import classe as cl
import customtkinter as ctk

"""
python3 -m venv .venv
source .venv/bin/activate
pip3 install bibliotheque/darkdetect-0.8.0-py3-none-any.whl
pip3 install bibliotheque/packaging-25.0-py3-none-any.whl
pip3 install bibliotheque/customtkinter-5.2.2-py3-none-any.whl
pip3 install bibliotheque/pillow-12.1.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
"""

# ======================
# VARIABLE GLOBALE
# ======================

journal = []
Action_joueur = []
conséquences_pestel = []
ETIQUETTES_PESTEL = ['Politique', 'Économique', 'Social', 'Technologique', 'Environnement', 'Légal']
PESTEL = []
case_clique=-1
nb_tours = 0
nb_tours_actuel = 0 
nb_action_actuel = 0
nb_action = 5
nombre_actuialité = 33
seuil_bas = 20
seuil_haut = 80
peut_faire_action = False
mon_jardin = None
type_plante = ["colza","romarin","tomate","orchide","fraise","coquelicot","vanille","plante_médicinale","tournesol"]
type_plante_accessible = ["colza","romarin","tomate","orchide","fraise","coquelicot","vanille","plante_médicinale","tournesol"]
fleur_can=None
fleur_choisie=""
Can_temp = None
#=======
evenements_différés = []
messages_pestel_tour_suivant = []
multiplicateur_cout_action = 1
action_gratuite = False
modificateur_actions_social = 0


actions_interdites = []
label_tour = None
progress_tour = None
label_action = None
progress_action = None
label_message = None
double_plante = False
indice_de_niveau=1

# ======================
# AFFICHAGE 
# ======================


### initialisation de la fenetre graphique ###
Mafenetre = ctk.CTk()
Mafenetre.geometry("700x700")
Mafenetre.title("Le Jardin")
Mafenetre.configure(bg="Dark")


### importation des images ###


journal_de_bord_image = ctk.CTkImage(light_image=Image.open("asset/journal_de_bord.png"),
                                  dark_image=Image.open("asset/journal_de_bord.png"),
                                  size=(70, 70))

mascotte = ctk.CTkImage(light_image=Image.open("asset/mascotte.png"),
                                  dark_image=Image.open("asset/mascotte.png"),
                                  size=(130, 200))

terre_image = ctk.CTkImage(light_image=Image.open("asset/fleur/terre.png"),
                                  dark_image=Image.open("asset/fleur/terre.png"),
                                  size=(80, 80))

### Création des Canvas ### *
jeu = ctk.CTkCanvas(Mafenetre, width=700, height=700 ,bg="#8DD618")
jeu.pack()

### Police custom tkinet ###
Titre = ctk.CTkFont(family="Arial", size=30, weight="bold")
texte = ctk.CTkFont(family="Times New Roman", size=20, weight="normal")

def afficher_jardin ():
    import os
    global jeu,mon_jardin 
    affichage_création_jardin()
    ligne = 0
    
    for elt in mon_jardin.jardin:
        colonne =0
        for el in elt :
            if el != None :
                # Déterminer le chemin selon si la plante est infectée
                if hasattr(el, 'infecté') and el.infecté:
                    base_chemin = "asset/fleur/infecté/"+str(el.type)+str(el.niveau)
                else:
                    base_chemin = "asset/fleur/"+str(el.type)+str(el.niveau)
                
                # Chercher d'abord .png, puis .jpg
                if os.path.exists(base_chemin + ".png"):
                    chemin = base_chemin + ".png"
                elif os.path.exists(base_chemin + ".jpg"):
                    chemin = base_chemin + ".jpg"
                else:
                    chemin = base_chemin + ".png"  # Par défaut, sinon erreur
                
                image_plante = ctk.CTkImage(light_image=Image.open(chemin),
                                    dark_image=Image.open(chemin),
                                    size=(80, 80))
                plante = ctk.CTkLabel(jeu,text = "", image = image_plante , height=80,width=80)
                plante.place(x=200+(100*colonne),y=200+(100*ligne))
            colonne+=1
        
        ligne +=1

def affichage():
    '''
    permet la création de l'interface graphique avec tkinter 
    '''
    global jeu, label_tour, label_action,progress_tour,progress_action,nb_tours_actuel,nb_tours,nb_action_actuel,nb_action
    button_journal = ctk.CTkButton(jeu, 
                                   text="", 
                                   command=affichage_journal_de_bord,
                                    image=journal_de_bord_image,
                                    corner_radius=50,
                                    width=70, height=70,
                                    fg_color="transparent",
                                     )
    button_journal.place(x=550, y=600)
    jardinier = ctk.CTkLabel(jeu,image=mascotte, text="")
    jardinier.place(x=10,y=480)
    afficher_jardin ()
    label_tour = ctk.CTkLabel(jeu, 
                              text=f"Tour : {nb_tours_actuel} / {nb_tours}", 
                              font=("Arial", 20, "bold"),
                              text_color="white",
                              fg_color="#333333",
                              corner_radius=8,
                              width=120, height=40)
    label_tour.place(x=20, y=20)
    progress_tour = ctk.CTkProgressBar(jeu, 
                                orientation="horizontal",
                                progress_color="#1EC5DF",
                                fg_color="#333333",
                                corner_radius=8,
                                width=120, height=15) 
    progress_tour.place(x=20, y=75)
    progress_tour.set(nb_tours_actuel / nb_tours)
                              

    label_action = ctk.CTkLabel(jeu, 
                              text=f"Action : {nb_action_actuel} / {nb_action}", 
                              font=("Arial", 20, "bold"),
                              text_color="white",
                              fg_color="#333333",
                              corner_radius=8,
                              width=120, height=40)
    label_action.place(x=550, y=20)
    progress_action = ctk.CTkProgressBar(jeu, 
                                orientation="horizontal",
                                progress_color="#1EC5DF",
                                fg_color="#333333",
                                corner_radius=8,
                                width=120, height=15) 
    progress_action.place(x=550, y=75)
    progress_action.set(1)
    choix_action_joueur()


   
def affichage_journal_de_bord_print(liste_evenements):
    print("Journal de bord :")
    for cat, texte in liste_evenements:
        print(f"- {texte}")

 
def affichage_journal_de_bord():
    global journal, nb_tours_actuel
    
    # Création de la fenêtre du journal
    Journal = ctk.CTkToplevel() 
    Journal.geometry("550x650")
    Journal.title("Journal de bord")
    Journal.attributes("-topmost", True) 

    # Zone de contenu défilante
    frame_contenu = ctk.CTkScrollableFrame(Journal, width=520, height=500, fg_color="white")
    frame_contenu.pack(pady=(10, 0), padx=10, fill="both", expand=True)

    def construire_contenu():
        # Nettoyer le contenu actuel pour rafraîchir
        for widget in frame_contenu.winfo_children():
            widget.destroy()

        # --- SECTION ACTUALITÉS ---
        label_titre_actu = ctk.CTkLabel(frame_contenu, text="ACTUALITÉS", 
                                        text_color="black", font=Titre)
        label_titre_actu.pack(pady=(10, 20))

        for elt in journal:
            if len(elt) >= 2:
                texte_brut = str(elt[1])
                if "[BILAN]" not in texte_brut:
                    lbl = ctk.CTkLabel(frame_contenu, text=f"• {texte_brut}", 
                                       text_color="black", font=texte, 
                                       wraplength=450, justify="left")
                    lbl.pack(pady=5, padx=20, anchor="w")

        # --- SECTION BILAN ---
        if nb_tours_actuel > 0:
            ctk.CTkLabel(frame_contenu, text="_______________________________________", 
                text_color="gray").pack(pady=20)
            
            label_titre_bilan = ctk.CTkLabel(frame_contenu, text="BILAN DU TOUR PRÉCÉDENT", 
                                            text_color="#2C3E50", font=("Arial", 22, "bold"))
            label_titre_bilan.pack(pady=(0, 20))

            for elt in journal:
                texte_brut = str(elt[1])
                if "[BILAN]" in texte_brut:
                    affichage_propre = texte_brut.replace("[BILAN] ", "")
                    lbl_bilan = ctk.CTkLabel(frame_contenu, text=f"📋 {affichage_propre}", 
                                            text_color="blue", font=texte, 
                                            wraplength=450, justify="left")
                    lbl_bilan.pack(pady=5, padx=20, anchor="w")

   
    construire_contenu()

    # --- BARRE DE BOUTONS ---
    frame_boutons = ctk.CTkFrame(Journal, fg_color="transparent")
    frame_boutons.pack(pady=15, fill="x")

    # Bouton Actualiser
    btn_refresh = ctk.CTkButton(frame_boutons, text='🔄 ACTUALISER', width=120, height=40,
                                 fg_color="#27AE60", hover_color="#219150",
                                 command=construire_contenu)
    btn_refresh.pack(side="left", padx=50)

    # Bouton Quitter
    btn_quitter = ctk.CTkButton(frame_boutons, text='QUITTER', width=120, height=40, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=Journal.destroy)
    btn_quitter.pack(side="right", padx=50)

    Journal.mainloop()
def affichage_création_jardin(): 
    global jeu,terre_image
    x_place= 200
    
    for i in range (3):
        y_place= 200
        for e in range (3):
            terre = ctk.CTkLabel(jeu,text = "", image = terre_image , height=80,width=80)
            terre.place(x= x_place,y=y_place)
            y_place+=100
        x_place+=100


def afficher_messages_pestel(liste_messages):
    if not liste_messages:
        return

  
    notif = ctk.CTkFrame(
        jeu, 
        fg_color="#2C3E50", 
        corner_radius=0  
    )
    notif.place(x=20, y=70)

    label_notif = ctk.CTkLabel(
        notif, 
        text="BILAN : Consultez le journal de bord", 
        font=("Arial", 12, "bold"), 
        text_color="#F1C40F", 
        padx=12, 
        pady=8
    )
    label_notif.pack(side="left")

    btn_close = ctk.CTkButton(
        notif, 
        text="✕", 
        width=25, 
        height=25, 
        fg_color="transparent", 
        hover_color="#E74C3C", 
        corner_radius=0, 
        command=notif.destroy
    )
    btn_close.pack(side="right", padx=5)


def afficher_message(texte, couleur):
    global label_message, message_after_id

    if label_message is None:
        label_message = ctk.CTkLabel(
            jeu,
            text="",
            text_color="white",
            fg_color=couleur,
            corner_radius=0,
            font=("Arial", 15, "bold"),
            wraplength=450,
            anchor="center"     
        )
        label_message.place(relx=0.5, y=120, anchor="center")

    label_message.configure(text=texte, fg_color=couleur)


def init_jauge():
    # P, E, S, T, E, L
    return [50, 50, 50, 50, 50, 50]

# ======================
# choix d'une case 
# ======================

def choix_case(callback):
    global  label_selection,Can_temp
    Can_temp = ctk.CTkCanvas(Mafenetre, width=700, height=700 ,bg="#8DD618")
    Can_temp.place(x=0,y=0)
    label_selection = ctk.CTkLabel(
        Can_temp, text='SELECTIONNER UNE CASE',
        fg_color='red', width=200, height=20, text_color="white"
    )
    label_selection.place(x=230, y=115)

    

    def selectionner_case(numero):
        global nb_action_actuel,Can_temp
        Can_temp.destroy()
        
        if numero != -1:
            callback(numero)
        else :
            # si on a annulé l'action
            nb_action_actuel +=1
            update_label_action()

    for i in range(1, 10):
        posX = 200 + ((i-1) % 3) * 100
        posY = 200 + ((i-1) // 3) * 100

        btn = ctk.CTkButton(
            Can_temp, text="",
            command=lambda n=i: selectionner_case(n),
            width=80, height=80, fg_color="brown"
        )
        btn.place(x=posX, y=posY)


    btn = ctk.CTkButton(
        Can_temp, text="Annuler",
        command=lambda n=-1: selectionner_case(n),
        width=80, height=80, fg_color="blue",corner_radius = 90, hover_color='red',
        )
    btn.place(x=250, y=600)



# ======================
# SYSTEME DE CHARGEMENT DES FLEURS
# ======================
def selectionner_Fleur_continuer(nb):
    """Cette fonction est appelée quand on clique sur un bouton de choix"""
    global fleur_choisie, mon_jardin
    nb -=1
    if mon_jardin.jardin[nb//3][(nb) % 3] != None :
        choix_case(selectionner_Fleur_continuer)
        erreur = ctk.CTkLabel(Can_temp, text="Invalide", text_color="white", fg_color="red")
        erreur.place(x=300, y=150)
        jeu.after(1000, erreur.destroy)
        
    else :
        nouvelle_plante = cl.Plante(fleur_choisie)
        mon_jardin.ajout_Plante(nouvelle_plante,(nb//3, (nb) % 3)) 
        afficher_jardin()
    afficher_message("✓ Plante ajoutée","green")


def selectionner_Fleur(numero):
    """Cette fonction est appelée quand on clique sur un bouton de choix"""
    global  fleur_can,fleur_choisie
    fleur_can.destroy()
    fleur_choisie = type_plante_accessible[numero]
    choix_case(selectionner_Fleur_continuer)


  
def choix_fleur(): 
    global fleur_can,type_plante_accessible
    fleur_can = ctk.CTkCanvas(Mafenetre, width=700, height=700 ,bg="#8DD618")
    fleur_can.place(x=0,y=0)

    for i in range(0, len(type_plante_accessible)):
        #position du bouton plante
        colonne = i % 3
        ligne = i // 3
        posX = 150 + (colonne * 150)
        posY = 150 + (ligne * 120)
        
      
        btn = ctk.CTkButton(fleur_can, text=type_plante_accessible[i], 
                             command=lambda n=i: selectionner_Fleur(n), 
                             width=80, height=80, fg_color="blue")
        btn.place(x=posX, y=posY)


def recolter_fleur_continuer(nb) : 
    global mon_jardin,double_plante
    if mon_jardin.jardin[nb//3][(nb - 1) % 3] == None or (mon_jardin.jardin[nb//3][(nb - 1) % 3].niveau!=2):

        choix_case(recolter_fleur_continuer)
        erreur = ctk.CTkLabel(Can_temp, text="Invalide", text_color="white", fg_color="red")
        erreur.place(x=300, y=150)
        jeu.after(1000, erreur.destroy)

    else :
        if double_plante :
            double_plante = False
            mon_jardin.recolter((nb//3,(nb - 1) % 3))
            afficher_message("✓ Plante récoltée, et doublé", "green")
            mon_jardin.recoltes.append( mon_jardin.recoltes[-1])
            afficher_jardin()
        else :

            mon_jardin.recolter((nb//3,(nb - 1) % 3))
            afficher_message("✓ Plante récoltée", "green")
            afficher_jardin()


def recolter_fleur() :
    choix_case(recolter_fleur_continuer)

def engrais_continuer(nb):
    global mon_jardin

    nb -= 1
    i, j = nb // 3, nb % 3
    plante = mon_jardin.jardin[i][j]

    if plante is None:
        choix_case(engrais_continuer)
        erreur = ctk.CTkLabel(Can_temp, text="Aucune plante ici", text_color="white", fg_color="red")
        erreur.place(x=300, y=150)
        jeu.after(1000, erreur.destroy)
        return

    if plante.engrais:
        choix_case(engrais_continuer)
        erreur = ctk.CTkLabel(Can_temp, text="Déjà fertilisée", text_color="white", fg_color="red")
        erreur.place(x=300, y=150)
        jeu.after(1000, erreur.destroy)
        return

    mon_jardin.engrais((i, j))
    afficher_message("✓ Engrais appliqué", "green")
    afficher_jardin()

def engrais():
    choix_case(engrais_continuer)


# ======================
# SYSTEME DE CHARGEMENT DES ACTIONS 
# ======================

liste_action_possible = [
    'fin',  # 0
    'planter',  # 1
    'arroser',  # 2
    'soin',  # 3
    'insecticide',  # 4
    'recolter',  # 5
    'engrais',  # 6 
]


Action_joueur_pestel = [-1,-1,-1,-1,-1,-1]

def realise_actions(nb):
    """
    Réalise une action selon sa valeur.
    
    Paramètres:
    -----------
    nb : int
        Le numéro de l'action à réaliser
        0 = fin (ne rien faire)
        1 = planter une nouvelle plante
        2 = arroser une plante
        3 = soin d'une plante
        4 = insecticide (traiter les parasites)
        5 = recolter une plante
        6 = engrais
    """
    global mon_jardin,fleur_can,nb_action_actuel
    
    if nb == 0:  # fin
        afficher_message("Fin de Tour","Green")
        fin_de_tour()

        
    elif nb == 1:  # planter
        
        choix_fleur()
        
        
    elif nb == 2:  # arroser
        
        # Arroser toutes les plantes du jardin
        plantes_arrosées = 0
        for i in range(mon_jardin.taille):
            for j in range(mon_jardin.taille):
                if mon_jardin.jardin[i][j] is not None:
                    if mon_jardin.jardin[i][j].niveau <2:
                        mon_jardin.arroser_plante((i, j))
                        plantes_arrosées += 1
                    else :
                        mon_jardin.jardin[i][j].abimé()
                    
        if plantes_arrosées == 1:
            message = "✓ "+str(plantes_arrosées)+" plante arrosée"
            afficher_message(message, "green")
        if plantes_arrosées > 1:
            message = "✓ "+str(plantes_arrosées)+" plante arrosées"
            afficher_message(message, "green")
        if plantes_arrosées == 0:
            nb_action_actuel += 1
            update_label_action()
            afficher_message("Aucune plante à arroser", "red")
        
            
        
    elif nb == 3:  # soin
        
        plantes_soignées = 0

        for i in range(mon_jardin.taille):
            for j in range(mon_jardin.taille):
                plante = mon_jardin.jardin[i][j]
                if plante is not None and plante.qualité < 2:
                    plante.soin()
                    plantes_soignées += 1

        if plantes_soignées == 1:
            afficher_message("✓ 1 plante soignée", "green")
        elif plantes_soignées > 1:
            afficher_message(f"✓ {plantes_soignées} plantes soignées", "green")
        else:
            nb_action_actuel+=1
            update_label_action()
            afficher_message("Aucune plante à soigner", "red")
          

        
    elif nb == 4:  # insecticide
       
        plantes_traitées = 0

        for i in range(mon_jardin.taille):
            for j in range(mon_jardin.taille):
                plante = mon_jardin.jardin[i][j]
                if plante is not None and plante.infecté:
                    plante.infecté = False
                    plante.qualité = max(0, plante.qualité - 1)
                    plantes_traitées += 1

        if plantes_traitées == 1:
            afficher_message("✓ 1 plante traitée", "green")
        elif plantes_traitées > 1:
            afficher_message(f"✓ {plantes_traitées} plantes traitées", "green")
        else:
            nb_action_actuel+=1
            update_label_action()
            afficher_message("Aucune plante infectée", "red")


        
    elif nb == 5:  # recolter
        recolter_fleur()
        

    elif nb == 6:  # engrais
        engrais()
        
    
    else:
        afficher_message(liste_action_possible[nb], "green")


    # actualisation 
    afficher_jardin ()
    


# ======================
# CHOIX D'UNE ACTION
# ======================

def selectionner_action(nb):
    """Cette fonction est appelée quand on clique sur un bouton de choix"""
    global  peut_faire_action, Action_joueur,nb_action_actuel,Action_joueur_pestel
    if nb == 0:
        realise_actions(nb)
    elif peut_faire_action :
        Action_joueur.append(nb)
        nb_action_actuel -=1
        Action_joueur.append(Action_joueur_pestel[nb])
        update_label_action()
        realise_actions(nb)
        if nb_action_actuel <=0 :
            peut_faire_action=False
            afficher_message("Tu ne peux plus faire d'action pour ce tour", "blue")

        

def choix_action_joueur():
    global jeu
    update_label_action()
   
    posX =50
    j=1
    p=450

    for i in range(1, len(liste_action_possible)):
     
        
        posY = p - ((i-j) ) * 50
        if posY < 150  :
            posX = 550 
            p=550
            j=i
      
        btn = ctk.CTkButton(jeu, text=liste_action_possible[i], 
                            command=lambda n=i: selectionner_action(n), 
                            width=50, height=30, fg_color="blue")
        btn.place(x=posX, y=posY)
    btn = ctk.CTkButton(jeu, text=liste_action_possible[0], 
                        command=lambda n=0: selectionner_action(n), 
                        width=80, height=80, fg_color="blue",corner_radius = 90, hover_color='red')
    btn.place(x=posX, y=posY)
    
class CustomMenu(ctk.CTkFrame):
    def __init__(self, master, titre, options, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        self.options = options
        self.titre = titre
        self.menu_ouvert = False

       
        self.main_button = ctk.CTkButton(
            self, 
            text=self.titre, 
            command=self.toggle_menu,
            fg_color="#1f78b4",     
            hover_color="#145a8d",
            height=50,
            width=250,
            corner_radius=8,
            font=("Segoe UI Emoji", 14)
        )
        self.main_button.pack(pady=0)

       
        self.dropdown_frame = ctk.CTkFrame(
            self, 
            fg_color="#2b2b2b",     
            corner_radius=12,
            border_width=1,
            border_color="#3d3d3d"
        )
        
        # Création des boutons à l'intérieur du menu
        for n in range(1,len(self.options)):

            btn = ctk.CTkButton(
                self.dropdown_frame,
                text=self.options[n],
                fg_color="#333333",   
                hover_color="#444444",
                text_color="white",
                height=30,
                width=230,
                corner_radius=6,
                command=lambda i=n: self.fermer_apres_clic(i),
                font=("Segoe UI Emoji", 14)
            )
            btn.pack(pady=2, padx=5)
    def toggle_menu(self):
        if self.menu_ouvert:
            self.dropdown_frame.pack_forget()
        else:
            self.dropdown_frame.pack(pady=10)
            self.dropdown_frame.lift() 
        self.menu_ouvert = not self.menu_ouvert
        self.lift() 
    def fermer_apres_clic(self, indice):
        selectionner_action(indice)
        self.dropdown_frame.pack_forget()
        self.menu_ouvert = False


def choix_action_joueur():
    global jeu,menu_jeu
    menu_jeu = CustomMenu(jeu, "Choix d'action", liste_action_possible)
    menu_jeu.place(relx=0.5, y =20, anchor="n")
    boutton_fin =ctk.CTkButton(
                jeu,
                text="Fin du tour",
                fg_color="blue",  
                hover_color="red",
                text_color="white",
                height=80,
                width=100,
                corner_radius=30,
                command=lambda i=0: selectionner_action(i)
                )
    boutton_fin.place(x=300,y=550)
        
    
        
def update_label_action():
    global label_action, nb_action_actuel, nb_action, progress_action
    if label_action is not None:
        label_action.configure(
            text=f"Action : {nb_action_actuel} / {nb_action}")
        progress_action.set((nb_action_actuel/nb_action))
            



# ======================
# EVENEMENTS
# ======================

def Charger_Actualité(ligne_choix):
    """Lit le fichier et le transforme en tuple `journal_bord.txt`.

    Renvoie une liste d'événements sous la forme [(types_evt, texte), ...].
    Spécialité: ingestion de données d'événements externes; ne modifie pas les jauges.
    """

    

    Actualités = []
    fichier = open('journal_bord.txt', "r", encoding="utf-8")
    lignes = fichier.readlines()
    fichier.close()

    for i in ligne_choix:
        ligne = lignes[i].strip()
        
        if ligne: 
            parties = ligne.split('"') # Découpe la ligne par les guillemets
            
         
            pestel_brut = parties[0].split('[')[1].split(']')[0]
   
            indices = [int(x) for x in pestel_brut.split(',')]
            
         
            texte = parties[1]
            

            
            
            Actualités.append((indices, texte))
            
    return Actualités


def choix_evenement_exterieur(nb_evenements):
    global nombre_actuialité
    """Choisit aléatoirement des événements externes à afficher dans le journal de bord.
    """
    liste = []
    for _ in range (nb_evenements):
        liste.append(randint(10, nombre_actuialité-1))
    return Charger_Actualité(liste)


# ======================
#  CONSEQUENCES/evenements
# ======================


def charger_consequences_evenements_pestel(fichier):
    """
    Charge les événements PESTEL depuis un fichier.
    Format attendu :
    [index],"+","texte";
    [index],"-","texte";

    Retour :
    {
        0: {"positif": "...", "negatif": "..."},
        ...
    }
    """
    consequences = {}

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()

            # ignorer lignes vides ou non conformes (ex: "model")
            if not ligne.startswith("["):
                continue

            try:
                # extraction de l'index
                idx = int(ligne.split("[")[1].split("]")[0])

                # extraction du signe et du texte
                parties = ligne.split('"')
                signe = parties[1]
                texte = parties[3]

                if idx not in consequences:
                    consequences[idx] = {"positif": None, "negatif": None}

                if signe == "+":
                    consequences[idx]["positif"] = texte
                elif signe == "-":
                    consequences[idx]["negatif"] = texte

            except (IndexError, ValueError):
                # ligne mal formée → on l’ignore proprement
                continue

    return consequences


EVENEMENTS_PESTEL = charger_consequences_evenements_pestel("consequences_evenement.txt")   

    


def modifie_jauge(PESTEL, actions_joueur, actualités):
    """
    Modifie les valeurs des jauges PESTEL en fonction des actions du joueur et des actualités.
    Wrapper pour traiter_actualités pour compatibilité.
    
    Paramètres:
    -----------
    PESTEL : list
        Les jauges PESTEL [P, E, S, T, En, L]
    actions_joueur : list
        Liste des numéros d'actions effectuées par le joueur
    actualités : list
        Liste des actualités
    
    Retour:
    -------
    PESTEL : list
        Les jauges mises à jour
    """
    global indice_de_niveau
     # Vérifier pour chaque actualité si l'action demandée a été réalisée
    print(actualités)
    for indices_pestel, texte in actualités:
        indices_pestel = indices_pestel[0]  
        
        
        if indices_pestel in actions_joueur:
            # L'action demandée a été réalisée : augmenter les jauges
           
            PESTEL[indices_pestel] = min(100, PESTEL[indices_pestel] + (7*indice_de_niveau))
        else:
            # L'action n'a pas été réalisée : diminuer les jauges
            PESTEL[indices_pestel] = max(0, PESTEL[indices_pestel] - (10*indice_de_niveau))
            
    
    # Borne les v5aleurs entre 0 et 100
    PESTEL = [max(0, min(100, val)) for val in PESTEL]
    return PESTEL
    

def consequence_evenement(PESTEL):
    """
    Analyse les jauges PESTEL et prépare les messages de conséquences
    pour le début du tour suivant.
    """
    global evenements_différés, messages_pestel_tour_suivant

    for i, valeur in enumerate(PESTEL):
        nom_jauge = ETIQUETTES_PESTEL[i]

        # =====================
        # CAS NÉGATIF (Seuil Bas)
        # =====================
        if valeur <= seuil_bas:
            if EVENEMENTS_PESTEL[i]["negatif"]:
                texte = EVENEMENTS_PESTEL[i]["negatif"]
                messages_pestel_tour_suivant.append(f"⚠️ {texte}")

            # Programmation des effets techniques pour le tour suivant
            if i == 0: evenements_différés.append(politique_negatif_action)
            elif i == 1: evenements_différés.append(economique_negatif)
            elif i == 2: evenements_différés.append(social_negatif_actions)
            elif i == 3: evenements_différés.append(arrivee_insectes)
            elif i == 4: evenements_différés.append(degradation_ecologique)
            elif i == 5: evenements_différés.append(activer_legal_bas)

        # =====================
        # CAS POSITIF (Seuil Haut)
        # =====================
        elif valeur >= seuil_haut:
            if EVENEMENTS_PESTEL[i]["positif"]:
                texte = EVENEMENTS_PESTEL[i]["positif"]
                messages_pestel_tour_suivant.append(f"{texte}")

            if i == 0: evenements_différés.append(politique_positif_plante_gratuite)
            elif i == 1: evenements_différés.append(economique_positif)
            elif i == 2: evenements_différés.append(social_positif_actions)
            elif i == 3: evenements_différés.append(protection_technologique)
            elif i == 4: evenements_différés.append(croissance_ecologique)
            elif i == 5: evenements_différés.append(lever_legal)

# ======================
# CONSEQUENCES DIFFÉRÉES
# ======================

def appliquer_evenements_différés():
    """
    Applique tous les effets différés stockés dans `evenements_différés`.
    Chaque fonction de la liste est appelée, puis la liste est vidée.
    Effets : insectes, croissance écologique, dégradation, légal, économique, social, technologique...
    """
    global evenements_différés

    # Appliquer tous les effets différés
    for effet in evenements_différés:

        effet()  # appelle la fonction (ex: arrivee_insectes, croissance_ecologique, etc.)

    # Vider la liste pour que les effets ne se répètent pas
    evenements_différés.clear()

def politique_positif_plante_gratuite():
    """
    Effet politique positif :
    - autorise UNE plantation gratuite au prochain tour
    """
    """
    Plante automatiquement une plante sur la première case vide trouvée.
    """
    global mon_jardin

    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            if mon_jardin.jardin[i][j] is None:
                nouvelle_plante = cl.Plante("romarin", injectee=True) 
                mon_jardin.ajout_Plante(nouvelle_plante, (i, j))
                
                afficher_message("Une plante gratuite a été plantée en ({i}, {j})", "green")
                return

def politique_negatif_action():
    """
    Effet politique négatif :
    - supprime une action
    """
    global nb_action

    nb_action -=1



def arrivee_insectes():
    """
    Infecte aléatoirement des plantes du jardin.
    Effet mécanique appliqué au début du tour suivant.
    """
    global mon_jardin, nombre_insectes
    nombre_insectes = 2
    plantes_saines = []

    # Récupérer toutes les plantes non infectées
    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            plante = mon_jardin.jardin[i][j]
            if plante is not None and not plante.infecté:
                plantes_saines.append(plante)

    # Aucun effet possible
    if not plantes_saines:
        return

    # Mélange aléatoire
    shuffle(plantes_saines)

    # Infecter jusqu'à nombre_insectes plantes
    for plante in plantes_saines[:nombre_insectes]:
        plante.infecté = True

def protection_technologique():
    """
    Effet positif technologique :
    - élimine toutes les infections
    - améliore la qualité des plantes
    Effet appliqué au tour suivant.
    """
    global mon_jardin

    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            plante = mon_jardin.jardin[i][j]
            if plante is not None:
                if plante.infecté:
                    plante.infecté = False
                plante.qualité = min(3, plante.qualité + 1)

def croissance_ecologique():
    """
    Effet positif environnemental :
    - accélère la croissance des plantes
    - améliore leur qualité
    Effet appliqué au tour suivant.
    """
    global mon_jardin

    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            plante = mon_jardin.jardin[i][j]
            if plante is not None:
                # augmentation du niveau de croissance
                plante.niveau = min(3, plante.niveau + 1)
                # amélioration de la qualité
                plante.qualité = min(3, plante.qualité + 1)

def degradation_ecologique():
    """
    Effet négatif environnemental :
    - réduit la qualité des plantes
    - détruit les plantes trop fragiles (qualité <= 0)
    Effet appliqué au tour suivant.
    """
    global mon_jardin

    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            plante = mon_jardin.jardin[i][j]
            if plante is not None:
                # diminution de la qualité
                plante.qualité -= 1

                # destruction si trop faible
                if plante.qualité <= 0:
                    mon_jardin.jardin[i][j] = None

def economique_positif():
    """
    Effet économique positif :
    - plante automatiquement une plante gratuite sur une case vide
    """
    global double_plante

    double_plante = True
    afficher_message("Votre Prochaine plantes compte double", "green")
    return


def economique_negatif():
    """
    Inflation :
    - interdit l'action planter
    """
    global actions_interdites

    if 1 not in actions_interdites:  
        actions_interdites.append(1)

def social_positif_actions():
    """
    Effet social positif :
    - l’entraide des voisins améliore la qualité des plantes fragiles
    """
    global mon_jardin
    for i in range(mon_jardin.taille):
        for j in range(mon_jardin.taille):
            plante = mon_jardin.jardin[i][j]
            if plante and plante.qualité < 2:
                plante.qualité += 1
                afficher_message(" Plante en ({i}, {j}) renforcée grâce à l’entraide des voisins", "green")


def social_negatif_actions():
    """
    Effet social négatif :
    - un changement de mode provoque la destruction d'une plante aléatoire
    """
    global mon_jardin
    from random import shuffle

    # Récupérer toutes les positions occupées
    positions = [(i, j) for i in range(mon_jardin.taille)
                          for j in range(mon_jardin.taille)
                          if mon_jardin.jardin[i][j] is not None]
    if not positions:
        return  # aucune plante à détruire

    # Mélanger et supprimer une plante
    shuffle(positions)
    i, j = positions[0]
    mon_jardin.jardin[i][j] = None
    afficher_message("Une plante a été détruite en ({i},{j}) à cause du changement de mode", "red")


def activer_legal_bas():
    """
    Effet légal négatif :
    - interdit certaines actions pour le prochain tour
    """
    global mon_jardin
    if len(mon_jardin.recoltes) != 0:
        mon_jardin.recoltes =  mon_jardin.recoltes[:len(mon_jardin.recoltes)-1]
        afficher_message("une plante de votre recolte est perdu")

def lever_legal():
    """
    Effet légal positif :
    - lève toutes les interdictions, toutes les actions redeviennent possibles
    """
    global nb_action
    nb_action+=1
    afficher_message("Vous gagner une action", "Green")





# ======================
# BOUCLE DE JEU
# ======================
    

def fin_de_tour():
    global mon_jardin, journal, nb_tours, nb_tours_actuel, nb_action_actuel, PESTEL, peut_faire_action,menu_jeu
    peut_faire_action = False

    actus_pour_calcul = [info for info in journal if len(info) == 2 and info[0]]

    PESTEL = modifie_jauge(PESTEL, Action_joueur, actus_pour_calcul)
    
    consequence_evenement(PESTEL)
    nb_tours_actuel += 1 
    afficher_jardin()

    if nb_tours_actuel == nb_tours:
        print("Fin du jeu")
        recoltes = mon_jardin.recoltes 
        nombre = len(recoltes)

        if nombre > 0:
            # 1. Calcul Qualité
            somme_qualite = sum([p['qualite'] for p in recoltes])
            moyenne_qualite = int((somme_qualite / (nombre * 3)) * 100)
            if moyenne_qualite > 100: moyenne_qualite = 100

            # 2. Calcul Variété
            # On récupère les types uniques récoltés
            types_recoltes = set([p['type'] for p in recoltes])
            # On compare au nombre total de types possibles (9 dans ton code)
            nb_total_especes = len(type_plante) 
            pourcentage_variete = int((len(types_recoltes) / nb_total_especes) * 100)
        else:
            moyenne_qualite = 0
            pourcentage_variete = 0
                
        # On envoie maintenant 'pourcentage_variete' à la fonction
        afficher_page_fin(
            Mafenetre,
            PESTEL,
            nombre,
            moyenne_qualite,
            pourcentage_variete,
            relancer_tout_le_projet,
            quitter_tout_le_projet
        )
        return
    tour()


def faire_actions_joueur() :
    global nb_action_actuel,Action_joueur,liste_action_possible,peut_faire_action

    afficher_message('A vous de jouer', "green")
    peut_faire_action = True

action_restante = []
with open("actions.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        ligne = ligne.strip()
        action_restante.append( (int((ligne.split(",")[0])[1]), ligne.split(",")[1]) )
    
    
def ajouter_action() :
    global Action_joueur_pestel,liste_action_possible,action_restante
    temp = randint(0,len(action_restante)-1)
    Action_joueur_pestel.append(action_restante[temp][0])
    liste_action_possible.append(action_restante[temp][1])
    action_restante = [elt for elt in action_restante if elt != action_restante[temp]]

    
def tour(): 
    global mon_jardin, journal, nb_tours_actuel, messages_pestel_tour_suivant,progress_tour, label_tour,nb_action_actuel, nb_action, label_action, Action_joueur,indice_de_niveau
    if nb_tours_actuel == 4 :
        indice_de_niveau=2
        nb_action +=3
    if nb_tours_actuel == 8 :
        indice_de_niveau=3
        nb_action +=3
    if label_tour is not None:  
        label_tour.configure(text=f"Tour : {nb_tours_actuel + 1} / {nb_tours}")
        progress_tour.set((nb_tours_actuel)/nb_tours)

    if nb_tours_actuel >= 1 and nb_tours_actuel <= 6:
        ajouter_action()
        ajouter_action()
    
    afficher_jardin()
    choix_action_joueur()
    
    journal = choix_evenement_exterieur(indice_de_niveau)

    if nb_tours_actuel > 0:
        if messages_pestel_tour_suivant:
            for msg in messages_pestel_tour_suivant:
                journal.append(([ ], f"[BILAN] {msg}", 0))
            
            afficher_messages_pestel(messages_pestel_tour_suivant)
            
            appliquer_evenements_différés()
        
            messages_pestel_tour_suivant = []

    nb_action_actuel = nb_action
    if label_action is not None:
        label_action.configure(text=f"Action : {nb_action_actuel} / {nb_action}")
    Action_joueur = []
    
    faire_actions_joueur()


def jouer():
    # On déclare 'jeu' en global pour que 'affichage()' puisse le voir
    global mon_jardin, journal, nb_tours, nb_tours_actuel, PESTEL, indice_de_niveau, nb_action, jeu

    # 3. Réinitialisation des données
    indice_de_niveau = 1
    nb_action = 3
    nb_tours_actuel = 0 
    nb_tours = 12
    PESTEL = init_jauge()
    mon_jardin = cl.Jardin(3)
    
    p1 = cl.Plante("tomate")
    mon_jardin.ajout_Plante(p1, (0, 0))

    # 4. Lancement de l'interface
    affichage() 
    tour()


def relancer_tout_le_projet():
    afficher_page_accueil(Mafenetre, jouer)

def quitter_tout_le_projet():
    Mafenetre.destroy()

# ======================
# LANCEMENT
# ======================

if __name__ == "__main__":
    
    afficher_page_accueil(Mafenetre, jouer)


Mafenetre.mainloop()