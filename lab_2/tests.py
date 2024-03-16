"""Module providing a function printing python version 3.11.8"""
import json
import logging
import math
import os
import numpy as np

from mpmath import gammainc

logging.basicConfig(level=logging.DEBUG)

pi = [0.2148, 0.3672, 0.2305, 0.1875]


def frequency_bitwise_test(bits: str) -> float:
    """
    If the sequence being checked is sufficiently random,
    then the magnitude of its P-value is close enough to one.

    parameters
    ----------
    bits : str
        A binary pseudorandom number

    returns
    -------
    p_value : float
        P is the value of the sequence being checked
    """
    sum_values = 0
    switch_case = {
        "0": -1,
        "1": 1
    }
    for bit in bits:
        sum_values += switch_case[bit]
    try:
        p_value = math.erfc(abs(sum_values) / np.sqrt(2 * len(bits)))
    except ZeroDivisionError as error:
        logging.error("Division by zero!")
    except Exception as error:
        logging.error(error)
    return p_value


def test_for_the_same_consecutive_bits(bits: str) -> float:
    """
    The main task of this test is
    to determine how often the change from "1" to "0" and back occurs.

    parameters
    ----------
    bits : str
        A binary pseudorandom number

    returns
    -------
    p_value : float
        P is the value of the sequence being checked
    """
    length = len(bits)
    share_of_units = bits.count("1") / length
    try:
        if math.fabs(share_of_units - 0.5) >= 2 / math.sqrt(length):
            return 0
        number_of_alternating = 0
        for i in range(0, length - 1):
            if bits[i] != bits[i + 1]:
                number_of_alternating += 1
        p_value = math.erfc(
            math.fabs(number_of_alternating - 2 * length * share_of_units * (1 - share_of_units)) /
            (2 * math.sqrt(2 * length) * share_of_units * (1 - share_of_units))
            )
    except ZeroDivisionError as error:
        logging.error("Division by zero!")
    except Exception as error:
        logging.error(error)
    return p_value


def longest_run_ones_test(bits: str) -> float:
    """
    A test for the longest sequence of units in a block.

    parameters
    ----------
    bits : str
        A binary pseudorandom number

    returns
    -------
    p_value : float
        P is the value of the sequence being checked
    """
    length = len(bits)
    statistics_on_lengths = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in range(0, length, 8):
        counter = 0
        max_counter = 0
        for bit in bits[i: i + 8]:
            if bit == "1":
                counter += 1
            else:
                max_counter = max(max_counter, counter)
                counter = 0
        max_counter = max(max_counter, counter)
        match max_counter:
            case 0:
                statistics_on_lengths[0] += 1
            case 1:
                statistics_on_lengths[0] += 1
            case 2:
                statistics_on_lengths[1] += 1
            case 3:
                statistics_on_lengths[2] += 1
            case _:
                statistics_on_lengths[3] += 1
    distribution_of_squares_k = 0
    for i in range(4):
        distribution_of_squares_k += (pow(statistics_on_lengths[i] - 16 * pi[i], 2) /
                                      (16 * pi[i]))
    p_value = gammainc(3 / 2, distribution_of_squares_k / 2)
    return p_value


if __name__ == "__main__":
    try:
        with open(os.path.join("lab_2", "json", "rows_of-random_bits.json"),
                  mode = "r",
                  encoding = "utf-8") as f:
            file = json.load(f)
        row_c = file["c++"]
        with open(os.path.join(file["folder"],
                               file["results"]),
                               mode = "w",
                               encoding = "utf-8") as f_for_results:
            f_for_results.write("Results for c++ generator:\n")
            f_for_results.write(
                f"\tfrequency bitwise test p-value: {frequency_bitwise_test(row_c)}\n")
            f_for_results.write(
                f"\ttest for the same consecutive bits p-value: {test_for_the_same_consecutive_bits(row_c)}\n")
            f_for_results.write(
                f"\tLongest run of ones test p-value: {longest_run_ones_test(row_c)}\n")

            row_java = file["java"]
            f_for_results.write("Results for java generator:\n")
            f_for_results.write(
                f"\tfrequency bitwise test p-value: {frequency_bitwise_test(row_java)}\n")
            f_for_results.write(
                f"\ttest for the same consecutive bits p-value: {test_for_the_same_consecutive_bits(row_java)}\n")
            f_for_results.write(
                f"\tLongest run of ones test p-value: {longest_run_ones_test(row_java)}")
    except Exception as error:
        logging.error(Exception)
