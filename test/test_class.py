import pytest
from pokemon import *

class TestMovimiento:
    
    def test_movimiento_creacion_correcta(self):
        mov = Movimiento("Impactrueno", "fuego", 40)
        assert mov.nombre == "Impactrueno"
        assert mov.tipo == "fuego"
        assert mov.potencia == 40
    
    def test_movimiento_atributos_accesibles(self):
        movimiento = Movimiento("Ataque Rápido", "agua", 30)
        assert movimiento.nombre == "Ataque Rápido"
        assert movimiento.tipo == "agua"
        assert movimiento.potencia == 30


class test_pokemon_iniciar:
    
    def test_pokemon_creacion_correcta(self):
        movimiento = Movimiento("Pistola Agua", "agua", 40)
        pokemon = Pokemon("Squirtle", "agua", 90, 48, 65, [movimiento])
        assert pokemon.get_nombre() == "Squirtle"
        assert pokemon.tipo == "agua"
        assert pokemon.hp == 90
        assert pokemon.ataque == 48
        assert pokemon.defensa == 65
        assert len(pokemon.movimientos) == 1
    
    def test_pokemon_hp_max_igual_hp_inicial(self):
        movimiento = Movimiento("Ataque", "fuego", 30)
        pokemon = Pokemon("Pikachu", "fuego", 100, 50, 40, [movimiento])
        assert pokemon.hp == pokemon.hp_max
        assert pokemon.hp_max == 100


class TestPokemonEstaVivo:
    
    def test_pokemon_esta_vivo_con_hp_positivo(self):
        movimiento = Movimiento("Ataque", "fuego", 30)
        pokemon = Pokemon("Pikachu", "fuego", 100, 50, 40, [movimiento])
        assert pokemon.esta_vivo() == True
        
        pokemon.hp = 50
        assert pokemon.esta_vivo() == True
        
        pokemon.hp = 1
        assert pokemon.esta_vivo() == True
    
    def test_pokemon_esta_vivo_con_hp_cero(self):
        movimiento = Movimiento("Ataque", "agua", 30)
        pokemon = Pokemon("Pikachu", "agua", 100, 50, 40, [movimiento])
        pokemon.hp = 0
        assert pokemon.esta_vivo() == False
    
    def test_pokemon_esta_vivo_con_hp_negativo(self):
        movimiento = Movimiento("Ataque", "tierra", 30)
        pokemon = Pokemon("Pikachu", "tierra", 100, 50, 40, [movimiento])
        pokemon.hp = -10
        assert pokemon.esta_vivo() == False


class TestTiposValidos:
    
    def test_pokemon_tipo_fuego_valido(self):
        movimiento = Movimiento("Lanzallamas", "fuego", 90)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [movimiento])
        assert pokemon.tipo == "fuego"
    
    def test_pokemon_tipo_agua_valido(self):
        movimiento = Movimiento("Hidrobomba", "agua", 110)
        pokemon = Pokemon("Blastoise", "agua", 110, 45, 50, [movimiento])
        assert pokemon.tipo == "agua"
    
    def test_pokemon_tipo_tierra_valido(self):
        movimiento = Movimiento("Terremoto", "tierra", 100)
        pokemon = Pokemon("Sandslash", "tierra", 95, 55, 60, [movimiento])
        assert pokemon.tipo == "tierra"
    
    def test_pokemon_tipo_aire_valido(self):
        movimiento = Movimiento("Vendaval", "aire", 110)
        pokemon = Pokemon("Pidgeot", "aire", 90, 40, 35, [movimiento])
        assert pokemon.tipo == "aire"

