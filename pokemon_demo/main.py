from pokemon import *
import random
import time

# Crear dos Pokemon
Maduro = Pokemon("Maduro", "Siniestro", 500, 50, 40, [expropiese, bigote_de_hierro, peace_peace])
DonaldT = Pokemon("DonaldT", "Económico", 600, 55, 35, [peluquin_volador, lluvia_de_billetes, twit])

print("=== COMBATE POKEMON ===\n")
print(Maduro)
print(DonaldT)
print("\n¡Comienza el combate!\n")

# Combate por turnos
turno = 1
turno = 1
print(" ¡COMIENZA EL COMBATE!")

while Maduro.esta_vivo() and DonaldT.esta_vivo():
    print(f"\n--- Turno {turno} ---")
    
    # Decidir orden aleatorio
    combatientes = [Maduro, DonaldT]
    random.shuffle(combatientes)
    
    for atacante in combatientes:
        # El defensor es el que no está atacando
        defensor = Maduro if atacante == Maduro else DonaldT
        
        if atacante.esta_vivo():
            atacante.atacar(defensor)
            print(defensor) # Muestra la vida restante
            
            if not defensor.esta_vivo():
                break # Si alguien muere, salimos del turno
    time.sleep(1)
    turno += 1

# Resultado
print("\n=== FIN DEL COMBATE ===")
if Maduro.esta_vivo():
    print(f"¡{Maduro.nombre} es el ganador!, Diddy le entrenó bien")
else:
    print(f"¡{DonaldT.nombre} es el ganador!Dadme su petróleo")
