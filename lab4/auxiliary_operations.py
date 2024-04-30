from enum import Enum
import json
import logging

logging.basicConfig(level=logging.DEBUG)


def serialisation_card_num(path: str, num: str)-> None:
    """
    Serialize the card number.

    Args:
    path: str, the path to save the card number
    num: str, the card number to be saved
    """
    try:
        with open(path, "w", encoding="UTF-8") as f:
            json.dump({"card_number":  num}, f)
    except Exception as error:
        logging.error(error)


def open_json(path: str):
    try:
        with open(path,
                    mode = "r",
                    encoding = "utf-8") as f:
                return json.load(f)
    except Exception as e:
         logging.exception(e)



class Mode(Enum):
    """
    Attributes
    ----------
    generate: int
        So you need to generate keys
    encrypt: int
        So you need to encrypt the text
    decrypt: int
        So you need to decrypt the text
    """
    SELECTION = 0
    LUHN = 1
    COLLISIONS = 2