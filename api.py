from fastapi import FastAPI
from pydantic import BaseModel
from pokemon import *
from main import *
from data.filtro_datos import *
from data.Persistencia_datos import *
import gestor_datos

app = FastAPI(
    title="Zteria Battle API",
    description="API para gestionar entidades y combates medievales",
    version="1.0.0"
)

# ____________________________________________

#  Cargar datos al iniciar
# ____________________________________________
habilidades_dict = cargar_habilidades()
entidades_dict = cargar_entidades(habilidades_dict)
datos_guardados = read("data/entidades.json")
gestor_datos.cargar_todo_al_inicio(entidades_dict, habilidades_dict)

class NuevaEntidad(BaseModel):
    id: str
    nombre: str
    tipo: str
    descripcion: str
    hp: int
    ataque: int
    defensa: int
    velocidad: int
    evasion: int
    mana: int

# ____________________________________________

#  Helpers
# ____________________________________________
def entidad_to_dict(e):
    """Convierte Entidad a diccionario para respuesta."""
    return {
        "id": e.id,
        "nombre": e.get_nombre(),
        "tipo": e.tipo,
        "descripcion": e.descripcion,
        "stats": {
            "hp": e.hp_max,
            "ataque": e.ataque,
            "defensa": e.defensa,
            "velocidad": e.velocidad,
            "evasion": e.evasion,
            "mana": e.mana_max
        },
        "habilidades": [
            {
                "nombre": h.nombre,
                "tipo": h.tipo,
                "potencia": h.potencia,
                "coste_mana": h.coste_mana,
                "descripcion": h.descripcion
            }
            for h in e.habilidades
        ]
    }


# ─────────────────────────────────────────────
#  ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a Zteria Battle API",
        "version": "1.0.0",
        "documentacion": "/docs",
        "endpoints": {
            "entidades": "/entidades",
            "habilidades": "/habilidades",
            "filtros": "/filtrar/tipo/{tipo} | /filtrar/estadistica/{stat}/{min}",
            "busqueda": "/buscar/{termino}",
            "combate": "POST /combate"
        }
    }


@app.get("/entidades")
def listar_entidades():
    """Lista todas las entidades con información básica."""
    return [
        {
            "id": e.id,
            "nombre": e.get_nombre(),
            "tipo": e.tipo,
            "descripcion": e.descripcion
        }
        for e in entidades_dict.values()
    ]


@app.get("/entidades/{id}")
def obtener_entidad(id: str):
    """Obtiene información completa de una entidad por su ID."""
    if id not in entidades_dict:
        return {"error": f"Entidad '{id}' no encontrada"}
    
    return entidad_to_dict(entidades_dict[id])


@app.get("/habilidades")
def listar_habilidades():
    """Lista todas las habilidades disponibles."""
    return [
        {
            "nombre": h.nombre,
            "tipo": h.tipo,
            "potencia": h.potencia,
            "coste_mana": h.coste_mana,
            "descripcion": h.descripcion
        }
        for h in habilidades_dict.values()
    ]


@app.get("/filtrar/tipo/{tipo}")
def filtrar_tipo(tipo: str):
    """Filtra entidades por tipo (hierro, arcano, bestia, sombra)."""
    df = filtrar_por_tipo(tipo)
    if df.empty:
        return {"error": f"No hay entidades del tipo '{tipo}'"}
    
    ids = df['id'].tolist()
    return [
        {
            "id": e.id,
            "nombre": e.get_nombre(),
            "tipo": e.tipo,
            "descripcion": e.descripcion
        }
        for eid in ids
        for e in [entidades_dict[eid]]
    ]


