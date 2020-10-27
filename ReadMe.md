# Mode Optimisation

## Partie GA
### Voir APP2/scripts/optimize-ga/

Pour exécuter l'algorithme, lancer le fichier main.py avec les configurations d'intérêts
Le fichier sexy_time.py comprend les différents algorithmes de reproduction des chromosomes
Le fichier GA_module.py comprend la définition des chromosomes ainsi que les différentes techniques de selection naturelle.

# Mode Circuit

## Partie Fuzzy
### Voir APP2/scripts/drive-fuzzy

Pour exécuter l'algorithme, lancer le fichier main.py avec les configurations d'intérêts. 
Le fichier Fuzzy_modules.py comprend les différentes fonction de pré et post traitement ainsi que les variables à fuzzyfier et les règles de fuzzyfication.

## Partie NN
### Voir APP2/scripts/drive-nnet

Installer sudo pip install nipype
et sudo pip install comet-ml.

On visualiser l'entrainement ici:
https://www.comet.ml/bertsam/app2/view/new

Dans main.py, la ligne 53 permet d'entrainer à partir d'un dataset ou de simuler à partir d'un modèle déjà entrainé. Utiliser les ligne 69 à 72 pour décider le dataset d'entrainement.
Le fichier nn_module.py contient les fonctions de formatage et de loading du dataset. Il comprend aussi les spécifications du modèle du nn pour l'entrainement.


