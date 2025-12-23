# Solveur d'Argumentation Abstraite (Projet RCR)

**Auteurs :**

* [Nicolas Adamczyk]
* [Sebastian Straut]

**Cours :** Représentation des Connaissances et Raisonnement (Université de Paris) 
**Année :** 2025-2026 

---

## Description

Ce projet implémente un solveur pour les systèmes d'argumentation abstraits (AF). Il permet de vérifier des propriétés sémantiques (Préférée et Stable) sur des graphes d'arguments définis au format `.apx`.

Le programme répond aux six tâches standard définies dans le sujet :

* **VE-PR / VE-ST** : Vérification d'une extension (Préférée / Stable).
* **DC-PR / DC-ST** : Acceptation crédule (Credulous acceptance).
* **DS-PR / DS-ST** : Acceptation sceptique (Skeptical acceptance).

## Prérequis

**Python 3.12** ou version ultérieure.

* Le module standard `argparse` est utilisé pour la gestion de la ligne de commande.
* (Optionnel) **pytest** pour lancer la suite de tests.

## Structure du Projet

```text
.
├── program.py              # Point d'entrée principal (CLI)
├── src/
│   ├── af.py               # Structure de données (AF) et vérifications de base
│   ├── apx_parser.py       # Chargement et validation des fichiers .apx
│   ├── semantics.py        # Gestionnaire des tâches (router)
│   ├── utils.py            # Utilitaires (normalisation des noms)
│   └── algorithms/
│       ├── preferred.py    # Algorithme pour la sémantique préférée
│       └── stable.py       # Algorithme pour la sémantique stable
├── tests/
│   ├── test_parser.py      # Tests du parseur et validation de format
│   ├── test_cli_examples.py # Tests des exemples CLI
│   ├── test_new_cases.py   # Tests sur les cas limites (cycles, self-attack, etc.)
│   └── data/               # Fichiers .apx de test (test_af1 à test_af9)
│       ├── test_af*.apx    # Fichiers d'entrée
│       ├── test_af*_pr.txt # Extensions préférées attendues
│       └── test_af*_st.txt # Extensions stables attendues
└── README.md               # Ce fichier

```

## Utilisation

Le programme s'exécute en ligne de commande via le fichier `program.py`.

### Syntaxe Générale

```bash
python program.py -p <TACHE> -f <FICHIER> -a <ARGUMENTS>
```


### Paramètres

* `-p` : Le problème à résoudre. Valeurs possibles : `VE-PR`, `VE-ST`, `DC-PR`, `DS-PR`, `DC-ST`, `DS-ST`.
* `-f` : Le chemin vers le fichier `.apx` décrivant le système d'argumentation.
* `-a` : Les arguments concernés par la requête.
* Pour **VE** (Vérification d'ensemble) : une liste séparée par des virgules (ex: `a,c,d`). 
* Pour **DC/DS** (Décision sur un argument) : un seul nom d'argument (ex: `a`). 

### Format des fichiers `.apx`

Le fichier d'entrée doit respecter le format suivant:

```prolog
arg(nom_argument).
att(attaquant, attaque).
```

**Notes importantes :**
* Les noms d'arguments sont **insensibles à la casse** : `A` et `a` sont équivalents (normalisés en minuscules).
* Pas d'espaces dans les lignes.
* Tous les arguments doivent être déclarés avant d'être utilisés dans une attaque.
* Les noms `arg` et `att` sont réservés et ne peuvent pas être utilisés comme noms d'arguments.
* Les arguments en double sont détectés et rejetés.

### Exemples d'Exécution

Supposons un fichier `graph.apx` contenant le graphe de la Figure 1 (a $\rightarrow$ b, b $\rightarrow$ c, b $\rightarrow$ d) :

1. **Vérifier si {a, c, d} est une extension préférée :**
```bash
python program.py -p VE-PR -f graph.apx -a a,c,d
# Sortie attendue : YES
```


2. **Vérifier si l'argument 'a' est accepté crédiblement (au moins une extension stable) :**
```bash
python program.py -p DC-ST -f graph.apx -a a
# Sortie attendue : YES
```


3. **Vérifier si l'argument 'b' est accepté sceptiquement (toutes les extensions préférées) :**
```bash
python program.py -p DS-PR -f graph.apx -a b
# Sortie attendue : NO
```


Le programme renvoie uniquement `YES` ou `NO` sur la sortie standard, ou un message d'erreur explicite en cas de problème (argument inconnu, fichier invalide).

## Tests

Une suite de tests automatisés est fournie pour valider la logique interne et le comportement de l'interface. Elle couvre les cas nominaux et les cas limites :

* **Self-attacks** (test_af6) : arguments qui s'attaquent eux-mêmes
* **Cycles impairs** (test_af9) : cycles de longueur 3 sans extensions stables
* **Cycles pairs** (test_af6) : cycles de longueur 2
* **Chaînes linéaires** (test_af7) : arguments en séquence
* **Arguments isolés** (test_af8) : arguments sans attaques
* **Graphes complexes** (test_af1-5) : cas variés du sujet

### Lancer tous les tests

```bash
python -m pytest -q
```

### Lancer un fichier de tests spécifique

```bash
python -m pytest tests/test_parser.py -v
python -m pytest tests/test_cli_examples.py -v
```

### Lancer les tests des nouveaux cas

```bash
python tests/test_new_cases.py
```

### Validation des extensions

Pour vérifier que toutes les extensions calculées correspondent aux fichiers .txt attendus :

```bash
python -m pytest tests/ -v
```