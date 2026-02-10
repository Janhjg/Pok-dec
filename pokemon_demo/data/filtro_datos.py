import pandas as pd
import json

RUTA_HABILIDADES = "data/habilidades_data.json"
RUTA_ENTIDADES   = "data/entidades.json"


# _____________________

#  CARGA DE DATAFRAMES
# _____________________

def cargar_df_habilidades() -> pd.DataFrame:
    """Devuelve un DataFrame con todas las habilidades."""
    with open(RUTA_HABILIDADES, encoding="utf-8") as f:
        datos = json.load(f)
    return pd.DataFrame(datos["habilidades"])


def cargar_df_entidades() -> pd.DataFrame:
    """
    Devuelve un DataFrame con todas las entidades.
    La columna 'habilidades' contiene la lista de nombres tal cual está en el JSON.
    """
    with open(RUTA_ENTIDADES, encoding="utf-8") as f:
        datos = json.load(f)
    return pd.DataFrame(datos["entidades"])


# ________________

#  EXPLORACIÓN
# ________________

def mostrar_entidades(df: pd.DataFrame = None):
    """Muestra la tabla de entidades sin la columna de habilidades (más limpio)."""
    if df is None:
        df = cargar_df_entidades()
    print("\n=== ENTIDADES ===")
    print(df.drop(columns=["habilidades", "descripcion"]).to_string(index=False))
    print()


def mostrar_habilidades(df: pd.DataFrame = None):
    """Muestra la tabla de habilidades."""
    if df is None:
        df = cargar_df_habilidades()
    print("\n=== HABILIDADES ===")
    print(df.drop(columns=["descripcion"]).to_string(index=False))
    print()


def ranking_entidades(df: pd.DataFrame = None, por="ataque", top=5):
    """Muestra el ranking de entidades por una estadística dada."""
    if df is None:
        df = cargar_df_entidades()
    print(f"\n=== TOP {top} por {por.upper()} ===")
    cols = ["nombre", "tipo", "hp", "ataque", "defensa"]
    print(df.sort_values(por, ascending=False)[cols].head(top).to_string(index=False))
    print()


# ─────────────────────────────────────────────
#  FILTROS PARA ELEGIR COMBATIENTES
# ─────────────────────────────────────────────

def filtrar_por_tipo(tipo: str, df: pd.DataFrame = None) -> pd.DataFrame:
    """Devuelve las entidades de un tipo concreto."""
    if df is None:
        df = cargar_df_entidades()
    resultado = df[df["tipo"].str.lower() == tipo.lower()]
    if resultado.empty:
        print(f"  No hay entidades del tipo '{tipo}'.")
    return resultado


def filtrar_por_estadistica(stat: str, minimo: int, df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Devuelve entidades cuya estadística (hp / ataque / defensa)
    supera el mínimo indicado.
    Ejemplo: filtrar_por_estadistica("ataque", 100)
    """
    if df is None:
        df = cargar_df_entidades()
    if stat not in ("hp", "ataque", "defensa"):
        raise ValueError("stat debe ser 'hp', 'ataque' o 'defensa'")
    resultado = df[df[stat] >= minimo]
    if resultado.empty:
        print(f"  Ninguna entidad con {stat} >= {minimo}.")
    return resultado


def elegir_combatiente(nombre: str, df: pd.DataFrame = None) -> dict | None:
    """
    Busca una entidad por nombre (insensible a mayúsculas) y
    devuelve su fila como diccionario, listo para instanciar.
    """
    if df is None:
        df = cargar_df_entidades()
    resultado = df[df["nombre"].str.lower() == nombre.lower()]
    if resultado.empty:
        print(f"  Entidad '{nombre}' no encontrada.")
        return None
    return resultado.iloc[0].to_dict()


def buscar_entidades(termino: str, df: pd.DataFrame = None) -> pd.DataFrame:
    """Búsqueda parcial por nombre (como un LIKE en SQL)."""
    if df is None:
        df = cargar_df_entidades()
    return df[df["nombre"].str.contains(termino, case=False)]
