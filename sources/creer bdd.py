#!/usr/bin/env python
import time
import sqlite3
import csv
import unidecode
import sys
def creer_BDD():
    conn.execute("DROP TABLE IF EXISTS MOTS")
    conn.execute("CREATE TABLE MOTS(mot varchar(50), difficulte float, langue varchar(255))")
    conn.execute("DROP TABLE IF EXISTS LANGUE")
    conn.execute("CREATE TABLE LANGUE(code varchar(2), libelle varchar(15), mess varchar(255))")
    conn.execute("DROP TABLE IF EXISTS LETTRES")
    conn.execute("CREATE TABLE LETTRES(lettre varchar(1), nb_occurence float, taux double)")
    conn.execute("DROP TABLE IF EXISTS SCORE")
    conn.execute("CREATE TABLE SCORE(joueur varchar(50),score float, langue varchar(2))")
    conn.execute("INSERT INTO LANGUE VALUES ('fr', 'francais', 'LIBERTE EGALITE FRATERNITE')")
    conn.execute("INSERT INTO LANGUE VALUES ('en', 'anglais', 'GOD SAVE THE QUEEN')")
    conn.execute("INSERT INTO LANGUE VALUES ('de', 'allemand', 'RENDEZ VOUS A L OKTOBER FEST')")
    conn.execute("INSERT INTO LANGUE VALUES ('es', 'espagnol', 'VIVA LA PLAYA')")
              

def mettre_lettre():
    """Initialise la table LETTRES avec toutes les lettres de l'alphabet."""
    query = "DELETE FROM LETTRES"
    curseur.execute(query)
    for i in range(26):
        lettre = chr(65 + i)
        query = "INSERT INTO LETTRES VALUES ('" + lettre + "', 0, 0)"
        curseur.execute(query)
        print("mettre lettre")
    conn.commit()

def remplir_mots(code):
    """ Remplir la table MOTS avec les mots d'une langue spécifique. """
    fichier = "../liste/liste_pendu_" + code + ".csv"
    print(fichier)
    query = "DELETE FROM MOTS WHERE langue = '" + code + "'"
    curseur.execute(query)
    conn.commit()
    with open(fichier, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for i, row2 in enumerate(reader, start=1):
            row = unidecode.unidecode(''.join(row2).upper().strip())
            query = "INSERT INTO MOTS VALUES ('"+row+"', 0, '"+langue[0]+"')"
            curseur.execute(query)
            print(row)
    conn.commit()


def calcul_proba_lettres(langue):
    """
    Calcule les probabilités des lettres pour une langue donnée
    et met à jour la table LETTRES.
    """
    query = "DELETE FROM LETTRES"
    curseur.execute(query)
    conn.commit()
    mettre_lettre()

    wtotal = 0
    query = "SELECT mot FROM MOTS WHERE langue = '" + langue + "'"
    print(query)
    curseur.execute(query)
    mots = curseur.fetchall()
    for mot_tuple in mots:
        mot = ''.join(mot_tuple)
        print(len(mot), mot)
        for char in mot:
            wtotal += 1
            query = "UPDATE LETTRES SET nb_occurence = nb_occurence + 1 WHERE lettre = '" + char + "'"
            curseur.execute(query)
        if wtotal > 0:
            query = "UPDATE LETTRES SET taux = nb_occurence / " + str(wtotal)
            curseur.execute(query)
        print("calcul proba lettre")

    conn.commit()

def difficulte(langue):
    """
    Calcule la difficulté des mots pour une langue donnée
    et met à jour la colonne difficulte de la table MOTS.
    """
    print(f"Début du calcul de difficulté pour la langue : {langue}")

    # Réinitialiser les difficultés
    query = f"UPDATE MOTS SET difficulte = 0 WHERE langue = '{langue}'"
    curseur.execute(query)
    conn.commit()

    # Récupérer tous les mots pour la langue donnée
    query = f"SELECT mot FROM MOTS WHERE langue = '{langue}'"
    curseur.execute(query)
    mots = curseur.fetchall()

    print(f"Nombre de mots récupérés pour {langue} : {len(mots)}")

    # Calculer la difficulté pour chaque mot
    for index, mot_tuple in enumerate(mots, start=1):
        mot = mot_tuple[0]  # Extraire le mot
        note = 0

        # Taux de la première lettre
        query = "SELECT taux FROM LETTRES WHERE lettre = '"+mot[0]+"'"
        curseur.execute(query)
        taux_debut = curseur.fetchone()
        if taux_debut and taux_debut[0] > 0:
            note += 1 / taux_debut[0]

        # Taux des autres lettres
        for i in range(1, len(mot)):
            char = mot[i]
            submot = mot[:i]  # Submot correct
            if char not in "- .":  # Ignorer les caractères spéciaux
                if char not in submot:  # Ne compter que les nouvelles lettres
                    query = f"SELECT taux FROM LETTRES WHERE lettre = '{char}'"
                    curseur.execute(query)
                    taux_char = curseur.fetchone()
                    if taux_char and taux_char[0] > 0:
                        note += 1 / taux_char[0]
        # Ajuster pour les mots longs
        if len(mot) > 4:
            note /= len(mot)

        # Mettre à jour la difficulté dans la base
        query = "UPDATE MOTS SET difficulte = "+str(note)+" WHERE mot = '"+mot+"' AND langue = '"+langue+"'"
        print(mot)
        curseur.execute(query)

    conn.commit()



conn = sqlite3.connect("../PenduNSI.db")
curseur = conn.cursor()
creer_BDD()

# Récupérer les langues
query = "SELECT code FROM 'LANGUE'"
curseur.execute(query)
langues = curseur.fetchall()  # [('fr',), ('en',), ('de',), ('es',)]

# Boucle sur chaque langue
for langue in langues:
    code = langue[0]  # Récupérer le code de la langue, ex : 'fr'
    remplir_mots(code)
    calcul_proba_lettres(code)
    difficulte(code)


conn.close()