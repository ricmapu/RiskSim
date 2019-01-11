class CContinente:

    def __init__(self, pnombre):
        self.nombre = pnombre
        self.pais = list()

class CPais:
    #nombre
    #vecino
    #propietario
    #nro_ejercitos

    def __init__(self, pnombre , pvecino = list(), ppropietario = None, pnro_ejercitos = 0):
        self.nombre = pnombre
        self.vecino = pvecino
        self.propietario = ppropietario
        self.nro_ejercitos = pnro_ejercitos

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        None

