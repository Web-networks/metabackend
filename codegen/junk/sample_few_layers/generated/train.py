import operator
import os

from tensorflow.keras.callbacks import ModelCheckpoint

from model import init_model


class TrainController:
    def __init__(self):
        self.model = init_model()

    def do_epoch(self):
        pass

    def get_vars(self):
        return ["epochs"]

    def do_compile(self):
        self.model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"],
        )

    def do_train(self, X_train, y_train, X_val, y_val, epochs, weights_filename):
        if not os.path.exists("weights"):
            os.makedirs("weights")

        weights_file = "weights/" + weights_filename + ".h5"
        callback = ModelCheckpoint(
            weights_file, monitor="acc", mode="max", save_best_only=True
        )
        result_train = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=[callback],
        )
        return result_train

    def print_sample_predictions(self, X_test, y_test):
        y_pred = self.model.predict(X_test[:10])
        print("i", "real", "pred", "prob", sep="\t")
        for i, pred in enumerate(y_pred):
            pred, prob = max(enumerate(pred), key=operator.itemgetter(1))
            print(i, y_test[i], pred, prob, sep="\t")
