import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

def charger_texte_accueil(nom_fichier="histoire.txt"):
    """Charge le texte depuis un fichier externe avec encodage UTF-8."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return "Bienvenue ! (Fichier texte manquant)"
    except Exception as e:
        return f"Erreur de lecture : {e}"

def afficher_page_accueil(fenetre_principale, callback_demarrage):
    # --- Configuration et Canvas ---
    W, H = 700, 700
    canvas = ctk.CTkCanvas(fenetre_principale, width=W, height=H, highlightthickness=0)
    canvas.place(x=0, y=0)

    # --- Image de fond ---
    try:
        img_brute = Image.open("asset/jardin_accueil.png")
        img_res = img_brute.resize((W, H), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_res)
        canvas.image_fond = img_tk 
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
    except:
        canvas.configure(bg="#2D5A27")

    # --- Overlay Arrondi ---
    def creer_rectangle_arrondi(largeur, hauteur, rayon, couleur_rgba):
        img = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((0, 0, largeur, hauteur), radius=rayon, fill=couleur_rgba)
        return ImageTk.PhotoImage(img)

    overlay_tk = creer_rectangle_arrondi(550, 380, 30, (255, 255, 255, 210))
    canvas.overlay_ref = overlay_tk
    canvas.create_image(75, 120, anchor="nw", image=overlay_tk)

    # --- Titre ---
    canvas.create_text(350, 175, text="LE JARDIN DE L'ÉQUILIBRE", 
                       font=("Arial", 20, "bold"), fill="#1B4D3E")

    # --- Zone de texte pour l'histoire ---
    id_texte_histoire = canvas.create_text(
        350, 240, 
        text="", 
        font=("Segoe UI", 11), # 'Segoe UI' ou 'Helvetica' sont plus modernes qu'Arial
        fill="#2C3E50", 
        width=440,            # Largeur max avant retour à la ligne
        justify="center",      # Centre le bloc de texte
        anchor="n"             # Accroche le texte par le haut
    )

    # --- Chargement et Animation ---
    # On récupère le texte depuis le fichier externe
    contenu_histoire = charger_texte_accueil("histoire.txt")

    def animer_texte(index=0):
        if canvas.winfo_exists() and index <= len(contenu_histoire):
            canvas.itemconfig(id_texte_histoire, text=contenu_histoire[:index])
            # On peut varier la vitesse (ex: 30ms)
            fenetre_principale.after(30, lambda: animer_texte(index + 1))

    animer_texte()

    # --- Bouton ---
    def demarrer():
        canvas.destroy()
        btn.destroy() # On détruit le bouton séparément s'il est placé hors canvas
        callback_demarrage()

    btn = ctk.CTkButton(fenetre_principale, text="COMMENCER", 
                        fg_color="#27AE60", hover_color="#1E8449",
                        width=220, height=55, font=("Arial", 16, "bold"), 
                        corner_radius=0,
                        command=demarrer)
    btn.place(x=350, y=560, anchor="center")