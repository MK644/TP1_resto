from tkinter import *
import tkinter.font as tkfont
import random
import time
import datetime
from PIL import ImageTk, Image
import pygame

###########################################################
# son (fichiers enregistrés) et horloge
###########################################################

# Structure des fichiers audio (tous en .mp3, dans le dossier du programme) :
#
#   audio/regis/    intro, gratin, plat, dessert, merci, facture
#   audio/aziz/     (les mêmes 6 fichiers)
#   audio/thomas/   (les mêmes 6 fichiers)
#   audio/racim/    (les mêmes 6 fichiers)
#
# La facture n'a pas de voix.

dossiers = {"Régis": "regis", "Aziz": "aziz", "Thomas": "thomas", "Racim": "racim"}
son_actuel = None

try:
    pygame.mixer.init()
except Exception:
    print("(Pas de son : pygame.mixer n'a pas pu démarrer)")


def parler(fichier, qui):
    """Joue audio/<qui>/<fichier>.mp3 (coupe la phrase d'avant)."""
    global son_actuel
    chemin = "audio/" + dossiers[qui] + "/" + fichier + ".mp3"
    try:
        if son_actuel is not None:
            son_actuel.stop()   # coupe la phrase d'avant
        son_actuel = pygame.mixer.Sound(chemin)
        son_actuel.play()
    except Exception:
        print("Audio introuvable :", chemin)


# horloge accélérée : 1 minute = 8 secondes
heure_depart = 18 * 60 + 30   # en minutes (change quand on choisit l'heure)
debut_reel = time.time()


def heure_actuelle():
    minutes = heure_depart + int((time.time() - debut_reel) / 8)
    heures = (minutes // 60) % 24
    reste = minutes % 60
    if int(time.time() * 2) % 2 == 0:
        deux_points = ":"
    else:
        deux_points = " "     # les deux points clignotent
    return f"{heures:02d}{deux_points}{reste:02d}"


def afficher_heure(etiquette):
    if etiquette.winfo_exists():
        etiquette.config(text=heure_actuelle())
        fenetre.after(500, lambda: afficher_heure(etiquette))


def ajouter_horloge(fen):
    etiquette = Label(fen, text=heure_actuelle(), font=("Courier", 14, "bold"))
    etiquette.place(relx=1.0, rely=1.0, anchor=SE, x=-8, y=-6)   # coin en bas à droite
    afficher_heure(etiquette)


###########################################################
# réservation
###########################################################
fenetre = Tk()
fenetre.withdraw()  # cachée tant que reservation() ne l'a pas configurée


def reservation():
    """Fenêtre d'accueil : l'hôtesse inscrit les infos du client
    et lui attribue une table parmi les 9 disponibles."""
    global mon_canevas, tables, champ, champ2, Bouton0, Bouton1, message

    fenetre.deiconify()
    fenetre.title("répétition...")
    fenetre.geometry("500x500")
    fenetre.minsize(500, 500)
    fenetre.maxsize(500, 500)

    mon_canevas = Canvas(fenetre, width=500, height=500)

    # 9 tables numérotées de 1 à 9, disposées en formation cube
    taille = 60
    marge = 10
    espace = 10
    numero = 1
    tables = {}
    decalage_x = 250  # décale tout le paquet de tables vers la droite
    decalage_y = 50
    for ligne in range(3):
        for colonne in range(3):
            x1 = marge + decalage_x + colonne * (taille + espace)
            y1 = marge + decalage_y + ligne * (taille + espace)
            x2 = x1 + taille
            y2 = y1 + taille
            table_id = mon_canevas.create_rectangle(x1, y1, x2, y2, fill="light grey", width=2)
            mon_canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(numero))
            tables[numero] = table_id
            numero += 1

    # boutons "Valider" et "assoir"
    Bouton0 = Button(fenetre, text="Valider", width=11, foreground="black", background="light grey", command=verifier)
    Bouton1 = Button(fenetre, text="assoir", width=11, foreground="grey", background="grey", relief=FLAT, state=DISABLED)
    Bouton0.place(relx=0.2, rely=0.5, anchor=CENTER)
    Bouton1.place(relx=0.2, rely=0.6, anchor=CENTER)

    Bouton0.bind("<Enter>", hover)
    Bouton0.bind("<Leave>", out)

    champ = Entry(fenetre)
    champ.place(x=80, y=105)
    champ2 = Entry(fenetre)
    champ2.place(x=80, y=130)
    Nom = Label(fenetre, text="Nom:")
    Prenom = Label(fenetre, text="Prenom:")
    Nom.place(x=6, y=105)
    Prenom.place(x=6, y=130)

    # message en haut de la fenêtre
    texte = "Bienvenue chez Aziz ! Inscrivez votre nom et prénom pour valider votre réservation du " + date_reservation + " à " + heure + "."
    message = Label(fenetre, text=texte, wraplength=480, justify=LEFT, font=("Arial", 11))
    message.place(x=10, y=8)

    ajouter_horloge(fenetre)
    mon_canevas.pack()
    fenetre.mainloop()


