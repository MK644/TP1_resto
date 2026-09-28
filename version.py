from enum import verify
from tkinter import *
import random
import math
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
    if nom == champ.get() and prenom == champ2.get():
        # choisir une des 9 tables, activer le bouton "assoir"
        changer(Bouton1)
        numero_choisi = random.choice(list(tables.keys()))
        mon_canevas.itemconfig(tables[numero_choisi], fill="white")
        print("Table attribuee :", numero_choisi)
        # désactiver "Valider" (même look que "assoir" désactivé)
        Bouton0.config(state=DISABLED, foreground="grey", background="grey", relief=FLAT)


###########################################################
# Menu
###########################################################
def commander():

    service()
def menu():
    global fenetre2
    fenetre2 =  Toplevel(fenetre) # nouvelle fenêtre
    fenetre2.title("Installation")
    fenetre2.geometry("500x500")
    Label(fenetre2, text="Entrées au choix", font=("Arial", 11)).pack(pady=20)
    Label(fenetre2, text="1. Soupe à l'oignon non gratinée : 7,50 $").pack()
    Label(fenetre2, text="   Gratinée : +2,00 $").pack()
    Label(fenetre2, text="2. Croquettes de thon : 9,00 $").pack(pady=20)

    Label(fenetre2, text="Repas au choix", font=("Arial", 11)).pack(pady=20)
    Label(fenetre2, text="1. Poisson avec pommes de terre : 22,00 $", ).pack()
    Label(fenetre2, text="2. Steak avec légumes du jardin : 28,00 $").pack(pady=20)

    Label(fenetre2, text="Desserts au choix", font=("Arial", 11)).pack(pady=20)
    Label(fenetre2, text="1. Café : 3,00 $").pack()
    Label(fenetre2, text="2. Un quart de gâteau au fromage : 7,00 $").pack(pady=20)

    Bouton3 = Button(fenetre2, text="COMMANDER", width=11, foreground="black", background="lightgrey", command=commander)
    Bouton3.place(relx=0.5, rely=0.95, anchor=CENTER)




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
    elif soupe_ok and not gratin_ok:
        texte = f"{nom_serveur} :\nGratinée ou non gratinée ?"
    elif not plat_ok:
        texte = f"{nom_serveur} :\nRepas #1 ou #2 ?\n(poisson ou steak)"
    elif not dessert_ok:
        texte = f"{nom_serveur} :\nDessert #1 ou #2 ?\n(café ou quart de gâteau)"
    else:
        texte = f"{nom_serveur} :\nMerci, ça ne sera pas long !"
        complet = True
    parole.config(text=texte)

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
    note1=canvas.create_text(100, 80, text="Soupe à l'oignon")
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
    maj_serveur()

def choix_gratiner():
    global note3
    selectionner(bouton_gratiner)
    reset(bouton_pas_gratiner)
    note3=canvas.create_text(100, 100, text="Gratinée")
    try:
        canvas.delete(note4)
    except:
        pass
    maj_serveur()

def choix_pas_gratiner():
    global note4
    selectionner(bouton_pas_gratiner)
    reset(bouton_gratiner)
    note4=canvas.create_text(100, 100, text="Pas gratiné")
    try:
        canvas.delete(note3)
    except:
        pass
    maj_serveur()
def choix_poisson():
    global note5
    selectionner(bouton_poisson)
    reset(bouton_steak)
    note5=canvas.create_text(100, 170, text="Poisson avec pommes de terre")
    try:
        canvas.delete(note6)
    except:
        pass
    maj_serveur()
def choix_steak():
    global note6
    selectionner(bouton_steak)
    reset(bouton_poisson)
    note6=canvas.create_text(100, 170, text="Steak avec légumes du jardin")
    try:
        canvas.delete(note5)
    except:
        pass
    maj_serveur()

def choix_cafe():
    global note7
    selectionner(bouton_cafe)
    reset(bouton_gateau)
    note7=canvas.create_text(100, 240, text="Café")
    try:
        canvas.delete(note8)
    except:
        pass
    maj_serveur()

def choix_gateau():
    global note8
    selectionner(bouton_gateau)
    reset(bouton_cafe)
    note8=canvas.create_text(100, 240, text="Un quart de gâteau au fromage")
    try:
        canvas.delete(note7)
    except:
        pass
    maj_serveur()
def servir():
    global listcommande
    listcommande=[]
    for bouton in listbouton:
        if bouton.cget("state")==DISABLED:
            listcommande.append(bouton.cget("text"))
    repas()
    # la fenêtre service disparait seulement ici
    fenetre3.destroy()


