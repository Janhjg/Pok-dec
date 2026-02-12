import os
from data.Persistencia_datos import read, update, write
from pokemon import _fila_a_entidad

PATH_JSON = "data/entidades.json"

def cargar_todo_al_inicio(entidades_dict, habilidades_dict):
    # Carga las entidades desde la lista 'entidades' del JSON.
    if os.path.exists(PATH_JSON):
        try:
            contenido = read(PATH_JSON)
            lista_entidades = contenido.get("entidades", [])
            
            for info in lista_entidades:
                entidades_dict[info["id"]] = _fila_a_entidad(info, habilidades_dict)
            
            print(f"-> Persistencia: {len(lista_entidades)} entidades cargadas desde JSON.")
        except Exception as e:
            print(f"Error al cargar persistencia: {e}")

def guardar_nueva_entidad(entidad_objeto, diccionario_entidad):
    # Añade la nueva entidad a la lista del archivo JSON.
    try:
        contenido = read(PATH_JSON)
        
        if "entidades" not in contenido:
            contenido["entidades"] = []

        contenido["entidades"] = [e for e in contenido["entidades"] if e["id"] != entidad_objeto.id]
        
        contenido["entidades"].append(diccionario_entidad)
        
        write(PATH_JSON, contenido)
        
    except Exception as e:
        print(f"Error al guardar en JSON: {e}")
        
def guardar_nueva_entidad(entidad_objeto, diccionario_entidad, entidades_dict):
    """
    Ahora recibe 3 cosas: 
    1. El objeto (para sacar el ID)
    2. El diccionario (para guardarlo en el JSON)
    3. El diccionario global (para actualizar la RAM)
    """
    try:
        # 1. Actualizar la memoria RAM de la API
        entidades_dict[entidad_objeto.id] = entidad_objeto
        
        # 2. Leer el archivo físico
        contenido = read(PATH_JSON)
        
        if "entidades" not in contenido:
            contenido["entidades"] = []
            
        # 3. Evitar duplicados en el JSON
        contenido["entidades"] = [e for e in contenido["entidades"] if e["id"] != entidad_objeto.id]
        
        # 4. Añadir y escribir
        contenido["entidades"].append(diccionario_entidad)
        write(PATH_JSON, contenido)
        
    except Exception as e:
        print(f"Error en gestor_datos: {e}")        