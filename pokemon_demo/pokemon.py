import random


class Pokemon:
    def __init__(self, nombre, tipo, hp, ataque, defensa):
        self.nombre = nombre
        self.tipo = tipo
        self.hp = hp
        self.hp_max = hp
        self.ataque = ataque
        self.defensa = defensa
    
    def atacar(self, enemigo):
        """Ataca a otro Pokemon"""
        daño = max(1, self.ataque - enemigo.defensa // 2)
        enemigo.hp -= daño
        print(f"{self.nombre} ataca a {enemigo.nombre} causando {daño} de daño!")
        
        if enemigo.hp <= 0:
            enemigo.hp = 0
            print(f"{enemigo.nombre} ha sido debilitado!")
    
    def esta_vivo(self):
        """Verifica si el Pokemon puede seguir luchando"""
        return self.hp > 0
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - HP: {self.hp}/{self.hp_max}"
