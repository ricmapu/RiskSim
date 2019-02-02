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


def load_data(filename):
    xcols = (2,3, 4, 5, 6, 7, 8, 9, 10)
    ycols = (11)
    xdata = genfromtxt(filename, delimiter=';', skip_header=1, dtype=int,
                       usecols=xcols)

    ydata = genfromtxt(filename, delimiter=';', skip_header=1, dtype=int,
                       usecols=ycols)

    # Tratamiento del dato

    return [xdata, ydata]


def show_example(index, classes, expected_y, num_output):
    plt.bar(np.arange(num_output), classes[index], )
    plt.show()
    print("Max value:", np.argmax(classes[index]))

    plt.bar(np.arange(num_output), expected_y[index])
    plt.show()
    print("Max value:", np.argmax(expected_y[index]))


def model1(xdata_train2, ydata_train2, xdata_eval2, ydata_eval2, verbose_param=1):
    model2 = Sequential()

    model2.add(Dense(units=6, activation='sigmoid', input_dim=2))
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

    [xdata_train, ydata_train] = load_data('../../logs_partidas/risk_ini_partida_train.csv')
    [xdata_eval, ydata_eval] = load_data('../../logs_partidas/risk_ini_partida_eval.csv')
    [xdata_test, ydata_test] = load_data('../../logs_partidas/risk_ini_partida_test.csv')

    model = model1(xdata_train, ydata_train, xdata_eval, ydata_eval, verbose)

    loss_and_metrics = model.evaluate(xdata_eval, ydata_eval)
    print("Model1----")
    print('Test loss:', loss_and_metrics[0])
    print('Test accuracy:', loss_and_metrics[1])

    model.save("../../datos/modelos/estimacion_ini_partida.mod")

