#Mika, Racim, Elliot, Olivier
from tkinter import *
import tkinter.font as tkfont
import random
import time
import datetime
from PIL import ImageTk, Image
import pygame

###########################################################
# son et horloge
###########################################################

#dossier audio de chaque serveur
dossiers = {"Régis": "regis", "Aziz": "aziz", "Thomas": "thomas", "Racim": "racim"}
#son en cours de lecture
son_actuel = None

#demarrer le mixer audio
pygame.mixer.init()


def parler(fichier, qui):
    global son_actuel
    #chemin du fichier mp3
    chemin = "audio/" + dossiers[qui] + "/" + fichier + ".mp3"

    #couper la phrase d'avant
    if son_actuel is not None:
        son_actuel.stop()
    #charger et jouer la nouvelle phrase
    son_actuel = pygame.mixer.Sound(chemin)
    son_actuel.play()


def heure_actuelle():
    #1 minute du jeu = 8 secondes reelles
    minutes = heure_depart + int((time.time() - debut_reel) / 8)
    heures = (minutes // 60) % 24
    reste = minutes % 60
    #deux points qui clignotent
    if int(time.time() * 2) % 2 == 0:
        deux_points = ":"
    else:
        deux_points = " "
    return f"{heures:02d}{deux_points}{reste:02d}"


def afficher_heure(etiquette):
    #mise a jour tant que la fenetre existe
    if etiquette.winfo_exists():
        etiquette.config(text=heure_actuelle())
        fenetre.after(500, lambda: afficher_heure(etiquette))


def ajouter_horloge(fen):
    etiquette = Label(fen, text=heure_actuelle(), font=("Courier", 14, "bold"))
    #coin en bas a droite
    etiquette.place(relx=1.0, rely=1.0, anchor=SE, x=-8, y=-6)
    afficher_heure(etiquette)


###########################################################
# réservation
###########################################################
#fenetre principale cachee
fenetre = Tk()
fenetre.withdraw()


def reservation():
    global mon_canevas, tables, champ, champ2, Bouton0, Bouton1, message

    #afficher la fenetre et regler sa taille
    fenetre.deiconify()
    fenetre.title("répétition...")
    fenetre.geometry("500x500")
    fenetre.minsize(500, 500)
    fenetre.maxsize(500, 500)

    mon_canevas = Canvas(fenetre, width=500, height=500)

    #reglages des 9 tables
    taille = 60
    marge = 10
    espace = 10
    numero = 1
    tables = {}
    #decalage du groupe de tables
    decalage_x = 250
    decalage_y = 50
    #dessiner les tables en grille 3x3
    for ligne in range(3):
        for colonne in range(3):
            x1 = marge + decalage_x + colonne * (taille + espace)
            y1 = marge + decalage_y + ligne * (taille + espace)
            x2 = x1 + taille
            y2 = y1 + taille
            table_id = mon_canevas.create_rectangle(x1, y1, x2, y2, fill="light grey", width=2)
            #numero au centre de la table
            mon_canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(numero))
            tables[numero] = table_id
            numero += 1

    #boutons valider et assoir
    Bouton0 = Button(fenetre, text="Valider", width=11, foreground="black", background="light grey", command=verifier)
    Bouton1 = Button(fenetre, text="assoir", width=11, foreground="grey", background="grey", relief=FLAT, state=DISABLED)
    Bouton0.place(relx=0.2, rely=0.5, anchor=CENTER)
    Bouton1.place(relx=0.2, rely=0.6, anchor=CENTER)

    #changement de couleur au survol
    Bouton0.bind("<Enter>", hover)
    Bouton0.bind("<Leave>", out)

    #champs nom et prenom
    champ = Entry(fenetre)
    champ.place(x=80, y=105)
    champ2 = Entry(fenetre)
    champ2.place(x=80, y=130)
    Nom = Label(fenetre, text="Nom:")
    Prenom = Label(fenetre, text="Prenom:")
    Nom.place(x=6, y=105)
    Prenom.place(x=6, y=130)

    #message de bienvenue
    texte = "Bienvenue chez Aziz ! Inscrivez votre nom et prénom pour valider votre réservation du " + date_reservation + " à " + heure + "."
    message = Label(fenetre, text=texte, wraplength=480, justify=LEFT, font=("Arial", 11))
    message.place(x=10, y=8)

    ajouter_horloge(fenetre)
    mon_canevas.pack()
    #lancer la boucle tkinter
    fenetre.mainloop()


