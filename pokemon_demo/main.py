from pokemon import Pokemon


# Crear dos Pokemon
pikachu = Pokemon("Pikachu", "Eléctrico", 100, 55, 40)
charmander = Pokemon("Charmander", "Fuego", 90, 52, 43)

print("=== COMBATE POKEMON ===\n")
print(pikachu)
print(charmander)
print("\n¡Comienza el combate!\n")

# Combate por turnos
turno = 1
while pikachu.esta_vivo() and charmander.esta_vivo():
    print(f"--- Turno {turno} ---")
    
    # Pikachu ataca
    if pikachu.esta_vivo():
        pikachu.atacar(charmander)
        print(charmander)
    
    # Charmander ataca
    if charmander.esta_vivo():
        charmander.atacar(pikachu)
        print(pikachu)
    
    print()
    turno += 1

# Resultado
print("\n=== FIN DEL COMBATE ===")
if pikachu.esta_vivo():
    print(f"¡{pikachu.nombre} es el ganador!")
else:
    print(f"¡{charmander.nombre} es el ganador!")
