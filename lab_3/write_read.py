"""Module providing a function printing python version 3.11.8"""
import logging

logging.basicConfig(level=logging.DEBUG)


def write(path: str, text: bytes)->None:
    """
    ## Description:
    This function writes the provided text to the specified file path in binary mode.

    ## Arguments:
    - path (str): A string representing the file path where the text will be written.
    - text (bytes): A bytes object containing the text to be written to the file.

    ## Returns:
    - None
    """
    try:
        with open(path, "wb") as f:
            f.write(text)
    except Exception as e:
        logging.exception(e)


def read(path: str)->bytes:
    """
    ## Description:
    This function reads the contents of the specified file path in binary mode and returns the read bytes.

    ## Arguments:
    - path: A string representing the file path from where to read the contents.

    ## Returns:
    - A bytes object containing the read contents of the file.
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        logging.exception(e)