def out(event):
    #ignorer si desactive
    if Bouton0["state"] == DISABLED:
        return
    #couleur normale
    Bouton0["bg"] = "light grey"


def hover(event):
    #ignorer si desactive
    if Bouton0["state"] == DISABLED:
        return
    #couleur survol
    Bouton0["bg"] = "dark grey"


###########################################################
# validation
###########################################################


def assoir():
    #cacher l'accueil et ouvrir le menu
    fenetre.withdraw()
    menu()


def changer(Bouton):
    #rendre le bouton actif
    Bouton["foreground"] = "black"
    Bouton["background"] = "light grey"
    Bouton["relief"] = RAISED
    Bouton["state"] = NORMAL
    Bouton["command"] = assoir


def verifier():
    global numero_choisi
    #comparer avec la reservation
    if nom == champ.get() and prenom == champ2.get():
        #activer assoir
        changer(Bouton1)
        #table au hasard
        numero_choisi = random.choice(list(tables.keys()))
        mon_canevas.itemconfig(tables[numero_choisi], fill="white")
        #griser valider
        Bouton0.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)
        texte = "Veuillez vous assoir à la table " + str(numero_choisi) + "."
        message.config(text=texte)
    else:
        #mauvais nom
        texte = "Non, aucune réservation à ce nom."
        message.config(text=texte)


###########################################################
# Menu
###########################################################
def commander():
    service()


def activer_commander():
    #rendre commander cliquable
    Bouton3["foreground"] = "black"
    Bouton3["background"] = "lightgrey"
    Bouton3["relief"] = RAISED
    Bouton3["state"] = NORMAL


def compte_menu(secondes):
    #compte a rebours sur le bouton
    if secondes > 0:
        Bouton3["text"] = "COMMANDER (" + str(secondes) + ")"
        fenetre2.after(1000, lambda: compte_menu(secondes - 1))
    else:
        Bouton3["text"] = "COMMANDER"
        activer_commander()


def police_luxe():
    #polices installees
    installees = tkfont.families()
    #premiere police chic trouvee
    for nom in ["Playfair Display", "Bodoni MT", "Didot", "GFS Didot", "Copperplate",
                "Cormorant Garamond", "EB Garamond", "Garamond", "Palatino Linotype",
                "Book Antiqua", "Georgia", "Times New Roman", "DejaVu Serif", "Times"]:
        if nom in installees:
            return nom
    #police par defaut
    return "Times"


