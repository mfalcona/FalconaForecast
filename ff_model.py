#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:22:04 2021

@author: matthewfalcona
"""

# falcona forecast model development

#!pip install eli5
#!pip install keras

from numpy.random import seed
seed(1)
import tensorflow as tf
tf.random.set_seed(2)


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras import backend as K
K.image_data_format()

from keras.utils import np_utils

from sklearn.preprocessing import LabelEncoder

import time

import pandas as pd
import numpy as np


train = pd.read_excel('/Users/matthewfalcona/FalconaForecast/seriea_train3.25.21.xlsx')
test = pd.read_excel('/Users/matthewfalcona/FalconaForecast/seriea_test3.25.21.xlsx')
pred = pd.read_excel('/Users/matthewfalcona/FalconaForecast/seriea_pred4.23.21.xlsx')

# est predictor variables and predictor column

y_train = train.Result
y_test = test.Result
x_train = train.drop('Result', axis = 1)
x_test = test.drop('Result', axis = 1)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_train)
y_train = encoder.transform(y_train)
# convert integers to dummy variables (i.e. one hot encoded)
y_train = np_utils.to_categorical(y_train)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_test)
y_test = encoder.transform(y_test)
# convert integers to dummy variables (i.e. one hot encoded)
y_test = np_utils.to_categorical(y_test)

# defining model function

def base_model():
    model = Sequential() # for training and inference features
    model.add(Dense(400, input_dim = 24, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(.15))
    model.add(Dense(3, kernel_initializer='normal', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    return(model)


# model fitting

start = time.time()  # TRACK TIME

model = base_model()

model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs = 20, batch_size = 100, verbose = 1)

#scores = model.evaluate(x_test, y_test, verbose=0)
#print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# # MODEL - RESULTS


end = time.time()
final_time = end-start
print(final_time)

pred = pred.drop(columns = ['Date','Home','Away'])

test_acc = model.predict(x_test)

pd.DataFrame(test_acc).to_csv('/Users/matthewfalcona/FalconaForecast/test_acc.csv')


probs = model.predict(pred)

pd.DataFrame(probs).to_csv('/Users/matthewfalcona/FalconaForecast/probs.csv')

# Results
# loss: 0.9262 - accuracy: 0.5738 - val_loss: 0.9580 - val_accuracy: 0.5647
