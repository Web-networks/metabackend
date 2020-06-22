from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, Dense, Dropout, Flatten, MaxPool2D

import ng_config


def init_model():
    model = Sequential()
    model.add(Input(shape=ng_config.input_shape))
    model.add(
        Conv2D(filters=128, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(
        Conv2D(filters=128, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2],))
    model.add(
        Conv2D(filters=256, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(
        Conv2D(filters=256, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2],))
    model.add(Dropout(rate=0.25,))
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="elu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2],))
    model.add(Dropout(rate=0.25,))
    model.add(Flatten())
    model.add(Dense(units=1024, activation="elu",))
    model.add(Dropout(rate=0.5,))
    model.add(Dense(units=100, activation="softmax",))
    return model
