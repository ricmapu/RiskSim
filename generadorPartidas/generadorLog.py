import csv
from copy import deepcopy


class Clog:
    max_num_records = 1000

    def __init__(self, fichero_ini=None, fichero_refuerzo=None,
                 fichero_partida=None, fichero_movimiento_ejercitos=None):
        self.nombre_fich_ini = fichero_ini
        self.nombre_fich_refuerzo = fichero_refuerzo
        self.nombre_fich_partida = fichero_partida
        self.nombre_fich_movimiento_ejercitos = fichero_movimiento_ejercitos
        self.FaseInicializacion = list()
        self.FaseRefuerzo = list()
        self.FaseAtaque = list()
        self.FaseMovEjer = list()

        self.FaseInicializacion_tmp = list()
        self.FaseRefuerzo_tmp = list()
        self.FaseAtaque_tmp = list()
        self.FaseMovEjer_tmp = list()
        self.cabecera_grabada = False

    def start_partida(self):
        self.FaseInicializacion_tmp = list()
        self.FaseRefuerzo_tmp = list()
        self.FaseAtaque_tmp = list()
        self.FaseMovEjer_tmp = list()

    def end_partida(self, ganador):
        if ganador is not None:
            for n, i in enumerate(self.FaseInicializacion_tmp):
                self.FaseInicializacion_tmp[n][3] = ganador
            self.FaseInicializacion += self.FaseInicializacion_tmp

            for n, i in enumerate(self.FaseRefuerzo_tmp):
                self.FaseRefuerzo_tmp[n][3] = ganador
            self.FaseRefuerzo += self.FaseRefuerzo_tmp

            for n, i in enumerate(self.FaseAtaque_tmp):
                self.FaseAtaque_tmp[n][5] = ganador
            self.FaseAtaque += self.FaseAtaque_tmp

            for n, i in enumerate(self.FaseMovEjer_tmp):
                self.FaseMovEjer_tmp[n][5] = ganador
            self.FaseMovEjer += self.FaseMovEjer_tmp

        if len(self.FaseInicializacion) > self.max_num_records or  \
                len(self.FaseRefuerzo) > self.max_num_records or  \
                len(self.FaseAtaque) > self.max_num_records or  \
                len(self.FaseMovEjer) > self.max_num_records:
            # Alcanzamos el tope, grabamos
            self.flush()
            self.cabecera_grabada = True

    def add_inicializacion(self, partida, jugador_turno, pais_seleccionado):
        self.FaseInicializacion_tmp.append([jugador_turno, deepcopy(partida), pais_seleccionado, None])

    def add_refuerzo(self, partida, jugador_turno, pais_seleccionado):
        self.FaseRefuerzo_tmp.append([jugador_turno, deepcopy(partida), pais_seleccionado, None])

    def add_ataque(self, partida, jugador_turno, pais_atacante=None, pais_atacado=None,
                   nro_ejercitos=None, pasar=False):
        if pasar:
            self.FaseAtaque_tmp.append([jugador_turno, deepcopy(partida), None, None, None, None])
        else:
            self.FaseAtaque_tmp.append([jugador_turno, deepcopy(partida), pais_atacante, pais_atacado, nro_ejercitos,
                                        None])

    def add_movimiento_ejercitos(self, partida, jugador_turno, pais_origen=None, pais_destino=None, nro_ejercitos=None,
                                 pasar=False):
        if pasar:
            self.FaseMovEjer_tmp.append([jugador_turno, deepcopy(partida), None, None, None, None])
        else:
            self.FaseMovEjer_tmp.append([jugador_turno, deepcopy(partida), pais_origen, pais_destino, nro_ejercitos,
                                         None])

    def flush(self):
        if self.nombre_fich_refuerzo is not None:
            ret = self.save_inicializacion()

            if not ret:
                return ret

            self.FaseInicializacion = list()

        if self.nombre_fich_refuerzo is not None:
            ret = self.save_refuerzo()

            if not ret:
                return ret
        self.FaseRefuerzo = list()

        if self.nombre_fich_partida is not None:
            ret = self.save_ataque()

            if not ret:
                return ret

        self.FaseAtaque = list()

        if self.nombre_fich_movimiento_ejercitos is not None:
            ret = self.save_movimiento_ejercitos()

            if not ret:
                return ret

        self.FaseMovEjer = list()

        return True

    def save_inicializacion(self):
        # Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseInicializacion) > 0:
            if not self.cabecera_grabada:
                # insertamos partida y turno
                row.append("partida")
                row.append("turno")
                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseInicializacion[0][1].paises_l.keys()):
                    row.append("propietario_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseInicializacion[0][1].paises_l.keys()):
                    row.append("seleccionar_" + i)

                row.append("Jugador")
                row.append("EsGanador")

                datos.append(row)

            for i in range(0, len(self.FaseInicializacion)):
                row = list()

                # insertamos partida y turno
                row.append(self.FaseInicializacion[i][1].id_partida)
                row.append(self.FaseInicializacion[i][1].nro_turno)

                # Recorremos cada pais y marcamos el jugador propietario
                for j in sorted(self.FaseInicializacion[i][1].paises_l.keys()):
                    if self.FaseInicializacion[i][1].paises_l[j].propietario is None:
                        row.append('')
                    else:
                        row.append(self.FaseInicializacion[i][1].paises_l[j].propietario)

                # Recorremos cada pais y marcamos el pais seleccionado
                pais_seleccionado = self.FaseInicializacion[i][2]
                for j in sorted(self.FaseInicializacion[i][1].paises_l.keys()):
                    if j == pais_seleccionado:
                        row.append(1)
                    else:
                        row.append(0)

                # Marcamos el jugador actual
                row.append(str(self.FaseInicializacion[i][0]))

                # Marcamos si es ganador o no y el jugador
                if self.FaseInicializacion[i][3] == self.FaseInicializacion[i][0]:
                    row.append(1)
                else:
                    row.append(0)

                datos.append(row)

        if self.cabecera_grabada:
            tipo_grabacion = 'a'
        else:
            tipo_grabacion = 'w'

        with open(self.nombre_fich_ini, tipo_grabacion, newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

    def save_refuerzo(self):
        # Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseRefuerzo) > 0:
            if not self.cabecera_grabada:
                # insertamos partida y turno
                row.append("partida")
                row.append("turno")

                # Recorremos cada pais y marcamos jugador
                for i in sorted(self.FaseRefuerzo[0][1].paises_l.keys()):
                    row.append(i)

                # Recorremos cada pais y marcamos el nro de ejercitos
                for i in sorted(self.FaseRefuerzo[0][1].paises_l.keys()):
                    row.append("ejercitos_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseRefuerzo[0][1].paises_l.keys()):
                    row.append("seleccionar_" + i)

                row.append("Jugador")
                row.append("EsGanador")

                datos.append(row)

            for i in range(0, len(self.FaseRefuerzo)):
                row = list()

                # insertamos partida y turno
                row.append(self.FaseRefuerzo[i][1].id_partida)
                row.append(self.FaseRefuerzo[i][1].nro_turno)

                # Recorremos cada pais y marcamos el jugador propietario
                for j in sorted(self.FaseRefuerzo[i][1].paises_l.keys()):
                    if self.FaseRefuerzo[i][1].paises_l[j].propietario is None:
                        row.append('')
                    else:
                        row.append(self.FaseRefuerzo[i][1].paises_l[j].propietario)

                # Recorremos cada pais y marcamos el pais seleccionado
                for j in sorted(self.FaseRefuerzo[i][1].paises_l.keys()):
                    row.append(self.FaseRefuerzo[i][1].paises_l[j].nro_ejercitos)

                # Recorremos cada pais y marcamos el pais seleccionado
                pais_atacante = self.FaseRefuerzo[i][2]
                for j in sorted(self.FaseRefuerzo[i][1].paises_l.keys()):
                    if j == pais_atacante:
                        row.append(1)
                    else:
                        row.append(0)

                # Marcamos si es ganador o no
                row.append(self.FaseRefuerzo[i][0])

                if self.FaseRefuerzo[i][3] == self.FaseRefuerzo[i][0]:
                    row.append(1)
                else:
                    row.append(0)

                datos.append(row)

        if self.cabecera_grabada:
            tipo_grabacion = 'a'
        else:
            tipo_grabacion = 'w'

        with open(self.nombre_fich_refuerzo, tipo_grabacion, newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

    def save_ataque(self):
        # Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseAtaque) > 0:
            if not self.cabecera_grabada:
                # insertamos partida y turno
                row.append("partida")
                row.append("nro_turno")

                # Recorremos cada pais y marcamos jugador
                for i in sorted(self.FaseAtaque[0][1].paises_l.keys()):
                    row.append(i)

                # Recorremos cada pais y marcamos el nro de ejercitos
                for i in sorted(self.FaseAtaque[0][1].paises_l.keys()):
                    row.append("ejercitos_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseAtaque[0][1].paises_l.keys()):
                    row.append("atacante_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseAtaque[0][1].paises_l.keys()):
                    row.append("atacado_" + i)

                row.append("Jugador")
                row.append("EsGanador")

                datos.append(row)

            for i in range(0, len(self.FaseAtaque)):
                row = list()

                # insertamos partida y turno
                row.append(self.FaseAtaque[i][1].id_partida)
                row.append(self.FaseAtaque[i][1].nro_turno)

                # Recorremos cada pais y marcamos el jugador propietario
                for j in sorted(self.FaseAtaque[i][1].paises_l.keys()):
                    if self.FaseAtaque[i][1].paises_l[j].propietario is None:
                        row.append('')
                    else:
                        row.append(self.FaseAtaque[i][1].paises_l[j].propietario)

                # Recorremos cada pais y ponemos el nro de ejercitos
                for j in sorted(self.FaseAtaque[i][1].paises_l.keys()):
                    row.append(self.FaseAtaque[i][1].paises_l[j].nro_ejercitos)

                # Recorremos cada pais y marcamos el pais atacante
                pais_seleccionado = self.FaseAtaque[i][2]
                for j in sorted(self.FaseAtaque[i][1].paises_l.keys()):
                    if j == pais_seleccionado:
                        row.append(1)
                    else:
                        row.append(0)

                # Recorremos cada pais y marcamos el pais atacado
                pais_atacado = self.FaseAtaque[i][3]
                for j in sorted(self.FaseAtaque[i][1].paises_l.keys()):
                    if j == pais_atacado:
                        row.append(1)
                    else:
                        row.append(0)

                row.append(self.FaseAtaque[i][0])

                # Marcamos si es ganador o no
                if self.FaseAtaque[i][5] == self.FaseAtaque[i][0]:
                    row.append(1)
                else:
                    row.append(0)

                datos.append(row)

        if self.cabecera_grabada:
            tipo_grabacion = 'a'
        else:
            tipo_grabacion = 'w'

        with open(self.nombre_fich_partida, tipo_grabacion, newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

    def save_movimiento_ejercitos(self):
        # Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseMovEjer) > 0:
            if not self.cabecera_grabada:
                # insertamos partida y turno
                row.append("partida")
                row.append("turno")

                # Recorremos cada pais y marcamos jugador
                for i in sorted(self.FaseMovEjer[0][1].paises_l.keys()):
                    row.append(i)

                # Recorremos cada pais y marcamos el nro de ejercitos
                for i in sorted(self.FaseMovEjer[0][1].paises_l.keys()):
                    row.append("ejercitos_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseMovEjer[0][1].paises_l.keys()):
                    row.append("origen_ejer_" + i)

                # Recorremos cada pais y marcamos el jugador
                for i in sorted(self.FaseMovEjer[0][1].paises_l.keys()):
                    row.append("destino_ejer_" + i)

                row.append("NroEjercitos")
                row.append("Jugador")
                row.append("EsGanador")

                datos.append(row)

            for i in range(0, len(self.FaseMovEjer)):
                row = list()

                # insertamos partida y turno
                row.append(self.FaseMovEjer[i][1].id_partida)
                row.append(self.FaseMovEjer[i][1].nro_turno)

                # Recorremos cada pais y marcamos el jugador propietario
                for j in sorted(self.FaseMovEjer[i][1].paises_l.keys()):
                    if self.FaseMovEjer[i][1].paises_l[j].propietario is None:
                        row.append('')
                    else:
                        row.append(self.FaseMovEjer[i][1].paises_l[j].propietario)

                # Recorremos cada pais y ponemos el nro de ejercitos
                for j in sorted(self.FaseMovEjer[i][1].paises_l.keys()):
                    row.append(self.FaseMovEjer[i][1].paises_l[j].nro_ejercitos)

                # Recorremos cada pais y marcamos el pais origen
                pais_origen = self.FaseMovEjer[i][2]
                for j in sorted(self.FaseMovEjer[i][1].paises_l.keys()):
                    if j == pais_origen:
                        row.append(1)
                    else:
                        row.append(0)

                # Recorremos cada pais y marcamos el pais destino
                pais_destino = self.FaseMovEjer[i][3]
                for j in sorted(self.FaseMovEjer[i][1].paises_l.keys()):
                    if j == pais_destino:
                        row.append(1)
                    else:
                        row.append(0)

                # indicamos el nro de ejercitos a mover
                row.append(self.FaseMovEjer[i][4])

                # indicamos el jugador
                row.append(str(self.FaseMovEjer[i][0]))

                # Marcamos si es ganador o no
                if self.FaseMovEjer[i][5] == self.FaseMovEjer[i][0]:
                    row.append(1)
                else:
                    row.append(0)

                datos.append(row)

        if self.cabecera_grabada:
            tipo_grabacion = 'a'
        else:
            tipo_grabacion = 'w'

        with open(self.nombre_fich_movimiento_ejercitos, tipo_grabacion, newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True
