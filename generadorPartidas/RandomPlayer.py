from generadorPartidas.PlayerBase import Cplayer
import numpy.random as rd

class CRandomPlayer(Cplayer):

    def seleccionarPais(self, estadoPartida):
        #Obtenemos todos los paises no asignados
        paises_libres = list()
        for pais in estadoPartida.paises_l.keys():
            if estadoPartida.paises_l[pais].propietario is None:
                paises_libres.append(pais)

        assert len(paises_libres) > 0 , "No quedan paises libres para seleccionar"

        if len(paises_libres) == 1:
            pais = 0
        else:
            pais = rd.randint(0, len(paises_libres))

        return paises_libres[pais]

    def reforzarPais(self, estadoPartida):
        #Obtenemos todos los paises no asignados
        paises_propietario = list()
        for pais in estadoPartida.paises_l.keys():
            if estadoPartida.paises_l[pais].propietario is self.propietario:
                paises_propietario.append(pais)

        assert len(paises_propietario) > 0 , "No hay paises para el propietario"

        if len(paises_propietario) == 1:
            pais =0
        else:
            pais = rd.randint(0, len(paises_propietario) )
        return paises_propietario[pais]


    def Ataque(self, estadoPartida):
        #Obtenemos todos los paises que podemos atacar
        paises_atacables = list()
        for pais in estadoPartida.paises_l.keys():
            if (estadoPartida.paises_l[pais].propietario is self.propietario) and (estadoPartida.paises_l[pais].nro_ejercitos > 1):
                #Buscamos todos los vecinos
                for vecino in estadoPartida.paises_l[pais].vecino:
                    #si el pais vecino es propiedad de otro se incluye en la lista
                    pais_candidato = estadoPartida.paises_l[vecino]
                    if pais_candidato.propietario != self.propietario:
                        #incluimos el atacante, el atacado y el nro de ejercitos a usar en la lista
                        if  estadoPartida.paises_l[pais].nro_ejercitos == 2:
                            ejercitos = 1
                        else:
                            ejercitos = rd.randint(1, estadoPartida.paises_l[pais].nro_ejercitos - 1)
                        paises_atacables.append([pais, pais_candidato.nombre, ejercitos])

        #Elegimos un pais para atacar o pasar
        paises_atacables.append(None)
        ataque = rd.randint(0, len(paises_atacables))

        return paises_atacables[ataque]

    def Defensa(self, estadoPartida, pais_atacante, nro_ejercitos_ataque, pais_atacado):
        # Todo: Comprobacion de que el pais pertene al jugador
        nro_defensores = estadoPartida.paises_l[pais_atacado].nro_ejercitos

        max_defensores = min(nro_defensores, 2)
        if max_defensores == 1:
            return max_defensores
        else:
            return rd.randint(1, max_defensores)

    def MovimientoTropa(self, estadoPartida):
        #Buscamos todos los paises con ejercitos de sobra para recolocar
        paises_candidatos = list()
        for pais in estadoPartida.paises_l.keys():
            if (estadoPartida.paises_l[pais].propietario is self.propietario) \
                    and (estadoPartida.paises_l[pais].nro_ejercitos > 1) \
                    and (len(estadoPartida.paises_l[pais].vecino) > 0):
                paises_candidatos.append(pais)

        paises_candidatos.append(None)
        candidato = rd.randint(0, len(paises_candidatos))

        if paises_candidatos[candidato] is None:
            return None

        pais_origen = paises_candidatos[candidato]

        # Obtenemos todos los vecinos del pais seleccionado
        paises_vecinos = self._getVecinos(pais_origen, estadoPartida)

        if len(paises_vecinos) == 0:
            return None

        #seleccionamos el vecino a mover
        pais_destino = paises_vecinos[rd.randint(0, len(paises_vecinos))]

        if estadoPartida.paises_l[pais_origen].nro_ejercitos == 2:
            nro_ejercitos_refuerzo = 1
        else:
            nro_ejercitos_refuerzo = rd.randint(1, estadoPartida.paises_l[pais_origen].nro_ejercitos - 1)


        return [pais_origen, pais_destino, nro_ejercitos_refuerzo]

    def _getVecinos(self, pais, estadoPartida):
        paises_visitados = list()

        self._visitar(pais, paises_visitados, estadoPartida)

        paises_visitados.remove(pais)

        return paises_visitados

    def _visitar(self, pais, paises_visitados, estadoPartida):

        if pais in paises_visitados:
            return

        paises_visitados.append(pais)
        for pais_vecino in estadoPartida.paises_l[pais].vecino:
            #Solo visitamos pais
            if estadoPartida.paises_l[pais].propietario != estadoPartida.paises_l[pais_vecino].propietario:
                continue

            self._visitar(pais_vecino, paises_visitados,estadoPartida)



