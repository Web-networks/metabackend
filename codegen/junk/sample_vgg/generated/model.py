from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPool2D


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
    model.add(
        Conv2D(filters=64, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2], strides=[2, 2],))
    model.add(
        Conv2D(filters=128, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=128, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2], strides=[2, 2],))
    model.add(
        Conv2D(filters=256, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=256, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=256, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2], strides=[2, 2],))
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(MaxPool2D(pool_size=[2, 2], strides=[2, 2],))
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(
        Conv2D(filters=512, kernel_size=[3, 3], padding="same", activation="relu",)
    )
    model.add(Flatten())
    model.add(Dense(units=4096, activation="relu",))
    model.add(Dense(units=4096, activation="relu",))
    model.add(Dense(units=10, activation="softmax",))
    return model
