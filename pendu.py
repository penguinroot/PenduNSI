import tkinter as tk
from tkinter import messagebox, simpledialog, Canvas, Menu
import random
import sqlite3
from PIL import Image, ImageTk

# Si vous gardez les téléchargements d'images
import io
import os
import sys

if getattr(sys, 'frozen', False):  # Si l'application est "frozen" (compilée)
    base_path = sys._MEIPASS  # Dossier temporaire contenant les fichiers embarqués
else:
    base_path = os.path.dirname(__file__)  # Répertoire du script

db_path = os.path.join(base_path, "PenduNSI.db")

# Connexion à la base de données
conn = sqlite3.connect(db_path)
curseur = conn.cursor()

def creation_liste(wdif1, wdif2, langue):
    query = "SELECT mot FROM MOTS WHERE difficulte <= " + str(wdif2) + " AND difficulte >= " + str(wdif1) + " AND langue = '" + langue + "'"
    print(query)
    curseur.execute(query)
    wliste = curseur.fetchall()
    return wliste

def choix_mot(wliste):
    if not wliste:
        raise ValueError("La liste des mots est vide.")
    wmot = random.choice(wliste)
    wmot = ''.join(wmot)
    print(wmot)
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

def ouvrir_jeu(borne_mini, borne_maxi, wlangue):
    nb_tentatives = [0]  # Utilisation d'une liste pour rendre nb_tentatives mutable
    max_tentatives = 10
    fenetre_jeu = tk.Toplevel(fenetre_principale)
    wlargeur = fenetre_jeu.winfo_screenwidth()
    whauteur = fenetre_jeu.winfo_screenheight()
    wminimum = min(wlargeur, whauteur)
    wratio = wminimum / 700
    wtaille = str(wminimum) + "x" + str(wminimum)
    fenetre_jeu.title('Jeu du Pendu')
    fenetre_jeu.geometry(wtaille+"+0+0")
    fenetre_jeu.resizable(height=True, width=True)
    fenetre_jeu.configure(bg="#dfe0d0")

    # Fenêtre indépendante pour le timer
    fenetre_timer = tk.Toplevel(fenetre_jeu)
    fenetre_timer.title("Minuteur")
    wlargeur = int(300 * wratio)
    whauteur = int(50 * wratio)
    fenetre_timer.geometry(str(wlargeur) + "x" + str(whauteur) + "+1250+250")
    fenetre_timer.resizable(height=False, width=False)
    fenetre_timer.config(bg="#dfe0d0")

    label_timer = tk.Label(fenetre_timer, text="Temps écoulé : 0 s", font=("Tahoma", 18), bg="#dfe0d0")
    label_timer.pack(pady=20)

    # Définir temps comme une variable mutable (global)
    temps = [0]  # Utilisation d'une liste pour modifier la valeur depuis une fonction imbriquée

    def timer():
        """Incrémente le minuteur de 1 seconde."""
        temps[0] += 1  # Modifier la valeur dans la liste
        label_timer.config(text="Temps écoulé : "+str(temps[0])+"s")
        fenetre_timer.after(1000, timer)

    # Chargement de l'image de fond
    bg_image_path = os.path.join(base_path, "image", "0.jpg")
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((int(500 * wratio), int(500 * wratio)))
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    zone_dessin = Canvas(fenetre_jeu, width=500 * wratio, height=500 * wratio, bg="#dfe0d0", bd=0)
    zone_dessin.pack()
    zone_dessin.create_image(0, 0, anchor="nw", image=bg_image_tk)
    zone_dessin.image = bg_image_tk

    label_mot = tk.Label(fenetre_jeu, text="", font=("Tahoma", int(24 * wratio)), bg="#dfe0d0")
    label_mot.pack(pady=int(10 * wratio), padx=int(10 * wratio))

    frame_boutons = tk.Frame(fenetre_jeu, bg="#dfe0d0")
    frame_boutons.pack(pady=int(5 * wratio))

    wl1 = creation_liste(borne_mini, borne_maxi, wlangue)
    mot = choix_mot(wl1)
    liste_sous_tirets = cacher_mot(mot)
    fenetre_principale.withdraw()
    # Lancer le minuteur
    timer()

    def mettre_a_jour_affichage():
        underscore_line = " ".join(liste_sous_tirets)
        label_mot.config(text=underscore_line)

    def saisir_lettre(lettre, bouton):
        lettre = lettre.upper()
        if lettre in mot:
            for i in range(len(mot)):
                if mot[i] == lettre:
                    liste_sous_tirets[i] = lettre
            mettre_a_jour_affichage()
            if "*" not in liste_sous_tirets:
                username = simpledialog.askstring("Félicitations", "Vous avez gagné en " + str(temps[0]) + " secondes !\nEntrez votre nom d'utilisateur :")
                if username:
                    # Calcul du score basé sur le temps écoulé et difficulté max
                    temps_score = (1 / temps[0]) * wdiffmax * 100
                    curseur.execute("INSERT INTO SCORE VALUES ('"+str(username)+"', "+str(round(temps_score))+", '"+wlangue+"')")
                    curseur.execute(query)
                    conn.commit()
                fenetre_principale.deiconify()
                fenetre_timer.destroy()
                fenetre_jeu.destroy()
        else:
            nb_tentatives[0] += 1
            dessiner_pendu(zone_dessin, nb_tentatives[0], wratio)
            if nb_tentatives[0] >= max_tentatives:
                messagebox.showinfo("Défaite", "Le mot était : " + mot)
                fenetre_principale.deiconify()
                fenetre_timer.destroy()
                fenetre_jeu.destroy()

        bouton.config(state="disabled")

    mettre_a_jour_affichage()

    # Définir la variable lettres juste avant la création des boutons
    lettres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Définir les lettres avant leur utilisation
    for index, lettre in enumerate(lettres):
        row = int(index // 13)
        col = int(index % 13)
        bouton = tk.Button(frame_boutons, text=lettre, font=("Tahoma", int(12 * wratio)), bg="#dfe0d0") # Changer la couleur d'UN bouton
        bouton.config(command=lambda l=lettre, b=bouton: saisir_lettre(l, b))  # Passer nb_tentatives ici
        bouton.grid(row=row, column=col, padx=5, pady=5,)

# Ajouter une langue au menu
def ajout_menu(param_langue):
    submenu.add_command(image=tk_image[i], command=lambda: changer_langue(param_langue))

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
    if wdiff and wdiff[0] is not None:
        wdiffmax = float(wdiff[0])
    else:
        wdiffmax = 0.0
    print(wdiffmax)

def set_langue(langue):
    global wlangue
    wlangue = langue

# Télécharger les images des drapeaux
def telecharger_image(path):
    return Image.open(path)

def afficher_scores():
    fenetre_scores = tk.Toplevel(fenetre_principale)
    fenetre_scores.title("Tableau des scores")
    fenetre_scores.geometry("500x400")
    
    query = "SELECT * FROM SCORE ORDER BY score DESC"
    curseur.execute(query)
    scores = curseur.fetchall()
    
    label_scores = tk.Label(fenetre_scores, text="Tableau des scores", font=("Arial", 14))
    label_scores.pack(pady=10)
    
    frame_scores = tk.Frame(fenetre_scores)
    frame_scores.pack(pady=10)
    
    for i, score in enumerate(scores):
        label_rank = tk.Label(frame_scores, text=str(i+1), font=("Arial", 12), borderwidth=1, relief="solid", width=5)
        label_rank.grid(row=i, column=0, padx=5, pady=5)
        
        label_user = tk.Label(frame_scores, text=score[0], font=("Arial", 12), borderwidth=1, relief="solid", width=20)
        label_user.grid(row=i, column=1, padx=5, pady=5)
        
        label_score = tk.Label(frame_scores, text=str(score[1]), font=("Arial", 12), borderwidth=1, relief="solid", width=10)
        label_score.grid(row=i, column=2, padx=5, pady=5)
        
        label_langue = tk.Label(frame_scores, text=score[2], font=("Arial", 12), borderwidth=1, relief="solid", width=10)
        label_langue.grid(row=i, column=3, padx=5, pady=5)

fenetre_principale = tk.Tk()
fenetre_principale.title("Choix difficulté et langue")
fenetre_principale.geometry("400x400")

label_principal = tk.Label(fenetre_principale, text="Quelle difficulté et langue voulez-vous ?", font=("Tahoma", 14, "bold"))
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
    path_drapeau = os.path.join(base_path, "image", "flag_" + j[i][0] + ".jpg")
    image = telecharger_image(path_drapeau)
    if image:
        pil_image.append(image)
        tk_image.append(ImageTk.PhotoImage(image))
        wchaine.append(j[i][0])
        ajout_menu(j[i][0])

menu_bar.add_cascade(label="Menu", menu=submenu)
fenetre_principale.config(menu=menu_bar)

query = "SELECT MAX(difficulte) FROM MOTS WHERE langue='"+wlangue+"'"
curseur.execute(query)
wdiff = curseur.fetchone()
if wdiff and wdiff[0] is not None:
    wdiffmax = float(wdiff[0])
else:
    wdiffmax = 0.0
print(wdiffmax)

bouton_facile = tk.Button(fenetre_principale, text="Facile 👍", font=("Tahoma", 12, "bold"), command=lambda: ouvrir_jeu(0, wdiffmax/6, wlangue))
bouton_facile.config(bg="#e9e7c7")
bouton_facile.pack(pady=10)

bouton_normal = tk.Button(fenetre_principale, text="Normal 😏", font=("Tahoma", 12, "bold"), command=lambda: ouvrir_jeu(wdiffmax/6, wdiffmax/2, wlangue))
bouton_normal.config(bg="#e9e7c7")
bouton_normal.pack(pady=10)

bouton_difficile = tk.Button(fenetre_principale, text="Difficile 😎", font=("Tahoma", 12, "bold"), command=lambda: ouvrir_jeu(wdiffmax/2,wdiffmax*(3/4), wlangue))
bouton_difficile.config(bg="#e9e7c7")
bouton_difficile.pack(pady=10)

bouton_extreme = tk.Button(fenetre_principale, text="Extrême 🔥", font=("Tahoma", 12, "bold"), command=lambda: ouvrir_jeu(wdiffmax*(3/4), wdiffmax, wlangue))
bouton_extreme.config(bg="#e9e7c7")
bouton_extreme.pack(pady=10)

bouton_scores = tk.Button(fenetre_principale, text="Voir les scores", font=("Tahoma", 12, "bold"), command=afficher_scores)
bouton_scores.config(bg="#e9e7c7")
bouton_scores.pack(pady=10)

fenetre_principale.mainloop()
