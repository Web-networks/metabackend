import pandas
import numpy as np

import ng_config

# parse feature sex
def parse_sex(val):

    if val == "male":
        return 0

    if val == "female":
        return 1

    raise ValueError(f"invalid value {val} for feature sex")


# parse feature class
def parse_class(val):

    if val == "First":
        return 0

    if val == "Second":
        return 1

    if val == "Third":
        return 2

    raise ValueError(f"invalid value {val} for feature class")


# parse feature alone
def parse_alone(val):

    if val == "n":
        return 0

    if val == "y":
        return 1

    raise ValueError(f"invalid value {val} for feature alone")


# parse feature n_siblings_spouses
def parse_n_siblings_spouses(val):

    return float(val)


# parse feature parch
def parse_parch(val):

    return float(val)


# parse target survived
def parse_survived(val):

    return int(val)


def read_csv(filename, train_mode):

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
    if not train_mode:
        return X

    feature_survived = map(parse_survived, df["survived"])
    y = np.array(list(feature_survived))
    return X, y


def add_result_column(source_filename, result):

    assert ng_config.model["output"]["target"] == "csv"
    i = -1
    out = ""
    for line in open(source_filename):

        line = line.strip()
        if i == -1:
            line += "," + "survived_out"
        else:
            line += "," + str(result[i])

        out += line + "\n"
        i += 1

    return out
