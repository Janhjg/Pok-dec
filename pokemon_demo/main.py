from pokemon import *
import random
import time

# Crear dos Pokemon
Maduro = Pokemon("Maduro", "fuego", 500, 50, 40, [expropiese, lanzallamas, ascuas])
DonaldT = Pokemon("DonaldT", "aire", 600, 55, 35, [peluquin_volador, lluvia_de_billetes, twit])

def combatepokemon():
    print("=== COMBATE POKEMON ===\n")
    print(Maduro)
    print(DonaldT)
    print("\n Comienza el combate!\n")

    # Reiniciar vida
    Maduro.vida = 500
    DonaldT.vida = 600
    
    combate_log = []
    turno = 1
    print(" COMIENZA EL COMBATE!")

    while Maduro.esta_vivo() and DonaldT.esta_vivo():
        print(f"\n--- Turno {turno} ---")
        
        combatientes = [Maduro, DonaldT]
        random.shuffle(combatientes)
        
        for atacante in combatientes:
            defensor = Maduro if atacante == DonaldT else DonaldT
            
            if atacante.esta_vivo():
                vida_antes = defensor.vida
                atacante.atacar(defensor)
                
                print(defensor)
                
                combate_log.append({
                    "turno": turno,
                    "atacante": atacante.get_nombre(),
                    "defensor": defensor.get_nombre(),
                    "vida_restante": defensor.vida
                })
                
                if not defensor.esta_vivo():
                    break
        
        time.sleep(1)
        turno += 1
    
    # Resultado
    print("\n=== FIN DEL COMBATE ===")
    if Maduro.esta_vivo():
        ganador = Maduro.get_nombre()
        mensaje = f"{ganador} es el ganador! Diddy le entrenó bien"
        print(mensaje)
    else:
        ganador = DonaldT.get_nombre()
        mensaje = f"{ganador} es el ganador! Dadme su petróleo"
        print(mensaje)
    
    return {
        "combate": combate_log,
        "ganador": ganador,
        "mensaje": mensaje
    }

# Solo ejecutar si se corre directamente (no cuando se importa)
if __name__ == "__main__":
    combatepokemon()