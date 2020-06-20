from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input


def init_model():
    model = Sequential()
    model.add(Input(shape=[28, 28, 1],))
    model.add(Flatten())
    model.add(Dense(units=10, activation="softmax",))
    return model
