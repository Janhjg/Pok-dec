from pokemon import *
import random
import time
from data.filtro_datos import *

# ─────────────────────────────────────────────
#  Cargar todo
# ─────────────────────────────────────────────
habilidades = cargar_habilidades()
entidades   = cargar_entidades(habilidades=habilidades)

# Ver tabla de todas las entidades
mostrar_entidades()

# Top 5 entidades por ataque
ranking_entidades(por="ataque", top=5)
