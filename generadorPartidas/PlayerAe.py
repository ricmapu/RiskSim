from generadorPartidas.RandomPlayer import CRandomPlayer
import numpy as np
from operator import itemgetter


# Jugador con Ataque estadístico, el resto de decisiones on aleatorias

class PlayerAe(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.prob_A_D = np.array(
            [[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
              0.00, 0.00, 0.00, 0.00],
             [0.00, 0.42, 0.75, 0.92, 0.97, 0.99, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
              1.00, 1.00, 1.00, 1.00],
             [0.00, 0.11, 0.36, 0.66, 0.79, 0.89, 0.93, 0.97, 0.98, 0.99, 0.99, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
              1.00, 1.00, 1.00, 1.00],
             [0.00, 0.03, 0.21, 0.47, 0.64, 0.77, 0.86, 0.91, 0.95, 0.97, 0.98, 0.99, 0.99, 1.00, 1.00, 1.00, 1.00,
              1.00, 1.00, 1.00, 1.00],
             [0.00, 0.01, 0.09, 0.31, 0.48, 0.64, 0.74, 0.83, 0.89, 0.93, 0.95, 0.97, 0.98, 0.99, 0.99, 1.00, 1.00,
              1.00, 1.00, 1.00, 1.00],
             [0.00, 0.00, 0.05, 0.21, 0.36, 0.51, 0.64, 0.74, 0.82, 0.87, 0.92, 0.94, 0.96, 0.98, 0.98, 0.99, 0.99,
              1.00, 1.00, 1.00, 1.00],
             [0.00, 0.00, 0.02, 0.13, 0.25, 0.40, 0.52, 0.64, 0.73, 0.81, 0.86, 0.91, 0.93, 0.96, 0.97, 0.98, 0.99,
              0.99, 0.99, 1.00, 1.00],
             [0.00, 0.00, 0.01, 0.08, 0.18, 0.30, 0.42, 0.54, 0.64, 0.73, 0.80, 0.85, 0.90, 0.93, 0.95, 0.96, 0.98,
              0.98, 0.99, 0.99, 1.00],
             [0.00, 0.00, 0.00, 0.05, 0.12, 0.22, 0.33, 0.45, 0.55, 0.65, 0.72, 0.79, 0.84, 0.89, 0.92, 0.94, 0.96,
              0.97, 0.98, 0.99, 0.99],
             [0.00, 0.00, 0.00, 0.03, 0.09, 0.16, 0.26, 0.36, 0.46, 0.56, 0.65, 0.72, 0.79, 0.84, 0.88, 0.91, 0.94,
              0.95, 0.97, 0.98, 0.98],
             [0.00, 0.00, 0.00, 0.02, 0.06, 0.12, 0.19, 0.29, 0.38, 0.48, 0.57, 0.65, 0.72, 0.79, 0.83, 0.88, 0.91,
              0.93, 0.95, 0.97, 0.97],
             [0.00, 0.00, 0.00, 0.01, 0.04, 0.08, 0.15, 0.22, 0.31, 0.40, 0.49, 0.58, 0.66, 0.72, 0.78, 0.83, 0.87,
              0.90, 0.93, 0.95, 0.96],
             [0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.11, 0.17, 0.25, 0.33, 0.42, 0.51, 0.58, 0.66, 0.72, 0.78, 0.83,
              0.87, 0.90, 0.92, 0.94],
             [0.00, 0.00, 0.00, 0.00, 0.02, 0.04, 0.08, 0.13, 0.20, 0.27, 0.35, 0.43, 0.52, 0.59, 0.67, 0.73, 0.78,
              0.83, 0.87, 0.89, 0.92],
             [0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.10, 0.15, 0.22, 0.29, 0.37, 0.45, 0.53, 0.60, 0.67, 0.73,
              0.78, 0.82, 0.86, 0.89],
             [0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.04, 0.07, 0.12, 0.17, 0.24, 0.31, 0.39, 0.46, 0.54, 0.61, 0.67,
              0.73, 0.78, 0.82, 0.86],
             [0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.05, 0.09, 0.14, 0.19, 0.26, 0.33, 0.40, 0.47, 0.55, 0.61,
              0.68, 0.73, 0.78, 0.82],
             [0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.04, 0.07, 0.11, 0.16, 0.21, 0.28, 0.34, 0.42, 0.48, 0.56,
              0.62, 0.68, 0.73, 0.78],
             [0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.03, 0.05, 0.08, 0.12, 0.17, 0.23, 0.29, 0.36, 0.43, 0.49,
              0.56, 0.62, 0.68, 0.73],
             [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.04, 0.06, 0.10, 0.14, 0.19, 0.24, 0.31, 0.37, 0.44,
              0.50, 0.57, 0.63, 0.69],
             [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.03, 0.05, 0.07, 0.11, 0.15, 0.20, 0.26, 0.32, 0.38,
              0.45, 0.51, 0.58, 0.63]])

    def ataque(self, estado_partida):
        # Obtenemos todos los paises que podemos atacar
        paises_atacables = list()
        for pais in estado_partida.paises_l.keys():
            if (estado_partida.paises_l[pais].propietario is self.propietario) and (
                    estado_partida.paises_l[pais].nro_ejercitos > 1):
                # Buscamos todos los vecinos
                for vecino in estado_partida.paises_l[pais].vecino:
                    # si el pais vecino es propiedad de otro se incluye en la lista
                    pais_candidato = estado_partida.paises_l[vecino]
                    if pais_candidato.propietario != self.propietario:
                        # atacamos con el mayor nro de ejercitos posible (hasta 20)
                        ejercitos_atacantes = min(20, estado_partida.paises_l[pais].nro_ejercitos - 1)
                        ejercitos_defensores = estado_partida.paises_l[pais_candidato.nombre].nro_ejercitos
                        prob_ganar = self.prob_A_D[ejercitos_defensores, ejercitos_atacantes]

                        # incluimos el atacante, el atacado y el nro de ejercitos a usar en la lista, asociado a la
                        # probabilidad de ganar
                        if prob_ganar > .5:
                            paises_atacables.append(([pais, pais_candidato.nombre, ejercitos_atacantes], prob_ganar))

        # Elegimos un pais para atacar con mayor nro de probabilidades de ganar
        if len(paises_atacables) == 0:
            return None

        ataque = max(paises_atacables, key=itemgetter(1))[0]

        return ataque

    def defensa(self, estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        # Todo: Comprobacion de que el pais pertenece al jugador
        nro_defensores = estado_partida.paises_l[pais_atacado].nro_ejercitos

        max_defensores = min(nro_defensores, 2)

        return max_defensores

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError
