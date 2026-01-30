import random

class Movimiento:
    def __init__(self, nombre, tipo, potencia):
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia

class Pokemon:
    __nombre = None
    
    def __init__(self, nombre, tipo, hp, ataque, defensa, movimientos):
        self.__nombre = nombre
        self.tipo = tipo
        self.hp = hp
        self.hp_max = hp
        self.ataque = ataque
        self.defensa = defensa
        self.movimientos = movimientos
        
    def get_nombre(self):
        return self.__nombre
    
    def set_nombre(self,nombre):
        self.__nombre = f"{nombre} (editado)"

    def aprender_movimiento(self, movimiento):
        if movimiento.tipo() != self.tipo:
            print(f" {self.__nombre} no puede aprender {movimiento.nombre}")
            print(f"   (Es tipo {self.tipo}, pero {movimiento.nombre} es tipo {movimiento.tipo})")
            return False
        
        self.movimientos.append(movimiento)
    
    def atacar(self, enemigo):
        movimiento = random.choice(self.movimientos)
        
        # Tu fórmula: daño = ((ataque + potencia) - defensa_enemigo / 2)
        daño = max(1, (self.ataque + movimiento.potencia) - (enemigo.defensa // 2))
        
        enemigo.hp -= daño
        if enemigo.hp < 0: enemigo.hp = 0
        
        print(f" {self.__nombre} usa {movimiento.nombre} contra {enemigo.__nombre}!")
        print(f"   ¡Causa {daño} de daño!")
        
        if enemigo.hp <= 0:
            print(f" {enemigo.__nombre} ha sido debilitado!")
    
    def esta_vivo(self):
        return self.hp > 0
    
    def __str__(self):
        return f"{self.__nombre} ({self.tipo}) - HP: {self.hp}/{self.hp_max}"

# --- Creación de Movimientos ---
expropiese = Movimiento("Expropiese Relámpago", "Siniestro", 50)
bigote_de_hierro = Movimiento("Latigazo de Bigote", "Físico", 25)
peace_peace = Movimiento("Rolita epica", "Psíquico", 35)

peluquin_volador = Movimiento("Peluquín Volador", "Normal", 30)
lluvia_de_billetes = Movimiento("Lluvia de Billetes", "Económico", 45)
twit = Movimiento("Twit basado", "Meme", 25)