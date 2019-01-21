# Clase que contiene el estado de una partida
from generadorPartidas.ClasesBasicas import CPais, CContinente


# Crea las definiciones para el mapa estandar
def inicializa_mapa_standar():
    # Creamos los paises
    pais_0_0 = CPais("0_0")
    pais_0_1 = CPais("0_1")
    pais_1_0 = CPais("1_0")
    pais_1_1 = CPais("1_1")

    pais_0_0.vecino = [pais_0_1.nombre, pais_1_1.nombre, pais_1_0.nombre]
    pais_0_1.vecino = [pais_0_0.nombre]
    pais_1_0.vecino = [pais_0_0.nombre]
    pais_1_1.vecino = [pais_0_0.nombre]

    paises = {pais_0_0.nombre: pais_0_0,
              pais_0_1.nombre: pais_0_1,
              pais_1_0.nombre: pais_1_0,
              pais_1_1.nombre: pais_1_1}

    # Creamos los continentes
    world = CContinente("world")

    world.pais = [pais_0_0.nombre, pais_1_0.nombre,
                  pais_0_1.nombre, pais_1_1.nombre]

    continentes = {world.nombre: world}

    return [paises, continentes]
