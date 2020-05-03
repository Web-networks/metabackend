import argparse
import sys
import numpy as np

import ng_bus
import ng_input
import train

from sklearn.metrics import classification_report

bus = ng_bus.NeurogenBus('train')
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

cli_vars = []
cli_vars += io.get_vars()
cli_vars += train.get_vars()

parser = argparse.ArgumentParser()

# не работает пока что
# for cli_var in cli_vars:
  # parser.add_argument('--' + cli_var)

# print('args:', parser.parse_args(sys.argv))

io.read_inputs()
X_train, y_train = io.get_train_xy()
X_test, y_test = io.get_test_xy()

# надо бы как-то чтобы пробрасывалось компонентно число эпох
# пока количество эпох чисто захардкожено
train.do_compile()
result_of_train = train.do_train(X_train, y_train, X_test, y_test)
#оценка работы модели
print (np.mean(result_of_train.history["val_acc"]))
