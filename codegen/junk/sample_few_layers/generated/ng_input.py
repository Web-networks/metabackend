import ng_config
import util


class NeurogenIO:
    def __init__(self, ng_bus):
        self.ng_bus = ng_bus

    # Returns list of CLI vars
    def get_vars(self):
        return ["train_test_ratio"]

    def read_train_data(self):
        from keras.datasets import mnist

        data = mnist.load_data()
        (self.X_train, self.y_train), (self.X_test, self.y_test) = data
        return data

    def get_train_xy(self):
        self.X_train = self.X_train.reshape(self.X_train.shape[0], 28, 28, 1)
        self.X_train = self.X_train.astype("float32")
        self.X_train /= 255
        return self.X_train[:-100], self.y_train[:-100]

    def get_test_xy(self):
        self.X_test = self.X_test.reshape(self.X_test.shape[0], 28, 28, 1)
        self.X_test = self.X_test.astype("float32")
        self.X_test /= 255
        return self.X_test[-100:], self.y_test[-100:]
