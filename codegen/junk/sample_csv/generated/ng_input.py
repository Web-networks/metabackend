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
            if y is not None:
                y = y[:sample_count]

        return X, y

    def read_train_data(self, sample_count):
        import util

        input_file = ng_config.train_data_path
        data = util.read_csv(input_file)
        return data

    def read_eval_data(self, filenames):
        import util

        input_file = ng_config.train_data_path
        data = util.read_csv(input_file)
        return data
