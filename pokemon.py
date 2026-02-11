import random
from data.filtro_datos import *

# _________________________

#  Clase Habilidad
# _________________________

class Habilidad:
    def __init__(self, nombre, tipo, potencia, coste_mana=0, descripcion=""):
        self._nombre     = nombre
        self.tipo        = tipo.lower()
        self.potencia    = potencia
        self.coste_mana  = coste_mana
        self.descripcion = descripcion

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    def __str__(self):
        return f"[{self.tipo.upper()}] {self._nombre} | Potencia: {self.potencia} | Mana: {self.coste_mana}"


# _________________________

#  Clase Entidad
# _________________________

class Entidad:
    TIPOS_VALIDOS = ["hierro", "arcano", "bestia", "sombra"]

    def __init__(self, id, nombre, tipo, hp, ataque, defensa,
                 velocidad, evasion, mana, habilidades, descripcion=""):
        if tipo.lower() not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo invalido '{tipo}'. Validos: {', '.join(self.TIPOS_VALIDOS)}")

        self.id          = id
        self.__nombre    = nombre
        self.tipo        = tipo.lower()
        self.hp          = hp
        self.hp_max      = hp
        self.ataque      = ataque
        self.defensa     = defensa
        self.velocidad   = velocidad          
        self.evasion     = evasion            
        self.mana        = mana               
        self.mana_max    = mana               
        self.descripcion = descripcion
        self.habilidades = []

        for habilidad in habilidades:
            self._aprender_habilidad(habilidad)

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = f"{nombre} (alterado)"

    def _aprender_habilidad(self, habilidad):
        if habilidad.tipo != self.tipo:
            print(f"  x {self.__nombre} no puede usar '{habilidad.nombre}' "
                  f"(tipo {habilidad.tipo} != {self.tipo})")
            return False
        self.habilidades.append(habilidad)
        return True

    def _habilidades_disponibles(self):
        """Devuelve solo las habilidades que la entidad puede costear con su mana actual."""
        return [h for h in self.habilidades if h.coste_mana <= self.mana]

    def atacar(self, enemigo):
        disponibles = self._habilidades_disponibles()

        # Si no puede costear ninguna, usa la más barata gastando lo que tenga
        if not disponibles:
            habilidad = min(self.habilidades, key=lambda h: h.coste_mana)
            print(f"  !! {self.__nombre} no tiene mana suficiente, usa {habilidad.nombre} a duras penas!")
        else:
            habilidad = random.choice(disponibles)

        # Consumir mana
        self.mana = max(0, self.mana - habilidad.coste_mana)

        # Comprobar evasión del enemigo
        if random.randint(1, 100) <= enemigo.evasion:
            print(f"  >> {self.__nombre} usa [{habilidad.nombre}]... "
                  f"¡pero {enemigo.get_nombre()} lo esquiva!")
            return

        # Calcular daño
        daño = max(1, ((self.ataque + habilidad.potencia) - (enemigo.defensa // 2)) // 5)
        enemigo.hp = max(0, enemigo.hp - daño)

        print(f"  >> {self.__nombre} usa [{habilidad.nombre}] "
              f"(mana restante: {self.mana}/{self.mana_max})")
        print(f"     Causa {daño} de daño | "
              f"{enemigo.get_nombre()} HP: {enemigo.hp}/{enemigo.hp_max}")

        if enemigo.hp <= 0:
            print(f"\n  *** {enemigo.get_nombre()} ha caido en combate ***\n")

    def esta_vivo(self):
        return self.hp > 0

    def __str__(self):
        habs = ", ".join(h.nombre for h in self.habilidades) if self.habilidades else "ninguna"
        return (
            f"{self.__nombre} [{self.tipo.upper()}]\n"
            f"  HP: {self.hp}/{self.hp_max} | ATQ: {self.ataque} | DEF: {self.defensa}\n"
            f"  VEL: {self.velocidad} | EVA: {self.evasion}% | MANA: {self.mana}/{self.mana_max}\n"
            f"  Habilidades: {habs}"
        )


# ─────────────────────────────────────────────
#  Subclases por tipo
# ─────────────────────────────────────────────
class EntidadHierro(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion=""):
        super().__init__(id, nombre, "hierro", hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion)

class EntidadArcano(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion=""):
        super().__init__(id, nombre, "arcano", hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion)

class EntidadBestia(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion=""):
        super().__init__(id, nombre, "bestia", hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion)

class EntidadSombra(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion=""):
        super().__init__(id, nombre, "sombra", hp, ataque, defensa, velocidad, evasion, mana, habilidades, descripcion)


# __________________________

#  Carga desde pandas
# __________________________

_SUBCLASES = {
    "hierro": EntidadHierro,
    "arcano": EntidadArcano,
    "bestia": EntidadBestia,
    "sombra": EntidadSombra,
}


def cargar_habilidades() -> dict:

    tabla = cargar_df_habilidades()
    
    return {
        fila["nombre"]: Habilidad(
            nombre      = fila["nombre"],
            tipo        = fila["tipo"],
            potencia    = fila["potencia"],
            coste_mana  = fila.get("coste_mana", 0),
            descripcion = fila.get("descripcion", "")
        )
        for _, fila in tabla.iterrows()
    }


def _fila_a_entidad(fila: dict, habilidades: dict) -> Entidad:
    """Convierte una fila del DataFrame (ya como dict) en un objeto Entidad"""

    # Resolver los nombres de habilidades a objetos Habilidad reales
    habs = []
    for nombre_hab in fila["habilidades"]:
        if nombre_hab in habilidades:
            habs.append(habilidades[nombre_hab])
        else:
            print(f"  Habilidad '{nombre_hab}' no encontrada para {fila['nombre']}")

    # Elegir la subclase correcta segun el tipo
    
    Clase = _SUBCLASES.get(fila["tipo"].lower(), Entidad)

    parametros = dict(
        id          = fila["id"],
        nombre      = fila["nombre"],
        hp          = fila["hp"],
        ataque      = fila["ataque"],
        defensa     = fila["defensa"],
        velocidad   = fila["velocidad"],
        evasion     = fila["evasion"],
        mana        = fila["mana"],
        habilidades = habs,
        descripcion = fila.get("descripcion", "")
    )

    # La clase base Entidad necesita el tipo explicitamente.
    # Las subclases (EntidadHierro etc.) ya lo tienen fijos
    if Clase is Entidad:
        return Entidad(tipo=fila["tipo"], **parametros)
    return Clase(**parametros)


def cargar_entidades(habilidades: dict = None) -> dict:

    if habilidades is None:
        habilidades = cargar_habilidades()

    tabla = cargar_df_entidades()  
    return {
        fila["id"]: _fila_a_entidad(fila.to_dict(), habilidades)
        for _, fila in tabla.iterrows()
    }

def cargar_entidades_filtradas(tabla_filtrada, habilidades: dict = None) -> dict:
    """
    Igual que cargar_entidades() pero recibe una tabla ya filtrada
    (resultado de filtrar_por_tipo, filtrar_por_estadistica, etc.)
    """
    if habilidades is None:
        habilidades = cargar_habilidades()
    return {
        fila["id"]: _fila_a_entidad(fila.to_dict(), habilidades)
        for _, fila in tabla_filtrada.iterrows()
    }