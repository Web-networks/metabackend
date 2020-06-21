from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten

import ng_config


def init_model():
    model = Sequential()
    model.add(Input(shape=ng_config.input_shape))
    model.add(
        Conv2D(filters=64, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(Flatten())
    model.add(Dense(units=64, activation="relu",))
    model.add(Dense(units=32, activation="relu",))
    model.add(Dense(units=10, activation="softmax",))
    return model
