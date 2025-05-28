import pytest
import os
import tempfile
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Fixture pour créer un client de test"""
    # Créer un répertoire temporaire pour les tests
    test_dir = tempfile.mkdtemp()
    
    # Configurer l'application pour les tests
    app.config['TESTING'] = True
    app.config['FILES_DIRECTORY'] = test_dir
    
    # Créer quelques fichiers de test
    test_file1 = os.path.join(test_dir, 'test.txt')
    test_file2 = os.path.join(test_dir, 'document.txt')
    
    with open(test_file1, 'w') as f:
        f.write('Contenu du fichier de test 1')
    
    with open(test_file2, 'w') as f:
        f.write('Contenu du fichier de test 2')
    
    with app.test_client() as client:
        yield client
    
    # Nettoyer après les tests
    import shutil
    shutil.rmtree(test_dir)

def test_index_page(client):
    """Test de la page d'accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'File Downloader' in response.data
    assert b'test.txt' in response.data
    assert b'document.txt' in response.data

def test_api_files_endpoint(client):
    """Test de l'endpoint API /api/files"""
    response = client.get('/api/files')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'files' in data
    assert 'count' in data
    assert data['count'] == 2
    
    # Vérifier que les fichiers sont présents
    filenames = [f['name'] for f in data['files']]
    assert 'test.txt' in filenames
    assert 'document.txt' in filenames


"""Test du téléchargement d’un fichier existant"""
def test_download_file(client):
    response = client.get('/download/test.txt')
    assert response.status_code == 200
    assert response.data == b'Contenu du fichier de test 1'
    assert 'attachment' in response.headers['Content-Disposition']


"""Test du téléchargement d’un fichier inexistant"""
def test_download_nonexistent_file(client):
    response = client.get('/download/inexistant.txt')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Fichier non retrouv' in data['message']


"""Test de la recherche de fichiers"""
def test_search_functionality(client):
    response = client.get('/?search=test')
    assert response.status_code == 200
    assert b'test.txt' in response.data
    assert b'document.txt' not in response.data


"""Test de la limitation du nombre de fichiers retournés"""
from app import get_files_list

def test_limit_results(client):
    files = get_files_list(limit=1)
    assert len(files) == 1


