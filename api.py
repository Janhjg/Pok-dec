from fastapi import FastAPI
from pydantic import BaseModel
import random
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

# El gestor ahora se encarga de inyectar los datos del JSON en entidades_dict
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
    """Convierte Entidad a diccionario para respuesta de la API."""
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
    """Filtra entidades por tipo."""
    df = filtrar_por_tipo(tipo)
    if df.empty:
        return {"error": f"No hay entidades del tipo '{tipo}'"}
    
    ids = df['id'].tolist()
    # Solo devolvemos los que están actualmente cargados en memoria
    return [
        {
            "id": entidades_dict[eid].id,
            "nombre": entidades_dict[eid].get_nombre(),
            "tipo": entidades_dict[eid].tipo,
            "descripcion": entidades_dict[eid].descripcion
        }
        for eid in ids if eid in entidades_dict
    ]

@app.post("/combate")
def iniciar_combate(data: dict):
    """Simula un combate entre dos entidades."""
    entidad1_id = data.get("entidad1_id")
    entidad2_id = data.get("entidad2_id")
    
    if entidad1_id not in entidades_dict or entidad2_id not in entidades_dict:
        return {"error": "Una o ambas entidades no existen"}
    
    e1 = entidades_dict[entidad1_id]
    e2 = entidades_dict[entidad2_id]
    
    resultado = simular_combate(e1, e2)
    return resultado

@app.post("/entidades")
def crear_entidad(datos: NuevaEntidad):
    # 1. Validar duplicados
    if datos.id in entidades_dict:
        return {"error": f"El ID {datos.id} ya existe."}

    # 2. Filtrar habilidades por tipo
    habs_del_mismo_tipo = [
        h for h in habilidades_dict.values() 
        if h.tipo == datos.tipo.lower()
    ]
    
    if not habs_del_mismo_tipo:
        return {"error": f"No hay habilidades para el tipo '{datos.tipo}'"}

    # 3. Selección aleatoria
    cantidad = min(4, len(habs_del_mismo_tipo))
    habilidades_seleccionadas = random.sample(habs_del_mismo_tipo, k=cantidad)

    from pokemon import _SUBCLASES, Entidad
    usar_clase = _SUBCLASES.get(datos.tipo.lower(), Entidad)

    try:
        # 4. Crear instancia del objeto
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
        
        # 5. Diccionario específico para persistencia (Formato JSON)
        # Importante: habilidades se guardan como lista de nombres (strings)
        datos_json = {
            "id": nueva_e.id,
            "nombre": nueva_e.get_nombre(),
            "tipo": nueva_e.tipo,
            "hp": nueva_e.hp_max,
            "ataque": nueva_e.ataque,
            "defensa": nueva_e.defensa,
            "velocidad": nueva_e.velocidad,
            "evasion": nueva_e.evasion,
            "mana": nueva_e.mana_max,
            "habilidades": [h.nombre for h in nueva_e.habilidades],
            "descripcion": nueva_e.descripcion
        }
        
        # 6. Guardar en RAM y en JSON mediante el gestor
        gestor_datos.guardar_nueva_entidad(nueva_e, datos_json, entidades_dict)
        
        return {
            "mensaje": f"Entidad '{nueva_e.get_nombre()}' creada y guardada.",
            "habilidades": [h.nombre for h in habilidades_seleccionadas]
        }

    except Exception as e:
        return {"error": f"Error al crear la entidad: {str(e)}"}