class TestRestriccionMovimientos:
    
    def test_pokemon_aprende_movimiento_mismo_tipo(self):
        mov_fuego = Movimiento("Lanzallamas", "fuego", 90)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [mov_fuego])
        assert len(pokemon.movimientos) == 1
        assert pokemon.movimientos[0].nombre == "Lanzallamas"
    
    def test_pokemon_no_aprende_movimiento_tipo_diferente(self):
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [mov_agua])
        assert len(pokemon.movimientos) == 0
    
    def test_pokemon_filtra_movimientos_incorrectos(self):
        mov_fuego1 = Movimiento("Lanzallamas", "fuego", 90)
        mov_fuego2 = Movimiento("Ascuas", "fuego", 40)
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        mov_tierra = Movimiento("Terremoto", "tierra", 100)
        
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, 
                         [mov_fuego1, mov_agua, mov_fuego2, mov_tierra])
        
        assert len(pokemon.movimientos) == 2
        assert pokemon.movimientos[0].tipo == "fuego"
        assert pokemon.movimientos[1].tipo == "fuego"
    
    def test_pokemon_acepta_multiples_movimientos_mismo_tipo(self):
        mov_agua1 = Movimiento("Hidrobomba", "agua", 110)
        mov_agua2 = Movimiento("Pistola Agua", "agua", 40)
        mov_agua3 = Movimiento("Surf", "agua", 90)
        
        pokemon = Pokemon("Blastoise", "agua", 110, 45, 50, 
                         [mov_agua1, mov_agua2, mov_agua3])
        
        assert len(pokemon.movimientos) == 3
        assert all(mov.tipo == "agua" for mov in pokemon.movimientos)


class TestMetodoAprenderMovimiento:
    
    def test_aprender_movimiento_tipo_compatible_retorna_true(self):
        mov_fuego = Movimiento("Lanzallamas", "fuego", 90)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        
        resultado = pokemon.aprender_movimiento(mov_fuego)
        
        assert resultado == True
        assert len(pokemon.movimientos) == 1
    
    def test_aprender_movimiento_tipo_incompatible_retorna_false(self):
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        
        resultado = pokemon.aprender_movimiento(mov_agua)
        
        assert resultado == False
        assert len(pokemon.movimientos) == 0
    
    def test_aprender_movimiento_no_duplica_movimientos_incompatibles(self):
        mov_agua1 = Movimiento("Hidrobomba", "agua", 110)
        mov_agua2 = Movimiento("Pistola Agua", "agua", 40)
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        
        pokemon.aprender_movimiento(mov_agua1)
        pokemon.aprender_movimiento(mov_agua2)
        
        assert len(pokemon.movimientos) == 0


class TestPokemonSinMovimientos:
    
    def test_pokemon_sin_movimientos_validos_lista_vacia(self):
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        mov_tierra = Movimiento("Terremoto", "tierra", 100)
        
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [mov_agua, mov_tierra])
        
        assert len(pokemon.movimientos) == 0
    
    def test_pokemon_creado_sin_movimientos(self):
        pokemon = Pokemon("Charizard", "fuego", 100, 50, 40, [])
        assert len(pokemon.movimientos) == 0
        assert pokemon.esta_vivo() == True


class TestAtaqueConRestricciones:
    
    def test_pokemon_con_movimientos_puede_atacar(self):
        mov_fuego = Movimiento("Lanzallamas", "fuego", 90)
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        
        charizard = Pokemon("Charizard", "fuego", 100, 50, 40, [mov_fuego])
        blastoise = Pokemon("Blastoise", "agua", 110, 45, 50, [mov_agua])
        
        hp_inicial = blastoise.hp
        charizard.atacar(blastoise)
        
        assert blastoise.hp < hp_inicial
    
    def test_pokemon_sin_movimientos_no_causa_dano(self):
        mov_agua = Movimiento("Hidrobomba", "agua", 110)
        
        # Charizard no tendrá movimientos porque son de agua
        charizard = Pokemon("Charizard", "fuego", 100, 50, 40, [mov_agua])
        blastoise = Pokemon("Blastoise", "agua", 110, 45, 50, [mov_agua])
        
        hp_inicial = blastoise.hp
        charizard.atacar(blastoise)
        
        assert blastoise.hp == hp_inicial
        