def menu():
    global fenetre2, Bouton3

    luxe = police_luxe()
    #fenetre du menu
    fenetre2 = Toplevel(fenetre)
    fenetre2.title("Installation")
    fenetre2.geometry("500x500")
    canvasmenu = Canvas(fenetre2, width=500, height=500, highlightthickness=0)
    canvasmenu.place(x=0, y=0)

    #triangle haut gauche
    canvasmenu.create_polygon(0, 0, 100, 0, 0, 100, fill="#8B2500", outline="")
    #triangle haut droite
    canvasmenu.create_polygon(500, 0, 400, 0, 500, 100, fill="#8B2500", outline="")
    #triangle bas gauche
    canvasmenu.create_polygon(0, 500, 100, 500, 0, 400, fill="#8B2500", outline="")
    #triangle bas droite
    canvasmenu.create_polygon(500, 500, 400, 500, 500, 400, fill="#8B2500", outline="")
    #entrees
    Label(fenetre2, text="Entrées au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Soupe à l'oignon non gratinée : 7,50 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="   Gratinée : +2,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Croquettes de thon : 9,00 $", font=(luxe, 12)).pack(pady=15)

    #repas
    Label(fenetre2, text="Repas au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Poisson avec pommes de terre : 22,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Steak avec légumes du jardin : 28,00 $", font=(luxe, 12)).pack(pady=15)

    #desserts
    Label(fenetre2, text="Desserts au choix", font=(luxe, 18, "bold")).pack(pady=15)
    Label(fenetre2, text="1. Café : 3,00 $", font=(luxe, 12)).pack()
    Label(fenetre2, text="2. Un quart de gâteau au fromage : 7,00 $", font=(luxe, 12)).pack(pady=15)

    #bouton commander grise au depart
    Bouton3 = Button(fenetre2, text="COMMANDER", width=15, foreground="grey", background="grey", relief=FLAT, state=DISABLED, command=commander)
    Bouton3.place(relx=0.5, rely=0.95, anchor=CENTER)
    #5 secondes avant de pouvoir commander
    compte_menu(5)
    ajouter_horloge(fenetre2)


###########################################################
# service
###########################################################


def reset(bouton):
    #bouton remis normal
    bouton["bg"] = "light grey"
    bouton["relief"] = RAISED
    bouton["state"] = NORMAL
    bouton["fg"] = "black"


def selectionner(bouton):
    #bouton vert et bloque pour imiter une sélection
    bouton["fg"] = "lightgreen"
    bouton["bg"] = "lightgreen"
    bouton["relief"] = FLAT
    bouton["state"] = DISABLED


def est_choisi(bouton):
    #un bouton bloque = choisi
    return bouton.cget("state") == DISABLED


def maj_serveur():
    #etat de chaque choix
    soupe_ok = est_choisi(bouton_soupe)
    entree_ok = soupe_ok or est_choisi(bouton_croquette)
    gratin_ok = est_choisi(bouton_gratiner) or est_choisi(bouton_pas_gratiner)
    plat_ok = est_choisi(bouton_poisson) or est_choisi(bouton_steak)
    dessert_ok = est_choisi(bouton_cafe) or est_choisi(bouton_gateau)

    #choisir la question du serveur
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
    #afficher et dire la phrase
    parole.config(text=texte)
    parler(son, nom_serveur)

    #activer servir seulement si tout est choisi
    if complet:
        bouton_servir.config(state=NORMAL, foreground="black", background="light grey", relief=RAISED)
    else:
        bouton_servir.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)


def choix_soupe():
    global note1
    #soupe choisie
    selectionner(bouton_soupe)
    reset(bouton_croquette)
    #montrer les boutons de gratin
    bouton_gratiner.place(relx=0.65, rely=0.37, anchor=CENTER)
    bouton_pas_gratiner.place(relx=0.8, rely=0.37, anchor=CENTER)
    #ecrire sur le bloc-note
    note1 = canvas.create_text(100, 80, text="Soupe à l'oignon")
    #effacer la note croquettes
    try:
        canvas.delete(note2)
    except:
        pass
    maj_serveur()


def choix_croquette():
    global note2
    #croquettes choisies
    selectionner(bouton_croquette)
    reset(bouton_soupe)
    reset(bouton_gratiner)
    reset(bouton_pas_gratiner)
    #cacher les boutons de gratin
    bouton_gratiner.place_forget()
    bouton_pas_gratiner.place_forget()
    #ecrire sur le bloc-note
    note2 = canvas.create_text(100, 80, text="Croquettes de thon")
    #effacer les notes de la soupe
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
    #gratinee choisie
    selectionner(bouton_gratiner)
    reset(bouton_pas_gratiner)
    note3 = canvas.create_text(100, 100, text="Gratinée")
    #effacer l'autre note
    try:
        canvas.delete(note4)
    except:
        pass
    maj_serveur()


def choix_pas_gratiner():
    global note4
    #non gratinee choisie
    selectionner(bouton_pas_gratiner)
    reset(bouton_gratiner)
    note4 = canvas.create_text(100, 100, text="Pas gratiné")
    #effacer l'autre note
    try:
        canvas.delete(note3)
    except:
        pass
    maj_serveur()


