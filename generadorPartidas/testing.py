import unittest
import numpy.random as rd

from generadorPartidas import Mapa
from generadorPartidas.ClasesBasicas import CPais, CContinente
from generadorPartidas.PlayerAe import PlayerAe
from generadorPartidas.arbitro import CArbitro
from generadorPartidas.generadorLog import Clog
from generadorPartidas.EstadoPartida import CEstadoPartida
from generadorPartidas.RandomPlayer import CRandomPlayer
from generadorPartidas.PlayerDe import PlayerDe
from generadorPartidas.PlayerDd import PlayerDd
from generadorPartidas.PlayerId import PlayerId
from generadorPartidas.PlayerRd import PlayerRd
from generadorPartidas.PlayerBd import PlayerBd
from generadorPartidas.PlayerMd import PlayerMd
from generadorPartidas.ModelContainer import ModelContainer
from keras.models import load_model


class CPaisTesting(unittest.TestCase):

    def test_nombre(self):
        country = CPais("AustraliaOccidental")
        self.assertEqual(country.nombre, 'AustraliaOccidental')


class CContinenteTesting(unittest.TestCase):

    def test_nombre(self):
        continent = CContinente("Australia")
        self.assertEqual(continent.nombre, "Australia")


class MapTestInt(unittest.TestCase):

    def testInicializaMapaStandar(self):
        [paises, continentes] = Mapa.inicializa_mapa_standar()

        self.assertEqual(len(paises), 4)
        self.assertEqual(len(continentes), 1)


