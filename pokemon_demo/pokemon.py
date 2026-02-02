import random

class Movimiento:
    def __init__(self, nombre, tipo, potencia):
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia


class Pokemon:
    # Tipos válidos de Pokémon
    TIPOS_VALIDOS = ['agua', 'fuego', 'tierra', 'aire']
    
    __nombre = None
    
    def __init__(self, nombre, tipo, hp, ataque, defensa, movimientos):
        # Validar que el tipo sea válido
        if tipo.lower() not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Debe ser uno de: {', '.join(self.TIPOS_VALIDOS)}")
        
        self.__nombre = nombre
        self.tipo = tipo.lower()
        self.hp = hp
        self.hp_max = hp
        self.ataque = ataque
        self.defensa = defensa
        self.movimientos = []
        
        # Añadir movimientos validando el tipo
        for movimiento in movimientos:
            self.aprender_movimiento(movimiento)
        
    def get_nombre(self):
        return self.__nombre
    
    def set_nombre(self, nombre):
        self.__nombre = f"{nombre} (editado)"

    def aprender_movimiento(self, movimiento):
        """Añade un movimiento solo si coincide con el tipo del Pokémon"""
        if movimiento.tipo.lower() != self.tipo:
            print(f"  {self.__nombre} no puede aprender {movimiento.nombre}")
            print(f"   (Es tipo {self.tipo}, pero {movimiento.nombre} es tipo {movimiento.tipo})")
            return False
        
        self.movimientos.append(movimiento)
        return True
    
    def atacar(self, enemigo):
        # Verificar que tenga movimientos
        if not self.movimientos:
            print(f"  {self.__nombre} no tiene movimientos disponibles!")
            return
        
        movimiento = random.choice(self.movimientos)
        
        # Tu fórmula: daño = ((ataque + potencia) - defensa_enemigo / 2)
        daño = max(1, (self.ataque + movimiento.potencia) - (enemigo.defensa // 2))
        
        enemigo.hp -= daño
        if enemigo.hp < 0: enemigo.hp = 0
        
        print(f" {self.__nombre} usa {movimiento.nombre} contra {enemigo.get_nombre()}!")
        print(f"   Causa {daño} de daño!")
        
        if enemigo.hp <= 0:
            print(f" {enemigo.get_nombre()} ha sido debilitado!")
    
    def esta_vivo(self):
        return self.hp > 0
    
    def __str__(self):
        movs = ", ".join([m.nombre for m in self.movimientos]) if self.movimientos else "ninguno"
        return f"{self.__nombre} ({self.tipo.capitalize()}) - HP: {self.hp}/{self.hp_max} | Movimientos: {movs}"


# --- Creación de Movimientos ---
# Movimientos de FUEGO
lanzallamas = Movimiento("Lanzallamas", "fuego", 90)
ascuas = Movimiento("Ascuas", "fuego", 40)
expropiese = Movimiento("Expropiese Relámpago", "fuego", 50)

# Movimientos de AGUA
hidrobomba = Movimiento("Hidrobomba", "agua", 110)
pistola_agua = Movimiento("Pistola Agua", "agua", 40)
bigote_de_hierro = Movimiento("Latigazo de Bigote", "agua", 25)

# Movimientos de TIERRA
terremoto = Movimiento("Terremoto", "tierra", 100)
excavar = Movimiento("Excavar", "tierra", 80)
peace_peace = Movimiento("Rolita epica", "tierra", 35)

# Movimientos de AIRE
vendaval = Movimiento("Vendaval", "aire", 110)
tornado = Movimiento("Tornado", "aire", 40)
peluquin_volador = Movimiento("Peluquín Volador", "aire", 30)
lluvia_de_billetes = Movimiento("Lluvia de Billetes", "aire", 45)
twit = Movimiento("Twit basado", "aire", 25)