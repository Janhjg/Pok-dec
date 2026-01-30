import pytest
from pokemon_demo.pokemon import *

class TestMovimiento:
    
    def test_movimiento_creacion_correcta(self):
        mov = Movimiento("Impactrueno", "Eléctrico", 40)
        assert mov.nombre == "Impactrueno"
        assert mov.tipo == "Eléctrico"
        assert mov.potencia == 40
    
    def test_movimiento_atributos_accesibles(self):
        movimiento = Movimiento("Ataque Rápido", "Normal", 30)
        assert movimiento.nombre == "Ataque Rápido"
        assert movimiento.tipo == "Normal"
        assert movimiento.potencia == 30

class test_pokemon_iniciar:
    
    def test_pokemon_creacion_correcta(self):
        movimiento = Movimiento("Pistola Agua", "Agua", 40)
        pokemon = Pokemon("Squirtle", "Agua", 90, 48, 65, [movimiento])
        assert pokemon.nombre == "Squirtle"
        assert pokemon.tipo == "Agua"
        assert pokemon.hp == 90
        assert pokemon.ataque == 48
        assert pokemon.defensa == 65
        assert len(pokemon.movimientos) == 1
    
    def test_pokemon_hp_max_igual_hp_inicial(self):
        movimiento = Movimiento("Ataque", "Normal", 30)
        pokemon = Pokemon("Pikachu", "Eléctrico", 100, 50, 40, [movimiento])
        assert pokemon.hp == pokemon.hp_max
        assert pokemon.hp_max == 100
    
class TestPokemonEstaVivo:
    
    def test_pokemon_esta_vivo_con_hp_positivo(self):
        movimiento = Movimiento("Ataque", "Normal", 30)
        pokemon = Pokemon("Pikachu", "Eléctrico", 100, 50, 40, [movimiento])
        assert pokemon.esta_vivo() == True
        
        pokemon.hp = 50
        assert pokemon.esta_vivo() == True
        
        pokemon.hp = 1
        assert pokemon.esta_vivo() == True
    
    def test_pokemon_esta_vivo_con_hp_cero(self):
        movimiento = Movimiento("Ataque", "Normal", 30)
        pokemon = Pokemon("Pikachu", "Eléctrico", 100, 50, 40, [movimiento])
        pokemon.hp = 0
        assert pokemon.esta_vivo() == False
    
    def test_pokemon_esta_vivo_con_hp_negativo(self):
        movimiento = Movimiento("Ataque", "Normal", 30)
        pokemon = Pokemon("Pikachu", "Eléctrico", 100, 50, 40, [movimiento])
        pokemon.hp = -10
        assert pokemon.esta_vivo() == False

class TestTiposValidos:
    
    def test_pokemon_tipo_fuego_valido(self):
        movimiento = Movimiento("Lanzallamas", "fuego", 90)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [movimiento])
        assert pokemon.tipo == "fuego"
    
    def test_pokemon_tipo_agua_valido(self):
        movimiento = Movimiento("Hidrobomba", "agua", 110)
        pokemon = Pokemon("Totodile", "agua", 110, 45, 50, [movimiento])
        assert pokemon.tipo == "agua"
    
    def test_pokemon_tipo_tierra_valido(self):
        movimiento = Movimiento("Terremoto", "tierra", 100)
        pokemon = Pokemon("Diglett", "tierra", 95, 55, 60, [movimiento])
        assert pokemon.tipo == "tierra"
    
    def test_pokemon_tipo_aire_valido(self):
        movimiento = Movimiento("Vendaval", "aire", 110)
        pokemon = Pokemon("Pidgeot", "aire", 90, 40, 35, [movimiento])
        assert pokemon.tipo == "aire"
        
class TestAprenderMovimiento:
    
    def test_aprender_movimiento_compatible(self):
        mov_fuego = Movimiento("Lanzallamas", "fuego", 90)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        
        resultado = pokemon.aprender_movimiento(mov_fuego)
        
        assert resultado == True
        assert len(pokemon.movimientos) == 1
    
    def test_aprender_movimiento_incompatible(self):
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        
        resultado = pokemon.aprender_movimiento(mov_agua)
        
        assert resultado == False
        assert len(pokemon.movimientos) == 0