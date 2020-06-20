import argparse
import os
import random
import logging
import json

import ng_bus
import ng_input
import train

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.DEBUG)

log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log_handler.setFormatter(log_formatter)
root_logger.addHandler(log_handler)

parser = argparse.ArgumentParser()

# common options
parser.add_argument("--mode", required=True, choices=["train", "eval"])

# train options
parser.add_argument("--epochs", default=5, type=int)
parser.add_argument("--sample-count", default=0, type=int)
parser.add_argument("--weights", default="weights.h5")

# eval options
parser.add_argument("--eval-data")

args = parser.parse_args()

logging.debug("args: %s", args)

bus = ng_bus.NeurogenBus(args.mode)
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

if args.mode == "train":
    io.read_train_data()
    X_train, y_train = io.get_train_xy()
    if args.sample_count:
        X_train, y_train = X_train[: args.sample_count], y_train[: args.sample_count]
    X_test, y_test = io.get_test_xy()

    logging.info("train data shape: %s", X_train.shape)

train.do_compile()
train.try_load_weights(args.weights)

if args.mode == "train":
    train.print_sample_predictions(X_test, y_test)
    result_of_train = train.do_train(
        X_train, y_train, X_test, y_test, args.epochs, args.weights
    )
    logging.info("history: %s", result_of_train.history)
    # print(np.mean(result_of_train.history["val_acc"]))
    train.print_sample_predictions(X_test, y_test)
elif args.mode == "eval":
    assert args.eval_data
    logging.debug("eval content: %s", os.listdir(args.eval_data))
    print(
        json.dumps(
            {
                "eval_result": {
                    filename: random.randint(0, 9)
                    for filename in os.listdir(args.eval_data)
                }
            }
        )
    )

from keras import backend as K

K.clear_session()