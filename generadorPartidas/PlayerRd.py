from generadorPartidas.RandomPlayer import CRandomPlayer
import numpy as np


# Jugador con Refuerzo DeepLearning, el resto de decisiones on aleatorias


class PlayerRd(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.model = None

    def set_models(self, p_model):
        self.model = p_model

    def reforzar_pais(self, estado_partida):
        # Obtenemos todos los paises asignados al jugador
        paises_propietario = list()
        for pais in estado_partida.paises_l.keys():
            if estado_partida.paises_l[pais].propietario is self.propietario:
                paises_propietario.append(pais)

        assert len(paises_propietario) > 0, "No hay paises para el propietario"

        if len(paises_propietario) == 1:
            return paises_propietario[0]

        # Construimos un vector de ordenes para cada jugador, teniendo en cuenta que el que mueve es el primer jugador
        ancho_matriz = (len(estado_partida.jugadores_l) * len(estado_partida.paises_l)) + len(estado_partida.paises_l)

        posicion = np.zeros(3, dtype=int)
        posicion[self.propietario] = 0
        posicion[(self.propietario + 1) % 3] = len(estado_partida.paises_l)
        posicion[(self.propietario + 2) % 3] = len(estado_partida.paises_l) * 2
        inicio_seleccion = len(estado_partida.paises_l) * 3

        input_vector = np.zeros((len(paises_propietario), ancho_matriz), dtype=int)

        # Recorremos la paises marcando los paises de cada propietario
        nro_pais = 0
        nro_fila = 0
        for pais in sorted(estado_partida.paises_l.keys()):
            # Marcamos la celdas del propietario del pais en la matriz
            input_vector[:, posicion[estado_partida.paises_l[pais].propietario] + nro_pais] = 1

            if pais in paises_propietario:
                input_vector[nro_fila,   inicio_seleccion + nro_pais] = 1
                nro_fila += 1

            nro_pais += 1

        # obtenemos el que fila tiene la probabilidad mas alta de ganar
        prob_ganar = self.model.predict(input_vector)
        pais = np.argmax(prob_ganar, axis=0)[0]

        return paises_propietario[pais]

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        newplayer = PlayerRd(self.propietario)

        newplayer.model = self.model

        return newplayer
