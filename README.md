# 🔗 shortURL

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

1. Assurez-vous que Docker et Docker Compose sont installés.

2. Lancez le conteneur :

    ```bash
    docker compose up -d
    ```

    L'application sera accessible à l'adresse `http://localhost:8080`.

## Configuration

Vous pouvez configurer l'URL de base de l'application via une variable d'environnement, notamment utile lors du déploiement avec Docker.

| Variable | Description | Valeur par défaut |
| :--- | :--- | :--- |
| `BASEURL` | L'URL de base utilisée pour générer les liens raccourcis. | `http://localhost:8080/` |

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.