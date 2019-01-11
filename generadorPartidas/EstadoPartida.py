#Clase que contiene el estado de una partida
from generadorPartidas.ClasesBasicas import CPais, CContinente


class CEstadoPartida:
    def __init__(self, lista_jugadores = {} , turno = 0, lista_paises = {}, lista_continentes = {},
                 partidaid = 0):
        self.id_partida = partidaid
        self.nro_turno = turno
        self.jugadores_l = lista_jugadores.copy()
        self.paises_l = lista_paises.copy()
        self.continentes_l = lista_continentes.copy()

    def __enter__(self):
        return self

    #Comprobamos si el jugador es ganador al tener todos los paises
    def esGanador(self, jugador):
        for pais in self.paises_l.keys():
            if self.paises_l[pais].propietario != jugador:
                return False

        return True


