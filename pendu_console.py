import random
import mariadb

# Connexion à la base de données
conn = mariadb.connect(
    user="project",
    password="pm",
    host="109.10.114.61",
    port=3306,
    database="PenduNSI"
)

curseur = conn.cursor()

# Fonction pour récupérer les mots depuis la base de données
def creation_liste():
    wrequete = "SELECT mot FROM MOTS"
    curseur.execute(wrequete)
    wliste = curseur.fetchall()
    return wliste

# Fonction pour choisir un mot aléatoire dans la liste
def choix_mot(wliste):
    wmot = random.choice(wliste)
    wmot = ''.join(wmot).lower()
    return str(wmot)

# Fonction pour cacher le mot avec des étoiles
def cacher_mot(mot):
    return ["*" for _ in mot]

# Fonction qui demande à l’utilisateur de choisir une lettre
def saisir_lettre():
    while True:
        lettre = input("Entrez une lettre : ").lower()
        if lettre.isalpha() and len(lettre) == 1:
            return lettre
        print("Veuillez entrer une seule lettre valide.")

# Fonction pour vérifier si une lettre est dans le mot
def chercher_lettre(mot, lettre):
    """Vérifie si la lettre est présente dans le mot."""
    return lettre in mot

# Fonction pour remplacer les étoiles par la lettre correcte
def remplacer_lettre(mot, lettre, lettres_trouvees):
    """Remplace les étoiles par la lettre correcte aux positions appropriées."""
    for i, l in enumerate(mot):
        if l == lettre:
            lettres_trouvees[i] = lettre

# Fonction principale du jeu
def jeu_pendu():
    # Récupérer les mots depuis la base de données
    wliste = creation_liste()
    mot_a_deviner = choix_mot(wliste)
    lettres_trouvees = cacher_mot(mot_a_deviner)
    essais_restants = 10

    print("Bienvenue au jeu du pendu !")
    print("Le mot à deviner :", " ".join(lettres_trouvees))

    while essais_restants > 0 and "*" in lettres_trouvees:
        # Saisie de l'utilisateur
        lettre = saisir_lettre()

        # Vérification de la lettre
        if chercher_lettre(mot_a_deviner, lettre):
            remplacer_lettre(mot_a_deviner, lettre, lettres_trouvees)
            print("Bravo ! Vous avez trouvé une lettre.")
        else:
            essais_restants -= 1
            print("Raté ! Il vous reste " + str(essais_restants) + " essais.")

        # Afficher le mot avec les lettres trouvées
        print("Mot :", " ".join(lettres_trouvees))

        # Vérification si le mot est entièrement trouvé
        if "*" not in lettres_trouvees:
            print("Félicitations, vous avez trouvé le mot : " + mot_a_deviner)
            return

    # Fin du jeu si le joueur a perdu
    print("Dommage, vous avez perdu ! Le mot était : " + mot_a_deviner)

# Programme principal
if __name__ == "__main__":
    jeu_pendu()
