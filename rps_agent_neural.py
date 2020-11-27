import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

IDString = "rps"
agentHistory = ""
agentScore=0
opponentHistory = ""
opponentScore=0
mixedHistory =""
strategy = "minasi"


x_train = []
y_train = []
n_future = 1
n_past = 10
for i in range(0, len(mixedHistory) - n_past - n_future + 1):
    x_train.append(mixedHistory[i : i + n_past, 0])
    y_train.append(mixedHistory[i + n_past : i + n_past + n_future, 0])

x_train , y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0] , x_train.shape[1], 1))

EPOCHS = 500
BATCH_SIZE = 32
regressor = Sequential()regressor.add(Bidirectional(LSTM(units=30, return_sequences=True, input_shape = (x_train.shape[1], 1))))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units= n_past, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units= n_past, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units= n_past))
regressor.add(Dropout(0.2))
regressor.add(Dense(units = n_future, activation=’relu’))regressor.compile( optimizer="adam", loss="mean_squared_error", metrics=["acc"])regressor.fit ( x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)
