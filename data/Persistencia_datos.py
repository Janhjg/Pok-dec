import json
import os

def read(file_path):
    """Lee y retorna el contenido del archivo JSON"""
    with open(file_path, 'r') as archivo:
        return json.load(archivo)

def write(file_path, datos):
    """Escribe datos en el archivo JSON"""
    with open(file_path, 'w') as archivo:
        json.dump(datos, archivo, indent=2)

def update(file_path, clave, valor):
    """Actualiza o añade un valor"""
    datos = read(file_path)
    datos[clave] = valor
    write(file_path, datos)

def clear(file_path):
    """Limpia archivo JSON"""
    write(file_path, {})

def delete(file_path):
    """Elimina el archivo JSON"""
    os.remove(file_path)


