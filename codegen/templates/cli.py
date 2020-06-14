import argparse

import ng_bus
import ng_input
import train

parser = argparse.ArgumentParser()

parser.add_argument('--mode', required=True, choices=['train', 'eval'])
parser.add_argument('--epochs', default=5, type=int)
parser.add_argument('--sample-count', default=0, type=int)
parser.add_argument('--weights', default='weights.h5')

args = parser.parse_args()

print('args:', args)

bus = ng_bus.NeurogenBus(args.mode)
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

io.read_inputs()
X_train, y_train = io.get_train_xy()
if args.sample_count:
    X_train, y_train = X_train[:args.sample_count], y_train[:args.sample_count]
X_test, y_test = io.get_test_xy()

print(X_train.shape)

train.do_compile()

train.print_sample_predictions(X_test, y_test)
result_of_train = train.do_train(X_train, y_train, X_test, y_test, args.epochs, args.weights)
print(result_of_train.history)
# print(np.mean(result_of_train.history["val_acc"]))

train.print_sample_predictions(X_test, y_test)

from keras import backend as K

K.clear_session()
