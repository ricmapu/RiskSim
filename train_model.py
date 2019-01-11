# -*- coding: utf-8 -*-
"""

"""
import math
import numpy as np
from numpy import genfromtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras import optimizers
import matplotlib.pyplot as plt


def load_data( filename):
    xcols = (0,1)
    xdata = genfromtxt(filename, delimiter=';', skip_header = 1, dtype = int,
                         usecols = xcols)
    
    ydata = genfromtxt(filename, delimiter=';', skip_header = 1, dtype = int,
                         usecols = 2)

    return [xdata, ydata]


def show_example (index,classes, expected_y,  num_output):
    plt.bar(np.arange(num_output), classes[index],)
    plt.show()
    print ("Max value:", np.argmax(classes[index]))
    
    
    plt.bar(np.arange(num_output), expected_y[index])
    plt.show()
    print ("Max value:", np.argmax(expected_y[index]))

    
def model1(xdata_train, ydata_train, xdata_eval , ydata_eval, verbose_param = 1 ):
    model = Sequential()

    model.add(Dense(units=6, activation='sigmoid', input_dim=2))
    model.add(Dense(units=3, activation='sigmoid'))
    model.add(Dense(units=1, activation='softmax'))
    
    sgd = optimizers.SGD()

    model.compile(loss='binary_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])
    
    
    earlyStopping=EarlyStopping(monitor='val_loss', patience=10)

    model.fit(xdata_train, ydata_train, 
                        validation_data=(xdata_eval, ydata_eval),
                        epochs = 300, batch_size = 32, verbose = verbose_param,
                        callbacks=[earlyStopping])

    return model
    


if __name__ == "__main__":
    verbose = 1

    [xdata_train, ydata_train] = load_data('../datos/risk_battle_train.csv')
    [xdata_eval , ydata_eval] = load_data('../datos/risk_battle_eval.csv')
    [xdata_test , ydata_test] = load_data('../datos/risk_battle_test.csv')
     
    model = model1(xdata_train, ydata_train, xdata_eval , ydata_eval, verbose )

    loss_and_metrics = model.evaluate(xdata_eval, ydata_eval)
    print("Model1----")
    print('Test loss:', loss_and_metrics[0])
    print('Test accuracy:', loss_and_metrics[1])
    

#    classes = model3.predict(xdata2_test, batch_size=128)
#    show_example (1, classes, ydata2_test, num_output)