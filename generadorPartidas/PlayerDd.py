from generadorPartidas.RandomPlayer import CRandomPlayer
import numpy as np


# Jugador con Ataque estadístico, el resto de decisiones on aleatorias


class PlayerDd(CRandomPlayer):
    def __init__(self, propietario):
        super().__init__(propietario)
        self.model = None

    def set_models(self, p_model):
        self.model = p_model

    def defensa(self, estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        if nro_ejercitos_ataque < 3:
            nro_ejercitos_ataque = nro_ejercitos_ataque

        # Todo: Comprobacion de que el pais pertenece al jugador
        nro_defensores = estado_partida.paises_l[pais_atacado].nro_ejercitos
        defensores = min(nro_defensores, 2)

        if defensores == 2:
            # Evaluamos que opcion es la más adecuada de defensa
            x = np.array([[nro_ejercitos_ataque, 1], [nro_ejercitos_ataque, 2]])

            assert self.model is not None, "Modelo nulo en PlayerDd"

            result = self.model.predict(x)
            if (1-result[0]) > (1-result[1]):
                defensores = 1
            else:
                defensores = 2

        return defensores

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        newplayer = PlayerDd(self.propietario)

        newplayer.model = self.model

        return newplayer
