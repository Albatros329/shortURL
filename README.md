# 🔗 shortURL

[[English](README_EN.md) | [Français](README.md)]

Un raccourcisseur d'URL open-source simple et efficace, construit avec Python et Flask. Raccourcissez simplement vos liens, sans redirection vers de la publicité ou des services tiers.

## Prérequis

* Python 3.x
* Docker (optionnel)

## Installation

### En local

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/Albatros329/shortURL.git
    cd shortURL
    ```

2. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

3. Lancez l'application :

    ```bash
    python app.py
    ```

    L'application sera accessible à l'adresse `http://localhost:8080`.

### Avec Docker (recommandé)

1. Assurez-vous que Docker est installé.

2. Téléchargez l'image :

    ```bash
    docker pull ghcr.io/albatros329/shorturl:latest
    ```

3. Lancez le conteneur :

    ```bash
    docker run -d -p 8080:8080 -e BASEURL=http://localhost:8080/ ghcr.io/albatros329/shorturl:latest
    # Veuillez ajuster la variable BASEURL selon votre nom de domaine.
    ```


## Configuration

Vous pouvez configurer l'URL de base de l'application via une variable d'environnement, notamment utile lors du déploiement avec Docker.

| Variable | Description | Valeur par défaut |
| :--- | :--- | :--- |
| `BASEURL` | L'URL de base utilisée pour générer les liens raccourcis. | `http://localhost:8080/` |
| `SECRET_KEY` | Clé secrète pour la sécurité des sessions et CSRF. | Générée aléatoirement (non persistant) |

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.