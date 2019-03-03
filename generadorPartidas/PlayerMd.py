from generadorPartidas.RandomPlayer import CRandomPlayer
from generadorPartidas.ModelContainer import ModelContainer
import numpy as np
from copy import deepcopy


# Jugador con Movimiento DeepLearning, el resto de decisiones on aleatorias


class PlayerMd(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.model = ModelContainer

    def set_models(self, p_model):
        self.model = p_model

    def movimiento_tropa(self, estado_partida):

        # Inicializacion de variables
        num_paises = len(estado_partida.paises_l)
        jugadores = len(estado_partida.jugadores_l)
        ancho_matriz = (num_paises * jugadores) + (num_paises * 2) + 1

        inicio_origen = num_paises * jugadores
        inicio_destino = inicio_origen + num_paises
        inicio_pasar = inicio_destino + num_paises

        posicion = np.zeros(3, dtype=int)
        posicion[self.propietario] = 0
        posicion[(self.propietario + 1) % 3] = len(estado_partida.paises_l)
        posicion[(self.propietario + 2) % 3] = len(estado_partida.paises_l) * 2

        # Obtenemos todos los paises asignados al jugador
        movimientos = []

        # Copiamos el nro de ejercitos
        paises_temp = deepcopy(estado_partida.paises_l)

        for pais in paises_temp.keys():
            if (paises_temp[pais].propietario is self.propietario) \
                    and (paises_temp[pais].nro_ejercitos > 1) \
                    and (len(paises_temp[pais].vecino) > 0):
                # Obtenemos todos los vecinos del pais seleccionado
                paises_vecinos = self._get_vecinos(pais, estado_partida)

                if len(paises_vecinos) > 0:
                    # Construimos un vector de ordenes para cada jugador, teniendo en cuenta que el que
                    # mueve es el primer jugador
                    input_vector = np.zeros((len(paises_vecinos) + 1, ancho_matriz), dtype=int)

                    # Primera pasada, recorremos los paises rellenando los propietarios
                    nro_pais = 0
                    for pais_t in sorted(paises_temp.keys()):
                        # Marcamos la celdas del propietario del pais en la matriz
                        input_vector[:, posicion[paises_temp[pais_t].propietario] + nro_pais] = 1
                        nro_pais += 1

                    # Segunda pasada, recorremos las vecinos posibles, rellenado la matriz
                    fila = 0

                    indices_paises = sorted(paises_temp)
                    for vecino in paises_vecinos:
                        # marcamos las celdas origen, destino
                        index_origen = indices_paises.index(pais)
                        index_destino = indices_paises.index(vecino)

                        input_vector[fila, inicio_origen + index_origen] = 1
                        input_vector[fila, inicio_destino + index_destino] = 1

                        fila += 1

                    # En la ultima fila ponemos pasar a 1
                    input_vector[-1, inicio_pasar] = 1

                    # obtenemos el que fila tiene la probabilidad mas alta de ganar
                    prob_ganar = self.model.movimiento_ejercitos.predict(input_vector)
                    index = np.argmax(prob_ganar, axis=0)[0]

                    if index == (len(prob_ganar) - 1):
                        # El jugador decide pasar y se finaliza el turno
                        movimientos.append((None, None, None))
                        return movimientos
                    else:
                        # Obtenemos el nro de ejercitos a mover, a partir de la opcion escogida
                        input_nro_eje = input_vector[1, 0:20]

                        input_nro_eje = np.reshape(input_nro_eje, (1, 20))

                        num_ejercitos = self.model.movimiento_num_ejercitos.predict(input_nro_eje)

                        num_ejercitos = round(num_ejercitos[0, 0])

                        # Hay que comprobar que el nro de ejercitos no sea mayor que el max a mover o 0
                        if num_ejercitos == 0:
                            num_ejercitos = 1

                        if num_ejercitos > (paises_temp[pais].nro_ejercitos - 1):
                            num_ejercitos = paises_temp[pais].nro_ejercitos - 1

                        movimientos.append((pais, paises_vecinos[index], 1))
                        # ajustamos el nro de ejercitos para la proxima iteracion
                        paises_temp[pais].nro_ejercitos -= num_ejercitos
                        paises_temp[paises_vecinos[index]].nro_ejercitos += num_ejercitos

        return movimientos

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        newplayer = PlayerMd(self.propietario)

        newplayer.model = self.model

        return newplayer
