import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('아이폰 계산기')
        self.setStyleSheet('background-color: #000;')

        main_layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            'font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;'
        )
        self.display.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()

        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setStyleSheet(self.get_button_style(text))
            button.clicked.connect(self.on_button_click)
            if span:
                button_layout.addWidget(button, row, col, *span)
            else:
                button_layout.addWidget(button, row, col)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # 내부 상태 변수
        self.current_input = ''
        self.last_operator = ''
        self.reset_next = False

    def get_button_style(self, text):
        if text in {'C', '±', '%'}:
            return 'font-size: 24px; background-color: #a5a5a5; color: #000; border-radius: 25px; height: 50px;'
        elif text in {'÷', '×', '-', '+', '='}:
            return 'font-size: 24px; background-color: #f09a36; color: #fff; border-radius: 25px; height: 50px;'
        else:
            return 'font-size: 24px; background-color: #333; color: #fff; border-radius: 25px; height: 50px;'

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.display.clear()
            self.current_input = ''
            self.last_operator = ''
            self.reset_next = False
        elif text == '=':
            self.calculate_result()
        elif text in {'+', '-', '×', '÷'}:
            self.input_operator(text)
        elif text == '±':
            self.toggle_sign()
        elif text == '%':
            self.input_percent()
        else:
            self.input_number(text)

    def input_number(self, num):
        if self.reset_next:
            self.display.clear()
            self.reset_next = False
        if num == '.' and '.' in self.get_last_number():
            return
        self.display.setText(self.display.text() + num)

    def input_operator(self, op):
        current = self.display.text()
        if not current:
            return
        if current[-1] in '+-×÷':
            self.display.setText(current[:-1] + op)
        else:
            self.display.setText(current + op)
        self.reset_next = False

    def calculate_result(self):
        expr = self.display.text().replace('×', '*').replace('÷', '/')
        try:
            # eval은 위험할 수 있으나, 입력이 버튼으로만 제한되어 있어 사용
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display.setText(str(result))
            self.reset_next = True
        except Exception:
            self.display.setText('오류임')
            self.reset_next = True

    def toggle_sign(self):
        current = self.display.text()
        if not current:
            return
        nums = self.split_expression(current)
        if not nums:
            return
        last_num = nums[-1]
        if last_num.startswith('-'):
            new_num = last_num[1:]
        else:
            new_num = '-' + last_num
        new_expr = ''.join(nums[:-1]) + new_num
        self.display.setText(new_expr)

    def input_percent(self):
        current = self.display.text()
        if not current:
            return
        nums = self.split_expression(current)
        if not nums:
            return
        try:
            percent_value = str(float(nums[-1]) / 100)
        except Exception:
            return
        new_expr = ''.join(nums[:-1]) + percent_value
        self.display.setText(new_expr)

    def split_expression(self, expr):
        # 연산자 기준으로 분리
        import re
        tokens = re.split(r'([+\-×÷])', expr)
        result = []
        temp = ''
        for token in tokens:
            if token in '+-×÷':
                if temp:
                    result.append(temp)
                result.append(token)
                temp = ''
            else:
                temp += token
        if temp:
            result.append(temp)
        return result

    def get_last_number(self):
        expr = self.display.text()
        nums = self.split_expression(expr)
        if not nums:
            return ''
        if nums[-1] in '+-×÷':
            return ''
        return nums[-1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.resize(350, 500)
    calculator.show()
    sys.exit(app.exec_())