def choix_poisson():
    global note5
    #poisson choisi
    selectionner(bouton_poisson)
    reset(bouton_steak)
    note5 = canvas.create_text(100, 170, text="Poisson avec pommes de terre")
    #effacer la note du steak
    try:
        canvas.delete(note6)
    except:
        pass
    maj_serveur()


def choix_steak():
    global note6
    #steak choisi
    selectionner(bouton_steak)
    reset(bouton_poisson)
    note6 = canvas.create_text(100, 170, text="Steak avec légumes du jardin")
    #effacer la note du poisson
    try:
        canvas.delete(note5)
    except:
        pass
    maj_serveur()


def choix_cafe():
    global note7
    #cafe choisi
    selectionner(bouton_cafe)
    reset(bouton_gateau)
    note7 = canvas.create_text(100, 240, text="Café")
    #effacer la note du gateau
    try:
        canvas.delete(note8)
    except:
        pass
    maj_serveur()


def choix_gateau():
    global note8
    #gateau choisi
    selectionner(bouton_gateau)
    reset(bouton_cafe)
    note8 = canvas.create_text(100, 240, text="Un quart de gâteau au fromage")
    #effacer la note du cafe
    try:
        canvas.delete(note7)
    except:
        pass
    maj_serveur()


def servir():
    global listcommande
    #liste des boutons choisis
    listcommande = []
    for bouton in listbouton:
        if bouton.cget("state") == DISABLED:
            listcommande.append(bouton.cget("text"))
    #aller au repas
    repas()
    #fermer la fenetre service
    fenetre3.destroy()


def service():
    #fermer le menu
    fenetre2.destroy()
    global fenetre3, \
        bouton_soupe, bouton_croquette, bouton_gratiner, bouton_pas_gratiner, \
        bouton_poisson, bouton_steak, bouton_cafe, bouton_gateau, bouton_servir, \
        note1, note2, note3, note4, note5, note6, note7, note8, \
        listbouton, \
        canvas, parole, nom_serveur, titre_serveur

    #serveur au hasard
    nom_serveur, titre_serveur = random.choice([
        ("Régis", "serveur"),
        ("Aziz", "serveur"),
        ("Thomas", "serveur"),
        ("Racim", "serveur"),
    ])

    #fenetre du service
    fenetre3 = Toplevel(fenetre)
    fenetre3.title("Service")
    fenetre3.geometry("500x500")
    #boutons de choix
    bouton_soupe = Button(fenetre3, text="Soupe", width=8, foreground="black", background="light grey", command=choix_soupe)
    bouton_croquette = Button(fenetre3, text="Croquette", width=8, foreground="black", background="light grey", command=choix_croquette)
    bouton_gratiner = Button(fenetre3, text="Gratiner", width=8, foreground="black", background="light grey", command=choix_gratiner)
    bouton_pas_gratiner = Button(fenetre3, text="Pas gratiner", width=8, foreground="black", background="light grey", command=choix_pas_gratiner)
    bouton_poisson = Button(fenetre3, text="Poisson", width=8, foreground="black", background="light grey", command=choix_poisson)
    bouton_steak = Button(fenetre3, text="Steak", width=8, foreground="black", background="light grey", command=choix_steak)
    bouton_cafe = Button(fenetre3, text="Café", width=8, foreground="black", background="light grey", command=choix_cafe)
    bouton_gateau = Button(fenetre3, text="gâteau", width=8, foreground="black", background="light grey", command=choix_gateau)
    #servir grise au depart
    bouton_servir = Button(fenetre3, text="SERVIR", width=11, foreground="grey", background="grey", relief=FLAT, state=DISABLED, command=servir)

    #placer les boutons
    bouton_soupe.place(relx=0.65, rely=0.3, anchor=CENTER)
    bouton_croquette.place(relx=0.8, rely=0.3, anchor=CENTER)
    bouton_poisson.place(relx=0.65, rely=0.45, anchor=CENTER)
    bouton_steak.place(relx=0.8, rely=0.45, anchor=CENTER)
    bouton_cafe.place(relx=0.65, rely=0.55, anchor=CENTER)
    bouton_gateau.place(relx=0.8, rely=0.55, anchor=CENTER)
    bouton_servir.place(relx=0.85, rely=0.85, anchor=CENTER)
    #liste de tous les boutons de choix
    listbouton = [bouton_soupe, bouton_croquette, bouton_gratiner, bouton_pas_gratiner, bouton_poisson, bouton_steak, bouton_cafe, bouton_gateau]

    #texte du serveur
    parole = Label(fenetre3, text="", font=("Arial", 11), wraplength=240, justify=LEFT)
    parole.place(x=240, y=20)

    #canvas du bloc-note
    canvas = Canvas(fenetre3, width=200, height=460, highlightthickness=0)
    canvas.place(x=20, y=20)

    #image du bloc-note
    try:
        note = ImageTk.PhotoImage(
            Image.open("note.png").resize((200, 460))
        )
        canvas.create_image(0, 0, image=note, anchor=NW)
        #garder l'image en memoire
        canvas.note = note
    except FileNotFoundError:
        #bloc-note dessine si pas d'image
        canvas.create_rectangle(0, 0, 200, 460, fill="lightyellow", outline="black")

    ajouter_horloge(fenetre3)
    maj_serveur()


