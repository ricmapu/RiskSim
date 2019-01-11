#Clase que contiene el estado de una partida
from generadorPartidas.ClasesBasicas import CPais, CContinente


#Crea las definiciones para el mapa estandar
def InicializaMapaStandar():
    #Creamos los paises
    pais_0_0 = CPais("0_0")
    pais_0_1 = CPais("0_1")
    pais_1_0 = CPais("1_0")
    pais_1_1 = CPais("1_1")

    pais_0_0.vecino=[pais_0_1.nombre, pais_1_1.nombre, pais_1_0.nombre]
    pais_0_1.vecino=[pais_0_0.nombre]
    pais_1_0.vecino = [pais_0_0.nombre]
    pais_1_1.vecino = [pais_0_0.nombre]

    paises = {pais_0_0.nombre:pais_0_0,
              pais_0_1.nombre:pais_0_1,
              pais_1_0.nombre:pais_1_0,
              pais_1_1.nombre:pais_1_1}

    #Creamos los continentes
    world = CContinente("world")

    world.pais=[pais_0_0.nombre, pais_1_0.nombre,
                pais_0_1.nombre, pais_1_1.nombre]

    continentes = {world.nombre: world}

    return [paises, continentes]

# def InicializaMapaStandar():
#     #Creamos los paises
#     indonesia = CPais("Indonesia")
#     nueva_guinea = CPais("NuevaGuinea")
#     australia_occidental = CPais("AustraliaOccidental")
#     australia_oriental = CPais("AustraliaOriental")
#
#     indonesia.vecino=[nueva_guinea.nombre, australia_occidental.nombre]
#     nueva_guinea.vecino=[indonesia.nombre, australia_oriental.nombre]
#     australia_occidental.vecino = [indonesia.nombre, australia_occidental.nombre]
#     australia_oriental.vecino = [nueva_guinea.nombre, australia_occidental.nombre]
#
#     paises = {indonesia.nombre:indonesia,
#               nueva_guinea.nombre: nueva_guinea,
#               australia_oriental.nombre: australia_oriental,
#               australia_occidental.nombre:australia_occidental}
#
#     #Creamos los continentes
#     australia = CContinente("Australia")
#
#     australia.pais=[indonesia.nombre, nueva_guinea.nombre,
#                     australia_occidental.nombre, australia_oriental.nombre]
#
#     continentes = {australia.nombre: australia}
#
#     return [paises, continentes]

