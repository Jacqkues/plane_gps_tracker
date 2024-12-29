# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Kafka borker IP
ENV BROKER_IP=10.18.190.97

# Lancer le script Python
ENTRYPOINT ["python", "generate.py"]