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
    xcols = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    ycols = (15,)

    xdata_temp = genfromtxt(filename, delimiter=',', skip_header=1, dtype=int, usecols=xcols)
    ydata_temp = genfromtxt(filename, delimiter=',', skip_header=1, dtype=int, usecols=ycols)

    # Construcción de la matriz
    x = np.zeros((xdata_temp.shape[0], 16), dtype=int)
    y = ydata_temp

    seccion_prop = 0
    seccion_nro_ejercitos = 4
    seccion_seleccion = 8
    jugador = 12

    for row in range(xdata_temp.shape[0]):
        # Construimos un vector de ordenes para cada jugador, teniendo en cuenta que el que mueve es el primer jugador
        posicion = np.zeros(3, dtype=int)
        posicion[xdata_temp[row, jugador]] = 0
        posicion[(xdata_temp[row, jugador] + 1) % 3] = num_paises
        posicion[(xdata_temp[row, jugador] + 2) % 3] = num_paises * 2

        inicio_seleccion = num_paises * 3
        for pais_selec in range(0, num_paises):

            if xdata_temp[row, seccion_seleccion + pais_selec] == 1:
                x[row, inicio_seleccion + pais_selec] = 1

            # Cargamos el nro de ejercitos del pais seleccionado al propietario
            x[row, posicion[xdata_temp[row, pais_selec]] + pais_selec] = xdata_temp[row, seccion_nro_ejercitos + pais_selec]

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

    model2.add(Dense(units=6, activation='sigmoid', input_dim=xdata_train2.shape[1]))
    model2.add(Dense(units=3, activation='sigmoid'))
    model2.add(Dense(units=1, activation='sigmoid'))

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

    [xdata, ydata] = load_data('../../datos/logs_partidas/risk_refuerzo_partida.csv', 4)

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

    model.save("../../datos/modelos/estimacion_refuerzo_partida.mod")
