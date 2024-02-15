"""Module providing a function printing python version 3.11.5."""
import argparse
import os
import logging
from enum import Enum


logging.basicConfig(level=logging.DEBUG)


RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"


class Mode(Enum):
    """
    Attributes
    ----------
    encrypt: int
        So you need to encrypt the text
    decrypt: int
        So you need to decrypt the text
    """
    ENCRYPT = 0
    DECRYPT = 1


def simple_cipher(
        from_where: str,
        to_where: str,
        key: str,
        mode: Mode) -> None:
    """
    By matching the Russian alphabet and random printed characters,
    this function encrypts and decrypts.

    parameters
    ---------
    from_where: str,
        Файл c текстом, который функция изменяет
    to_where: str,
        The path where the modified text is saved
    key: str,
        The key for encryption or decryption
    mode: int
        Switch: Mode.ENCRYPT.value or Mode.DECRYPT.value
    """
    try:
        with open(key, encoding="utf-8") as k:
            key = k.read()
        if mode == Mode.ENCRYPT:
            dictionary = dict(zip(RUSSIAN_ALPHABET, key))
        elif mode == Mode.DECRYPT:
            dictionary = dict(zip(key, RUSSIAN_ALPHABET))
        else:
            logging.exception("Incorrect mode!")
        answer = ""
        with open(from_where, encoding="utf-8") as text:
            for letter in text.read():
                if letter.isalpha():
                    answer += dictionary[letter]
                else:
                    answer += letter
        with open(to_where, mode="w", encoding="utf-8") as recording:
            recording.write(answer)
    except Exception as e:
            logging.exception(e)
    logging.info("The program was executed in normal mode")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='message encryption UTF-8',
                        description='encryption - descrypton'
                        )
    parser.add_argument('-k', '--key',
                        type = str, default = os.path.join("lab_1", "for_first", "key.txt"),
                        help = 'The path to the key'
                        )
    parser.add_argument('-m', '--mode',
                        type = int, default = Mode.ENCRYPT,
                        help = 'What do you want: to encrypt or decrypt'
                        )
    parser.add_argument('-f', '--from_where',
                        type = str, default = os.path.join("lab_1", "for_first", "planned_text.txt")
                        )
    parser.add_argument('-t', '--to_where',
                        type = str, default = os.path.join("lab_1", "for_first", "encrypted.txt")
                        )
    args = parser.parse_args()
    simple_cipher(args.from_where, args.to_where, args.key, args.mode)
