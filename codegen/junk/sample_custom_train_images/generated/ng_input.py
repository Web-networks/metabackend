import ng_config
import util


class NeurogenIO:
    def __init__(self, ng_bus):
        self.ng_bus = ng_bus

    # Returns list of CLI vars
    def get_vars(self):
        return ["train_test_ratio"]

    def preprocess(self, X, y, sample_count):
        X = X.reshape(X.shape[0], *ng_config.input_shape)
        X = X.astype("float32")
        X /= 255
        if sample_count:
            X = X[:sample_count]
            y = y[:sample_count]

        return X, y

    def read_train_data(self, sample_count):
        input_dir = ng_config.train_data_path
        return util.read_train_val_images(input_dir, (28, 28), 1 / 255)
