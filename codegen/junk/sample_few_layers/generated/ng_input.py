class NeurogenIO:
    def __init__(self, ng_bus):
        self.ng_bus = ng_bus

    # Returns list of CLI vars
    def get_vars(self):
        return ["train_test_ratio"]

    def read_inputs(self):
        if self.ng_bus.mode == "inference":
            # TODO
            pass
        elif self.ng_bus.mode == "train":
            from keras.datasets import mnist

            (self.X_train, self.y_train), (self.X_test, self.y_test) = mnist.load_data()
        else:
            raise Exception("invalid mode: " + self.ng_bus.mode)

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
