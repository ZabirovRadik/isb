"""Module providing a function printing python version 3.11.5."""
import argparse
import os


def simple_cipher(alphabet: str, from_where: str, to_where: str, key: str, mode: int):
    """
    By matching the Russian alphabet and random printed characters,
    this function encrypts and decrypts.
    """
    with open(key, encoding="utf-8") as k:
        key = k.read()
    if mode == 0:
        dictionary = dict(zip(alphabet, key))
    else:
        dictionary = dict(zip(key, alphabet))
    answer = ""
    with open(from_where, encoding="utf-8") as text:
        for letter in text.read():
            if letter.isalpha():
                answer += dictionary[letter]
            else:
                answer += letter
    with open(to_where, mode="w", encoding="utf-8") as recording:
        recording.write(answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='message encryption UTF-8',
                        description='encryption - descrypton'
                        )
    parser.add_argument('-a', '--alphabet',
                        type = str,
                        default = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                        )
    parser.add_argument('-k', '--key',
                        type = str, default = os.path.join("lab_1", "for_first", "key.txt"),
                        help = 'The path to the key'
                        )
    parser.add_argument('-m', '--mode',
                        type = int, default = 0,
                        help = '0-encrypt, 1-decrypt'
                        )
    parser.add_argument('-f', '--from_where',
                        type = str, default = os.path.join("lab_1", "for_first", "planned_text.txt")
                        )
    parser.add_argument('-t', '--to_where',
                        type = str, default = os.path.join("lab_1", "for_first", "encrypted.txt")
                        )
    args = parser.parse_args()
    simple_cipher(args.alphabet, args.from_where, args.to_where, args.key, args.mode)
