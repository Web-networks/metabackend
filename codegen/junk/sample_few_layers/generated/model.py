from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Flatten


def init_model():
    model = Sequential()
    model.add(
        Conv2D(
            input_shape=[28, 28, 1],
            filters=64,
            kernel_size=[3, 3],
            padding="same",
            activation="relu",
        )
    )
    model.add(Flatten())
    model.add(Dense(units=64, activation="relu",))
    model.add(Dense(units=32, activation="relu",))
    model.add(Dense(units=10, activation="softmax",))
    return model
