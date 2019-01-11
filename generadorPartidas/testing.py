import unittest
import numpy.random as rd

from ClasesBasicas import CPais, CContinente
import Mapa
from generadorPartidas.arbitro import CArbitro
from generadorPartidas.generadorLog import Clog
from generadorPartidas.EstadoPartida import CEstadoPartida
from generadorPartidas.RandomPlayer import CRandomPlayer



class CPaisTesting(unittest.TestCase):

    def test_nombre(self):
        pais = CPais ("AustraliaOccidental")
        self.assertEqual(pais.nombre, 'AustraliaOccidental')

class CContinenteTesting(unittest.TestCase):

    def test_nombre(self):
        continente = CContinente( "Australia")
        self.assertEqual(continente.nombre, "Australia")

class MapTestint(unittest.TestCase):

    def testInicializaMapaStandar(self):
        [paises, continentes] = Mapa.InicializaMapaStandar()

        self.assertEqual(len(paises)      , 4)
        self.assertEqual(len(continentes) , 1)

class TestCRandomPlayer(unittest.TestCase):
    def testCRandomPlayer(self):
        [paises, continentes] = Mapa.InicializaMapaStandar()
        tstEstadoPartida = CEstadoPartida({1, 2, 3}, 0, paises, continentes, 0);

        tstEstadoPartida.paises_l['0_0'].propietario = 1
        tstEstadoPartida.paises_l['0_0'].nro_ejercitos = 1

        tstEstadoPartida.paises_l['0_1'].propietario = 1
        tstEstadoPartida.paises_l['0_1'].nro_ejercitos = 1

        tstEstadoPartida.paises_l['1_0'].propietario = 2
        tstEstadoPartida.paises_l['1_0'].nro_ejercitos = 1

        tstEstadoPartida.paises_l['1_1'].propietario = 1
        tstEstadoPartida.paises_l['1_1'].nro_ejercitos = 1

        tstPlayer =  CRandomPlayer(1)

        self.assertIsNone(tstPlayer.Ataque(tstEstadoPartida))


        tstEstadoPartida.paises_l['0_0'].propietario = 1
        tstEstadoPartida.paises_l['0_0'].nro_ejercitos = 2

        tstEstadoPartida.paises_l['0_1'].propietario = 1
        tstEstadoPartida.paises_l['0_1'].nro_ejercitos = 1

        tstEstadoPartida.paises_l['1_0'].propietario = 2
        tstEstadoPartida.paises_l['1_0'].nro_ejercitos = 1

        tstEstadoPartida.paises_l['1_1'].propietario = 1
        tstEstadoPartida.paises_l['1_1'].nro_ejercitos = 1

        tstPlayer = CRandomPlayer(1)

        result = tstPlayer.Ataque(tstEstadoPartida)

        if (result is not None):
            result = result


class TestCArbitro(unittest.TestCase):

    def testCArbitro(self):

        rd.seed(3)

        arbitro = CArbitro()

        result = arbitro.play(0)


    def testCArbitroyLog(self):
        arbitro = CArbitro()

        tstLog = Clog( "../../datos/unittest/ini_partida2.csv",
                       "../../datos/unittest/refuerzo_partida2.csv",
                       "../../datos/unittest/batalla_partida2.csv",
                       "../../datos/unittest/movimiento_ejercitos2.csv")

        rd.seed(1)

        arbitro.setLog(tstLog)
        ganador = arbitro.play(0)
        self.assertTrue(tstLog.flush(1))

    def testCArbitroMultiplePartidas(self):
        #Comprobamos la creación de 100 partidas
        arbitro = CArbitro()

        tstLog = Clog("../../datos/unittest/ini_partida3.csv",
                      "../../datos/unittest/refuerzo_partida3.csv",
                      "../../datos/unittest/batalla_partida3.csv",
                      "../../datos/unittest/movimiento_ejercitos3.csv")

        rd.seed(1)

        arbitro.setLog(tstLog)

        for partida in range(0, 10):
            print ("partida:" + str(partida))
            ganador = arbitro.play(partida)
        self.assertTrue(tstLog.flush(1))



class TestClog(unittest.TestCase):

     def testClog(self):
         tstLog = Clog( "../../datos/unittest/ini_partida.csv",
                        "../../datos/unittest/refuerzo_partida.csv",
                        "../../datos/unittest/batalla_partida.csv",
                        "../../datos/unittest/movimiento_ejercitos.csv")

         [paises, continentes] = Mapa.InicializaMapaStandar()
         tstEstadoPartida = CEstadoPartida({1,2,3} ,  0, paises, continentes);

         tstEstadoPartida.paises_l['0_0'].propietario = 1
         tstLog.addInicializacion(tstEstadoPartida, 1, '0_0')

         tstEstadoPartida.paises_l['0_1'].propietario = 2
         tstLog.addInicializacion(tstEstadoPartida, 2, '0_1')

         tstEstadoPartida.paises_l['1_0'].propietario = 0
         tstLog.addInicializacion(tstEstadoPartida, 0, '1_0')

         tstEstadoPartida.paises_l['1_1'].propietario = 1
         tstLog.addInicializacion(tstEstadoPartida, 1, '1_1')

         self.assertTrue(tstLog.flush(2))


if __name__ == '__main__':
    unittest.main()