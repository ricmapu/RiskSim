from generadorPartidas.EstadoPartida import CEstadoPartida
#Clase base que define un jugador IA.

class Cplayer:
    propietario = None

    def __init__(self, propietario):
        self.propietario = propietario

    def seleccionarPais(self, estadoPartida):
        return None

    def reforzarPais(self, estadoPartida):
        return None

    def test_cambio_cartas(self, ejercitoPorCambio, cambioObligatorio = False):
        return [False, None]

    #Seleccion del pais a atacar o None en el caso de que pasar ataques
    def Ataque(self, estadoPartida):
        return None

    # Seleccion del nro de ejercitos para defender
    def Defensa(estadoPartida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        return None

    def MovimientoTropa(self, estadoPartida):
        return None

