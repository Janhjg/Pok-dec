import random
from data.filtro_datos import *


# ─────────────────────────────────────────────
#  Clase Habilidad
# ─────────────────────────────────────────────
class Habilidad:
    def __init__(self, nombre, tipo, potencia, descripcion=""):
        self._nombre     = nombre
        self.tipo        = tipo.lower()
        self.potencia    = potencia
        self.descripcion = descripcion

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    def __str__(self):
        return f"[{self.tipo.upper()}] {self._nombre} (Potencia: {self.potencia})"


# ─────────────────────────────────────────────
#  Clase Entidad
# ─────────────────────────────────────────────
class Entidad:
    TIPOS_VALIDOS = ["hierro", "arcano", "bestia", "sombra"]

    def __init__(self, id, nombre, tipo, hp, ataque, defensa, habilidades, descripcion=""):
        if tipo.lower() not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo invalido '{tipo}'. Validos: {', '.join(self.TIPOS_VALIDOS)}")

        self.id          = id
        self.__nombre    = nombre
        self.tipo        = tipo.lower()
        self.hp          = hp
        self.hp_max      = hp
        self.ataque      = ataque
        self.defensa     = defensa
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

    def atacar(self, enemigo):
        if not self.habilidades:
            print(f"  {self.__nombre} no tiene habilidades disponibles!")
            return
        habilidad = random.choice(self.habilidades)
        daño = max(1, (self.ataque + habilidad.potencia) - (enemigo.defensa // 2))
        enemigo.hp = max(0, enemigo.hp - daño)
        print(f"  >> {self.__nombre} usa [{habilidad.nombre}] sobre {enemigo.get_nombre()}!")
        print(f"     Causa {daño} de daño! ({enemigo.get_nombre()} HP: {enemigo.hp}/{enemigo.hp_max})")
        if enemigo.hp <= 0:
            print(f"\n  *** {enemigo.get_nombre()} ha caido en combate ***\n")

    def esta_vivo(self):
        return self.hp > 0

    def __str__(self):
        habs = ", ".join(h.nombre for h in self.habilidades) if self.habilidades else "ninguna"
        return (f"{self.__nombre} [{self.tipo.upper()}] "
                f"HP: {self.hp}/{self.hp_max} | ATQ: {self.ataque} | DEF: {self.defensa}\n"
                f"  Habilidades: {habs}")


# ─────────────────────────────────────────────
#  Subclases por tipo
# ─────────────────────────────────────────────
class EntidadHierro(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, habilidades, descripcion=""):
        super().__init__(id, nombre, "hierro", hp, ataque, defensa, habilidades, descripcion)

class EntidadArcano(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, habilidades, descripcion=""):
        super().__init__(id, nombre, "arcano", hp, ataque, defensa, habilidades, descripcion)

class EntidadBestia(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, habilidades, descripcion=""):
        super().__init__(id, nombre, "bestia", hp, ataque, defensa, habilidades, descripcion)

class EntidadSombra(Entidad):
    def __init__(self, id, nombre, hp, ataque, defensa, habilidades, descripcion=""):
        super().__init__(id, nombre, "sombra", hp, ataque, defensa, habilidades, descripcion)


# ─────────────────────────────────────────────
#  Carga desde pandas (via datos.py)
# ─────────────────────────────────────────────
_SUBCLASES = {
    "hierro": EntidadHierro,
    "arcano": EntidadArcano,
    "bestia": EntidadBestia,
    "sombra": EntidadSombra,
}


def cargar_habilidades() -> dict:
    """Devuelve {nombre: Habilidad} usando el DataFrame de pandas."""
    df = cargar_df_habilidades()
    return {
        row["nombre"]: Habilidad(
            nombre      = row["nombre"],
            tipo        = row["tipo"],
            potencia    = row["potencia"],
            descripcion = row.get("descripcion", "")
        )
        for _, row in df.iterrows()
    }


def _fila_a_entidad(fila: dict, habilidades: dict) -> Entidad:
    """Convierte una fila del DataFrame (o dict) en un objeto Entidad."""
    habs = []
    for nombre_hab in fila["habilidades"]:
        if nombre_hab in habilidades:
            habs.append(habilidades[nombre_hab])
        else:
            print(f"  ⚠ Habilidad '{nombre_hab}' no encontrada para {fila['nombre']}")

    Clase = _SUBCLASES.get(fila["tipo"].lower(), Entidad)

    if Clase is Entidad:
        return Entidad(
            id=fila["id"], nombre=fila["nombre"], tipo=fila["tipo"],
            hp=fila["hp"], ataque=fila["ataque"], defensa=fila["defensa"],
            habilidades=habs, descripcion=fila.get("descripcion", "")
        )
    return Clase(
        id=fila["id"], nombre=fila["nombre"],
        hp=fila["hp"], ataque=fila["ataque"], defensa=fila["defensa"],
        habilidades=habs, descripcion=fila.get("descripcion", "")
    )


def cargar_entidades(habilidades: dict = None) -> dict:
    """Devuelve {id: Entidad} cargando el DataFrame de pandas."""
    if habilidades is None:
        habilidades = cargar_habilidades()

    df = cargar_df_entidades()
    return {
        row["id"]: _fila_a_entidad(row.to_dict(), habilidades)
        for _, row in df.iterrows()
    }


def cargar_entidades_filtradas(df_filtrado, habilidades: dict = None) -> dict:
    """
    Igual que cargar_entidades() pero recibe un DataFrame ya filtrado
    (resultado de filtrar_por_tipo, filtrar_por_estadistica, etc.)
    Perfecto para elegir combatientes con filtros previos.
    """
    if habilidades is None:
        habilidades = cargar_habilidades()
    return {
        row["id"]: _fila_a_entidad(row.to_dict(), habilidades)
        for _, row in df_filtrado.iterrows()
    }