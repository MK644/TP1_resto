from enum import verify
from tkinter import *
import random
from PIL import ImageTk, Image

###########################################################
# réservation
###########################################################
fenetre = Tk()
fenetre.withdraw()  # cachée tant que reservation() ne l'a pas configurée


def reservation():
    """Fenêtre d'accueil : l'hôtesse inscrit les infos du client
    et lui attribue une table parmi les 9 disponibles."""
    global mon_canevas, tables, champ, champ2, Bouton0, Bouton1

    fenetre.deiconify()
    fenetre.title("répétition...")
    fenetre.geometry("500x340")
    fenetre.minsize(500, 340)
    fenetre.maxsize(500, 340)

    mon_canevas = Canvas(fenetre, width=500, height=500)

    # 9 tables numérotées de 1 à 9, disposées en formation cube
    taille = 60
    marge = 10
    espace = 10
    numero = 1
    tables = {}
    decalage_x = 200  # décale tout le paquet de tables vers la droite
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
    champ.place(x=57, y=105)
    champ2 = Entry(fenetre)
    champ2.place(x=57, y=130)
    Nom = Label(fenetre, text="Nom:")
    Prenom = Label(fenetre, text="Prenom:")
    Nom.place(x=6, y=105)
    Prenom.place(x=6, y=130)

    mon_canevas.pack()
    fenetre.mainloop()


def out(event):
    Bouton0["bg"] = "light grey"


def hover(event):
    Bouton0["bg"] = "dark grey"


###########################################################
# validation
###########################################################


def assoir():
    fenetre.destroy()
    menu()


def changer(Bouton):
    Bouton["foreground"] = "black"
    Bouton["background"] = "light grey"
    Bouton["relief"] = RAISED
    Bouton["state"] = NORMAL
    Bouton["command"] = assoir


def verifier():
    if nom == champ.get() and prenom == champ2.get():
        # choisir une des 9 tables, activer le bouton "assoir"
        changer(Bouton1)
        numero_choisi = random.choice(list(tables.keys()))
        mon_canevas.itemconfig(tables[numero_choisi], fill="white")
        print("Table attribuee :", numero_choisi)


###########################################################
# Menu
###########################################################
def commander():

    service()
def menu():
    global fenetre2
    fenetre2 =  Toplevel(fenetre) # nouvelle fenêtre
    fenetre2.title("Installation")
    fenetre2.geometry("300x500")
    Label(fenetre2, text="Entrées au choix").pack(pady=20)
    Label(fenetre2, text="1. Soupe à l'oignon non gratinée : 7,50 $").pack()
    Label(fenetre2, text="   Gratinée : +2,00 $").pack()
    Label(fenetre2, text="2. Croquettes de thon : 9,00 $").pack(pady=20)

    Label(fenetre2, text="Repas au choix").pack(pady=20)
    Label(fenetre2, text="1. Poisson avec pommes de terre : 22,00 $").pack()
    Label(fenetre2, text="2. Steak avec légumes du jardin : 28,00 $").pack(pady=20)

    Label(fenetre2, text="Desserts au choix").pack(pady=20)
    Label(fenetre2, text="1. Café : 3,00 $").pack()
    Label(fenetre2, text="2. Un quart de gâteau au fromage : 7,00 $").pack()

    Bouton3 = Button(fenetre2, text="commander", width=11, foreground="black", background="lightgrey", command=commander)
    Bouton3.place(relx=0.5, rely=0.9, anchor=CENTER)

    fenetre2.mainloop()


###########################################################
# service
###########################################################
def reset(bouton):
    bouton["bg"] = "light grey"
    bouton["relief"] = RAISED
    bouton["state"] = NORMAL
    bouton["fg"] = "black"
def selectionner(bouton):
    bouton["fg"]="lightgreen"
    bouton["bg"]="lightgreen"
    bouton["relief"] = FLAT
    bouton["state"] = DISABLED
def Bouton0():
    selectionner(Bouton0)
    l2=l.copy()
    l2.remove(Bouton0)
    for b in l2:
        reset(b)
def Bouton1():
    selectionner(Bouton1)
    l2 = l.copy()
    l2.remove(Bouton1)

    for b in l2:
        reset(b)
    Bouton2 = Button(fenetre3, text="croquette", width=11, foreground="black", background="light grey",command=Bouton1 )

    Bouton3 = Button(fenetre3, text="croquette", width=11, foreground="black", background="light grey", command=Bouton1)


def service():
    global fenetre3, Bouton0, Bouton1, l
    fenetre3=  Toplevel(fenetre)
    fenetre3.title("Service")
    fenetre3.geometry("700x500")
    Bouton0 = Button(fenetre3, text="soupe", width=11, foreground="black", background="light grey", command=Bouton0 )
    Bouton1 = Button(fenetre3, text="croquette", width=11, foreground="black", background="light grey",command=Bouton1 )
    Bouton1.place(relx=0.8, rely=0.3, anchor=CENTER)
    Bouton0.place(relx=0.7, rely=0.3, anchor=CENTER)
    l=[Bouton0, Bouton1]

    # IMAGE
    canvas = Canvas(fenetre3, width=200, height=460, highlightthickness=0)
    canvas.place(x=20, y=20)

    note = ImageTk.PhotoImage(
        Image.open("note.png").resize((200, 460))
    )

    canvas.create_image(0, 0, image=note, anchor=NW)

    canvas.note = note

    fenetre3.mainloop()

###########################################################
# repas a table
###########################################################

# (à venir : présentation de l'entrée/repas/dessert avec formes géométriques)


###########################################################
# facture
###########################################################

# (à venir)


###########################################################
# Lancement du programme
###########################################################

#nom = input("Nom: ")
#prenom = input("Prenom: ")
service()
