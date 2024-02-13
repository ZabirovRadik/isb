"""Module providing a function printing python version 3.11.5."""
import os
import argparse
import logging
import pandas as pd


logging.basicConfig(level=logging.DEBUG)


def count_occurrences(
        encrypted_text: str,
        file_for_info: str) -> pd.DataFrame:
    """
    Creating a file with information about unique text characters

    parameters
    ---------
    encrypted_text : str
        Encrypted text
    file_for_info : str
        The path for the information file
    """
    df = pd.DataFrame(columns=["symbols","counting", "in_relation_to"])
    with open(encrypted_text, encoding="utf-8") as t:
        text = t.read()
        symbols = set(text)
        index = 0
        for symbol in symbols:
            count = text.count(symbol)
            df.loc[index] = {'symbols': symbol,
                             "counting": count,
                             "in_relation_to": count / len(text)}
            index += 1
    df = df.sort_values(by="counting", ascending=False)
    df.to_csv(file_for_info)
    logging.info(f"A file {file_for_info} has been created")
    return df


def replace_letters(
        encrypted_text: str,
        alphabet_in_text: str,
        right_alphabet: str,
        file_to_decrypted_text: str) -> str:
    """
    Replacing encrypted text characters with the correct ones

    parameters
    ---------
    encrypted_text : str
        The text that needs to be deciphered
    alphabet_in_text: str
        A set of unique characters in the encrypted text
    right_alphabet: str
        Russian letters + space are in order to match the order with "alphabet_in_text" to replace
    file_to_decrypted_text : str
        The path for the decrypted text
    """
    with open(encrypted_text, encoding="utf-8") as t:
        text = t.read()
    i = 0
    for right_char in right_alphabet:
        text = text.replace(alphabet_in_text[i], right_char)
        i += 1
    with open(file_to_decrypted_text, mode = "w", encoding="utf-8") as t:
        t.write(text)
    logging.info(f"Decrypted text saved by path {file_to_decrypted_text}")
    return file_to_decrypted_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='decryption UTF-8',
                        description='descrypton text'
                        )
    parser.add_argument('-t', '--encrypted_text',
                        type = str, default = os.path.join("lab_1","for_second","cod5.txt")
                        )
    parser.add_argument('-i', '--info',
                        type = str, default = os.path.join("lab_1","for_second", "info.csv")
                        )
    parser.add_argument('-f', '--file_to_decrypted_text',
                        type = str, default = os.path.join("lab_1","for_second", "decrypted_text.txt")
                        )
    parser.add_argument('-a', '--alphabet_in_text',
                        type = str, default = " М\nУ1Р4Д>ОЕ<ИПЪШtФrЙ82АХ7ЧЛК5ЫЩЬ"
                        )
    parser.add_argument('-r', '--right_alphabet',
                        type = str, default = "ы ыилданевочсгцфрйптзмькжуяюбшхщ"
                        )
    args = parser.parse_args()
    count_occurrences(args.encrypted_text, args.info)
    replace_letters(args.encrypted_text,
                    args.alphabet_in_text,
                    args.right_alphabet,
                    args.file_to_decrypted_text)
