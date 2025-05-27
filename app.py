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