def out(event):
    if Bouton0["state"] == DISABLED:
        return
    Bouton0["bg"] = "light grey"


def hover(event):
    if Bouton0["state"] == DISABLED:
        return
    Bouton0["bg"] = "dark grey"


###########################################################
# validation
###########################################################


def assoir():
    fenetre.withdraw()
    menu()


def changer(Bouton):
    Bouton["foreground"] = "black"
    Bouton["background"] = "light grey"
    Bouton["relief"] = RAISED
    Bouton["state"] = NORMAL
    Bouton["command"] = assoir


def verifier():
    global numero_choisi
    if nom == champ.get() and prenom == champ2.get():
        # choisir une des 9 tables, activer le bouton "assoir"
        changer(Bouton1)
        numero_choisi = random.choice(list(tables.keys()))
        mon_canevas.itemconfig(tables[numero_choisi], fill="white")
        print("Table attribuee :", numero_choisi)
        # désactiver "Valider" (même look que "assoir" désactivé)
        Bouton0.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)
        texte = "Veuillez vous assoir à la table " + str(numero_choisi) + "."
        message.config(text=texte)
    else:
        texte = "Non, aucune réservation à ce nom."
        message.config(text=texte)


###########################################################
# Menu
###########################################################
def commander():
    service()


def activer_commander():
    Bouton3["foreground"] = "black"
    Bouton3["background"] = "lightgrey"
    Bouton3["relief"] = RAISED
    Bouton3["state"] = NORMAL


def compte_menu(secondes):
    if secondes > 0:
        Bouton3["text"] = "COMMANDER (" + str(secondes) + ")"
        fenetre2.after(1000, lambda: compte_menu(secondes - 1))
    else:
        Bouton3["text"] = "COMMANDER"
        activer_commander()


def police_luxe():
    """Choisit la police la plus chic qui est installée sur l'ordinateur."""
    installees = tkfont.families()
    for nom in ["Playfair Display", "Bodoni MT", "Didot", "GFS Didot", "Copperplate",
                "Cormorant Garamond", "EB Garamond", "Garamond", "Palatino Linotype",
                "Book Antiqua", "Georgia", "Times New Roman", "DejaVu Serif", "Times"]:
        if nom in installees:
            return nom
    return "Times"   # si aucune n'est trouvée