@app.get("/filtrar/estadistica/{stat}/{minimo}")
def filtrar_estadistica(stat: str, minimo: int):
    """Filtra entidades por estadística mínima."""
    stats_validas = ['hp', 'ataque', 'defensa', 'velocidad', 'evasion', 'mana']
    if stat not in stats_validas:
        return {"error": f"Estadística '{stat}' no válida. Opciones: {stats_validas}"}
    
    df = filtrar_por_estadistica(stat, minimo)
    if df.empty:
        return {"error": f"No hay entidades con {stat} >= {minimo}"}
    
    ids = df['id'].tolist()
    return [
        {
            "id": e.id,
            "nombre": e.get_nombre(),
            "tipo": e.tipo,
            "descripcion": e.descripcion
        }
        for eid in ids
        for e in [entidades_dict[eid]]
    ]


@app.get("/buscar/{termino}")
def buscar(termino: str):
    """Busca entidades por nombre (búsqueda parcial)."""
    df = buscar_entidades(termino)
    if df.empty:
        return {"error": f"No se encontraron entidades con '{termino}' en el nombre"}
    
    ids = df['id'].tolist()
    return [
        {
            "id": e.id,
            "nombre": e.get_nombre(),
            "tipo": e.tipo,
            "descripcion": e.descripcion
        }
        for eid in ids
        for e in [entidades_dict[eid]]
    ]


@app.post("/combate")
def iniciar_combate(data: dict):
    """
    Simula un combate entre dos entidades.
    Body JSON: {"entidad1_id": "e001", "entidad2_id": "e002"}
    """
    entidad1_id = data.get("entidad1_id")
    entidad2_id = data.get("entidad2_id")
    
    if not entidad1_id or not entidad2_id:
        return {"error": "Se requieren 'entidad1_id' y 'entidad2_id'"}
    
    if entidad1_id not in entidades_dict:
        return {"error": f"Entidad '{entidad1_id}' no encontrada"}
    if entidad2_id not in entidades_dict:
        return {"error": f"Entidad '{entidad2_id}' no encontrada"}
    
    e1 = entidades_dict[entidad1_id]
    e2 = entidades_dict[entidad2_id]
    
    # Usa la función compartida de main.py
    resultado = simular_combate(e1, e2)
    
    return {
        "combatiente1": entidad_to_dict(entidades_dict[entidad1_id]),
        "combatiente2": entidad_to_dict(entidades_dict[entidad2_id]),
        "turnos_totales": resultado["turnos_totales"],
        "log": resultado["log"],
        "ganador": resultado["ganador"],
        "ganador_id": resultado["ganador_id"],
        "perdedor": resultado["perdedor"],
        "perdedor_id": resultado["perdedor_id"]
    }


@app.post("/entidades")
def crear_entidad(datos: NuevaEntidad):
    # 1. Validar si el ID ya existe
    if datos.id in entidades_dict:
        return {"error": f"El ID {datos.id} ya existe."}

    # 2. Filtrar habilidades
    habs_del_mismo_tipo = [
        h for h in habilidades_dict.values() 
        if h.tipo == datos.tipo.lower()
    ]
    
    if not habs_del_mismo_tipo:
        return {"error": f"No hay habilidades cargadas para el tipo '{datos.tipo}'"}

    # 3. Selección aleatoria
    cantidad = min(4, len(habs_del_mismo_tipo))
    habilidades_seleccionadas = random.sample(habs_del_mismo_tipo, k=cantidad)

    from pokemon import _SUBCLASES, Entidad
    usar_clase = _SUBCLASES.get(datos.tipo.lower(), Entidad)

    try:
        nueva_e = usar_clase(
            id=datos.id,
            nombre=datos.nombre,
            hp=datos.hp,
            ataque=datos.ataque,
            defensa=datos.defensa,
            velocidad=datos.velocidad,
            evasion=datos.evasion,
            mana=datos.mana,
            habilidades=habilidades_seleccionadas,
            descripcion=datos.descripcion
        )
        
        datos_dict = entidad_to_dict(nueva_e)
        gestor_datos.guardar_nueva_entidad(nueva_e, datos_dict, entidades_dict)
        
        return {
            "mensaje": f"Entidad '{nueva_e.get_nombre()}' creada y guardada.",
            "habilidades": [h.nombre for h in habilidades_seleccionadas]
        }

    except Exception as e:
        return {"error": f"Error al crear la entidad: {str(e)}"}