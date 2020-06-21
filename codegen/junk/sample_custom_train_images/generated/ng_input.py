import ng_config


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
        import util

        input_dir = ng_config.train_data_path
        data = util.read_train_val_images(input_dir, 1 / 255)
        data = (
            self.preprocess(*data[0], sample_count),
            self.preprocess(*data[1], None),
        )
        return data
