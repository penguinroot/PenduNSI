import tkinter as tk
from tkinter import messagebox
import requests
import random
from PIL import Image, ImageTk
import mariadb


conn = mariadb.connect(
    user="project",
    password="pm",
    host="109.10.114.61",
    port=3306,
    database="PenduNSI"

)

curseur = conn.cursor()



def creation_liste(wdif1,wdif2) :
    wrequete="SELECT mot FROM MOTS WHERE difficulte<="+str(wdif2)+" AND difficulte>="+str(wdif1)
    curseur.execute(wrequete)
    wliste=curseur.fetchall()
    return wliste
        
def choix_mot(wliste):
    wmot = random.choice(wliste)
    wmot=''.join(wmot)
    return str(wmot)

def mot_en_liste(mot):
    return ['_' for _ in mot]

def precharger_images():
    images = []
    for i in range(11):
        image_url = f"http://109.10.114.61/{i}.png"
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_data = Image.open(response.raw)
            image_resized = image_data.resize((200, 200))
            images.append(ImageTk.PhotoImage(image_resized))
        else:
            images.append(None)
    return images

def ouvrir_jeu(borne_mini,borne_maxi):
    fenetre_jeu = tk.Toplevel(fenetre_principale)
    fenetre_jeu.title('Jeu du Pendu')
    fenetre_jeu.geometry("600x600+200+50")
    fenetre_jeu.resizable(height=True, width=True)
    fenetre_jeu.configure(bg="white")

    frame_listbox = tk.Frame(fenetre_jeu)
    frame_listbox.pack(fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(fenetre_jeu, font=("Arial", 16), selectbackground="#4286f4", selectforeground="white")
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    frame_boutons = tk.Frame(fenetre_jeu)
    frame_boutons.pack(pady=5)

    frame_image = tk.Frame(fenetre_jeu)
    frame_image.pack(pady=10)
    label_image = tk.Label(frame_image)
    label_image.pack()
    wl1=creation_liste(borne_mini, borne_maxi)
    mot = choix_mot(wl1)
    liste_underscores = mot_en_liste(mot)
    nb_tentatives = 0
    max_tentatives = 10
    fenetre_principale.withdraw()

    images_pendu = precharger_images()

    def mettre_a_jour_affichage():
        underscore_line = " ".join(liste_underscores)
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, underscore_line)

    def mettre_a_jour_image(nb_tentatives):
        if 0 <= nb_tentatives < len(images_pendu):
            label_image.config(image=images_pendu[nb_tentatives])
            label_image.image = images_pendu[nb_tentatives]

    def bouton_click(letter, button):
        nonlocal nb_tentatives
        letter = letter.upper()
        if letter in mot:
            for i in range(len(mot)):
                if mot[i] == letter:
                    liste_underscores[i] = letter
            mettre_a_jour_affichage()
            if "_" not in liste_underscores:
                messagebox.showinfo("Félicitations", "Vous avez gagné !")
                fenetre_principale.deiconify()
        else:
            nb_tentatives += 1
            mettre_a_jour_image(nb_tentatives)
            if nb_tentatives >= max_tentatives:
                messagebox.showinfo("Défaite", "Vous avez perdu !"+mot)
                
                fenetre_principale.deiconify()
        button.config(state="disabled")

    mettre_a_jour_affichage()
    mettre_a_jour_image(nb_tentatives)

    lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
               "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    for index, lettre in enumerate(lettres):
        row = index // 13
        col = index % 13
        bouton = tk.Button(frame_boutons, text=lettre, font=("Tahoma", 12))
        bouton.config(command=lambda l=lettre, b=bouton: bouton_click(l, b))
        bouton.grid(row=row, column=col, padx=5, pady=5)
creation_liste(1000,1200)
fenetre_principale = tk.Tk()
fenetre_principale.title("Choix difficulté")
fenetre_principale.geometry("400x300")

label_principal = tk.Label(fenetre_principale, text="Quelle difficulté voulez-vous ?", font=("Arial", 14))
label_principal.pack(pady=20)

bouton_facile = tk.Button(fenetre_principale, text="Facile", font=("Arial", 12), command=lambda: ouvrir_jeu(0,50))
bouton_facile.pack(pady=10)

bouton_normal = tk.Button(fenetre_principale, text="Normal", font=("Arial", 12), command=lambda: ouvrir_jeu(51,250))
bouton_normal.pack(pady=10)

bouton_difficile = tk.Button(fenetre_principale, text="Difficile", font=("Arial", 12), command=lambda: ouvrir_jeu(251,750))
bouton_difficile.pack(pady=10)

bouton_extreme = tk.Button(fenetre_principale, text="Extrême", font=("Arial", 12), command=lambda: ouvrir_jeu(751,10000))
bouton_extreme.pack(pady=10)

fenetre_principale.mainloop()
