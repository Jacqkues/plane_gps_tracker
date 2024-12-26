from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.websocket import websocket_router

app = FastAPI()

# Configuration des CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8080"],  # Adresse de l'application Vue.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter la route WebSocket
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Serveur FastAPI opérationnel"}
