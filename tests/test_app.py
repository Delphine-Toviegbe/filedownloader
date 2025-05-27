import pytest
import os
import tempfile
import json
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
    test_file1 = os.path.join(test_dir, 'test1.txt')
    test_file2 = os.path.join(test_dir, 'test2.pdf')
    
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
    assert b'test1.txt' in response.data
    assert b'test2.pdf' in response.data

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
    assert 'test1.txt' in filenames
    assert 'test2.pdf' in filenames
