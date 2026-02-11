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
# ─────────────────────────────────────────────
#  Combate
# ─────────────────────────────────────────────
def combate(e1: Entidad, e2: Entidad):
    # Reiniciar stats
    e1.hp   = e1.hp_max
    e2.hp   = e2.hp_max
    e1.mana = e1.mana_max
    e2.mana = e2.mana_max

    limpiar()
    print(SEP)
    print("         BATALLA POR ZTERIA")
    print(SEP)
    print(f"  {e1.get_nombre()}")
    print(f"            VS")
    print(f"  {e2.get_nombre()}")
    print(SEP)

    # La velocidad determina quién ataca primero cada turno
    # Si hay empate, orden aleatorio
    turno = 1
    combate_log = []

    while e1.esta_vivo() and e2.esta_vivo():
        print(f"\n{SEP2}")
        print(f"  Turno {turno}")
        print(f"  {e1.get_nombre()}: HP {e1.hp}/{e1.hp_max} | MANA {e1.mana}/{e1.mana_max}")
        print(f"  {e2.get_nombre()}: HP {e2.hp}/{e2.hp_max} | MANA {e2.mana}/{e2.mana_max}")
        print(SEP2)

        # Ordenar por velocidad (mayor velocidad ataca primero)
        if e1.velocidad > e2.velocidad:
            orden = [e1, e2]
        elif e2.velocidad > e1.velocidad:
            orden = [e2, e1]
        else:
            orden = random.sample([e1, e2], 2)   # empate → aleatorio

        primero = orden[0]
        print(f"  {primero.get_nombre()} ataca primero (VEL {primero.velocidad})\n")

        for atacante in orden:
            defensor = e1 if atacante == e2 else e2
            if atacante.esta_vivo():
                atacante.atacar(defensor)
                combate_log.append({
                    "turno":       turno,
                    "atacante":    atacante.get_nombre(),
                    "defensor":    defensor.get_nombre(),
                    "hp_restante": defensor.hp,
                })
                if not defensor.esta_vivo():
                    break

        time.sleep(1)
        turno += 1

    ganador  = e1 if e1.esta_vivo() else e2
    perdedor = e2 if e1.esta_vivo() else e1

    print(SEP)
    print(f"  FIN DEL COMBATE — Turno {turno - 1}")
    print(SEP)
    mensaje = f"{ganador.get_nombre()} aplasta a {perdedor.get_nombre()} sin piedad!"
    print(f"  {mensaje}")
    print(SEP)

    return {"combate": combate_log, "ganador": ganador.get_nombre(), "mensaje": mensaje}
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

    input("\n  Pulsa ENTER para comenzar el combate...")
    combate(combatiente1, combatiente2)