def menu():
    global fenetre2, Bouton3
    luxe = police_luxe()
    print("Police du menu :", luxe)
    fenetre2 = Toplevel(fenetre)  # nouvelle fenêtre
    fenetre2.title("Installation")
    fenetre2.geometry("500x500")
    Label(fenetre2, text="Entrées au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Soupe à l'oignon non gratinée : 7,50 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="   Gratinée : +2,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Croquettes de thon : 9,00 $", font=(luxe, 12)).pack(pady=15)

    Label(fenetre2, text="Repas au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Poisson avec pommes de terre : 22,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Steak avec légumes du jardin : 28,00 $", font=(luxe, 12)).pack(pady=15)

    Label(fenetre2, text="Desserts au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Café : 3,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Un quart de gâteau au fromage : 7,00 $", font=(luxe, 12)).pack(pady=15)

    Bouton3 = Button(fenetre2, text="COMMANDER", width=15, foreground="grey", background="grey", relief=FLAT, state=DISABLED, command=commander)
    Bouton3.place(relx=0.5, rely=0.95, anchor=CENTER)
    compte_menu(5)   # compte à rebours de 5 secondes, puis le bouton devient cliquable
    ajouter_horloge(fenetre2)


###########################################################
# service
###########################################################


def reset(bouton):
    bouton["bg"] = "light grey"
    bouton["relief"] = RAISED
    bouton["state"] = NORMAL
    bouton["fg"] = "black"


def selectionner(bouton):
    bouton["fg"] = "lightgreen"
    bouton["bg"] = "lightgreen"
    bouton["relief"] = FLAT
    bouton["state"] = DISABLED


def est_choisi(bouton):
    return bouton.cget("state") == DISABLED


def maj_serveur():
    """Le serveur pose la bonne question selon ce qui est déjà choisi.
    Quand tout est choisi, il remercie et le bouton SERVIR devient actif."""
    soupe_ok = est_choisi(bouton_soupe)
    entree_ok = soupe_ok or est_choisi(bouton_croquette)
    gratin_ok = est_choisi(bouton_gratiner) or est_choisi(bouton_pas_gratiner)
    plat_ok = est_choisi(bouton_poisson) or est_choisi(bouton_steak)
    dessert_ok = est_choisi(bouton_cafe) or est_choisi(bouton_gateau)

    complet = False
    if not entree_ok:
        texte = (f"Bonjour, je m'appelle {nom_serveur}, je serai votre {titre_serveur}.\n\n"
                 "Entrée #1 ou #2 ?\n(soupe ou croquettes)")
        son = "intro"
    elif soupe_ok and not gratin_ok:
        texte = f"{nom_serveur} :\nGratinée ou non gratinée ?"
        son = "gratin"
    elif not plat_ok:
        texte = f"{nom_serveur} :\nRepas #1 ou #2 ?\n(poisson ou steak)"
        son = "plat"
    elif not dessert_ok:
        texte = f"{nom_serveur} :\nDessert #1 ou #2 ?\n(café ou quart de gâteau)"
        son = "dessert"
    else:
        texte = f"{nom_serveur} :\nMerci, ça ne sera pas long !"
        son = "merci"
        complet = True
    parole.config(text=texte)
    parler(son, nom_serveur)   # le serveur dit la phrase (avec sa voix)

    if complet:
        bouton_servir.config(state=NORMAL, foreground="black", background="light grey", relief=RAISED)
    else:
        bouton_servir.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)


def choix_soupe():
    global note1
    selectionner(bouton_soupe)
    reset(bouton_croquette)
    bouton_gratiner.place(relx=0.65, rely=0.37, anchor=CENTER)
    bouton_pas_gratiner.place(relx=0.8, rely=0.37, anchor=CENTER)
    note1 = canvas.create_text(100, 80, text="Soupe à l'oignon")
    try:
        canvas.delete(note2)
    except:
        pass
    maj_serveur()


def choix_croquette():
    global note2
    selectionner(bouton_croquette)
    reset(bouton_soupe)
    reset(bouton_gratiner)
    reset(bouton_pas_gratiner)
    bouton_gratiner.place_forget()
    bouton_pas_gratiner.place_forget()
    note2 = canvas.create_text(100, 80, text="Croquettes de thon")
    try:
        canvas.delete(note1)
    except:
        pass
    try:
        canvas.delete(note3)
    except:
        pass
    try:
        canvas.delete(note4)
    except:
        pass
    maj_serveur()


def choix_gratiner():
    global note3
    selectionner(bouton_gratiner)
    reset(bouton_pas_gratiner)
    note3 = canvas.create_text(100, 100, text="Gratinée")
    try:
        canvas.delete(note4)
    except:
        pass
    maj_serveur()


def choix_pas_gratiner():
    global note4
    selectionner(bouton_pas_gratiner)
    reset(bouton_gratiner)
    note4 = canvas.create_text(100, 100, text="Pas gratiné")
    try:
        canvas.delete(note3)
    except:
        pass
    maj_serveur()


def choix_poisson():
    global note5
    selectionner(bouton_poisson)
    reset(bouton_steak)
    note5 = canvas.create_text(100, 170, text="Poisson avec pommes de terre")
    try:
        canvas.delete(note6)
    except:
        pass
    maj_serveur()


def choix_steak():
    global note6
    selectionner(bouton_steak)
    reset(bouton_poisson)
    note6 = canvas.create_text(100, 170, text="Steak avec légumes du jardin")
    try:
        canvas.delete(note5)
    except:
        pass
    maj_serveur()


