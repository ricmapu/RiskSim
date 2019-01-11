import csv
from copy import deepcopy


class Clog():
    def __init__(self, fichero_ini = None,  ficheroRefuerzo = None, ficheroPartida = None, ficheroMovimientoEjercitos = None):
        self.nombre_fich_ini = fichero_ini
        self.nombre_fich_refuerzo = ficheroRefuerzo
        self.nombre_fich_partida = ficheroPartida
        self.nombre_fich_movimiento_ejercitos = ficheroMovimientoEjercitos
        self.FaseInicializacion = list()
        self.FaseRefuerzo = list()
        self.FaseAtaque = list()
        self.FaseMovEjer = list()

    def addInicializacion(self, partida, jugadorTurno, pais_seleccionado):
        self.FaseInicializacion.append([jugadorTurno, deepcopy(partida), pais_seleccionado])

    def addRefuerzo(self, partida, jugadorTurno, pais_seleccionado):
        self.FaseRefuerzo.append([jugadorTurno, deepcopy(partida), pais_seleccionado])


    def addAtaque(self, partida , jugadorTurno , pais_atacante , pais_atacado , nro_ejercitos ):
        self.FaseAtaque.append([jugadorTurno, deepcopy(partida), pais_atacante , pais_atacado , nro_ejercitos])

    def addMovimientoEjercitos(self, partida, jugadorTurno, pais_origen, pais_destino, nro_ejercitos):
        self.FaseMovEjer.append([jugadorTurno, deepcopy(partida), pais_origen, pais_destino, nro_ejercitos])

    def flush(self, ganador):
        ret = self.saveInicializacion(ganador)

        if not ret:
            return ret

        ret = self.saveRefuerzo(ganador)
        if not ret:
            return ret

        ret = self.saveAtaque(ganador)

        if not ret:
            return ret

        ret = self.saveMovimientoEjercitos(ganador)

        return ret

    def saveInicializacion(self, ganador):
        #Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        #insertamos partida y turno
        row.append("partida")
        row.append("turno")
        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseInicializacion[0][1].paises_l.keys():
            row.append(i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseInicializacion[0][1].paises_l.keys():
            row.append("seleccionar_"+i)

        row.append("EsGanador")

        datos.append(row)

        for i in range(0, len(self.FaseInicializacion)):
            row = list()

            # insertamos partida y turno
            row.append(self.FaseInicializacion[i][1].id_partida)
            row.append(self.FaseInicializacion[i][1].nro_turno)

            #Recorremos cada pais y marcamos el jugador propietario
            for j in self.FaseInicializacion[i][1].paises_l.keys():
                if self.FaseInicializacion[i][1].paises_l[j].propietario == None:
                    row.append('')
                elif self.FaseInicializacion[i][1].paises_l[j].propietario == ganador:
                    row.append("ganador")
                else:
                    #obtenemos la diferencia entre el ganador y el turno
                    diff_turno = self.FaseInicializacion[i][1].paises_l[j].propietario - ganador
                    row.append("ganador" + str(diff_turno))

            # Recorremos cada pais y marcamos el pais seleccionado
            pais_seleccionado = self.FaseInicializacion[i][2]
            for j in self.FaseInicializacion[i][1].paises_l.keys():
                if j == pais_seleccionado:
                    row.append(1)
                else:
                    row.append(0)


            #Marcamos si es ganador o no
            if ganador == self.FaseInicializacion[i][ 0]:
                row.append(1)
            else:
                row.append(0)

            datos.append(row)


        with open(self.nombre_fich_ini, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True



    def saveRefuerzo(self, ganador):
        #Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseRefuerzo) == 0:
            return True

        # insertamos partida y turno
        row.append("partida")
        row.append("turno")

        # Recorremos cada pais y marcamos jugador
        for i in self.FaseRefuerzo[0][1].paises_l.keys():
            row.append(i)

        # Recorremos cada pais y marcamos el nro de ejercitos
        for i in self.FaseRefuerzo[0][1].paises_l.keys():
            row.append("ejercitos_"+i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseRefuerzo[0][1].paises_l.keys():
            row.append("seleccionar_"+i)

        row.append("Turno")
        row.append("EsGanador")

        datos.append(row)

        for i in range(0, len(self.FaseRefuerzo)):
            row = list()

            # insertamos partida y turno
            row.append(self.FaseRefuerzo[i][1].id_partida)
            row.append(self.FaseRefuerzo[i][1].nro_turno)

            #Recorremos cada pais y marcamos el jugador propietario
            for j in self.FaseRefuerzo[i][1].paises_l.keys():
                if self.FaseRefuerzo[i][1].paises_l[j].propietario == None:
                    row.append('')
                elif self.FaseRefuerzo[i][1].paises_l[j].propietario == ganador:
                    row.append("ganador")
                else:
                    #obtenemos la diferencia entre el ganador y el turno
                    diff_turno = self.FaseRefuerzo[i][1].paises_l[j].propietario - ganador
                    row.append("ganador" + str(diff_turno))

            # Recorremos cada pais y marcamos el pais seleccionado
            for j in self.FaseRefuerzo[i][1].paises_l.keys():
                    row.append(self.FaseRefuerzo[i][1].paises_l[j].nro_ejercitos)

            # Recorremos cada pais y marcamos el pais seleccionado
            pais_atacante = self.FaseRefuerzo[i][2]
            for j in self.FaseRefuerzo[i][1].paises_l.keys():
                if j == pais_atacante:
                    row.append(1)
                else:
                    row.append(0)

            #Marcamos si es ganador o no
            if ganador == self.FaseRefuerzo[i][ 0]:
                row.append("ganador")
                row.append(1)
            else:
                diff_turno = self.FaseRefuerzo[i][0] - ganador
                row.append("ganador" + str(diff_turno))

                row.append(0)

            datos.append(row)


        with open(self.nombre_fich_refuerzo, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

    def saveAtaque(self, ganador):
        #Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseAtaque) == 0:
            return True

        # insertamos partida y turno
        row.append("partida")
        row.append("turno")

        # Recorremos cada pais y marcamos jugador
        for i in self.FaseAtaque[0][1].paises_l.keys():
            row.append(i)

        # Recorremos cada pais y marcamos el nro de ejercitos
        for i in self.FaseAtaque[0][1].paises_l.keys():
            row.append("ejercitos_"+i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseAtaque[0][1].paises_l.keys():
            row.append("atacante_"+i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseAtaque[0][1].paises_l.keys():
            row.append("atacado_"+i)


        row.append("Turno")

        row.append("EsGanador")

        datos.append(row)

        for i in range(0, len(self.FaseAtaque)):
            row = list()

            # insertamos partida y turno
            row.append(self.FaseAtaque[i][1].id_partida)
            row.append(self.FaseAtaque[i][1].nro_turno)

            #Recorremos cada pais y marcamos el jugador propietario
            for j in self.FaseAtaque[i][1].paises_l.keys():
                if self.FaseAtaque[i][1].paises_l[j].propietario == None:
                    row.append('')
                elif self.FaseAtaque[i][1].paises_l[j].propietario == ganador:
                    row.append("ganador")
                else:
                    #obtenemos la diferencia entre el ganador y el turno
                    diff_turno = self.FaseAtaque[i][1].paises_l[j].propietario - ganador
                    row.append("ganador" + str(diff_turno))

            # Recorremos cada pais y ponemos el nro de ejercitos
            for j in self.FaseAtaque[i][1].paises_l.keys():
                    row.append(self.FaseAtaque[i][1].paises_l[j].nro_ejercitos)

            # Recorremos cada pais y marcamos el pais atacante
            pais_seleccionado = self.FaseAtaque[i][2]
            for j in self.FaseAtaque[i][1].paises_l.keys():
                if j == pais_seleccionado:
                    row.append(1)
                else:
                    row.append(0)

            # Recorremos cada pais y marcamos el pais atacado
            pais_atacado = self.FaseAtaque[i][3]
            for j in self.FaseAtaque[i][1].paises_l.keys():
                if j == pais_atacado:
                    row.append(1)
                else:
                    row.append(0)


            #Marcamos si es ganador o no
            if ganador == self.FaseAtaque[i][ 0]:
                row.append("ganador")
                row.append(1)
            else:
                diff_turno = self.FaseAtaque[i][0] - ganador
                row.append("ganador" + str(diff_turno))

                row.append(0)

            datos.append(row)


        with open(self.nombre_fich_partida, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

    def saveMovimientoEjercitos(self, ganador):
        # Creamos una lista con los campos a guardar
        datos = list()
        row = list()

        if len(self.FaseMovEjer) == 0:
            return True

        # insertamos partida y turno
        row.append("partida")
        row.append("turno")

        # Recorremos cada pais y marcamos jugador
        for i in self.FaseMovEjer[0][1].paises_l.keys():
            row.append(i)

        # Recorremos cada pais y marcamos el nro de ejercitos
        for i in self.FaseMovEjer[0][1].paises_l.keys():
            row.append("ejercitos_" + i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseMovEjer[0][1].paises_l.keys():
            row.append("origen_ejer_" + i)

        # Recorremos cada pais y marcamos el jugador
        for i in self.FaseMovEjer[0][1].paises_l.keys():
            row.append("destino_ejer_" + i)

        row.append("NroEjercitos")

        row.append("EsGanador")

        datos.append(row)

        for i in range(0, len(self.FaseMovEjer)):
            row = list()

            # insertamos partida y turno
            row.append(self.FaseMovEjer[i][1].id_partida)
            row.append(self.FaseMovEjer[i][1].nro_turno)

            # Recorremos cada pais y marcamos el jugador propietario
            for j in self.FaseMovEjer[i][1].paises_l.keys():
                if self.FaseMovEjer[i][1].paises_l[j].propietario == None:
                    row.append('')
                elif self.FaseMovEjer[i][1].paises_l[j].propietario == ganador:
                    row.append("ganador")
                else:
                    # obtenemos la diferencia entre el ganador y el turno
                    diff_turno = self.FaseMovEjer[i][1].paises_l[j].propietario - ganador
                    row.append("ganador" + str(diff_turno))

            # Recorremos cada pais y ponemos el nro de ejercitos
            for j in self.FaseMovEjer[i][1].paises_l.keys():
                row.append(self.FaseMovEjer[i][1].paises_l[j].nro_ejercitos)

            # Recorremos cada pais y marcamos el pais origen
            pais_origen = self.FaseMovEjer[i][2]
            for j in self.FaseMovEjer[i][1].paises_l.keys():
                if j == pais_origen:
                    row.append(1)
                else:
                    row.append(0)

            # Recorremos cada pais y marcamos el pais destino
            pais_destino = self.FaseMovEjer[i][3]
            for j in self.FaseMovEjer[i][1].paises_l.keys():
                if j == pais_destino:
                    row.append(1)
                else:
                    row.append(0)

            # Marcamos si es ganador o no
            if ganador == self.FaseMovEjer[i][0]:
                row.append("ganador")
                row.append(1)
            else:
                diff_turno = self.FaseMovEjer[i][0] - ganador
                row.append("ganador" + str(diff_turno))

                row.append(0)

            datos.append(row)

        with open(self.nombre_fich_movimiento_ejercitos, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, csv.excel)
            csvwriter.writerows(datos)

        return True