###########################################################
# repas a table
###########################################################

#entrees
def soupe():
    #bol de soupe
    canvas2.create_oval(50, 50, 450, 450, fill="saddlebrown")
    canvas2.create_oval(70, 70, 430, 430, fill="beige")
    #morceaux d'oignon
    canvas2.create_arc(100, 100, 250, 250, fill="burlywood", style="chord")
    canvas2.create_arc(80, 200, 230, 350, fill="burlywood", style="chord")
    canvas2.create_arc(70, 300, 220, 450, fill="burlywood", style="chord")
    canvas2.create_arc(200, 250, 350, 400, fill="burlywood", style="chord")
    #fromage si gratinee
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
    #assiette
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    #4 croquettes
    canvas2.create_oval(124, 232, 184, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(188, 232, 248, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(252, 232, 312, 268, fill="goldenrod", outline="saddlebrown", width=2)
    canvas2.create_oval(316, 232, 376, 268, fill="goldenrod", outline="saddlebrown", width=2)


#repas
def poisson():
    #assiette
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    #queue
    canvas2.create_polygon(330, 230, 395, 190, 395, 270, fill="peru", outline="saddlebrown", width=3)
    #corps sans la tete
    canvas2.create_polygon(176, 198, 206, 191, 240, 188, 274, 191, 304, 198, 327, 209, 338, 223, 338, 237, 327, 251, 304, 262, 274, 269, 240, 272, 206, 269, 176, 262, fill="peru", outline="saddlebrown", width=3)

    #arete centrale
    canvas2.create_line(165, 230, 335, 230, fill="ivory", width=4)
    #aretes sur les cotes
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

    #pommes de terre
    canvas2.create_oval(180, 300, 230, 330, fill="khaki", outline="darkgoldenrod", width=2)
    canvas2.create_oval(240, 300, 290, 330, fill="khaki", outline="darkgoldenrod", width=2)
    canvas2.create_oval(300, 300, 350, 330, fill="khaki", outline="darkgoldenrod", width=2)


def steak():
    #assiette
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    #viande
    canvas2.create_oval(100, 180, 200, 320, fill="#7b3b21", outline="#4a1f10", width=3)

    #marques de grill
    canvas2.create_line(120, 205, 180, 215, fill="black", width=4)
    canvas2.create_line(115, 240, 185, 250, fill="black", width=4)
    canvas2.create_line(120, 275, 180, 285, fill="black", width=4)
    #carottes
    canvas2.create_oval(270, 110, 310, 150, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(320, 130, 360, 170, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(220, 80, 260, 120, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(380, 180, 420, 220, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(270, 170, 310, 210, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(330, 200, 370, 240, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(375, 225, 415, 265, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(270, 230, 310, 270, fill="orange", outline="darkorange", width=2)
    canvas2.create_oval(320, 245, 360, 285, fill="orange", outline="darkorange", width=2)

    #haricots
    canvas2.create_rectangle(270, 290, 400, 302, fill="green", outline="darkgreen")
    canvas2.create_rectangle(260, 310, 390, 322, fill="green", outline="darkgreen")
    canvas2.create_rectangle(230, 340, 350, 352, fill="green", outline="darkgreen")
    canvas2.create_rectangle(220, 360, 360, 372, fill="green", outline="darkgreen")
    canvas2.create_rectangle(200, 380, 330, 392, fill="green", outline="darkgreen")
    canvas2.create_rectangle(210, 400, 300, 412, fill="green", outline="darkgreen")


#desserts
def cafe():
    #petite assiette
    canvas2.create_oval(170, 170, 330, 330, fill="white", outline="gray", width=2)
    #poigner
    canvas2.create_oval(295, 238, 330, 262, outline="gray", width=4)
    #tasse
    canvas2.create_oval(200, 200, 300, 300, fill="white", outline="gray", width=2)
    #cafe
    canvas2.create_oval(212, 212, 288, 288, fill="saddlebrown")


def gateau():
    #assiette au bord bleu
    canvas2.create_oval(50, 50, 450, 450, fill="lightblue")
    canvas2.create_oval(90, 90, 410, 410, fill="white")
    #quart de gateau
    canvas2.create_arc(40, 180, 320, 460, start=0, extent=90, style="pieslice", fill="papaya whip", outline="saddlebrown", width=3)
    #queue de la fraise
    canvas2.create_oval(244, 224, 256, 234, fill="forestgreen")
    #fraise
    canvas2.create_oval(236, 231, 264, 259, fill="red", outline="darkred", width=2)


def afficher_plat():
    #vider le canvas
    canvas2.delete("all")
    #dessiner le plat actuel
    etapes[etape_actuelle]()


def manger():
    global etape_actuelle
    #plat suivant
    etape_actuelle += 1
    if etape_actuelle < len(etapes):
        afficher_plat()
    else:
        #plus de plat : miettes et bouton serveur
        miettes()
        bouton_manger.config(text="APPELER SERVEUR", width=16, command=appeler_serveur)


def assiette_vide():
    canvas2.delete("all")
    #assiette vide
    canvas2.create_oval(50, 50, 450, 450, fill="white")
    canvas2.create_oval(90, 90, 410, 410, fill="white")


def miettes():
    assiette_vide()
    #petites miettes
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
    #compte a rebours avant le plat
    if secondes > 0:
        canvas2.delete("compte")
        canvas2.create_text(250, 250, text="Votre plat arrive dans " + str(secondes) + "...", font=("Arial", 14), tags="compte")
        fenetre4.after(1000, lambda: compte_repas(secondes - 1))
    else:
        debut_repas()


def compte_facture(secondes):
    #compte a rebours avant la facture
    if secondes > 0:
        canvas2.delete("compte")
        canvas2.create_text(250, 250, text="La facture arrive dans " + str(secondes) + "...", font=("Arial", 14), tags="compte")
        fenetre4.after(1000, lambda: compte_facture(secondes - 1))
    else:
        montrer_facture()


def appeler_serveur():
    #griser le bouton
    bouton_manger.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)
    canvas2.create_text(250, 25, text=nom_serveur + " : Je vous apporte la facture.", font=("Arial", 12))
    parler("facture", nom_serveur)
    #facture dans 3 secondes
    compte_facture(3)


def montrer_facture():
    #fermer le repas
    fenetre4.destroy()
    #ouvrir la facture
    facture()


def debut_repas():
    #afficher le bouton manger
    bouton_manger.place(relx=0.5, rely=0.95, anchor=CENTER)
    #premier plat
    afficher_plat()


def repas():
    global fenetre4, canvas2, etapes, etape_actuelle, bouton_manger
    #fenetre du repas
    fenetre4 = Toplevel(fenetre)
    fenetre4.title("Repas")
    fenetre4.geometry("500x500")
    #fermer la fenetre = fin du programme
    fenetre4.protocol("WM_DELETE_WINDOW", fenetre.destroy)
    #canvas brun comme une table
    canvas2 = Canvas(fenetre4, width=500, height=500, bg="#8B5A2B", highlightthickness=0)
    canvas2.pack()
    #assiette vide au depart
    assiette_vide()
    ajouter_horloge(fenetre4)

    bouton_manger = Button(fenetre4, text="MANGER", width=11, foreground="black", background="light grey", command=manger)

    #plats dans l'ordre : entree, repas, dessert
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
    #5 secondes avant le premier plat
    compte_repas(5)


###########################################################
# facture
###########################################################

#prix de chaque article
prix = {"Soupe": 7.50, "Gratinée": 2.00, "Croquette": 9.00,
        "Poisson": 22.00, "Steak": 28.00, "Café": 3.00, "gâteau": 7.00}
#noms courts pour le ticket
noms_ticket = {"Soupe": "Soupe à l'ognion", "Gratinée": "Gratinée", "Croquette": "Croquettes de thon",
               "Poisson": "Poisson avec pomme de terre", "Steak": "Steak avec légumes", "Café": "Café", "gâteau": "Gâteau"}


def argent(montant):
    #virgule et symbole $
    return f"{montant:.2f}".replace(".", ",") + " $"


def facture():
    #fenetre pygame
    pygame.init()
    ecran = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Facture")

    #polices de ticket
    police = pygame.font.SysFont("couriernew,consolas,courier", 14)
    gras = pygame.font.SysFont("couriernew,consolas,courier", 20, bold=True)

    #image du terminal a droite
    terminal = pygame.image.load("terminal.png").convert_alpha()
    terminal = pygame.transform.smoothscale(terminal, (235, 235))

    #table et serveur
    table = numero_choisi
    serveur = nom_serveur

    #articles et sous-total
    articles = []
    soustotal = 0
    for article in ["Soupe", "Gratiner", "Croquette", "Poisson", "Steak", "Café", "gâteau"]:
        if article in listcommande:
            articles.append(article)
            soustotal += prix[article]

    #taxes
    tps = soustotal * 0.05
    tvq = soustotal * 0.10
    total = soustotal * 1.15

    #date et heure de la facture
    date_facture = date_reservation
    #sans clignotement
    heure_facture = heure_actuelle().replace(" ", ":")

    def texte(t, x, y, f=police):
        #texte aligne a gauche
        ecran.blit(f.render(t, True, "black"), (x, y))

    def texte_droite(t, y, f=police):
        #texte aligne a droite du ticket
        surface = f.render(t, True, "black")
        ecran.blit(surface, (245 - surface.get_width(), y))

    running = True
    while running:
        #quitter avec fermeture, touche ou clic
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        #fond blanc
        ecran.fill("white")

        #terminal a droite
        if terminal is not None:
            ecran.blit(terminal, (262, 95))

        #titre du ticket
        texte(f"TABLE N°{table}", 70, 12)

        #articles
        y = 42
        for article in articles:
            texte("1 " + noms_ticket[article], 10, y)
            texte_droite(argent(prix[article]), y)
            y += 20

        #sous-total et taxes
        y += 6
        texte("SOUS-TOTAL", 30, y)
        texte_droite(argent(soustotal), y)
        y += 20
        texte("TPS", 30, y)
        texte_droite(argent(tps), y)
        y += 18
        texte("TVQ", 30, y)
        texte_droite(argent(tvq), y)

        #total
        y += 26
        texte("TOTAL", 10, y, gras)
        texte_droite(argent(total), y, gras)

        #date et heure
        y += 36
        texte("Date : " + date_facture, 10, y)
        texte("Heure : " + heure_facture, 10, y + 18)

        #numeros de taxes
        y += 50
        texte("TPS : 000000000 RT0001", 10, y)
        texte("TVQ : 000000000 TQ0001", 10, y + 15)

        #serveur
        y += 45
        texte("VOUS AVEZ ÉTÉ SERVI", 10, y)
        texte("PAR : " + serveur, 40, y + 16)

        #horloge dans le coin
        h = police.render(heure_actuelle(), True, "black")
        ecran.blit(h, (492 - h.get_width(), 470))

        #consigne pour quitter
        texte("Appuyez sur une touche pour quitter", 10, 470)

        #ligne verticale
        pygame.draw.line(ecran, (0, 0, 0), (250, 0), (250, 460), 2)

        #ligne horizontale
        pygame.draw.line(ecran, (0, 0, 0), (0, 460), (250, 460), 2)

        #afficher l'image
        pygame.display.flip()
        pygame.time.wait(50)

    #fermer pygame et tkinter
    pygame.quit()
    fenetre.destroy()


###########################################################
# Lancement du programme
###########################################################

print("Bienvenue chez Aziz, le restaurant reconnu pour ses 4 étoiles Michelin !")

#jours et mois en francais
jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
#les 4 prochains jours
aujourdhui = datetime.date.today()
dates = []
for i in range(1, 5):
    jour = aujourdhui + datetime.timedelta(days=i)
    dates.append(jours[jour.weekday()] + " " + str(jour.day) + " " + mois[jour.month - 1])
#choix de la date
print("Pour quelle date souhaitez-vous venir ?")
print("Nous prenons les réservations pour les 4 prochains jours :")
for i in range(4):
    print("  " + str(i + 1) + ". " + dates[i])
choix_date = input("Laquelle voulez-vous (1 à 4) ? ")
#redemander si invalide
while choix_date != "1" and choix_date != "2" and choix_date != "3" and choix_date != "4":
    choix_date = input("Désolé, choisissez un numéro de 1 à 4 : ")
date_reservation = dates[int(choix_date) - 1]

#choix de l'heure
print("À quelle heure souhaitez-vous venir ?")
print("Nous avons 4 réservations disponibles ce soir-là :")
print("  1. 17h00")
print("  2. 18h30")
print("  3. 20h00")
print("  4. 21h30")
choix = input("Laquelle voulez-vous prendre (1 à 4) ? ")
#redemander si invalide
while choix != "1" and choix != "2" and choix != "3" and choix != "4":
    choix = input("Désolé, choisissez un numéro de 1 à 4 : ")
#heure selon le choix
if choix == "1":
    heure = "17h00"
elif choix == "2":
    heure = "18h30"
elif choix == "3":
    heure = "20h00"
else:
    heure = "21h30"
nom = ""
prenom = ""
#demander le prenom
while not nom.isalpha():

    nom = input("prénom: ")

    #enlever les espaces
    nom = nom.replace(" ", "")

    #verifier la saisie
    if not nom:
        print("Erreur : Le champ ne peut pas être vide !")
    elif not nom.isalpha():
        print("Erreur : Chiffres et symboles interdits.")

#demander le nom
while not prenom.isalpha():

    prenom = input("Nom : ")
    #enlever les espaces
    prenom = prenom.replace(" ", "")

    #verifier la saisie
    if not prenom:
        print("Erreur : Le champ ne peut pas être vide !")
    elif not prenom.isalpha():
        print("Erreur : Chiffres et symboles interdits.")

#confirmation
print(f"Saisie acceptée ! Le prénom enregistré est : {prenom} et votre nom {nom}")

print("Ok, réservation prise le " + date_reservation + " à " + heure + " au nom de " + prenom + " " + nom + ".")
print("Merci, hâte de vous voir chez Aziz !")

#l'horloge part de l'heure de la reservation
heure_depart = int(heure[0:2]) * 60 + int(heure[3:5])
debut_reel = time.time()

#musique de fond en boucle
pygame.mixer.music.load("musique.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#commence le programme
reservation()
