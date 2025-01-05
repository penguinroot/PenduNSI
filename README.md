
# PenduNSI

## Description

PenduNSI est une implémentation du jeu du pendu en Python, développée dans le cadre des cours de NSI (Numérique et Sciences Informatiques). Le jeu permet de jouer au pendu en console, avec des listes de mots disponibles en plusieurs langues.

## Fonctionnalités

- Jeu du pendu en mode console.
- Listes de mots en différentes langues : français, anglais, espagnol, allemand.
- Gestion des accents et des caractères spéciaux.
- Affichage du drapeau correspondant à la langue sélectionnée.

## Prérequis

- Python 3.x installé sur votre machine.

## Installation

1. Clonez le dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/Pi-Aime/PenduNSI.git
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd PenduNSI
   ```

## Utilisation

Pour lancer le jeu en mode console, exécutez le script `pendu_console.py` :

```bash
python pendu_console.py
```

Suivez les instructions à l'écran pour jouer au jeu du pendu. Vous serez invité à choisir une langue, puis à deviner les lettres du mot secret.

## Structure du Projet

- `pendu.py` : Contient les fonctions principales du jeu.
- `pendu_console.py` : Script pour lancer le jeu en mode console.
- `connexion_db.py` : Module pour la gestion de la connexion à la base de données (si applicable).
- `liste_pendu_fr.csv`, `liste_pendu_en.csv`, etc. : Fichiers CSV contenant les listes de mots pour chaque langue.
- `flag_fr.jpg`, `flag_en.jpg`, etc. : Images des drapeaux pour chaque langue.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le dépôt.
2. Créez une branche pour votre fonctionnalité ou correction de bug :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. Commitez vos modifications :
   ```bash
   git commit -m "Ajout de ma fonctionnalité"
   ```
4. Poussez vers votre fork :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
5. Créez une pull request sur le dépôt principal.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

Merci aux enseignants de NSI pour leur soutien et leurs conseils tout au long du développement de ce projet.
