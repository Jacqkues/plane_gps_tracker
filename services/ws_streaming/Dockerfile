# Dockerfile dans le dossier ./backend
FROM python:3.9-slim


# Copier le code de l'application
WORKDIR /app
COPY . /app


EXPOSE  8000
# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level","debug"]
