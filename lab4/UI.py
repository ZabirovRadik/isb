import argparse
import os
import sys
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QLabel, QPushButton,\
        QInputDialog, QGridLayout, \
            QWidget, QMessageBox

from tasks_funcs import card_selection, algorithm_luhn, find_collisions
from auxiliary_operations import open_json

class MainWindow(QMainWindow):
    def __init__(self, json_file: str, start_card_num: str):
        super().__init__()
        file = open_json(json_file)
        self.iins = file["iins"]
        self.last_numbers = file["last_numbers"]
        self.card_hash = file["hash"]
        self.card_number = start_card_num
        self.path_card_number = file["path_to_card"]
        
        grid_layout = QGridLayout()

        self.iins_update = QPushButton("Update")
        self.iins_update.clicked.connect(self.iins_button_update_clicked)

        self.last_numbers_update = QPushButton("Update")
        self.last_numbers_update.clicked.connect(self.last_numbers_button_update_clicked)

        self.hash_update = QPushButton("Update")
        self.hash_update.clicked.connect(self.hash_button_update_clicked)

        self.card_number_update = QPushButton("Update")
        self.card_number_update.clicked.connect(self.card_number_button_update_clicked)

        self.button_path_card_number_update = QPushButton("Update")
        self.button_path_card_number_update.clicked.connect(self.path_card_number_update)

        self.label_iins = QLabel(f'IINs: {", ".join(str(i) for i in self.iins)}')
        self.label_iins.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.label_iins, 0, 0)
        grid_layout.addWidget(self.iins_update, 0, 1)

        self.label_last_numbers = QLabel(f'Last numbers: {self.last_numbers}')
        self.label_last_numbers.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.label_last_numbers, 1, 0)
        grid_layout.addWidget(self.last_numbers_update, 1, 1)

        self.label_hash = QLabel(f'Hash: {self.card_hash}')
        self.label_hash.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.label_hash, 2, 0)
        grid_layout.addWidget(self.hash_update, 2, 1)

        self.label_card_number = QLabel(f'Card Number: {self.card_number}')
        self.label_card_number.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.label_card_number, 3, 0)
        grid_layout.addWidget(self.card_number_update, 3, 1)

        self.label_path_card_number = QLabel(f'Path to save card: {self.path_card_number}')
        self.label_path_card_number.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.label_path_card_number, 4, 0)
        grid_layout.addWidget(self.button_path_card_number_update, 4, 1)

        self.button_change_card = QPushButton('Select card number')
        self.button_change_card.clicked.connect(self.select_card_number)
        grid_layout.addWidget(self.button_change_card, 5,0)

        self.button_check_luhn = QPushButton('Check with Luhn algorithm')
        self.button_check_luhn.clicked.connect(self.check_luhn_algorithm)
        grid_layout.addWidget(self.button_check_luhn, 6,0)

        self.button_find_collisions = QPushButton('Find Collisions')
        self.button_find_collisions.clicked.connect(self.find_collisions)
        grid_layout.addWidget(self.button_find_collisions, 7, 0)
        self.setGeometry(0, 0, 400, 500)
        main_widget = QWidget()
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Hack bank')
        self.show()

    def iins_button_update_clicked(self):
        """
        Changes the value self.iins
        """
        new_value, ok = QInputDialog.getText(self, "Update iins", "Enter iins(delimetr is ' '):")
        if ok:
            self.iins = new_value.split()
            self.label_iins.setText(f'IINs: {", ".join(str(i) for i in self.iins)}')
    
    def last_numbers_button_update_clicked(self):
        """
        Changes the value self.last_numbers
        """
        new_value, ok = QInputDialog.getText(self, "Update last numbers", "Enter new last numbers:")
        if ok:
            self.last_numbers = new_value
            self.label_last_numbers.setText(f'Last numbers: {self.last_numbers}')
    
    def hash_button_update_clicked(self):
        """
        Changes the value self.card_hash
        """
        new_value, ok = QInputDialog.getText(self, "Update hash", "Enter new hash:")
        if ok:
            self.card_hash = new_value
            self.label_hash.setText(f'Hash: {self.card_hash}')

    def card_number_button_update_clicked(self):
        """
        Changes the value self.card_number
        """
        new_value, ok = QInputDialog.getText(self, "Update card number", "Enter new card number:")
        if ok:
            self.card_number = new_value
            self.label_card_number.setText(f'Card Number: {self.card_number}')

    def path_card_number_update(self):
        """
        Changes the value self.path_card_number
        """
        new_value, ok = QInputDialog.getText(self, "Update path card number", "Enter new path card number:")
        if ok:
            self.path_card_number = new_value
            self.label_path_card_number.setText(f'Path card number: {self.path_card_number}')

    def select_card_number(self):
        """
        Using function card_selection to select the card number
        """
        message = QMessageBox()
        message.setWindowTitle("Result")
        self.card_number = card_selection(self.iins, self.last_numbers, self.card_hash, self.path_card_number)
        self.label_card_number.setText(f'Path card number: {self.card_number}')
        message.setText(f"Card Number changed successfully!\n{self.card_number}")
        message.exec_()

    def check_luhn_algorithm(self):
        """
        Using function luhn to check correctness card number
        """
        message = QMessageBox()
        message.setWindowTitle("Результат")
        if algorithm_luhn(self.card_number):
            message.setText('Card Number is valid according to Luhn Algorithm')
        else:
            message.setText('Card Number is not valid according to Luhn Algorithm')
        message.exec_()

    def find_collisions(self):
        """
        find collisions by func find_collisions
        """
        message = QMessageBox()
        message.setWindowTitle("Result")
        find_collisions(self.card_hash, self.iins[1], self.last_numbers)
        message.setText('Collisions found successfully!')
        message.exec_()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-j',
                       '--json_file_path',
                       type= str,
                       default= os.path.join("lab4", "json", "settings.json"),
                       help= 'Путь к файлу json для начальных настроек')
    parser.add_argument('-c',
                       '--any_card_number',
                       type= str,
                       default= "5559210557390254",
                       help= 'Начальный номер карты')
    args = parser.parse_args()
    app = QApplication(sys.argv)
    windowExample = MainWindow(args.json_file_path, args.any_card_number)
    sys.exit(app.exec_())