import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

def afficher_page_fin(root, pestel, nb_plantes, qualite_moyenne, variete_perc, rejouer_callback, quitter_callback):
    # ================================
    # LOGIQUE DU BILAN
    # ================================
    moyenne_pestel = sum(pestel) / len(pestel)

    if moyenne_pestel >= 75 and nb_plantes >= 6:
        image_fond = "asset/jardin_accueil.png"
        titre_bilan = "EXCELLENCE STRATEGIQUE"
        message = (
            "Felicitations. Vous avez parfaitement maitrise votre micro-environnement. "
            "En anticipant les facteurs PESTEL, vous avez transforme les menaces en opportunites, "
            "ce qui a permis une recolte abondante et de haute qualite."
        )
        color_bilan = "#27ae60"
    elif moyenne_pestel >= 60 and nb_plantes < 4:
        image_fond = "asset/jardin_accueil.png"
        titre_bilan = "GESTION PRUDENTE"
        message = (
            "Votre analyse des facteurs externes est bonne, mais votre jardin manque de productivite. "
            "Vous avez securise l'environnement sans exploiter pleinement le potentiel de vos terres."
        )
        color_bilan = "#2980b9"
    elif moyenne_pestel < 50 and nb_plantes >= 5:
        image_fond = "asset/jardin_detruit.png"
        titre_bilan = "PRODUCTION FRAGILE"
        message = (
            "Attention : bien que vous ayez recolte plusieurs plantes, vous avez ignore le macro-environnement. "
            "Votre structure est vulnerable aux crises politiques ou legales. "
            "Un jardin ne peut survivre longtemps sans une veille environnementale active."
        )
        color_bilan = "#e67e22"
    else:
        image_fond = "asset/jardin_detruit.png"
        titre_bilan = "ALERTE DE GESTION"
        message = (
            "Le bilan est insuffisant. Le manque d'attention aux indicateurs PESTEL a laisse les facteurs "
            "externes degrader votre culture. Sans une vision globale des forces en presence, "
            "le micro-environnement ne peut pas prosperer."
        )
        color_bilan = "#c0392b"

    # ================================
    # FRAME + CANVAS OVERLAY
    # ================================
    W, H = 700, 700

    # Frame parent pour contrôler le z-order
    overlay_frame = ctk.CTkFrame(root, width=W, height=H, fg_color="transparent")
    overlay_frame.place(x=0, y=0)
    overlay_frame.lift()  # <-- met la frame au-dessus de tout

    canvas = ctk.CTkCanvas(overlay_frame, width=W, height=H, highlightthickness=0, bg="#1e1e1e")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", lambda e: None)  # ignore les clics

    # --- Image de fond ---
    try:
        img = Image.open(image_fond).resize((W, H), Image.LANCZOS)
        bg = ImageTk.PhotoImage(img)
        canvas.bg_ref = bg
        canvas.create_image(0, 0, anchor="nw", image=bg)
    except Exception:
        canvas.configure(bg="#1e1e1e")

    # --- Overlay blanc arrondi ---
    def overlay_arrondi(w, h, r, color):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((0, 0, w, h), r, fill=color)
        return ImageTk.PhotoImage(img)

    overlay = overlay_arrondi(640, 620, 35, (255, 255, 255, 225))
    canvas.overlay_ref = overlay
    canvas.create_image(30, 40, anchor="nw", image=overlay)

    # --- Textes ---
    canvas.create_text(350, 80, text="RAPPORT D'ANALYSE FINALE",
                       font=("Segoe UI", 24, "bold"), fill="#2c3e50")
    canvas.create_text(350, 125, text=titre_bilan,
                       font=("Segoe UI", 16, "bold"), fill=color_bilan)
    canvas.create_text(350, 175, text=message,
                       font=("Segoe UI", 11), fill="#34495e", width=550, justify="center")

    text_stats = f"Recolte : {nb_plantes} unites  |  Qualite : {qualite_moyenne}%  |  Variete : {variete_perc}%"
    canvas.create_text(350, 230, text=text_stats,
                       font=("Segoe UI", 12, "bold"), fill="#2c3e50")
    canvas.create_line(150, 255, 550, 255, fill="#bdc3c7", width=1)

    # --- Jauges PESTEL ---
    ETIQUETTES = ["Politique", "Economique", "Social", "Technologique", "Environnement", "Legal"]
    start_y = 300
    espacement_y = 45
    for i, (nom, valeur) in enumerate(zip(ETIQUETTES, pestel)):
        y = start_y + i * espacement_y
        canvas.create_text(110, y, text=nom, anchor="w", font=("Segoe UI", 11, "bold"), fill="#333")
        couleur = "#2ecc71" if valeur > 70 else "#f39c12" if valeur > 40 else "#e74c3c"
        barre = ctk.CTkProgressBar(root, orientation="horizontal", width=250, height=12,
                                   progress_color=couleur, fg_color="#ecf0f1",
                                   border_color="#bdc3c7", border_width=1)
        barre.set(valeur / 100)
        canvas.create_window(350, y, window=barre)
        canvas.create_text(520, y, text=f"{valeur}%", font=("Segoe UI", 11, "bold"), fill=couleur)

    # --- Note pédagogique ---
    canvas.create_line(200, 560, 500, 560, fill="#bdc3c7", width=1)
    canvas.create_text(350, 590,
                       text=("L'analyse PESTEL est indispensable en gestion : elle permet de comprendre "
                             "comment les decisions mondiales impactent votre projet local."),
                       font=("Segoe UI", 9, "italic"), fill="#7f8c8d", width=500, justify="center")

    # ================================
    # BOUTONS
    # ================================
    def fermer_overlay():
        overlay_frame.destroy()
        quitter_callback()


    btn_rejouer = ctk.CTkButton(root, text="REJOUER", width=140, height=35,
                                corner_radius=20, font=("Segoe UI", 12, "bold"),
                                command=lambda: [overlay_frame.destroy(), rejouer_callback()])
    canvas.create_window(270, 630, window=btn_rejouer)

    btn_quitter = ctk.CTkButton(root, text="FERMER", width=140, height=35,
                                corner_radius=20, fg_color="#d9534f", hover_color="#c9302c",
                                font=("Segoe UI", 12, "bold"), command=fermer_overlay)
    canvas.create_window(430, 630, window=btn_quitter)