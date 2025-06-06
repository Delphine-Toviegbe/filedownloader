# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Expose le port 5000
EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

#Copie le code de l'application
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Crée le répertoire pour les fichiers
RUN mkdir -p /app/files


# Définit les variables d'environnement
ENV FLASK_APP=app.py
ENV FILES_DIRECTORY=/app/files

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
