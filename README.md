# File Downloader - Application Web Dockerisée

Une application web Flask conteneurisée permettant de lister et télécharger des fichiers depuis un volume Docker monté.

## Fonctionnalités

- Interface web intuitive listant tous les fichiers disponibles
- API REST JSON pour lister les fichiers
- Téléchargement sécurisé des fichiers
- Application conteneurisée avec Docker
- Volume Docker pour fichiers dynamiques
- Tests automatiques complets

##  Prérequis

- Docker installé sur votre système
- Git pour cloner le repository

## Installation et lancement

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/file-downloader-app.git
cd file-downloader-app
```

### 2. Créer des fichiers de test (optionnel)

```bash
mkdir -p files
echo "Fichier de test 1" > files/document.txt
echo "Fichier de test 2" > files/readme.md
# Ajoutez vos propres fichiers dans le dossier files/
```

### 3. Construction et lancement avec Docker

**Commande unique pour tout faire :**

```bash
docker build -t file-downloader . && docker run -p 5000:5000 -v $(pwd)/files:/app/files file-downloader
```

**Ou étape par étape :**

```bash
# Construction de l'image
docker build -t file-downloader .

# Lancement du conteneur avec volume monté
docker run -p 5000:5000 -v $(pwd)/files:/app/files file-downloader
```

### 4. Accéder à l'application

- **Interface web :** http://localhost:5000
- **API JSON :** http://localhost:5000/api/files

## Endpoints API

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/` | Page HTML listant les fichiers à télécharger |
| `GET` | `/download/<filename>` | Téléchargement du fichier spécifié |
| `GET` | `/api/files` | Renvoie la liste des fichiers au format JSON |

## Exemples d'utilisation de l'API

### Lister tous les fichiers

```bash
curl http://localhost:5000/api/files
```

**Réponse JSON :**
```json
{
  "status": "success",
  "files": [
    {
      "name": "document.txt",
      "size": 1024,
      "modified": 1640995200.0
    },
    {
      "name": "image.jpg",
      "size": 2048576,
      "modified": 1640995300.0
    }
  ],
  "count": 2
}
```

### Télécharger un fichier

```bash
curl -O http://localhost:5000/download/document.txt
```

### Avec wget

```bash
wget http://localhost:5000/download/document.txt
```

## Exécution des tests

### Tests locaux (sans Docker)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
pytest tests/ -v
```

### Tests dans Docker

```bash
# Construction de l'image de test
docker build -t file-downloader-test .

# Lancement des tests
docker run --rm file-downloader-test pytest tests/ -v
```

## Structure du projet

```
file-downloader-app/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── templates/            # Templates HTML
│   └── index.html        # Page d'accueil
├── tests/                # Tests automatiques
│   └── test_app.py       # Tests unitaires
├── files/                # Dossier pour les fichiers (volume Docker)
└── README.md             # Cette documentation
```

## Configuration

### Variables d'environnement

- `FILES_DIRECTORY` : Chemin vers le dossier contenant les fichiers (défaut: `./files`)

### Personnalisation du volume

Vous pouvez monter n'importe quel dossier local :

```bash
docker run -p 5000:5000 -v /chemin/vers/vos/fichiers:/app/files file-downloader
```

## Sécurité

- Les noms de fichiers sont sécurisés avec `secure_filename()`
- Protection contre les attaques de traversée de répertoire
- Vérification de l'existence des fichiers
- Gestion d'erreurs appropriée

##  Dépannage

### Le conteneur ne démarre pas
- Vérifiez que le port 5000 n'est pas utilisé : `lsof -i :5000`
- Vérifiez les logs : `docker logs <container_id>`

### Aucun fichier n'apparaît
- Vérifiez que le volume est correctement monté
- Vérifiez les permissions du dossier local
- Assurez-vous que des fichiers existent dans le dossier

### Erreur 404 lors du téléchargement
- Vérifiez que le fichier existe dans le dossier monté
- Vérifiez l'orthographe du nom de fichier
