from generadorPartidas.RandomPlayer import CRandomPlayer


# Jugador con Ataque estadístico, el resto de decisiones on aleatorias

class PlayerDe(CRandomPlayer):

    def defensa(self, estado_partida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        # Todo: Comprobacion de que el pais pertenece al jugador
        nro_defensores = estado_partida.paises_l[pais_atacado].nro_ejercitos

        max_defensores = min(nro_defensores, 2)

        return max_defensores

    def test_cambio_cartas(self, ejercito_por_cambio, cambio_obligatorio=False):
        raise NotImplementedError
