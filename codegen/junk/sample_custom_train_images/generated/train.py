import operator
import os
import logging

from tensorflow.keras.callbacks import ModelCheckpoint

from model import init_model
import ng_config


class TrainController:
    def __init__(self):
        self.model = init_model()

    def do_epoch(self):
        pass

    def get_vars(self):
        return ["epochs"]

    def do_compile(self):
        self.model.compile(
            loss="mean_squared_error", optimizer="adam", metrics=["accuracy"]
        )

    def try_load_weights(self, weights_file):
        if os.path.exists(weights_file):
            logging.info("Loading weights...")
            self.model.load_weights(weights_file)
            logging.info("Done!")

    def do_train(self, train_data, val_data, epochs, weights_file):
        callback = ModelCheckpoint(
            weights_file, monitor="val_accuracy", mode="max", save_best_only=True
        )
        if ng_config.use_generator_fit:
            return self.model.fit(
                *train_data,
                validation_data=val_data,
                epochs=epochs,
                batch_size=32,
                callbacks=[callback],
            )
        else:
            return self.model.fit(
                *train_data,
                validation_data=val_data,
                epochs=epochs,
                batch_size=32,
                callbacks=[callback],
            )

    def do_eval(self, eval_data):
        preds = self.model.predict(eval_data)
        self.show_predictions(preds)
        result = []
        for probs in preds:
            d, prob = max(enumerate(probs), key=operator.itemgetter(1))
            result.append(d)

        return result

    def show_predictions(self, preds):
        print("i", "real", "pred", "prob", sep="\t")
        for i, pred in enumerate(preds):
            pred, prob = max(enumerate(pred), key=operator.itemgetter(1))
            print(i, "n/a", pred, prob, sep="\t")

    def print_sample_predictions(self, Xy_test):
        if not isinstance(Xy_test, (tuple, list)):
            return
        X_test, y_test = Xy_test
        if len(X_test) == 0:
            return
        y_pred = self.model.predict(X_test[:10])
        print("i", "real", "pred", "prob", sep="\t")
        for i, pred in enumerate(y_pred):
            pred, prob = max(enumerate(pred), key=operator.itemgetter(1))
            assert isinstance(pred, (float, int))
            pred = "n/a"
            print(i, y_test[i], pred, prob, sep="\t")
