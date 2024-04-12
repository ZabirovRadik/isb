"""Module providing a function printing python version 3.11.9"""
import argparse
import json
import logging
import os

from cryptography_hybrid_system import Cryptograthy

from auxiliary_operations import Mode

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
                       '--mode',
                       type= int,
                       default= Mode.DECRYPT,
                       help= 'Выбор режима работы')
    parser.add_argument('-j',
                       '--json_file_path',
                       type= str,
                       default= os.path.join("lab_3", "json", "settings.json"),
                       help= 'Путь к файлу json для пользовательских настроек')
    args = parser.parse_args()
    try:
        with open(args.json_file_path,
                    mode = "r",
                    encoding = "utf-8") as f:
                file = json.load(f)
    except Exception as e:
         logging.exception(e)
    cryptography = Cryptograthy(os.path.join(file["path_keys"],
                                             file["symmetric_key"]),
                                os.path.join(file["path_keys"],
                                             file["public_key"]),
                                os.path.join(file["path_keys"],
                                             file["secret_key"])
                                )
    match args.mode:
        case Mode.GENERATE:
            cryptography.generate_and_save_keys(file["key_size"])
        case Mode.ENCRYPT:
              cryptography.encript_by_hybrid(os.path.join(file["files"],
                                                          file["initial_file"]),
                                            os.path.join(file["files"],
                                                         file["encrypted_file"])
                                            )
        case Mode.DECRYPT:
               cryptography.decript_by_hybrid(os.path.join(file["files"],
                                                           file["encrypted_file"]),
                                              os.path.join(file["files"],
                                                           file["decrypted_file"])
                                            )
