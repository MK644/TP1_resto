m enum import verify
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


def Bouton1():
    global note1
    selectionner(Bouton1)
    reset(Bouton2)
    Bouton3.place(relx=0.65, rely=0.37, anchor=CENTER)
    Bouton4.place(relx=0.8, rely=0.37, anchor=CENTER)
    note1=canvas.create_text(100, 80, text="Soupe à l'oignon")
    try:
        canvas.delete(note2)
    except:
        pass
def Bouton2():
    global note2
    selectionner(Bouton2)
    reset(Bouton1)
    reset(Bouton3)
    reset(Bouton4)
    Bouton3.place_forget()
    Bouton4.place_forget()
    note2=canvas.create_text(100, 80, text="Croquettes de thon")
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

def Bouton3():
    global note3
    selectionner(Bouton3)
    reset(Bouton4)
    note3=canvas.create_text(100, 100, text="Gratinée")
    try:
        canvas.delete(note4)
    except:
        pass

def Bouton4():
    global note4
    selectionner(Bouton4)
    reset(Bouton3)
    note4=canvas.create_text(100, 100, text="Pas gratiné")
    try:
        canvas.delete(note3)
    except:
        pass
def Bouton5():
    global note5
    selectionner(Bouton5)
    reset(Bouton6)
    note5=canvas.create_text(100, 170, text="Poisson avec pommes de terre")
    try:
        canvas.delete(note6)
    except:
        pass
def Bouton6():
    global note6
    selectionner(Bouton6)
    reset(Bouton5)
    note6=canvas.create_text(100, 170, text="Steak avec légumes du jardin")
    try:
        canvas.delete(note5)
    except:
        pass

def Bouton7():
    global note7
    selectionner(Bouton7)
    reset(Bouton8)
    note7=canvas.create_text(100, 240, text="Café")
    try:
        canvas.delete(note8)
    except:
        pass

def Bouton8():
    global note8
    selectionner(Bouton8)
    reset(Bouton7)
    note8=canvas.create_text(100, 240, text="Un quart de gâteau au fromage")
    try:
        canvas.delete(note7)
    except:
        pass

def service():
    global fenetre3, \
        Bouton1, Bouton2, Bouton3, Bouton4, Bouton5, Bouton6, Bouton7, Bouton8,\
        note1, note2, note3, note4, note5, note6, note7, note8,\
        canvas

    fenetre3=  Toplevel(fenetre)
    fenetre3.title("Service")
    fenetre3.geometry("700x500")
    Bouton1 = Button(fenetre3, text="Soupe", width=11, foreground="black", background="light grey", command=Bouton1 )
    Bouton2 = Button(fenetre3, text="Croquette", width=11, foreground="black", background="light grey",command=Bouton2 )
    Bouton3 = Button(fenetre3, text="Gratiner", width=11, foreground="black", background="light grey", command=Bouton3)
    Bouton4 = Button(fenetre3, text="Pas gratiner", width=11, foreground="black", background="light grey", command=Bouton4)
    Bouton5 = Button(fenetre3, text="Poisson", width=11, foreground="black", background="light grey", command=Bouton5)
    Bouton6 =  Button(fenetre3, text="Steak", width=11, foreground="black", background="light grey", command=Bouton6)
    Bouton7 = Button(fenetre3, text="Café", width=11, foreground="black", background="light grey", command=Bouton7)
    Bouton8 = Button(fenetre3, text="gâteau", width=11, foreground="black", background="light grey", command=Bouton8)

    Bouton1.place(relx=0.65, rely=0.3, anchor=CENTER)
    Bouton2.place(relx=0.8, rely=0.3, anchor=CENTER)
    Bouton5.place(relx=0.65, rely=0.45, anchor=CENTER)
    Bouton6.place(relx=0.8, rely=0.45, anchor=CENTER)
    Bouton7.place(relx=0.65, rely=0.55, anchor=CENTER)
    Bouton8.place(relx=0.8, rely=0.55, anchor=CENTER)




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
