
from numpy.random import randint, shuffle
from numpy import sort

def simula_ataque(nro_atacantes, nro_defensores):
    #simula un ataque entre atacantes y defensores
    #devuelve el nro de ejercitos derrotados

    # print("   Atacamos " + str(nro_atacantes) + " a " + str(nro_defensores))

    #tiramos los dados del atacantes
    tirada_atacante = sort(randint(1,6, size = nro_atacantes ))[::-1]
    tirada_defensor = sort(randint(1,6, size = nro_defensores))[::-1]

    # print ("    atacantes" + str(tirada_atacante))
    # print ("    defensores" + str(tirada_defensor))

    comparaciones = min(tirada_atacante.size, tirada_defensor.size)

    perdida_atacantes = 0
    perdida_defensores = 0

    for i in range(0, comparaciones):
        if (tirada_defensor[i] >= tirada_atacante[i]):
            perdida_atacantes +=1
        else:
            perdida_defensores += 1

    # print("   Perdidas " + str(perdida_atacantes) + " a " + str(perdida_defensores))

    return [perdida_atacantes, perdida_defensores]

def simula_batalla(nro_atacantes, nro_defensores):
    #simula una batalla de Risk hasta que uno de los dos gana
    #devuelve si gana el atacate

    #Calculamos el nro de atacantes
    if nro_atacantes > 2:
        a = randint(1, min(3,nro_atacantes - 1))
    else:
        a = nro_atacantes - 1

    if nro_defensores >1:
        b = randint(1, 2)
    else:
        b = 1

    result = simula_ataque(a, b)
    nro_atacantes -= result[0]
    nro_defensores -= result[1]

    # print("  Total Fuerzas:" +str(nro_atacantes) + " "+ str(nro_defensores))

    if nro_atacantes == 1:
        return False
    if nro_defensores == 0:
        return True

    return simula_batalla(nro_atacantes, nro_defensores)

def genera_fichero_sim(nombre_fichero, nro_simulaciones = 1000, max_atacantes = 20, max_defensores = 20):
    file = open(nombre_fichero, 'w')
    file.write("nro_atacantes;nro_defensores;atacante_ganador\n")


    for i in range(1, nro_simulaciones):
        nro_atacantes = randint(2, max_atacantes)
        nro_defensores = randint(1, max_defensores)
        result = simula_batalla(nro_atacantes, nro_defensores)
        file.write(str(nro_atacantes)+";"+str(nro_defensores)+";")
        if result:
            file.write("1\n")
        else:
            file.write("0\n")


    file.close()

atacantes = 20
defensores = 20
print ("Ataque:")
print ("Atacamos con " + str(atacantes) +  " a " + str(defensores))
result = simula_ataque(atacantes, defensores)

print ("Atacantes:"  + str(atacantes - result[0]))
print ("Defensores:" + str(defensores - result[1]))

print ("Batalla:")
print ("Atacamos con " + str(atacantes) +  " a " + str(defensores))

if simula_batalla(atacantes, defensores):
    print ("Gana atacantes")
else:
    print("Gana defensores")

genera_fichero_sim("../datos/risk_battle_train.csv", 800000)
genera_fichero_sim("../datos/risk_battle_eval.csv", 100000)
genera_fichero_sim("../datos/risk_battle_test.csv", 100000)

