import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.QtCore import QFile, QTextStream
import random
import string
import sympy
import pyperclip

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.setGeometry(100, 100, 400, 500)
        self.password_length = 12
        self.complexity = 'Strong'
        self.include_lowercase = True
        self.include_uppercase = True
        self.include_digits = True
        self.include_symbols = True
        self.initUI()
        self.generate_password()

        # Load the CSS file
        css_file = QFile("styles.css")
        if css_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(css_file)
            style = stream.readAll()
            self.setStyleSheet(style)
            css_file.close()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Password length input
        self.length_label = QLabel("Enter Password Length:")
        self.length_input = QLineEdit()
        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_input)

        # Complexity options
        complexity_grid = QGridLayout()
        complexities = ['Strong', 'Medium', 'Fair']
        self.complexity_buttons = {}
        row, col = 0, 0
        for complexity in complexities:
            button = QPushButton(complexity)
            self.complexity_buttons[complexity] = button
            button.clicked.connect(self.set_complexity)
            complexity_grid.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Data type options
        data_type_grid = QGridLayout()
        data_types = ['Lowercase', 'Uppercase', 'Digits', 'Symbols', 'Prime Password']
        self.data_type_buttons = {}
        row, col = 0, 0
        for data_type in data_types:
            checkbox = QCheckBox(data_type)
            self.data_type_buttons[data_type] = checkbox
            data_type_grid.addWidget(checkbox, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.layout.addLayout(complexity_grid)
        self.layout.addLayout(data_type_grid)

        # Generated password
        self.generated_password_label = QLabel("Generated Password:")
        self.generated_password = QLineEdit()
        self.generated_password.setReadOnly(True)
        self.layout.addWidget(self.generated_password_label)
        self.layout.addWidget(self.generated_password)

        # Buttons
        button_grid = QGridLayout()
        buttons = ['Generate', 'Re-generate', 'Copy to Clipboard']
        self.button_actions = {
            'Generate': self.generate_password,
            'Re-generate': self.regenerate_password,
            'Copy to Clipboard': self.copy_to_clipboard
        }
        row, col = 0, 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.button_actions[button_text])
            button_grid.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.layout.addLayout(button_grid)
        self.setLayout(self.layout)

    def set_complexity(self):
        sender = self.sender()
        self.complexity = sender.text()
        self.generate_password()

    def generate_password(self):
        try:
            length = int(self.length_input.text())
            if length < 8:
                self.generated_password_label.setText("Generated Password: (Password length should be at least 8 characters)")
                self.generated_password.clear()
                return

            characters = []
            if self.data_type_buttons['Lowercase'].isChecked():
                characters.extend(string.ascii_lowercase)
            if self.data_type_buttons['Uppercase'].isChecked():
                characters.extend(string.ascii_uppercase)
            if self.data_type_buttons['Digits'].isChecked():
                characters.extend(string.digits)
            if self.data_type_buttons['Symbols'].isChecked():
                characters.extend(string.punctuation)
            if self.data_type_buttons['Prime Password'].isChecked():
                prime_candidate = sympy.randprime(10 ** (length - 1), 10 ** length - 1)
                password = str(prime_candidate)

            if not characters and not self.data_type_buttons['Prime Password'].isChecked():
                self.generated_password_label.setText("Generated Password: (Select at least one data type)")
                self.generated_password.clear()
                return

            if not self.data_type_buttons['Prime Password'].isChecked():
                password = ''.join(random.choice(characters) for _ in range(length))

            self.generated_password_label.setText("Generated Password:")
            self.generated_password.setText(password)
        except ValueError:
            pass

    def regenerate_password(self):
        self.generate_password()

    def copy_to_clipboard(self):
        pyperclip.copy(self.generated_password.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
