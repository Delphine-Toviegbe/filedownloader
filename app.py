import os
import json
from datetime import datetime
from flask import Flask, render_template, send_file, jsonify, abort, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


# Configuration
FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY', './files')

# Filtre personnalisé pour les dates
@app.template_filter('datetime')
def datetime_filter(timestamp):
    """Convertit un timestamp en date lisible"""
    return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')


""" Récupation de la liste des fichiers dans le repertoire avec filtres optionnels et 
retourne une liste vide si le repertoire n'exite pas."""
def get_files_list( search_term = None, limit = None):

    directory = app.config.get('FILES_DIRECTORY', './files')  # utilisation dynamique

    if not os.path.exists(FILES_DIRECTORY):
        return []
    files = []
    for fileName in os.listdir(FILES_DIRECTORY):
        filePath = os.path.join(FILES_DIRECTORY, fileName)
        if os.path.isfile(filePath):
            # Filtrer par terme de recherche si fourni
            if search_term and search_term.lower() not in fileName.lower():
                continue
            fileInfo = {
                'name' : fileName,
                'size' : os.path.getsize(filePath),
                'modified' : os.path.getatime(filePath)
            }
            files.append(fileInfo)

    # Trie par nom

    files.sort(key=lambda x: x['name'])

    # Limitation du nombre de résultat si  c'est demandé
    if limit :
        files = files[:limit]
    
    return files

""" Page d'accueil listant les fichiers """
@app.route('/')
def indexPage() :
    search = request.args.get('search', '')

    files = get_files_list(search_term= search if search else None)
    return render_template('index.html', files = files, search = search)

""" API JSON Liste des fichiers disponibles dans le volume"""
@app.route('/api/files')
def api_file():
    files = get_files_list()
    return jsonify({
        'status' : 'success',
        'files' : files,
        'count' : len(files)
    })
""" Téléchargement d'un fichier spécifique"""
@app.route('/download/<fileName>')
def download_file(fileName):
    # Sécuriser le nom du fichier
    secureName = secure_filename(fileName)
    directory = app.config.get('FILES_DIRECTORY', './files')
    filePath = os.path.join(directory, secureName)

    #Vérification de l'existance du fichier ou si c'est bien un fichier
    if not os.path.exists(filePath) or not os.path.isfile(filePath):
        abort(404)

    return send_file(filePath, as_attachment=True)

""" Page 404 en cas de non existance"""
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'status' : 'error',
        'message' : 'Fichier non retrouvé'
    }), 404

""" Page erreur serveur"""
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status' : 'error',
        'message': 'Erreur interne du serveur',
    }), 500

if __name__ == '__main__':
    # Création du dossier s'il n'existe pas
    directory = app.config.get('FILES_DIRECTORY', './files')
    os.makedirs(directory, exist_ok=True)

    # Lancement de l'application

    app.run(host ='0.0.0.0', port=5000, debug=True)