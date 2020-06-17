import argparse
import sys
import numpy as np

import ng_bus
import ng_input
import train

from sklearn.metrics import classification_report

parser = argparse.ArgumentParser()

parser.add_argument("--mode", required=True, choices=["train", "eval"])
parser.add_argument("--epochs", default=5, type=int)

args = parser.parse_args()

print("args:", args)

bus = ng_bus.NeurogenBus(args.mode)
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

cli_vars = []
cli_vars += io.get_vars()
cli_vars += train.get_vars()

io.read_inputs()
X_train, y_train = io.get_train_xy()
X_test, y_test = io.get_test_xy()

print(X_train.shape)


train.do_compile()

train.print_sample_predictions(X_test, y_test)
result_of_train = train.do_train(
    X_train, y_train, X_test, y_test, args.epochs, "weights"
)
print(result_of_train.history)
# print(np.mean(result_of_train.history["val_acc"]))

train.print_sample_predictions(X_test, y_test)