def choix_cafe():
    global note7
    selectionner(bouton_cafe)
    reset(bouton_gateau)
    note7 = canvas.create_text(100, 240, text="Café")
    try:
        canvas.delete(note8)
    except:
        pass
    maj_serveur()


def choix_gateau():
    global note8
    selectionner(bouton_gateau)
    reset(bouton_cafe)
    note8 = canvas.create_text(100, 240, text="Un quart de gâteau au fromage")
    try:
        canvas.delete(note7)
    except:
        pass
    maj_serveur()


def servir():
    global listcommande
    listcommande = []
    for bouton in listbouton:
        if bouton.cget("state") == DISABLED:
            listcommande.append(bouton.cget("text"))
    repas()
    # la fenêtre service disparait seulement ici
    fenetre3.destroy()


def service():
    fenetre2.destroy()
    global fenetre3, \
        bouton_soupe, bouton_croquette, bouton_gratiner, bouton_pas_gratiner, \
        bouton_poisson, bouton_steak, bouton_cafe, bouton_gateau, bouton_servir, \
        note1, note2, note3, note4, note5, note6, note7, note8, \
        listbouton, \
        canvas, parole, nom_serveur, titre_serveur

    # serveur au hasard parmi 4 prénoms
    nom_serveur, titre_serveur = random.choice([
        ("Régis", "serveur"),
        ("Aziz", "serveur"),
        ("Thomas", "serveur"),
        ("Racim", "serveur"),
    ])

    fenetre3 = Toplevel(fenetre)
    fenetre3.title("Service")
    fenetre3.geometry("500x500")
    bouton_soupe = Button(fenetre3, text="Soupe", width=8, foreground="black", background="light grey", command=choix_soupe)
    bouton_croquette = Button(fenetre3, text="Croquette", width=8, foreground="black", background="light grey", command=choix_croquette)
    bouton_gratiner = Button(fenetre3, text="Gratiner", width=8, foreground="black", background="light grey", command=choix_gratiner)
    bouton_pas_gratiner = Button(fenetre3, text="Pas gratiner", width=8, foreground="black", background="light grey", command=choix_pas_gratiner)
    bouton_poisson = Button(fenetre3, text="Poisson", width=8, foreground="black", background="light grey", command=choix_poisson)
    bouton_steak = Button(fenetre3, text="Steak", width=8, foreground="black", background="light grey", command=choix_steak)
    bouton_cafe = Button(fenetre3, text="Café", width=8, foreground="black", background="light grey", command=choix_cafe)
    bouton_gateau = Button(fenetre3, text="gâteau", width=8, foreground="black", background="light grey", command=choix_gateau)
    # SERVIR : grisé tant que le serveur n'a pas remercié
    bouton_servir = Button(fenetre3, text="SERVIR", width=11, foreground="grey", background="grey", relief=FLAT, state=DISABLED, command=servir)

    bouton_soupe.place(relx=0.65, rely=0.3, anchor=CENTER)
    bouton_croquette.place(relx=0.8, rely=0.3, anchor=CENTER)
    bouton_poisson.place(relx=0.65, rely=0.45, anchor=CENTER)
    bouton_steak.place(relx=0.8, rely=0.45, anchor=CENTER)
    bouton_cafe.place(relx=0.65, rely=0.55, anchor=CENTER)
    bouton_gateau.place(relx=0.8, rely=0.55, anchor=CENTER)
    bouton_servir.place(relx=0.85, rely=0.85, anchor=CENTER)
    listbouton = [bouton_soupe, bouton_croquette, bouton_gratiner, bouton_pas_gratiner, bouton_poisson, bouton_steak, bouton_cafe, bouton_gateau]

    # ce que dit le serveur
    parole = Label(fenetre3, text="", font=("Arial", 11), wraplength=240, justify=LEFT)
    parole.place(x=240, y=20)

    # IMAGE
    canvas = Canvas(fenetre3, width=200, height=460, highlightthickness=0)
    canvas.place(x=20, y=20)

    try:
        note = ImageTk.PhotoImage(
            Image.open("note.png").resize((200, 460))
        )
        canvas.create_image(0, 0, image=note, anchor=NW)
        canvas.note = note
    except FileNotFoundError:
        # si note.png est introuvable : un bloc-note dessiné à la place
        canvas.create_rectangle(0, 0, 200, 460, fill="lightyellow", outline="black")

    ajouter_horloge(fenetre3)
    maj_serveur()


