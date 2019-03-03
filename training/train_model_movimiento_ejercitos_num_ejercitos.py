# -*- coding: utf-8 -*-
"""

"""
import numpy as np
from numpy import genfromtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras import optimizers
import matplotlib.pyplot as plt


def load_data(filename, num_paises):
    xcols = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    ycols = (18,20)

    xdata_t = genfromtxt(filename, delimiter=',', skip_header=1, dtype=int, usecols=xcols)
    ydata_t = genfromtxt(filename, delimiter=',', skip_header=1, dtype=int, usecols=ycols)

    # Filtramos registros donde se mueven ejercitos y donde el jugador es ganador
    xdata_temp = np.asarray([x for x in xdata_t if ((x[18] == 1) and (x[16] > 0))])
    ydata_temp = np.asarray([x[0] for x in ydata_t if ((x[1] == 1) and (x[0] > 0))])

    # Construcción de la matriz
    jugadores = 3

    x = np.zeros((xdata_temp.shape[0], (num_paises * jugadores) + (num_paises * 2)), dtype=int)
    y = ydata_temp

    seccion_nro_ejercitos = 4
    seccion_origen = 8
    seccion_destino = 12
    seccion_movimiento = 16

    jugador = 17

    for row in range(xdata_temp.shape[0]):
        # Construimos un vector de ordenes para cada jugador, teniendo en cuenta que el que mueve es el primer jugador
        posicion = np.zeros(3, dtype=int)
        posicion[xdata_temp[row, jugador]] = 0
        posicion[(xdata_temp[row, jugador] + 1) % 3] = num_paises
        posicion[(xdata_temp[row, jugador] + 2) % 3] = num_paises * 2

        inicio_origen = num_paises * jugadores
        inicio_destino = inicio_origen + num_paises
       # inicio_nro_ejercitos = inicio_destino + num_paises

        jugador_pasa = 1
        for pais_selec in range(0, num_paises):

            if xdata_temp[row, seccion_origen + pais_selec] == 1:
                x[row, inicio_origen + pais_selec] = 1
                jugador_pasa = 0

            if xdata_temp[row, seccion_destino + pais_selec] == 1:
                x[row, inicio_destino + pais_selec] = 1

            # Cargamos el nro de ejercitos del pais seleccionado al propietario
            x[row, posicion[xdata_temp[row, pais_selec]] + pais_selec] =\
                xdata_temp[row, seccion_nro_ejercitos + pais_selec]

        #x[row, inicio_nro_ejercitos] = xdata_temp[row, seccion_movimiento]

    return [x, y]


def show_example(index, classes, expected_y, num_output):
    plt.bar(np.arange(num_output), classes[index], )
    plt.show()
    print("Max value:", np.argmax(classes[index]))

    plt.bar(np.arange(num_output), expected_y[index])
    plt.show()
    print("Max value:", np.argmax(expected_y[index]))


def model1(xdata_train2, ydata_train2, xdata_eval2, ydata_eval2, verbose_param=1):
    model2 = Sequential()

    model2.add(Dense(units=20, kernel_initializer='normal', activation='relu', input_dim=xdata_train2.shape[1]))
    model2.add(Dense(units=30, kernel_initializer='normal',  activation='relu'))
    model2.add(Dense(units=1, kernel_initializer='normal',  activation='linear'))

    sgd = optimizers.SGD()

    model2.compile(loss='binary_crossentropy',
                   optimizer=sgd,
                   metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10)

    model2.fit(xdata_train2, ydata_train2,
               validation_data=(xdata_eval2, ydata_eval2),
               epochs=300, batch_size=32, verbose=verbose_param,
               callbacks=[early_stopping])

    return model2


if __name__ == "__main__":
    verbose = 1

    [xdata, ydata] = load_data('../../datos/logs_partidas/risk_movimiento_ejercitos.csv', 4)

    eval_size = test_size = int(xdata.shape[0] * .1)

    train_size = xdata.shape[0] - eval_size - test_size

    xdata_train = xdata[0:train_size, :]
    ydata_train = ydata[0:train_size]
    xdata_eval = xdata[0:(eval_size - 1), :]
    ydata_eval = ydata[0:(eval_size - 1)]
    xdata_test = xdata[0:(test_size - 1), :]
    ydata_test = ydata[0:(test_size - 1)]

    model = model1(xdata_train, ydata_train, xdata_test, ydata_test, verbose)

    loss_and_metrics = model.evaluate(xdata_eval, ydata_eval)
    print("Model1----")
    print('Test loss:', loss_and_metrics[0])
    print('Test accuracy:', loss_and_metrics[1])

    model.save("../../datos/modelos/estimacion_movimiento_partida_num_eje.mod")
