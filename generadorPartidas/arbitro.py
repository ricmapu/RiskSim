import generadorPartidas.Mapa as mapa
from generadorPartidas.RandomPlayer import CRandomPlayer
from generadorPartidas.EstadoPartida import CEstadoPartida
import numpy.random as rd
from generadorPartidas.generadorLog import Clog
from numpy import sort
from copy import deepcopy


class CArbitro:
    def __init__(self, jugadores = 3, max_turnos = 1000. ):

        self.paises = {}
        self.continentes = {}
        self.jugadores = {}
        self.num_jugadores = 0
        self.max_turnos = 0
        self.log = Clog()

        [self.paises, self.continentes] = mapa.InicializaMapaStandar()
        self.num_jugadores = jugadores

        #Cargamos el tipo de jugador base
        for jug in range(self.num_jugadores):
            self.jugadores[jug] = CRandomPlayer(jug)

        self.max_turnos = max_turnos


    def setLog(self, logObject):
        self.log = logObject

    def play(self, id_partida):
        partida = self.__InicializarTablero(id_partida)

        partidaGanada = False
        jugadorGanador = None
        turno = 0
        while (not partidaGanada) and (turno < self.max_turnos):
            turno += 1
            #for player in range(0, self.num_jugadores):
                #CambioCartas(player)
                # #partida = TurnoNuevosEjercitos(player, partida)

            for player in range (0, self.num_jugadores):
                self.__TurnoAtaque(player, partida)
                #Comprobamos si el jugador ha ganado el turno
                if partida.esGanador(player):
                    partidaGanada = True
                    jugadorGanador = player
                    break

                partida = self.__TurnoRecolocarEjercitos(player, partida)

        if partidaGanada:
            return jugadorGanador
        else:
            return None

    #Fase 0- Se inicializa el tablero y se rellenan como vacios
    def __InicializarTablero(self, id_partida):
        partida = CEstadoPartida(deepcopy(self.jugadores) ,  0,
                                 deepcopy(self.paises),
                                 deepcopy(self.continentes), id_partida)

        #Asignación incial de paises
        #Seleccionamos el primer jugador
        keyList = list(partida.jugadores_l.keys())
        rd.shuffle(keyList)
        currentPlayer = 0
        for TurnoInicio in range(0,len(partida.paises_l)):
            pais = partida.jugadores_l[keyList[currentPlayer]].seleccionarPais(estadoPartida=partida)
            assert partida.paises_l[pais].propietario is None, "Pais "+ pais +" ya seleccionado"

            #registramos la seleccion partida, jugadorTurno, pais_seleccionado
            self.log.addInicializacion(partida = partida, jugadorTurno= currentPlayer,
                                       pais_seleccionado = pais)

            with partida.paises_l[pais] as p:
                p.propietario =  keyList[currentPlayer]
                p.nro_ejercitos = 1

            currentPlayer = (currentPlayer + 1) % len(keyList)

        #Asignacion de ejercitos
        numEjercitos = 12

        for TurnoAsignacion in range (0, numEjercitos):
            for currentPlayer in range (0, len(keyList)):
                pais = partida.jugadores_l[currentPlayer].reforzarPais(partida)
                assert partida.paises_l[pais].propietario == currentPlayer, "Pais equivocado"

                #registramos la seleccion partida, jugadorTurno, pais_seleccionado
                self.log.addRefuerzo(partida = partida, jugadorTurno= currentPlayer,
                                       pais_seleccionado = pais)

                partida.paises_l[pais].nro_ejercitos += 1

        return partida


    #Fase 1- Revisar si el jugador puede cambiar cartas
    def __CambioCartas(self, player):

        pass

    #Fase 2
    def __TurnoNuevosEjercitos(self, player):
        pass

    #Fase 3.- REvisar Turno Ataque

    def __TurnoAtaque(self, player, partida):
        result = partida.jugadores_l[player].Ataque(partida)

        #Atacar hasta que el jugador se retire
        while (result is not  None):
            # TODO:Hacer codigo de comprobación de que la jugada es viable
            #el ejercito ataca; obtenemos nro de defensores
            pais_atacante = result[0]
            pais_atacado = result[1]
            jugador_atacado = partida.paises_l[pais_atacado].propietario
            nro_ejercitos = result[2]

            # registramo el ataque
            self.log.addAtaque(partida = partida, jugadorTurno= player,
                                       pais_atacante = pais_atacante,
                                       pais_atacado = pais_atacado,
                                       nro_ejercitos = nro_ejercitos)

            nro_defensores = partida.jugadores_l[jugador_atacado].Defensa(partida,pais_atacante, nro_ejercitos,pais_atacado )

            [perdida_atacantes, perdida_defensores] = self.__simula_ataque(nro_ejercitos, nro_defensores)

            partida.paises_l[pais_atacante].nro_ejercitos -= nro_ejercitos

            partida.paises_l[pais_atacado].nro_ejercitos -= perdida_defensores
            nro_ejercitos -= perdida_atacantes

            if partida.paises_l[pais_atacado].nro_ejercitos == 0:
                #se pierde el pais y es conquistado
                partida.paises_l[pais_atacado].propietario = player
                partida.paises_l[pais_atacado].nro_ejercitos = nro_ejercitos
            else:
                #no se pierde, y los ejercitos atacantes vuelve al pais
                partida.paises_l[pais_atacante].nro_ejercitos += nro_ejercitos

            result = partida.jugadores_l[player].Ataque(partida)


    #Fase 4 .- Recolocar Ejercitos
    def __TurnoRecolocarEjercitos(self, player, partida):
        result = partida.jugadores_l[player].MovimientoTropa(partida)

        #Atacar hasta que el jugador se retire

        while (result is not  None):

            [pais_origen, pais_destino, nro_ejercitos] = result

            # TODO:Hacer codigo de comprobación de que la jugada es viable
            assert partida.paises_l[pais_origen].propietario == player, "El pais origen no pertenece al jugador"
            assert partida.paises_l[pais_destino].propietario == player, "El pais destino no pertenece al jugador"
            assert partida.paises_l[pais_origen].nro_ejercitos > nro_ejercitos, "El pais origen no tiene ejercitos"

            #Movemos la tropa indicada
            partida.paises_l[pais_origen].nro_ejercitos  -= nro_ejercitos
            partida.paises_l[pais_destino].nro_ejercitos += nro_ejercitos

            self.log.addMovimientoEjercitos(partida, player, pais_origen,
                                           pais_destino, nro_ejercitos)

            result = partida.jugadores_l[player].MovimientoTropa(partida)
        return partida


    def __simula_ataque(self, nro_atacantes, nro_defensores):
        # simula un ataque entre atacantes y defensores
        # devuelve el nro de ejercitos derrotados

        # tiramos los dados del atacantes
        tirada_atacante = sort(rd.randint(1, 6, size=nro_atacantes))[::-1]
        tirada_defensor = sort(rd.randint(1, 6, size=nro_defensores))[::-1]

        comparaciones = min(tirada_atacante.size, tirada_defensor.size)

        perdida_atacantes = 0
        perdida_defensores = 0

        for i in range(0, comparaciones):
            if (tirada_defensor[i] >= tirada_atacante[i]):
                perdida_atacantes += 1
            else:
                perdida_defensores += 1

        return [perdida_atacantes, perdida_defensores]