# Clase base que define un jugador IA.


class Cplayer:
    propietario = None

    def __init__(self, propietario):
        self.propietario = propietario

    def set_models(self, model):
        raise NotImplementedError

    def seleccionar_pais(self, estado_partida):
        raise NotImplementedError

    def reforzar_pais(self, estado_partida):
        raise NotImplementedError

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    # Seleccion del pais a atacar o None en el caso de que pasar ataques
    def ataque(self, estado_partida):
        raise NotImplementedError

    # Seleccion del nro de ejercitos para defender
    def defensa(self, estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        raise NotImplementedError

    def movimiento_tropa(self, estado_partida):
        raise NotImplementedError