class TestCRandomPlayer(unittest.TestCase):
    def testCRandomPlayer(self):
        [paises, continentes] = Mapa.inicializa_mapa_standar()
        tst_estado_partida = CEstadoPartida({1, 2, 3}, 0, paises, continentes, 0)

        tst_estado_partida.paises_l['0_0'].propietario = 1
        tst_estado_partida.paises_l['0_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['0_1'].propietario = 1
        tst_estado_partida.paises_l['0_1'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_0'].propietario = 2
        tst_estado_partida.paises_l['1_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_estado_partida.paises_l['1_1'].nro_ejercitos = 1

        tst_player = CRandomPlayer(1)

        self.assertIsNone(tst_player.ataque(tst_estado_partida)[0])

        tst_estado_partida.paises_l['0_0'].propietario = 1
        tst_estado_partida.paises_l['0_0'].nro_ejercitos = 2

        tst_estado_partida.paises_l['0_1'].propietario = 1
        tst_estado_partida.paises_l['0_1'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_0'].propietario = 2
        tst_estado_partida.paises_l['1_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_estado_partida.paises_l['1_1'].nro_ejercitos = 1

        tst_player = CRandomPlayer(1)

        tst_player.ataque(tst_estado_partida)


class TestPlayerAe(unittest.TestCase):
    def testPlayer_Ae(self):
        [countries, continents] = Mapa.inicializa_mapa_standar()
        tst_estado_partida = CEstadoPartida({1, 2, 3}, 0, countries, continents, 0)

        tst_estado_partida.paises_l['0_0'].propietario = 1
        tst_estado_partida.paises_l['0_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['0_1'].propietario = 1
        tst_estado_partida.paises_l['0_1'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_0'].propietario = 2
        tst_estado_partida.paises_l['1_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_estado_partida.paises_l['1_1'].nro_ejercitos = 1

        tst_player = PlayerAe(1)

        self.assertIsNone(tst_player.ataque(tst_estado_partida))

        tst_estado_partida.paises_l['0_0'].propietario = 2
        tst_estado_partida.paises_l['0_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['0_1'].propietario = 1
        tst_estado_partida.paises_l['0_1'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_0'].propietario = 1
        tst_estado_partida.paises_l['1_0'].nro_ejercitos = 2

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_estado_partida.paises_l['1_1'].nro_ejercitos = 1

        tst_player = PlayerAe(1)

        self.assertIsNone(tst_player.ataque(tst_estado_partida))

        tst_estado_partida.paises_l['0_0'].propietario = 2
        tst_estado_partida.paises_l['0_0'].nro_ejercitos = 1

        tst_estado_partida.paises_l['0_1'].propietario = 1
        tst_estado_partida.paises_l['0_1'].nro_ejercitos = 1

        tst_estado_partida.paises_l['1_0'].propietario = 1
        tst_estado_partida.paises_l['1_0'].nro_ejercitos = 2

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_estado_partida.paises_l['1_1'].nro_ejercitos = 3

        tst_player = PlayerAe(1)

        self.assertIsNotNone(tst_player.ataque(tst_estado_partida))


class TestGeneracionLogs(unittest.TestCase):

    def testCArbitro(self):
        rd.seed(3)

        arbitro = CArbitro(jugadores=3, max_turnos=1000., player_class=[CRandomPlayer, CRandomPlayer, CRandomPlayer],
                           atack_models=[None, None, None])

        arbitro.play(0)

    def testCArbitroyLog(self):
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, CRandomPlayer],
                           atack_models=[None, None, None])

        tst_log = Clog("../../datos/unittest/ini_partida2.csv",
                       "../../datos/unittest/refuerzo_partida2.csv",
                       "../../datos/unittest/batalla_partida2.csv",
                       "../../datos/unittest/movimiento_ejercitos2.csv")

        rd.seed(1)

        arbitro.set_log(tst_log)
        arbitro.play(0)
        self.assertTrue(tst_log.flush())

    def testCArbitroMultiplePartidas(self):
        # Comprobamos la creación de 100 partidas
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, CRandomPlayer],
                           atack_models=[None, None, None])

        tst_log = Clog("../../datos/unittest/ini_partida3.csv",
                       "../../datos/unittest/refuerzo_partida3.csv",
                       "../../datos/unittest/batalla_partida3.csv",
                       "../../datos/unittest/movimiento_ejercitos3.csv")

        rd.seed(1)

        arbitro.set_log(tst_log)

        for partida in range(0, 100):
            arbitro.play(partida)
            if partida % 100 == 0:
                print(partida)

        self.assertTrue(tst_log.flush())


class TestCArbitro(unittest.TestCase):
    def testCArbitroAleatorio(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, CRandomPlayer], atack_models=[None, None, None])
        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, Random]:" + str(total_ganadas) + " -> "
              + str(total_ganadas[3] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerDe(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, PlayerDe], atack_models=[None, None, None])
        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerDe]:" + str(total_ganadas) + " -> "
              + str(total_ganadas[3] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerDd(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        model = load_model("../../datos/modelos/estimacion_ataque_defensa.mod")
        modelos = ModelContainer(ataque=model)

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, PlayerDd],
                           atack_models=[None, None, modelos])
        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerDd]:" + str(total_ganadas) + " -> "
              + str(total_ganadas[3] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerId(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        model = load_model("../../datos/modelos/estimacion_ini_partida.mod")
        modelos = ModelContainer(inicializacion=model)

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, PlayerId],
                           atack_models=[None, None, modelos])

        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerId]:" + str(total_ganadas)
              + " -> " + str(total_ganadas[3] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerRd(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        model = load_model("../../datos/modelos/estimacion_refuerzo_partida.mod")
        modelos = ModelContainer(refuerzo=model)

        rd.seed(1)
        arbitro = CArbitro(player_class=[PlayerRd, CRandomPlayer, CRandomPlayer],
                           atack_models=[modelos, None, None])

        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerRd]:" + str(total_ganadas)
              + " -> " + str(total_ganadas[1] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerBd(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        model = load_model("../../datos/modelos/estimacion_batalla_partida.mod")

        modelos = ModelContainer(batalla=model)

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, PlayerBd],
                           atack_models=[None, None, modelos])

        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerBd]:" + str(total_ganadas)
              + " -> " + str(total_ganadas[3] / sum(total_ganadas)))

    def testCArbitroAleatorioVsPlayerMd(self):
        # Comprobamos la creación de 100 partidas
        total_ganadas = [0, 0, 0, 0]

        model = load_model("../../datos/modelos/estimacion_movimiento_partida.mod")
        modelmov = load_model("../../datos/modelos/estimacion_movimiento_partida_num_eje.mod")

        modelos = ModelContainer(mov_ejercitos=model, mov_num_ejercitos=modelmov)

        rd.seed(1)
        arbitro = CArbitro(player_class=[CRandomPlayer, CRandomPlayer, PlayerMd],
                           atack_models=[None, None, modelos])

        for partida in range(0, 10):
            jug_ganador = arbitro.play(partida)
            if jug_ganador is None:
                jug_ganador = 0
            else:
                jug_ganador += 1
            total_ganadas[jug_ganador] += 1

        print("Ganadas [tablas, Random, Random, PlayerMd]:" + str(total_ganadas)
              + " -> " + str(total_ganadas[3] / sum(total_ganadas)))


class TestClog(unittest.TestCase):

    def testClog(self):
        tst_log = Clog("../../datos/unittest/ini_partida.csv",
                       "../../datos/unittest/refuerzo_partida.csv",
                       "../../datos/unittest/batalla_partida.csv",
                       "../../datos/unittest/movimiento_ejercitos.csv")

        [paises, continentes] = Mapa.inicializa_mapa_standar()
        tst_estado_partida = CEstadoPartida({1, 2, 3}, 0, paises, continentes)

        tst_estado_partida.paises_l['0_0'].propietario = 1
        tst_log.add_inicializacion(tst_estado_partida, 1, '0_0')

        tst_estado_partida.paises_l['0_1'].propietario = 2
        tst_log.add_inicializacion(tst_estado_partida, 2, '0_1')

        tst_estado_partida.paises_l['1_0'].propietario = 0
        tst_log.add_inicializacion(tst_estado_partida, 0, '1_0')

        tst_estado_partida.paises_l['1_1'].propietario = 1
        tst_log.add_inicializacion(tst_estado_partida, 1, '1_1')

        self.assertTrue(tst_log.flush())


if __name__ == '__main__':
    unittest.main()
