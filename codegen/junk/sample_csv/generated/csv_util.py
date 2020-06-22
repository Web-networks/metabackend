import pandas
import numpy as np

import ng_config

# parse feature sex
def parse_sex(val):

    # print(f'debug: value {val} for feature sex')
    if val == "male":
        return 0

    if val == "female":
        return 1

    raise ValueError(f"invalid value {val} for feature sex")


# parse feature class
def parse_class(val):

    # print(f'debug: value {val} for feature class')
    if val == "First":
        return 0

    if val == "Second":
        return 1

    if val == "Third":
        return 2

    raise ValueError(f"invalid value {val} for feature class")


# parse feature alone
def parse_alone(val):

    # print(f'debug: value {val} for feature alone')
    if val == "n":
        return 0

    if val == "y":
        return 1

    raise ValueError(f"invalid value {val} for feature alone")


# parse feature n_siblings_spouses
def parse_n_siblings_spouses(val):

    # print(f'debug: value {val} for feature n_siblings_spouses')
    return float(val)


# parse feature parch
def parse_parch(val):

    # print(f'debug: value {val} for feature parch')
    return float(val)


# parse target survived
def parse_survived(val):

    # print(f'debug: value {val} for feature survived')
    return int(val)


def read_csv(filename):

    df = pandas.read_csv(filename)
    feature_sex = map(parse_sex, df["sex"])
    feature_class = map(parse_class, df["class"])
    feature_alone = map(parse_alone, df["alone"])
    feature_n_siblings_spouses = map(parse_n_siblings_spouses, df["n_siblings_spouses"])
    feature_parch = map(parse_parch, df["parch"])
    X = np.array(
        list(
            zip(
                feature_sex,
                feature_class,
                feature_alone,
                feature_n_siblings_spouses,
                feature_parch,
            )
        )
    )
    assert X[0].shape == ng_config.input_shape
    feature_survived = map(parse_survived, df["survived"])
    y = np.array(list(feature_survived))
    print(X, y)
    return X, y
