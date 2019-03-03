import generadorPartidas.Mapa as Mapa
from generadorPartidas.EstadoPartida import CEstadoPartida
import numpy.random as rd
from generadorPartidas.generadorLog import Clog
from numpy import sort
from copy import deepcopy


class CArbitro:
    def __init__(self, player_class, atack_models, jugadores=3, max_turnos=1000.):

        self.paises = {}
        self.continentes = {}
        self.jugadores = {}
        self.num_jugadores = 0
        self.max_turnos = 0
        self.log = Clog()

        [self.paises, self.continentes] = Mapa.inicializa_mapa_standar()
        self.num_jugadores = jugadores

        # Cargamos el tipo de jugador base
        for jug in range(self.num_jugadores):
            self.jugadores[jug] = player_class[jug](jug)
            self.jugadores[jug].set_models(atack_models[jug])

        self.max_turnos = max_turnos

    def set_log(self, log_object):
        self.log = log_object

    def play(self, id_partida):

        self.log.start_partida()

        partida = self.__inicializar_tablero(id_partida)

        partida_ganada = False
        jugador_ganador = None
        turno = 0
        while (not partida_ganada) and (turno < self.max_turnos):
            turno += 1
            partida.nro_turno = turno
            # for player in range(0, self.num_jugadores):
            # CambioCartas(player)
            # #partida = TurnoNuevosEjercitos(player, partida)

            for player in range(0, self.num_jugadores):
                self.__turno_ataque(player, partida)
                # Comprobamos si el jugador ha ganado el turno
                if partida.esGanador(player):
                    partida_ganada = True
                    jugador_ganador = player
                    break

                partida = self.__turno_recolocar_ejercitos(player, partida)

        if partida_ganada:
            self.log.end_partida(jugador_ganador)
            return jugador_ganador
        else:
            self.log.end_partida(None)
            return None

    # Fase 0- Se inicializa el tablero y se rellenan como vacios
    def __inicializar_tablero(self, id_partida):
        partida = CEstadoPartida(deepcopy(self.jugadores), 0,
                                 deepcopy(self.paises),
                                 deepcopy(self.continentes), id_partida)

        # Asignación incial de paises
        # Seleccionamos el primer jugador
        # key_list = list(partida.jugadores_l.keys())
        # rd.shuffle(key_list)
        current_player = 0
        for TurnoInicio in range(0, len(partida.paises_l)):
            pais = partida.jugadores_l[current_player].seleccionar_pais(estado_partida=partida)
            assert partida.paises_l[pais].propietario is None, "Pais " + pais + " ya seleccionado"

            # registramos la seleccion partida, jugadorTurno, pais_seleccionado
            self.log.add_inicializacion(partida=partida, jugador_turno=current_player,
                                        pais_seleccionado=pais)

            with partida.paises_l[pais] as p:
                p.propietario = current_player
                p.nro_ejercitos = 1

            current_player = (current_player + 1) % 3

        # Asignacion de ejercitos
        num_ejercitos = 12

        for TurnoAsignacion in range(0, num_ejercitos):
            for current_player in range(0, 3):
                pais = partida.jugadores_l[current_player].reforzar_pais(partida)
                assert partida.paises_l[pais].propietario == current_player, "Pais equivocado"

                # registramos la seleccion partida, jugadorTurno, pais_seleccionado
                self.log.add_refuerzo(partida=partida, jugador_turno=current_player,
                                      pais_seleccionado=pais)

                partida.paises_l[pais].nro_ejercitos += 1

        return partida

    # Fase 1- Revisar si el jugador puede cambiar cartas
    def __cambio_cartas(self, player):

        pass

    # Fase 2
    def __turno_nuevos_ejercitos(self, player):
        pass

    # Fase 3.- REvisar Turno Ataque

    def __turno_ataque(self, player, partida):

        result = partida.jugadores_l[player].ataque(partida)

        if result is None:
            # El jugador no puede atacar, se retira
            return partida

        # Atacar hasta que el jugador se retire
        while result[0] is not None:
            # TODO:Hacer código de comprobación de que la jugada es viable
            # el ejército ataca; obtenemos nro de defensores
            pais_atacante = result[0]
            pais_atacado = result[1]
            jugador_atacado = partida.paises_l[pais_atacado].propietario
            nro_ejercitos = result[2]

            # registramos el ataque
            self.log.add_ataque(partida=partida, jugador_turno=player,
                                pais_atacante=pais_atacante,
                                pais_atacado=pais_atacado,
                                nro_ejercitos=nro_ejercitos)

            nro_defensores = partida.jugadores_l[jugador_atacado].defensa(partida, pais_atacante, nro_ejercitos,
                                                                          pais_atacado)

            [perdida_atacantes, perdida_defensores] = self.__simula_ataque(nro_ejercitos, nro_defensores)

            partida.paises_l[pais_atacante].nro_ejercitos -= nro_ejercitos

            partida.paises_l[pais_atacado].nro_ejercitos -= perdida_defensores
            nro_ejercitos -= perdida_atacantes

            if partida.paises_l[pais_atacado].nro_ejercitos == 0:
                # se pierde el pais y es conquistado
                partida.paises_l[pais_atacado].propietario = player
                partida.paises_l[pais_atacado].nro_ejercitos = nro_ejercitos
            else:
                # no se pierde, y los ejercitos atacantes vuelve al pais
                partida.paises_l[pais_atacante].nro_ejercitos += nro_ejercitos

            result = partida.jugadores_l[player].ataque(partida)
            if result is None:
                self.log.add_ataque(partida=partida, jugador_turno=player, pasar=True)
                # El jugador no puede atacar, pasa turno
                return partida

        # El jugador pasa y se registra
        self.log.add_ataque(partida=partida, jugador_turno=player, pasar=True)

    # Fase 4 .- Recolocar Ejercitos
    def __turno_recolocar_ejercitos(self, player, partida):

        result = partida.jugadores_l[player].movimiento_tropa(partida)
        if len(result) == 0:
            # El jugador no puede mover, pasa turno
            return partida

        # TODO:Adaptar el codigo a una lista de movimientos
        for movimiento in result:
            (pais_origen, pais_destino, nro_ejercitos) = movimiento

            if pais_origen is None:
                # Se guarda el movimiento de pasar
                self.log.add_movimiento_ejercitos(partida, player, pasar=True)
            else:
                assert partida.paises_l[pais_origen].propietario == player, "El pais origen no pertenece al jugador"
                assert partida.paises_l[pais_destino].propietario == player, "El pais destino no pertenece al jugador"
                assert partida.paises_l[pais_origen].nro_ejercitos > nro_ejercitos, "El pais origen no tiene ejercitos"

                # Movemos la tropa indicada
                partida.paises_l[pais_origen].nro_ejercitos -= nro_ejercitos
                partida.paises_l[pais_destino].nro_ejercitos += nro_ejercitos

                self.log.add_movimiento_ejercitos(partida, player, pais_origen, pais_destino, nro_ejercitos)

        return partida

    @staticmethod
    def __simula_ataque(nro_atacantes, nro_defensores):
        # simula un ataque entre atacantes y defensores
        # devuelve el nro de ejercitos derrotados

        # tiramos los dados del atacantes
        tirada_atacante = sort(rd.randint(1, 6, size=nro_atacantes))[::-1]
        tirada_defensor = sort(rd.randint(1, 6, size=nro_defensores))[::-1]

        comparaciones = min(tirada_atacante.size, tirada_defensor.size)

        perdida_atacantes = 0
        perdida_defensores = 0

        for i in range(0, comparaciones):
            if tirada_defensor[i] >= tirada_atacante[i]:
                perdida_atacantes += 1
            else:
                perdida_defensores += 1

        return [perdida_atacantes, perdida_defensores]
