import sys
import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QFont
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel
from qframelesswindow import FramelessWindow, StandardTitleBar

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

class CustomTitleBar(StandardTitleBar):

    def __init__(self, parent):
        super().__init__(parent)

        self.titleLabel.setStyleSheet("background: transparent; margin: 0 5px;")
        self.titleLabel.setFont(QFont("Google Sans Code", 14))

        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-normalColor: #f2f2f2;
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: #2f2f2f;
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

        self.minBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-normalColor: #f2f2f2;
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: #2f2f2f;
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

        self.closeBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-normalColor: #f2f2f2;
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: #2f2f2f;
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

class Window(FramelessWindow):

    def __init__(self, parent=None):

        self.eqn = ""
        self.last_equal = False

        super().__init__(parent=parent)
        self.setTitleBar(CustomTitleBar(self))
        self.setFixedSize(360, 600)

        self.setWindowIcon(QIcon("calc.png"))
        self.setWindowTitle("Calculator")
        self.setStyleSheet("background:#1f1f1f;color: #f2f2f2;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        display_layout = QHBoxLayout()

        self.display = QLabel("0")
        self.display.setFont(QFont("Google Sans Code", 28))
        self.display.setFixedWidth(360)
        self.display.setContentsMargins(8, 0, 8, 0)
        self.display.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        display_layout.addWidget(self.display)

        button_layout = QGridLayout()
        button_layout.setSpacing(0)

        btn_pos = [ ("C", 0, 0), ("⌫", 0, 1), ("(", 0, 2), (")", 0, 3), 
                    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("÷", 1, 3),
                    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("×", 2, 3),
                    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
                    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),]

        for text, row, column in btn_pos:
            button = QPushButton(text) 
            button.setFixedSize(90, 90)
            button.clicked.connect(lambda checked, t=text: self.on_button_clicked(t))
            button.setContentsMargins(0, 0, 0, 0)
            button.setFont(QFont("Google Sans Code", 18))
            button_layout.addWidget(button, row, column)

        main_layout.addLayout(display_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.titleBar.raise_()

    def get_display_text(self):
        return self.eqn.replace("*", "×").replace("/", "÷")

    def on_button_clicked(self, input_char):
        if input_char == "=":
            if not self.eqn or self.last_equal:
                return
            
            temp_eqn = self.eqn.rstrip("+-*/")

            if not re.fullmatch(r"[\d\.\+\-\*/\(\)]+", temp_eqn):
                self.display.setText("Error")
                self.eqn = ""
                self.last_equal = False
                return

            try:
                result = eval(temp_eqn) 
                
                self.eqn = str(result)
                self.display.setText(self.get_display_text())
                self.last_equal = True
            except (SyntaxError, ZeroDivisionError, TypeError):
                self.display.setText("Error")
                self.eqn = ""
                self.last_equal = False
        
        elif input_char == "C":
            self.eqn = ""
            self.display.setText("0")
            self.last_equal = False
        elif input_char == "⌫":
            if self.eqn:
                self.eqn = self.eqn[:-1]
                if self.eqn:
                    self.display.setText(self.get_display_text())
                else:
                    self.display.setText("0")
                self.last_equal = False
        elif input_char in ["+", "-", "×", "÷"]:
            op_map = {"+": "+", "-": "-", "×": "*", "÷": "/"}
            op_e = op_map[input_char]
            if not self.last_equal and self.eqn and self.eqn[-1] in "+-*/":
                self.eqn = self.eqn[:-1]
            self.eqn += op_e
            self.display.setText(self.get_display_text())
            self.last_equal = False
        elif input_char == ".":
            if self.last_equal:
                self.eqn = "0."
                self.display.setText("0.")
                self.last_equal = False
            else:
                last_term = re.split(r"[\+\-\*\/\(\)]", self.eqn)[-1]
                if "." in last_term:
                    return
                self.eqn += "."
            self.display.setText(self.get_display_text())
        else:
            if self.last_equal:
                self.eqn = input_char
            else:
                self.eqn += input_char
            self.display.setText(self.get_display_text())
            self.last_equal = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())