def service():
    fenetre2.destroy()
    global fenetre3, \
        bouton_soupe, bouton_croquette, bouton_gratiner, bouton_pas_gratiner, \
        bouton_poisson, bouton_steak, bouton_cafe, bouton_gateau, bouton_servir ,\
        note1, note2, note3, note4, note5, note6, note7, note8,\
        listbouton,\
        canvas, parole, nom_serveur, titre_serveur

    # serveur / serveuse au hasard parmi 4 prénoms
    nom_serveur, titre_serveur = random.choice([
        ("Sophie", "serveuse"),
        ("Marc", "serveur"),
        ("Julie", "serveuse"),
        ("Antoine", "serveur"),
    ])

    fenetre3=  Toplevel(fenetre)
    fenetre3.title("Service")
    fenetre3.geometry("500x500")
    bouton_soupe = Button(fenetre3, text="Soupe", width=8, foreground="black", background="light grey", command=choix_soupe )
    bouton_croquette = Button(fenetre3, text="Croquette", width=8, foreground="black", background="light grey",command=choix_croquette )
    bouton_gratiner = Button(fenetre3, text="Gratiner", width=8, foreground="black", background="light grey", command=choix_gratiner)
    bouton_pas_gratiner = Button(fenetre3, text="Pas gratiner", width=8, foreground="black", background="light grey", command=choix_pas_gratiner)
    bouton_poisson = Button(fenetre3, text="Poisson", width=8, foreground="black", background="light grey", command=choix_poisson)
    bouton_steak =  Button(fenetre3, text="Steak", width=8, foreground="black", background="light grey", command=choix_steak)
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

    # ce que dit le serveur / la serveuse
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

    maj_serveur()




###########################################################
# repas a table
###########################################################

def assiette(canvas):
    canvas.create_oval(50, 50, 450, 450, fill="white")
    canvas.create_oval(90, 90, 410, 410, fill="white")


# ---------- entrées ----------
def soupe(canvas, cx=250, cy=250, gratinee=False):
    canvas.create_oval(cx-42, cy-42, cx+42, cy+42, fill="saddlebrown", outline="black", width=2)   # bol
    canvas.create_oval(cx-34, cy-34, cx+34, cy+34, fill="beige", outline="")                       # soupe
    if gratinee:
        canvas.create_oval(cx-34, cy-34, cx+34, cy+34, fill="gold", outline="")                    # fromage fondu
        canvas.create_oval(cx-20, cy-14, cx-6, cy, fill="peru", outline="")                        # taches dorées
        canvas.create_oval(cx+6, cy-24, cx+22, cy-10, fill="peru", outline="")
        canvas.create_oval(cx-4, cy+8, cx+14, cy+24, fill="peru", outline="")
    else:
        canvas.create_arc(cx-26, cy-26, cx-2, cy-2, fill="burlywood", style="chord")               # croûtons
        canvas.create_arc(cx+2, cy+4, cx+26, cy+28, fill="burlywood", style="chord")


def croquette(canvas, y=235):
    nombre = 4
    largeur = 52
    hauteur = 30
    espace = 4
    x_depart = 250 - (nombre * largeur + (nombre - 1) * espace) / 2  # centre la rangée

    for i in range(nombre):
        x1 = x_depart + i * (largeur + espace)
        canvas.create_oval(x1, y, x1 + largeur, y + hauteur,
                           fill="goldenrod", outline="saddlebrown", width=2)


# ---------- repas ----------
def poisson(canvas, cx=220, cy=234):
    # queue (triangle vers la droite), dessinée avant le corps
    canvas.create_polygon(cx+65, cy, cx+115, cy-30, cx+115, cy+30,
                          fill="peru", outline="saddlebrown", width=3)
    # corps : ovale dont la tête (côté gauche) est coupée
    points = []
    for angle in range(-132, 133, 12):
        t = math.radians(angle)
        points.append(cx + 75 * math.cos(t))
        points.append(cy - 30 * math.sin(t))
    canvas.create_polygon(points, fill="peru", outline="saddlebrown", width=3)
    # arêtes : colonne + côtes
    canvas.create_line(cx-62, cy, cx+62, cy, fill="ivory", width=3)
    for dx in range(-40, 50, 18):
        canvas.create_line(cx+dx, cy, cx+dx+8, cy-18, fill="ivory", width=2)
        canvas.create_line(cx+dx, cy, cx+dx+8, cy+18, fill="ivory", width=2)
    # pommes de terre à côté
    for dx in (-40, 0, 40):
        canvas.create_oval(cx+dx-16, cy+42, cx+dx+16, cy+62,
                           fill="khaki", outline="darkgoldenrod", width=2)


def steak(canvas, cx=250, cy=234):
    canvas.create_oval(cx-70, cy-35, cx+70, cy+35, fill="saddlebrown", outline="black", width=3)
    for dx in (-30, 0, 30):   # marques de grill
        canvas.create_line(cx+dx-10, cy-20, cx+dx+10, cy+20, fill="sienna", width=3)
    # légumes du jardin à côté
    for dx, couleur in ((-45, "forestgreen"), (-10, "orange"), (25, "forestgreen"), (60, "orange")):
        canvas.create_oval(cx+dx-12, cy+46, cx+dx+12, cy+68, fill=couleur, outline="black")


# ---------- desserts ----------
def cafe(canvas, cx=250, cy=250):
    canvas.create_oval(cx-30, cy-30, cx+30, cy+30, fill="white", outline="gray", width=2)      # soucoupe
    canvas.create_oval(cx+16, cy-7, cx+36, cy+7, outline="gray", width=3)                       # anse
    canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill="white", outline="gray", width=2)      # tasse
    canvas.create_oval(cx-14, cy-14, cx+14, cy+14, fill="saddlebrown", outline="")             # café


