from generadorPartidas.RandomPlayer import CRandomPlayer
import numpy as np


# Jugador con inicializacion DeepLearning, el resto de decisiones on aleatorias


class PlayerId(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.model = None

    def set_models(self, p_model):
        self.model = p_model

    def seleccionar_pais(self, estado_partida):
        # Construimos un vector de ordenes para cada jugador, teniendo en cuenta que el que mueve es el primer jugador
        posicion = np.zeros(3, dtype=int)
        posicion[self.propietario] = 0
        posicion[(self.propietario + 1) % 3] = len(estado_partida.paises_l)
        posicion[(self.propietario + 2) % 3] = len(estado_partida.paises_l) * 2

        # Creamos el vector de entrada
        nro_col = (len(estado_partida.jugadores_l) * len(estado_partida.paises_l)) + len(estado_partida.paises_l)
        nro_filas = sum(estado_partida.paises_l[x].propietario is not None for x in estado_partida.paises_l)

        assert nro_filas > 0, "No quedan paises libres para seleccionar"

        input_vector = np.zeros((nro_filas, nro_col), dtype=int)

        # Obtenemos todos los paises no asignados
        paises_libres = list()
        nro_pais = 0
        nro_fila = 0
        inicio_seleccion = len(estado_partida.paises_l) * 3

        # recorremos la lista de paises y rellenamos la matriz de entrada
        for pais in sorted(estado_partida.paises_l.keys()):
            if estado_partida.paises_l[pais].propietario is None:
                # Marcamos la seleccion del pais en la fila siguiente
                paises_libres.append(pais)
                input_vector[nro_fila,  inicio_seleccion + nro_pais] = 1

                nro_fila += 1
            else:
                # Marcamos la celdas del propietario del pais en la matriz
                input_vector[:, posicion[estado_partida.paises_l[pais].propietario] + nro_pais] = 1

            nro_pais += 1

        if len(paises_libres) == 1:
            pais = 0
        else:
            # obtenemos el que fila tiene la probabilidad mas alta de ganar
            prob_ganar = self.model.predict(input_vector)
            pais = np.argmax(prob_ganar, axis=0)

        return paises_libres[pais[0]]

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        newplayer = PlayerId(self.propietario)

        newplayer.model = self.model

        return newplayer
