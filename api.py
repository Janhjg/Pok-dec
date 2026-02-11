from main import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Pokemones"}

@app.get("/pokemones")
def obtener_pokemones():
    return [Maduro, DonaldT]

@app.post("/pokemones")
def crear_pokemon():
    return {"status": "Pokemon creado"}

@app.get("/combate")
def iniciar_combate():
    resultado = combatepokemon()
    return resultado