# Module Imports
import mariadb
import csv
import unidecode
import sys

def mettre_lettre():
    """Initialise la table LETTRES avec toutes les lettres de l'alphabet."""
    query = "DELETE FROM LETTRES"
    curseur.execute(query)
    for i in range(26):
        lettre = chr(65 + i)
        query = "INSERT INTO LETTRES VALUES ('" + lettre + "', 0, 0)"
        curseur.execute(query)
    conn.commit()

def remplir_mots(code):
    """ Remplir la table MOTS avec les mots d'une langue spécifique. """
    code = code[0]  # Extract the string from the tuple
    fichier = "liste_pendu_" + code + ".csv"
    query = "DELETE FROM MOTS WHERE langue = '" + code + "'"
    curseur.execute(query)
    conn.commit()
    sys.exit("Arrêt du script avec un message")
    with open(fichier, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for i, row2 in enumerate(reader, start=1):
            row = unidecode.unidecode(''.join(row2).upper().strip())
            print(i, row)

            if "'" not in row:
                # Vérification des doublons avant insertion
                query_check = "SELECT 1 FROM MOTS WHERE mot = %s AND langue = %s"
                curseur.execute(query_check, (row, langue))
                if curseur.fetchone():
                    print(f"Le mot '{row}' existe déjà dans la langue '{langue}', il ne sera pas inséré.")
                else:
                    query = "INSERT INTO MOTS (mot, difficulte, langue) VALUES (%s, 0, %s)"
                    curseur.execute(query, (row, langue))

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
    conn.commit()

def difficulte(langue):
    """
    Calcule la difficulté des mots pour une langue donnée
    et met à jour la colonne `difficulte` de la table MOTS.
    """
    query = "UPDATE MOTS SET difficulte = 0 WHERE langue = '" + langue + "'"
    curseur.execute(query)
    conn.commit()

    query = "SELECT mot FROM MOTS WHERE langue = '" + langue + "'"
    curseur.execute(query)
    mots = curseur.fetchall()

    for mot_tuple in mots:
        mot = ''.join(mot_tuple)
        print(len(mot), mot)
        note = 0
        query = "SELECT taux FROM LETTRES WHERE lettre = '" + mot[0] + "'"
        curseur.execute(query)
        taux_debut = curseur.fetchone()

        if taux_debut:
            note += 1 / taux_debut[0]

        for i in range(1, len(mot)):
            char = mot[i]
            submot = mot[1:i-1]
            if char not in "- .":
                if char not in submot:
                    query = "SELECT taux FROM LETTRES WHERE lettre = '" + char + "'"
                    curseur.execute(query)
                    taux_char = curseur.fetchone()
                    if taux_char:
                        note += 1 / taux_char[0]

        if len(mot) > 4:
            note /= len(mot)

        query = "UPDATE MOTS SET difficulte = " + str(note) + " WHERE mot = '" + mot + "' AND langue = '" + langue + "'"
        curseur.execute(query)
    conn.commit()

conn = mariadb.connect(
    user="project",
    password="pm",
    host="109.10.114.61",
    port=3306,
    database="PenduNSI"
)
curseur = conn.cursor()
query = "SELECT code FROM LANGUE "
curseur.execute(query)
langues=curseur.fetchall()
print(langues)
wlangues=[]
wlangues.append(langues)


for langue in wlangues:
    code = langue[0]
    print(code)
    remplir_mots(code)
    calcul_proba_lettres(code)
    difficulte(code)
    query = "SELECT * FROM LETTRES"
    curseur.execute(query)
    test = curseur.fetchall()
    print(test)

conn.close()
