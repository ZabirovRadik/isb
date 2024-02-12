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
    df.index = range(len(df))
    df.to_csv(info, encoding='utf-8')
    return df


def replace_one_letter(encoded_text:str,
                       encoded_char: str,
                       into_what: str,
                       file_to_save: str) -> str:
    after_replace = ""
    with open(encoded_text, encoding="utf-8") as t:
        for char in t.read():
            if char == encoded_char:
                after_replace += into_what
            elif char == into_what:
                after_replace += encoded_char
            else:
                after_replace += char
    with open(file_to_save, mode = "w", encoding="utf-8") as t:
        t.write(after_replace)
    return file_to_save


def for_start(encoded_text:str,
              info: str,
              file_to_save: str) -> str:
    """ 
    the most common symbol -> ' '
    the second most common symbol -> 'О'
    and for convenience of further decryption:
        '\n' -> 'L'
        '>'  -> 'Q'
        '<'  -> 'G'
    """
    df = pd.read_csv(info, encoding = "utf-8")
    after_replace = ""
    with open(encoded_text, encoding="utf-8") as t:
        for char in t.read():
            if char == df.iloc[0]["symbols"]:
                after_replace += " "
            elif char == " ":
                after_replace += df.iloc[0]["symbols"]
            elif char == "\n":
                after_replace += "L"
            elif char == ">":
                after_replace += "Q"
            elif char == "<":
                after_replace += "G"
            elif char == df.iloc[1]["symbols"]:
                after_replace += "О"
            elif char == "О":
                after_replace += df.iloc[1]["symbols"]
            else:
                after_replace += char
    with open(file_to_save, mode = "w", encoding="utf-8") as t:
        t.write(after_replace)
    return file_to_save


def replacing_a_letter(encoded_text:str,
                       info: str,
                       folder: str,
                       ranking: str):
    df = pd.read_csv(info, encoding = "utf-8")
    start = for_start(encoded_text, info, os.path.join(folder, "first_letter_and_more_convenient"))
    #слов 'е' не существует, скорее всего это либо 'а' либо 'и', но в начале текста есть слово 'а*а' или 'и*и' которое повторяетсячерез пару слов наверно это все же 'или'
    replace_one_letter(start,
                       df.iloc[2]["symbols"],
                       "И",
                       os.path.join(folder, "second_letter"))
    replace_one_letter(os.path.join(folder, "second_letter"),
                       "1",
                       "Л",
                       os.path.join(folder, "third_letter"))
    #одинокая '4' с большим числом вхождений намекает на то, что это 'а'
    replace_one_letter(os.path.join(folder, "third_letter"),
                       "4",
                       "А",
                       os.path.join(folder, "fourth_letter"))
    df = count_occurrences(os.path.join(folder, "fourth_letter"), os.path.join(folder,"info2.csv"))
    replace_one_letter(os.path.join(folder, "fourth_letter"),
                       df.iloc[4]["symbols"],
                       "Е",
                       os.path.join(folder, "fiveth_letter"))
    count_occurrences(os.path.join(folder, "fiveth_letter"), os.path.join(folder,"after_five.csv"))
    print(df)
    print(ranking)
    print(f" {ranking[1]}ИАЕЛ")
    


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
    ranking_by_frequency_of_occurrence = " ОЕАИНТСРВЛКМДПУЯЫЗЪБГЧЙЧЖЮШЦЩЭФ"
    args = parser.parse_args()
    #count_occurrences(args.encoded_text, args.info)
    replacing_a_letter(args.encoded_text, args.info, args.folder, ranking_by_frequency_of_occurrence)
