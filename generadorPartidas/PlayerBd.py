from generadorPartidas.RandomPlayer import CRandomPlayer
import numpy as np

#Todo Finalizar ataque Deep Learning

# Jugador con Batalla  DeepLearning, el resto de decisiones son aleatorias

class PlayerBd(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.model = None

    def set_models(self, p_model):
        self.model = p_model

    def ataque(self, estado_partida):
        return super().ataque(estado_partida)
        # assert self.model is not None, "Modelo nulo en PlayerDd"
        # # Obtenemos todos los paises que podemos atacar
        # paises_atacables = list()
        # for pais in estado_partida.paises_l.keys():
        #     if (estado_partida.paises_l[pais].propietario is self.propietario) and (
        #             estado_partida.paises_l[pais].nro_ejercitos > 1):
        #         # Buscamos todos los vecinos
        #         for vecino in estado_partida.paises_l[pais].vecino:
        #             # si el pais vecino es propiedad de otro se incluye en la lista
        #             pais_candidato = estado_partida.paises_l[vecino]
        #             if pais_candidato.propietario != self.propietario:
        #                 # atacamos con el mayor nro de ejercitos posible (hasta 20)
        #                 ejercitos_atacantes = min(20, estado_partida.paises_l[pais].nro_ejercitos - 1)
        #                 ejercitos_defensores = estado_partida.paises_l[pais_candidato.nombre].nro_ejercitos
        #
        #                 x = np.array([[ejercitos_atacantes, ejercitos_defensores]])
        #                 prob_ganar = self.model.predict(x)
        #
        #                 # incluimos el atacante, el atacado y el nro de ejercitos a usar en la lista, asociado a la
        #                 # probabilidad de ganar
        #                 if prob_ganar > .5:
        #                     paises_atacables.append(([pais, pais_candidato.nombre, ejercitos_atacantes], prob_ganar))
        #
        # # Elegimos un pais para atacar con mayor nro de probabilidades de ganar
        # if len(paises_atacables) == 0:
        #     return None
        #
        # ataque = max(paises_atacables, key=itemgetter(1))[0]
        #
        # return ataque

    def defensa(self, estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        return super().defensa(estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado)

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        newplayer = PlayerBd(self.propietario)

        newplayer.model = self.model

        return newplayer
