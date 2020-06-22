from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense

import ng_config


def init_model():
    model = Sequential()
    model.add(Input(shape=ng_config.input_shape))
    model.add(Dense(units=2, activation="relu",))
    model.add(Dense(units=1, activation="relu",))
    return model
