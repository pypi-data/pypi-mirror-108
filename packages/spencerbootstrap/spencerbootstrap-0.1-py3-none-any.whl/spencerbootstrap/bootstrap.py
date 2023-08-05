from arch.bootstrap import StationaryBootstrap
from os import path
import numpy as np
import pandas as pd


def __readCSV(file_path):
    """
    Reads a csv file an returns it as a np array
    :param file: the relative path of a csv file
    :return: np array containing the csv file
    """

    # Check to make sure the path exists
    assert path.exists(file_path)

    return pd.read_csv(file_path, sep=',', header=None)


def runBootStrap(file_path, testingFlag=False):
    np_array = __readCSV(file_path)

    if testingFlag:
        print(np_array)

    bs = StationaryBootstrap(12, np_array[1])

    print(" I dont know what to do with the object returned by the StationaryBootstrap function but here is a print of it")
    print(bs)
