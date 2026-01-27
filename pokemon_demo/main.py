from pokemon import Pokemon
import random

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
    
    combatientes = [pikachu, charmander]
    random.shuffle(combatientes)
    
    for atacante in combatientes:
        # Definimos quién es el defensor
        defensor = charmander if atacante == pikachu else pikachu
        
        # Atacar solo si el atacante sigue vivo (por si murió en este mismo turno)
        if atacante.esta_vivo():
            atacante.atacar(defensor)
            print(defensor)
            
            # Si el defensor muere, terminamos el turno inmediatamente
            if not defensor.esta_vivo():
                break

# Resultado
print("\n=== FIN DEL COMBATE ===")
if pikachu.esta_vivo():
    print(f"¡{pikachu.nombre} es el ganador!")
else:
    print(f"¡{charmander.nombre} es el ganador!")
