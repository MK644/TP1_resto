from tkinter import *
fenetre = Tk()

fenetre.title("répétition...")

fenetre.geometry("500x340")

fenetre.minsize(500, 340)

fenetre.maxsize(500, 340)

Bouton0 = Button(fenetre, text="Valider", width=11, foreground="black", background="light grey")
Bouton0.place(relx=0.2, rely=0.5, anchor=CENTER)

def out(event):
    Bouton0["bg"] = "light grey"

def hover(event):
    Bouton0["bg"] = "dark grey"

Bouton0.bind("<Enter>", hover)
Bouton0.bind("<Leave>", out)
champ = Entry(fenetre)
champ.place(x=57, y=105)
champ2 = Entry(fenetre)
champ2.place(x=57, y=130)
Nom=Label(fenetre, text="Nom:")
Prenom=Label(fenetre, text="Prenom:")
Nom.place(x=6, y=105)
Prenom.place(x=6, y=130)
fenetre.mainloop()

