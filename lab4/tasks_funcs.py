"""Module providing a function printing python version 3.11.9"""
import argparse
import hashlib
import logging
import os
import multiprocessing as mp
import matplotlib.pyplot as plt

from time import time
from tqdm import tqdm

from auxiliary_operations import serialisation_card_num, open_json, Mode


logging.basicConfig(level=logging.DEBUG)


def checking_the_correctness(iins: list, middle: int, last_numbers: int, card_hash: str)->str:
    """
    Check the correctness of the card details.

    Args:
    iins: list, the list of IINs
    middle: int, the middle part of the card number
    last_numbers: int, the last numbers of the card number
    card_hash: str, the hash of the card

    Returns:
    str: The correct card number if found, None otherwise
    """
    for iin in iins:
        result = hashlib.sha256(f"{iin}{middle:0>6}{last_numbers:0>4}".encode()).hexdigest()
        if  result == card_hash:
            return f"{iin}{middle:0>6}{last_numbers:0>4}"
    return None


def card_selection(iins: list, last_numbers: int, card_hash: str, path_to_save: str)->str|None:
    """
    Select the correct card details.

    Args:
    iins: list, the list of IINs
    last_numbers: int, the last numbers of the card number
    card_hash: str, the hash of the card
    path_to_save: str, the path to save the card number

    Returns:
    str|None: The correct card number if found, None otherwise
    """
    cores = mp.cpu_count()
    with mp.Pool(processes=cores) as p:
        for result in p.starmap(checking_the_correctness,
                                [(iins, i, last_numbers, card_hash) for i in list(range(0, 1000000))]):
            if result:
                logging.debug(f'we have found {result} and have terminated pool')
                serialisation_card_num(path_to_save, result)
                p.terminate()
                return result
    return None


def algorithm_luhn(card_number: str)->bool:
    """
    Implement the Luhn algorithm.

    Args:
    card_number: str, the card number to be validated

    Returns:
    bool: True if the card number is valid, False otherwise
    """
    answer = 0
    for i in range(0, len(card_number) // 2):
        tmp = int(card_number[i+1]) * 2
        answer += int(card_number[i]) + (tmp if tmp <= 9 else tmp // 10 + tmp % 10)
    logging.debug(answer)
    return 0 == answer % 10 


def find_collisions(card_hash: str, iin: str, last_numbers: int)->None:
    """
    Find collisions in the card details.

    Args:
    card_hash: str, the hash of the card
    iin: str, the IIN of the card
    last_numbers: int, the last numbers of the card number
    """
    times = []
    for process_number in tqdm(range(1, int(1.5 * (mp.cpu_count()/2)))):
      start = time()
      with mp.Pool(process_number) as p:
        for result in p.starmap(checking_the_correctness,
                                [([iin], i, last_numbers, card_hash) for i in list(range(0, 1000000))]):
            if result:
                p.terminate()
                diff = time()-start
                times.append(diff)
    plt.ylabel('time')
    plt.xlabel('number of processes')
    plt.title('find collisions')
    plt.plot(range(1, int(1.5 * (mp.cpu_count()/2))),
             times,
             color='navy',
             linestyle = '--',
             marker='x',
             linewidth=1,
             markersize=4)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
                       '--mode',
                       type= int,
                       default= Mode.SELECTION,
                       help= 'Выбор режима работы')
    parser.add_argument('-j',
                       '--json_file_path',
                       type= str,
                       default= os.path.join("lab4", "json", "settings.json"),
                       help= 'Путь к файлу json для пользовательских настроек')
    args = parser.parse_args()
    file = open_json(args.json_file_path)
    match args.mode:
        case Mode.SELECTION:
            logging.info(card_selection(file["iins"],file["last_numbers"], file["hash"], file["path_to_card"]))
        case Mode.LUHN:
            card_num = open_json(file["path_to_card"])
            logging.info(algorithm_luhn(card_num["card_number"]))
        case Mode.COLLISIONS:
               find_collisions(file["hash"],
                               file["iins"][1],
                               file["last_numbers"]
                               )