###########################################################
# repas a table
###########################################################

# ---------- entrées ----------
def soupe():
    canvas2.create_oval(50, 50, 450, 450, fill="saddlebrown")
    canvas2.create_oval(70, 70, 430, 430, fill="beige")
    canvas2.create_arc(100, 100, 250, 250, fill="burlywood", style="chord")
    canvas2.create_arc(80, 200, 230, 350, fill="burlywood", style="chord")
    canvas2.create_arc(70, 300, 220, 450, fill="burlywood", style="chord")
    canvas2.create_arc(200, 250, 350, 400, fill="burlywood", style="chord")
    if "Gratiner" in listcommande:
        canvas2.create_rectangle(95, 180, 110, 260, fill="wheat")
        canvas2.create_rectangle(150, 110, 165, 190, fill="wheat")
        canvas2.create_rectangle(242, 90, 257, 170, fill="wheat")
        canvas2.create_rectangle(335, 110, 350, 190, fill="wheat")
        canvas2.create_rectangle(380, 200, 395, 280, fill="wheat")
        canvas2.create_rectangle(300, 270, 315, 350, fill="wheat")
        canvas2.create_rectangle(210, 300, 225, 380, fill="wheat")
        canvas2.create_rectangle(130, 270, 145, 350, fill="wheat")
        canvas2.create_rectangle(220, 190, 235, 270, fill="wheat")


