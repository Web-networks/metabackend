import ng_config


class NeurogenIO:
    def __init__(self, ng_bus):
        self.ng_bus = ng_bus

    # Returns list of CLI vars
    def get_vars(self):
        return ["train_test_ratio"]

    def bite_sample(self, X, y, sample_count):

        if sample_count:
            X = X[:sample_count]
            if y is not None:
                y = y[:sample_count]

        return X, y

    def preprocess(self, X, y, sample_count):
        X = X.reshape(X.shape[0], *ng_config.input_shape)
        X = X.astype("float32")
        X /= 255
        X, y = self.bite_sample(X, y, sample_count)
        return X, y

    def read_train_data(self, sample_count):
        import util

        input_dir = ng_config.train_data_path
        data = util.read_train_images(input_dir, 1 / 255)
        data = util.val_split(*data)
        data = (
            self.preprocess(*data[0], sample_count),
            self.preprocess(*data[1], None),
        )
        return data

    def read_eval_data(self, filenames):
        import util

        input_dir = ng_config.train_data_path
        data = util.load_images(filenames)
        data, _ = self.preprocess(data, None, None)
        return data
