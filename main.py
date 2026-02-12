from pokemon import *
import random
import time
from data.filtro_datos import *

SEP  = "=" * 52
SEP2 = "-" * 52

def limpiar():
    print("\n" * 2)

def mostrar_ficha(entidad: Entidad):
    """Muestra la ficha completa de una entidad."""
    print(SEP2)
    print(f"  {entidad.get_nombre()}  [{entidad.tipo.upper()}]")
    print(SEP2)
    print(f"  {entidad.descripcion}")
    print(SEP2)
    print(f"  HP:        {entidad.hp_max:<6}  ATQ:  {entidad.ataque}")
    print(f"  DEF:       {entidad.defensa:<6}  VEL:  {entidad.velocidad}")
    print(f"  EVASION:   {entidad.evasion}%{'':<4}  MANA: {entidad.mana_max}")
    print(SEP2)
    print("  Habilidades:")
    for h in entidad.habilidades:
        print(f"    • {h.nombre:<30} PTN: {h.potencia:<4} MANA: {h.coste_mana}")
    print(SEP2)

def listar_entidades(entidades: dict):
    """Muestra todas las entidades con número, nombre y descripción corta."""
    lista = list(entidades.values())
    print(SEP)
    print("  ELIGE TU COMBATIENTE")
    print(SEP)
    for i, e in enumerate(lista, 1):
        print(f"  [{i:>2}] {e.get_nombre():<35} [{e.tipo.upper()}]")
        print(f"        {e.descripcion}")
        print()
    print(SEP)
    return lista

def seleccionar_entidad(entidades: dict, titulo: str) -> Entidad:
    """
    Menú interactivo:
      1. Lista todas las entidades con descripcion
      2. El jugador elige un número
      3. Se muestra la ficha completa con stats y habilidades
      4. Confirma o vuelve a elegir
    """
    lista = listar_entidades(entidades)

    while True:
        try:
            eleccion = int(input(f"\n  {titulo} (1-{len(lista)}): "))
            if not 1 <= eleccion <= len(lista):
                print(f"  Numero fuera de rango. Elige entre 1 y {len(lista)}.")
                continue
        except ValueError:
            print("  Introduce un numero valido.")
            continue

        candidato = lista[eleccion - 1]

        limpiar()
        mostrar_ficha(candidato)

        confirma = input("\n  ¿Confirmas esta eleccion? (s/n): ").strip().lower()
        if confirma == "s":
            print(f"\n  {candidato.get_nombre()} seleccionado!\n")
            return candidato
        else:
            print("\n  Volviendo al listado...\n")
            listar_entidades(entidades)

# ______________________________________________

#  Combate bonito ,usa simular_combate de pokemon.py
# ______________________________________________

def combate_con_ui(e1: Entidad, e2: Entidad):
    """
    Visual para simular_combate().
    """
    limpiar()
    print(SEP)
    print("         COMBATE POR ZTERIA")
    print(SEP)
    print(f"  {e1.get_nombre()}")
    print(f"            VS")
    print(f"  {e2.get_nombre()}")
    print(SEP)
    input("\n  Pulsa ENTER para comenzar...")

    # Llamar a la lógica pura del combate
    resultado = simular_combate(e1, e2)

    # Mostrar el combate turno a turno con delays
    print("\n" + SEP2)
    print("  INICIANDO COMBATE")
    print(SEP2)
    
    turno_actual = 0
    for entrada in resultado["log"]:
        if entrada["turno"] != turno_actual:
            turno_actual = entrada["turno"]
            print(f"\n{SEP2}")
            print(f"  Turno {turno_actual}")
            print(SEP2)

        atacante = entrada["atacante"]
        defensor = entrada["defensor"]
        habilidad = entrada["habilidad"]
        
        if entrada["esquivado"]:
            print(f"  >> {atacante} usa [{habilidad}]... ¡{defensor} lo esquiva!")
        else:
            daño = entrada["daño"]
            hp = entrada["hp_restante"]
            print(f"  >> {atacante} usa [{habilidad}]")
            print(f"     Causa {daño} de daño | {defensor} HP: {hp}")
            
            if hp <= 0:
                print(f"\n  *** {defensor} ha caido en combate ***\n")

        time.sleep(0.8)

    # Resultado final
    print(SEP)
    print(f"  FIN DEL COMBATE — Turno {resultado['turnos_totales']}")
    print(SEP)
    print(f"  {resultado['ganador']} aplasta a {resultado['perdedor']} sin piedad!")
    print(SEP)

    return resultado

# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    habilidades = cargar_habilidades()
    entidades   = cargar_entidades(habilidades=habilidades)

    print(SEP)
    print("    BIENVENIDO AL COLISEO MEDIEVAL")
    print(SEP)

    combatiente1 = seleccionar_entidad(entidades, "Jugador 1 — elige tu entidad")
    combatiente2 = seleccionar_entidad(entidades, "Jugador 2 — elige tu entidad")

    combate_con_ui(combatiente1, combatiente2)