def croquette():
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    canvas2.create_oval(124, 232, 184, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(188, 232, 248, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(252, 232, 312, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(316, 232, 376, 268, fill="goldenrod", outline="saddlebrown", width=2)


# ---------- repas ----------
def poisson():
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    # queue
    canvas2.create_polygon(330, 230, 395, 190, 395, 270, fill="peru", outline="saddlebrown", width=3)
    # corps (la tête est coupée à gauche)
    canvas2.create_polygon(176, 198, 206, 191, 240, 188, 274, 191, 304, 198, 327, 209, 338, 223, 338, 237, 327, 251, 304, 262, 274, 269, 240, 272, 206, 269, 176, 262, fill="peru", outline="saddlebrown", width=3)

    # arêtes
    canvas2.create_line(165, 230, 335, 230, fill="ivory", width=4)
    canvas2.create_line(195, 230, 205, 208, fill="ivory", width=3)
    canvas2.create_line(195, 230, 205, 252, fill="ivory", width=3)
    canvas2.create_line(220, 230, 230, 208, fill="ivory", width=3)
    canvas2.create_line(220, 230, 230, 252, fill="ivory", width=3)
    canvas2.create_line(245, 230, 255, 208, fill="ivory", width=3)
    canvas2.create_line(245, 230, 255, 252, fill="ivory", width=3)
    canvas2.create_line(270, 230, 280, 208, fill="ivory", width=3)
    canvas2.create_line(270, 230, 280, 252, fill="ivory", width=3)
    canvas2.create_line(295, 230, 305, 208, fill="ivory", width=3)
    canvas2.create_line(295, 230, 305, 252, fill="ivory", width=3)

    # pommes de terre
    canvas2.create_oval(180, 300, 230, 330, fill="khaki", outline="darkgoldenrod", width=2)
    canvas2.create_oval(240, 300, 290, 330, fill="khaki", outline="darkgoldenrod", width=2)
    canvas2.create_oval(300, 300, 350, 330, fill="khaki", outline="darkgoldenrod", width=2)


def steak():
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    canvas2.create_oval(100, 180, 200, 320, fill="#7b3b21", outline="#4a1f10", width=3)

    # Marques de grill
    canvas2.create_line(120, 205, 180, 215, fill="#3a180b", width=4)
    canvas2.create_line(115, 240, 185, 250, fill="#3a180b", width=4)
    canvas2.create_line(120, 275, 180, 285, fill="#3a180b", width=4)
    # Carottes (cercles orange)
    canvas2.create_oval(270, 110, 310, 150, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(320, 130, 360, 170, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(220, 80, 260, 120, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(380, 180, 420, 220, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(270, 170, 310, 210, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(330, 200, 370, 240, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(375, 225, 415, 265, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(270, 230, 310, 270, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(320, 245, 360, 285, fill="orange", outline="darkorange", width=2)

    # Haricots (rectangles verts)
    canvas2.create_rectangle(270, 290, 400, 302, fill="green", outline="darkgreen")
    canvas2.create_rectangle(260, 310, 390, 322, fill="green", outline="darkgreen")
    canvas2.create_rectangle(230, 340, 350, 352, fill="green", outline="darkgreen")
    canvas2.create_rectangle(220, 360, 360, 372, fill="green", outline="darkgreen")
    canvas2.create_rectangle(200, 380, 330, 392, fill="green", outline="darkgreen")
    canvas2.create_rectangle(210, 400, 300, 412, fill="green", outline="darkgreen")


# ---------- desserts ----------
def cafe():
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    canvas2.create_oval(170, 170, 330, 330, fill="white", outline="gray", width=2)     # soucoupe
    canvas2.create_oval(295, 238, 330, 262, outline="gray", width=4)                   # anse
    canvas2.create_oval(200, 200, 300, 300, fill="white", outline="gray", width=2)     # tasse
    canvas2.create_oval(212, 212, 288, 288, fill="saddlebrown")                        # café


def gateau():
    # autre assiette : bord bleu
    canvas2.create_oval(50, 50, 450, 450, fill="lightblue")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    # un quart de gâteau
    canvas2.create_arc(40, 180, 320, 460, start=0, extent=90, style="pieslice", fill="papaya whip", outline="saddlebrown", width=3)
    # fraise rouge
    canvas2.create_oval(244, 224, 256, 234, fill="forestgreen")
    canvas2.create_oval(236, 231, 264, 259, fill="red", outline="darkred", width=2)


def afficher_plat():
    canvas2.delete("all")   # l'assiette est vidée
    etapes[etape_actuelle]()   # chaque plat dessine sa propre assiette


def manger():
    global etape_actuelle
    etape_actuelle += 1
    if etape_actuelle < len(etapes):
        afficher_plat()      # plat suivant
    else:
        miettes()            # dernier "manger" : assiette vide avec des miettes
        bouton_manger.config(text="APPELER SERVEUR", width=16, command=appeler_serveur)


def assiette_vide():
    canvas2.delete("all")
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")


def miettes():
    assiette_vide()
    canvas2.create_oval(170, 230, 178, 236, fill="burlywood")
    canvas2.create_oval(215, 190, 222, 195, fill="tan")
    canvas2.create_oval(260, 175, 268, 181, fill="burlywood")
    canvas2.create_oval(300, 205, 307, 210, fill="sandybrown")
    canvas2.create_oval(325, 255, 334, 261, fill="tan")
    canvas2.create_oval(285, 300, 292, 305, fill="burlywood")
    canvas2.create_oval(230, 320, 238, 326, fill="sandybrown")
    canvas2.create_oval(190, 285, 196, 290, fill="tan")
    canvas2.create_oval(250, 245, 258, 251, fill="burlywood")
    canvas2.create_oval(205, 255, 210, 259, fill="sandybrown")


def compte_repas(secondes):
    if secondes > 0:
        canvas2.delete("compte")
        canvas2.create_text(250, 250, text="Votre plat arrive dans " + str(secondes) + "...", font=("Arial", 14), tags="compte")
        fenetre4.after(1000, lambda: compte_repas(secondes - 1))
    else:
        debut_repas()


def compte_facture(secondes):
    if secondes > 0:
        canvas2.delete("compte")
        canvas2.create_text(250, 250, text="La facture arrive dans " + str(secondes) + "...", font=("Arial", 14), tags="compte")
        fenetre4.after(1000, lambda: compte_facture(secondes - 1))
    else:
        montrer_facture()


def appeler_serveur():
    bouton_manger.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)
    canvas2.create_text(250, 25, text=nom_serveur + " : Je vous apporte la facture.", font=("Arial", 12))
    parler("facture", nom_serveur)
    compte_facture(3)   # la facture apparait 3 secondes plus tard


def montrer_facture():
    fenetre4.destroy()   # on ferme la fenêtre du repas avant
    facture()            # la facture termine le programme elle-même


def debut_repas():
    bouton_manger.place(relx=0.5, rely=0.95, anchor=CENTER)
    afficher_plat()   # premier plat (l'entrée)


def repas():
    global fenetre4, canvas2, etapes, etape_actuelle, bouton_manger
    fenetre4 = Toplevel(fenetre)
    fenetre4.title("Repas")
    fenetre4.geometry("500x500")
    # fermer cette fenêtre termine le programme
    fenetre4.protocol("WM_DELETE_WINDOW", fenetre.destroy)
    canvas2 = Canvas(fenetre4, width=500, height=500, bg="white")
    canvas2.pack()
    assiette_vide()   # assiette vide au début
    ajouter_horloge(fenetre4)

    bouton_manger = Button(fenetre4, text="MANGER", width=11, foreground="black", background="light grey", command=manger)

    # les plats dans l'ordre : entrée, repas, dessert
    etapes = []
    if "Soupe" in listcommande:
        etapes.append(soupe)
    if "Croquette" in listcommande:
        etapes.append(croquette)
    if "Poisson" in listcommande:
        etapes.append(poisson)
    if "Steak" in listcommande:
        etapes.append(steak)
    if "Café" in listcommande:
        etapes.append(cafe)
    if "gâteau" in listcommande:
        etapes.append(gateau)

    etape_actuelle = 0
    compte_repas(5)   # 5 secondes avec l'assiette vide, puis le bouton et le premier plat


###########################################################
# facture
###########################################################

prix = {"Soupe": 7.50, "Gratiner": 2.00, "Croquette": 9.00,
        "Poisson": 22.00, "Steak": 28.00, "Café": 3.00, "gâteau": 7.00}
# noms courts pour que ça rentre sur le ticket
noms_ticket = {"Soupe": "Soupe", "Gratiner": "Gratinée", "Croquette": "Croquettes",
               "Poisson": "Poisson", "Steak": "Steak", "Café": "Café", "gâteau": "Gâteau"}


def argent(montant):
    return f"{montant:.2f}".replace(".", ",") + " $"


def facture():
    pygame.init()
    ecran = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Facture")

    # Polices style ticket (petites pour laisser la place à la photo)
    police = pygame.font.SysFont("couriernew,consolas,courier", 14)
    gras = pygame.font.SysFont("couriernew,consolas,courier", 20, bold=True)

    # la photo du terminal de paiement, rapetissée, pour le côté droit
    try:
        terminal = pygame.image.load("terminal.png").convert_alpha()
        terminal = pygame.transform.smoothscale(terminal, (235, 235))
    except Exception:
        terminal = None    # pas de photo : la facture s'affiche quand même

    table = numero_choisi     # la table donnée par l'hôte
    serveur = nom_serveur     # le serveur qui nous a servis

    # les articles de la facture (donc pas "Pas gratiner")
    articles = []
    soustotal = 0
    for article in ["Soupe", "Gratiner", "Croquette", "Poisson", "Steak", "Café", "gâteau"]:
        if article in listcommande:
            articles.append(article)
            soustotal += prix[article]

    tps = soustotal * 0.05
    tvq = soustotal * 0.10      # TPS + TVQ = 15 %
    total = soustotal * 1.15

    # la date de la réservation et l'heure de l'horloge accélérée
    date_facture = date_reservation
    heure_facture = heure_actuelle().replace(" ", ":")   # sans clignotement

    def texte(t, x, y, f=police):
        ecran.blit(f.render(t, True, "black"), (x, y))

    def texte_droite(t, y, f=police):
        surface = f.render(t, True, "black")
        ecran.blit(surface, (245 - surface.get_width(), y))   # le ticket finit à x = 245

    running = True
    while running:
        for event in pygame.event.get():
            # fermer la fenêtre, appuyer sur une touche ou cliquer = fin du programme
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        ecran.fill("white")

        # la photo à droite
        if terminal is not None:
            ecran.blit(terminal, (262, 95))

        # le ticket à gauche
        texte(f"TABLE N°{table}", 70, 12)

        # Les articles
        y = 42
        for article in articles:
            texte("1 " + noms_ticket[article], 10, y)
            texte_droite(argent(prix[article]), y)
            y += 20

        y += 6
        texte("SOUS-TOTAL", 30, y)
        texte_droite(argent(soustotal), y)
        y += 20
        texte("TPS", 30, y)
        texte_droite(argent(tps), y)
        y += 18
        texte("TVQ", 30, y)
        texte_droite(argent(tvq), y)

        y += 26
        texte("TOTAL", 10, y, gras)
        texte_droite(argent(total), y, gras)

        y += 36
        texte("Date : " + date_facture, 10, y)
        texte("Heure : " + heure_facture, 10, y + 18)

        y += 50
        texte("TPS : 000000000 RT0001", 10, y)
        texte("TVQ : 000000000 TQ0001", 10, y + 15)

        y += 45
        texte("VOUS AVEZ ÉTÉ SERVI", 10, y)
        texte("PAR : " + serveur, 40, y + 16)

        texte("Appuyez sur une touche pour quitter", 10, 470)

        # l'horloge accélérée dans le coin (les deux points clignotent)
        h = police.render(heure_actuelle(), True, "black")
        ecran.blit(h, (492 - h.get_width(), 470))

        pygame.display.flip()
        pygame.time.wait(50)

    pygame.quit()       # arrête aussi la musique
    fenetre.destroy()   # ferme tout : le programme est fini


###########################################################
# Lancement du programme
###########################################################

TEST = False   # True = ouvre seulement la fenêtre repas (sans réservation) / False = programme normal

if TEST:
    # fausse commande pour tester : change la liste comme tu veux
    nom_serveur = "Régis"
    numero_choisi = 5
    date_reservation = "lundi 1 janvier"
    listcommande = ["Soupe", "Gratiner", "Poisson", "Café"]
    # autres exemples : ["Croquette", "Steak", "gâteau"]  /  ["Soupe", "Pas gratiner", "Steak", "gâteau"]
    repas()
    fenetre.mainloop()
else:
    print("Bienvenue chez Aziz, le restaurant reconnu pour ses 4 étoiles Michelin !")

    # la date : les 4 prochains jours
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
            "septembre", "octobre", "novembre", "décembre"]
    aujourdhui = datetime.date.today()
    dates = []
    for i in range(1, 5):
        jour = aujourdhui + datetime.timedelta(days=i)
        dates.append(jours[jour.weekday()] + " " + str(jour.day) + " " + mois[jour.month - 1])
    print("Pour quelle date souhaitez-vous venir ?")
    print("Nous prenons les réservations pour les 4 prochains jours :")
    for i in range(4):
        print("  " + str(i + 1) + ". " + dates[i])
    choix_date = input("Laquelle voulez-vous (1 à 4) ? ")
    while choix_date != "1" and choix_date != "2" and choix_date != "3" and choix_date != "4":
        choix_date = input("Désolé, choisissez un numéro de 1 à 4 : ")
    date_reservation = dates[int(choix_date) - 1]

    # l'heure
    print("À quelle heure souhaitez-vous venir ?")
    print("Nous avons 4 réservations disponibles ce soir-là :")
    print("  1. 17h00")
    print("  2. 18h30")
    print("  3. 20h00")
    print("  4. 21h30")
    choix = input("Laquelle voulez-vous prendre (1 à 4) ? ")
    while choix != "1" and choix != "2" and choix != "3" and choix != "4":
        choix = input("Désolé, choisissez un numéro de 1 à 4 : ")
    if choix == "1":
        heure = "17h00"
    elif choix == "2":
        heure = "18h30"
    elif choix == "3":
        heure = "20h00"
    else:
        heure = "21h30"

    print("Très bien ! À quel nom la réservation ?")
    nom = input("Nom: ")
    prenom = input("Prenom: ")
    print("Ok, réservation prise le " + date_reservation + " à " + heure + " au nom de " + prenom + " " + nom + ".")
    print("Merci, hâte de vous voir chez Aziz !")

    # l'horloge du restaurant part de l'heure de la réservation
    heure_depart = int(heure[0:2]) * 60 + int(heure[3:5])
    debut_reel = time.time()

    # la musique commence ici, une fois la réservation prise dans la console
    try:
        pygame.mixer.music.load("musique.mp3")   # le fichier doit être dans le même dossier que le programme
        pygame.mixer.music.set_volume(0.3)       # 0.0 = muet, 1.0 = fort
        pygame.mixer.music.play(-1)              # -1 = recommence sans arrêt
    except Exception:
        print("(Pas de musique : mets musique.mp3 dans le dossier)")

    reservation()
