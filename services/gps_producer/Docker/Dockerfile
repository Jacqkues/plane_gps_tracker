# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Copier les fichiers de l'application dans le conteneur
COPY ./app/ /app/

# Installer les dépendances à partir de requirements.txt
RUN pip install -r requirements.txt

# Exposer le port que l'application va utiliser
EXPOSE 5432

# Lancer le script Python (modifiez selon votre besoin)
CMD ["python", "ecoute.py"]