def gateau(canvas, cx=225, cy=275):
    # un quart de cercle vu de dessus
    canvas.create_arc(cx-50, cy-50, cx+50, cy+50, start=0, extent=90, style="pieslice",
                      fill="papaya whip", outline="saddlebrown", width=3)
    # la chose rouge : une fraise
    canvas.create_oval(cx+22, cy-36, cx+38, cy-20, fill="red", outline="darkred", width=2)
    canvas.create_oval(cx+26, cy-40, cx+34, cy-34, fill="forestgreen", outline="")


def afficher_plat():
    canvas2.delete("all")   # l'assiette est vidée
    assiette(canvas2)       # toujours en premier
    etapes[etape_actuelle]()


def manger():
    global etape_actuelle
    etape_actuelle += 1
    if etape_actuelle < len(etapes):
        afficher_plat()      # plat suivant
    else:
        facture()            # dernier "manger" : on passe à la facture
        fenetre4.destroy()


def repas():
    global fenetre4, canvas2, etapes, etape_actuelle
    fenetre4 = Toplevel(fenetre)
    fenetre4.title("Repas")
    fenetre4.geometry("500x500")
    # fermer cette fenêtre termine le programme
    fenetre4.protocol("WM_DELETE_WINDOW", fenetre.destroy)
    canvas2 = Canvas(fenetre4, width=500, height=500, bg="white")
    canvas2.pack()

    bouton_manger = Button(fenetre4, text="MANGER", width=11, foreground="black", background="light grey", command=manger)
    bouton_manger.place(relx=0.5, rely=0.95, anchor=CENTER)

    # les plats dans l'ordre : entrée, repas, dessert
    etapes = []
    if "Soupe" in listcommande:
        etapes.append(lambda: soupe(canvas2, gratinee=("Gratiner" in listcommande)))
    if "Croquette" in listcommande:
        etapes.append(lambda: croquette(canvas2))
    if "Poisson" in listcommande:
        etapes.append(lambda: poisson(canvas2))
    if "Steak" in listcommande:
        etapes.append(lambda: steak(canvas2))
    if "Café" in listcommande:
        etapes.append(lambda: cafe(canvas2))
    if "gâteau" in listcommande:
        etapes.append(lambda: gateau(canvas2))

    etape_actuelle = 0
    afficher_plat()   # premier plat (l'entrée)


###########################################################
# facture
###########################################################

prix = {"Soupe": 7.50, "Gratiner": 2.00, "Croquette": 9.00,
        "Poisson": 22.00, "Steak": 28.00, "Café": 3.00, "gâteau": 7.00}
noms_facture = {"Soupe": "Soupe à l'oignon", "Gratiner": "   Gratinée (extra)",
                "Croquette": "Croquettes de thon", "Poisson": "Poisson avec pommes de terre",
                "Steak": "Steak avec légumes du jardin", "Café": "Café",
                "gâteau": "Quart de gâteau au fromage"}


def argent(montant):
    return f"{montant:.2f}".replace(".", ",") + " $"


def facture():
    fenetre5 = Toplevel(fenetre)
    fenetre5.title("Facture")
    fenetre5.geometry("500x500")
    fenetre5.protocol("WM_DELETE_WINDOW", fenetre.destroy)

    Label(fenetre5, text="FACTURE", font=("Arial", 14, "bold")).pack(pady=20)

    lignes = Frame(fenetre5)
    lignes.pack(padx=40, fill=X)
    total = 0
    rang = 0
    for article in ["Soupe", "Gratiner", "Croquette", "Poisson", "Steak", "Café", "gâteau"]:
        if article in listcommande:
            Label(lignes, text=noms_facture[article]).grid(row=rang, column=0, sticky=W, pady=3)
            Label(lignes, text=argent(prix[article])).grid(row=rang, column=1, sticky=E, pady=3)
            total += prix[article]
            rang += 1
    lignes.columnconfigure(0, weight=1)

    Label(fenetre5, text="_" * 50).pack(pady=(10, 0))
    Label(fenetre5, text="Total : " + argent(total), font=("Arial", 12, "bold")).pack(pady=10)
    Label(fenetre5, text="Merci de votre visite !").pack(pady=20)
    Button(fenetre5, text="QUITTER", width=11, foreground="black", background="light grey",
           command=fenetre.destroy).place(relx=0.5, rely=0.95, anchor=CENTER)


###########################################################
# Lancement du programme
###########################################################

TEST = False   # True = ouvre seulement la fenêtre repas (sans réservation) / False = programme normal

if TEST:
    # fausse commande pour tester : change la liste comme tu veux
    listcommande = ["Soupe", "Gratiner", "Poisson", "Café"]
    # autres exemples : ["Croquette", "Steak", "gâteau"]  /  ["Soupe", "Pas gratiner", "Steak", "gâteau"]
    repas()
    fenetre.mainloop()
else:
    nom = input("Nom: ")
    prenom = input("Prenom: ")
    reservation()
