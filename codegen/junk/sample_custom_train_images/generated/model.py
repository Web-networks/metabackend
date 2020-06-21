from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten

import ng_config


def init_model():
    model = Sequential()
    model.add(Input(shape=ng_config.input_shape))
    model.add(Flatten())
    model.add(Dense(units=10, activation="softmax",))
    return model
