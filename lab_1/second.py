"""Module providing a function printing python version 3.11.5."""
import csv
import os
import argparse
import pandas as pd

def count_occurrences(encoded_text: str, info: str) -> pd.DataFrame:
    df = pd.DataFrame(columns=["symbols","counting", "in_relation_to"])
    with open(encoded_text, encoding="utf-8") as t:
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
    return df

def replace_letters(encoded_text:str,
                       alphabet_in_text: str,
                       right_alphabet: str,
                       file_to_save: str) -> str:
    with open(encoded_text, encoding="utf-8") as t:
        text = t.read()
    i = 0
    for right_char in right_alphabet:
        text = text.replace(alphabet_in_text[i], right_char)
        i += 1
    text.replace("  ", "-")
    # text = text.replace(" ", "ы")
    # text = text.replace(df.iloc[0]["symbols"], " ")
    # text = text.replace("\n", "ы")
    # text = text.replace("У", "и")
    # text = text.replace("1", "л")
    # text = text.replace("Р", "д")
    # text = text.replace("4", "а")
    # text = text.replace("Д", "н")
    # text = text.replace(">", "е")
    # text = text.replace("О", "в")
    # text = text.replace("Е", "о")
    # text = text.replace("<", "ч")
    # text = text.replace("И", "с")
    # text = text.replace("П", "г")
    # text = text.replace("Ъ", "ц")
    # text = text.replace("Ш", "ф")
    # text = text.replace("t", "р")
    # text = text.replace("Ф", "й")
    # text = text.replace("r", "п")
    # text = text.replace("Й", "т")
    # text = text.replace("8", "з")
    # text = text.replace("2", "м")
    # text = text.replace("А", "ь")
    # text = text.replace("Х", "к")
    # text = text.replace("7", "ж")
    # text = text.replace("Ч", "у")
    # text = text.replace("Л", "я")
    # text = text.replace("К", "ю")
    # text = text.replace("5", "б")
    # text = text.replace("Ы", "ш")
    # text = text.replace("Щ", "х")
    # text = text.replace("Ь", "щ")
    with open(file_to_save, mode = "w", encoding="utf-8") as t:
        t.write(text)
    return file_to_save


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='decryption UTF-8',
                        description='descrypton text'
                        )
    parser.add_argument('-t', '--encoded_text',
                        type = str, default = os.path.join("lab_1","for_second","cod5.txt")
                        )
    parser.add_argument('-i', '--info',
                        type = str, default = os.path.join("lab_1","for_second", "info.csv")
                        )
    parser.add_argument('-f', '--folder',
                        type = str, default = os.path.join("lab_1","for_second")
                        )
    alphabet_in_text = " М\nУ1Р4Д>ОЕ<ИПЪШtФrЙ82АХ7ЧЛК5ЫЩЬ"
    right_alphabet = "ы ыилданевочсгцфрйптзмькжуяюбшхщ" 
    args = parser.parse_args()
    #count_occurrences(args.encoded_text, args.info)
    replace_letters(args.encoded_text,
                    alphabet_in_text,
                    right_alphabet,
                    os.path.join(args.folder, "decoded_text"))
