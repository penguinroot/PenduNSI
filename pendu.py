import tkinter as tk
from tkinter import *
import requests
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import mariadb
import io  # Pour lire les images en mémoire

# Adresse du serveur de base de données
wserveur = "109.10.114.61"

# Connexion à la base de données
conn = mariadb.connect(
    user="project",
    password="pm",
    host=wserveur,
    port=3306,
    database="PenduNSI"
)

curseur = conn.cursor()

def creation_liste(wdif1, wdif2, langue):
    query = "SELECT mot FROM MOTS WHERE difficulte <= " + str(wdif2) + " AND difficulte >= " + str(wdif1) + " AND langue = '" + langue + "'"
    curseur.execute(query)
    wliste = curseur.fetchall()
    return wliste

def choix_mot(wliste):
    wmot = random.choice(wliste)
    wmot = ''.join(wmot)
    return str(wmot)

def cacher_mot(mot):
    return ['*' for _ in mot]

def dessiner_pendu(zone_dessin, nb_tentatives, wratio):
    if nb_tentatives == 1:
        zone_dessin.create_line(150 * wratio, 490 * wratio, 250 * wratio, 490 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 2:
        zone_dessin.create_line(200 * wratio, 490 * wratio, 200 * wratio, 20 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 3:
        zone_dessin.create_line(196.5 * wratio, 20 * wratio, 404 * wratio, 20 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 4:
        zone_dessin.create_line(400 * wratio, 20 * wratio, 400 * wratio, 50 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 5:
        zone_dessin.create_oval(375 * wratio, 50 * wratio, 425 * wratio, 100 * wratio, width=8 * wratio, outline="black")
    elif nb_tentatives == 6:
        zone_dessin.create_line(400 * wratio, 100 * wratio, 400 * wratio, 200 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 7:
        zone_dessin.create_line(400 * wratio, 120 * wratio, 360 * wratio, 170 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 8:
        zone_dessin.create_line(400 * wratio, 120 * wratio, 440 * wratio, 170 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 9:
        zone_dessin.create_line(400 * wratio, 200 * wratio, 360 * wratio, 280 * wratio, width=8 * wratio, fill="black")
    elif nb_tentatives == 10:
        zone_dessin.create_line(400 * wratio, 200 * wratio, 440 * wratio, 280 * wratio, width=8 * wratio, fill="black")

def changer_langue(langue):
    global wlangue
    wlangue = langue
    query = "SELECT libelle,mess FROM LANGUE WHERE code='" + wlangue + "'"
    curseur.execute(query)
    message = curseur.fetchone()
    messagebox.showinfo("", "Vous avez choisi " + message[0] + "\n" + message[1])
    query = str("SELECT MAX(difficulte) FROM MOTS WHERE langue='"+wlangue+"'")
    curseur.execute(query)
    wdiff=curseur.fetchone()
    global wdiffmax
    wdiffmax=float(wdiff[0])
    print(wdiffmax)


def ajout_menu(param_langue):
    submenu.add_command(image=tk_image[i], command=lambda: changer_langue(param_langue))

def ouvrir_jeu(borne_mini, borne_maxi, wlangue):
    fenetre_jeu = tk.Toplevel(fenetre_principale)
    wlargeur = fenetre_jeu.winfo_screenwidth()
    whauteur = fenetre_jeu.winfo_screenheight()
    wminimum = min(wlargeur, whauteur)
    wratio = wminimum / 700
    wtaille = str(wminimum) + "x" + str(wminimum)
    fenetre_jeu.title('Jeu du Pendu')
    fenetre_jeu.geometry(wtaille)
    fenetre_jeu.resizable(height=True, width=True)
    fenetre_jeu.configure(bg="white")

    bg_image_path = "0.jpg"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((int(500 * wratio), int(500 * wratio)))
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    zone_dessin = Canvas(fenetre_jeu, width=500 * wratio, height=500 * wratio, bg="white", bd=0)
    zone_dessin.pack()
    zone_dessin.create_image(0, 0, anchor="nw", image=bg_image_tk)
    zone_dessin.image = bg_image_tk

    label_mot = tk.Label(fenetre_jeu, text="", font=("Arial", int(24 * wratio)), bg="white")
    label_mot.pack(pady=int(10 * wratio), padx=int(10 * wratio))

    frame_boutons = tk.Frame(fenetre_jeu)
    frame_boutons.pack(pady=int(5 * wratio))

    wl1 = creation_liste(borne_mini, borne_maxi, wlangue)
    mot = choix_mot(wl1)
    liste_sous_tirets = cacher_mot(mot)
    nb_tentatives = 0
    max_tentatives = 10
    fenetre_principale.withdraw()

    def mettre_a_jour_affichage():
        underscore_line = " ".join(liste_sous_tirets)
        label_mot.config(text=underscore_line)

    def saisir_lettre(lettre, bouton):
        nonlocal nb_tentatives
        lettre = lettre.upper()
        if lettre in mot:
            for i in range(len(mot)):
                if mot[i] == lettre:
                    liste_sous_tirets[i] = lettre
            mettre_a_jour_affichage()
            if "*" not in liste_sous_tirets:
                messagebox.showinfo("Félicitations", "Vous avez gagné !")
                fenetre_principale.deiconify()
        else:
            nb_tentatives += 1
            dessiner_pendu(zone_dessin, nb_tentatives, wratio)
            if nb_tentatives >= max_tentatives:
                messagebox.showinfo("Défaite", "Le mot était : " + mot)
                fenetre_principale.deiconify()

        bouton.config(state="disabled")

    mettre_a_jour_affichage()

    lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index, lettre in enumerate(lettres):
        row = int(index // 13)
        col = int(index % 13)
        bouton = tk.Button(frame_boutons, text=lettre, font=("Tahoma", int(12 * wratio)))
        bouton.config(command=lambda l=lettre, b=bouton: saisir_lettre(l, b))
        bouton.grid(row=row, column=col, padx=5, pady=5)

# Télécharger les images des drapeaux
def telecharger_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))


fenetre_principale = tk.Tk()
fenetre_principale.title("Choix difficulté et langue")
fenetre_principale.geometry("400x400")

label_principal = tk.Label(fenetre_principale, text="Quelle difficulté et langue voulez-vous ?", font=("Arial", 14))
label_principal.pack(pady=20)

wlangue = "fr"

menu_bar = Menu(fenetre_principale)
submenu = Menu(menu_bar, tearoff=0)

query = "SELECT * FROM LANGUE"
curseur.execute(query)
j = curseur.fetchall()
tk_image = []
pil_image = []
wnomvar = []
wchaine = []

for i in range(len(j)):
    url_drapeau = str("http://109.10.114.61/PenduNSI/flag_"+j[i][0]+".jpg")
    image = telecharger_image(url_drapeau)
    if image:
        pil_image.append(image)
        tk_image.append(ImageTk.PhotoImage(image))
        wchaine.append(j[i][0])
        ajout_menu(j[i][0])

menu_bar.add_cascade(label="Menu", menu=submenu)
fenetre_principale.config(menu=menu_bar)

query = str("SELECT MAX(difficulte) FROM MOTS WHERE langue='"+wlangue+"'")
curseur.execute(query)
wdiff=curseur.fetchone()
wdiffmax=float(wdiff[0])
print(wdiffmax)


bouton_facile = tk.Button(fenetre_principale, text="Facile", font=("Arial", 12), command=lambda: ouvrir_jeu(0, wdiffmax/6, wlangue))
bouton_facile.pack(pady=10)

bouton_normal = tk.Button(fenetre_principale, text="Normal", font=("Arial", 12), command=lambda: ouvrir_jeu(wdiffmax/6, wdiffmax/2, wlangue))
bouton_normal.pack(pady=10)

bouton_difficile = tk.Button(fenetre_principale, text="Difficile", font=("Arial", 12), command=lambda: ouvrir_jeu(wdiffmax/2,wdiffmax*(5/6), wlangue))
bouton_difficile.pack(pady=10)

bouton_extreme = tk.Button(fenetre_principale, text="Extrême", font=("Arial", 12), command=lambda: ouvrir_jeu(wdiffmax*0.833, round(wdiffmax,0), wlangue))
bouton_extreme.pack(pady=10)

fenetre_principale.mainloop()
