import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator:
    # 계산기의 핵심 로직을 담당하는 클래스

    def __init__(self):
        self.reset()

    def reset(self):
        # 계산기 상태 초기화
        self.current_value = 0
        self.operation = None
        self.previous_value = None
        self.new_input = True
        self.error_state = False
        return '0'

    def add(self, a, b):
        # 덧셈 연산
        return a + b

    def subtract(self, a, b):
        # 뺄셈 연산
        return a - b

    def multiply(self, a, b):
        # 곱셈 연산
        return a * b

    def divide(self, a, b):
        # 나눗셈 연산
        if b == 0:
            self.error_state = True
            return '오류: 0으로 나눌 수 없음'
        return a / b

    def negative_positive(self, value):
        # 양수/음수 전환
        return -value

    def percent(self, value):
        # 퍼센트 변환
        return value / 100

    def equal(self):
        # 현재까지의 연산 결과 계산
        if self.operation is None or self.previous_value is None:
            return str(self.format_number(self.current_value))

        if self.operation == '+':
            result = self.add(self.previous_value, self.current_value)
        elif self.operation == '-':
            result = self.subtract(self.previous_value, self.current_value)
        elif self.operation == '×':
            result = self.multiply(self.previous_value, self.current_value)
        elif self.operation == '÷':
            result = self.divide(self.previous_value, self.current_value)

        # 에러 상태 확인
        if self.error_state:
            self.reset()
            return result  # 에러 메시지 반환

        # 결과 저장 및 상태 업데이트
        self.current_value = result
        self.previous_value = None
        self.operation = None
        self.new_input = True

        return str(self.format_number(result))

    def format_number(self, num):
        # 숫자 형식 포맷팅 (소수점 처리 등)
        if isinstance(num, str):  # 이미 문자열이면 그대로 반환
            return num

        # 너무 큰 숫자나 작은 숫자 처리
        if abs(num) > 1e15:
            return f'{num:.2e}'

        # 정수인 경우 정수로 변환
        if isinstance(num, float) and num.is_integer():
            return int(num)

        # 소수점 6자리까지만 표시 (반올림)
        if isinstance(num, float):
            rounded = round(num, 6)
            # 필요없는 0 제거
            return (
                str(rounded).rstrip('0').rstrip('.')
                if '.' in str(rounded)
                else str(rounded)
            )

        return num

    def process_number(self, display_text, digit):
        # 숫자 입력 처리
        if self.new_input or display_text == '0':
            self.new_input = False
            if digit == '.':
                return '0.'
            return digit

        # 소수점이 이미 있는지 확인
        if digit == '.' and '.' in display_text:
            return display_text

        return display_text + digit

    def process_operation(self, display_text, op):
        # 연산자 입력 처리
        # 이전에 에러가 있었다면 초기화
        if self.error_state:
            self.reset()
            self.error_state = False
            return '0'

        # 현재 값 업데이트
        try:
            self.current_value = float(display_text)
        except ValueError:
            self.reset()
            return '0'

        # 이전 연산 처리
        if self.operation is not None and self.previous_value is not None:
            display_text = self.equal()
            self.current_value = float(display_text) if display_text != 'Error' else 0

        # 새 연산 설정
        self.previous_value = self.current_value
        self.operation = op
        self.new_input = True

        return display_text


class CalculatorUI(QWidget):
    # 계산기 UI 클래스

    def __init__(self):
        super().__init__()
        self.calculator = Calculator()  # 계산기 로직 인스턴스
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('아이폰 계산기')
        self.setStyleSheet('background-color: #000;')

        # 레이아웃 설정
        main_layout = QVBoxLayout()

        # 계산 결과 표시창
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            'font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;'
        )
        main_layout.addWidget(self.display)

        # 버튼 레이아웃
        button_layout = QGridLayout()

        # 버튼 텍스트, 위치(row, col), (선택적으로 span)
        buttons = [
            ('C', 0, 0),
            ('±', 0, 1),
            ('%', 0, 2),
            ('÷', 0, 3),
            ('7', 1, 0),
            ('8', 1, 1),
            ('9', 1, 2),
            ('×', 1, 3),
            ('4', 2, 0),
            ('5', 2, 1),
            ('6', 2, 2),
            ('-', 2, 3),
            ('1', 3, 0),
            ('2', 3, 1),
            ('3', 3, 2),
            ('+', 3, 3),
            ('0', 4, 0, 1, 2),
            ('.', 4, 2),
            ('=', 4, 3),
        ]

        # 버튼 생성 및 레이아웃에 추가
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

    def get_button_style(self, text):
        # 버튼 스타일 반환
        if text in {'C', '±', '%'}:
            return 'font-size: 24px; background-color: #a5a5a5; color: #000; border-radius: 25px; height: 50px;'
        elif text in {'÷', '×', '-', '+', '='}:
            return 'font-size: 24px; background-color: #f09a36; color: #fff; border-radius: 25px; height: 50px;'
        else:
            return 'font-size: 24px; background-color: #333; color: #fff; border-radius: 25px; height: 50px;'

    def on_button_click(self):
        # 버튼 클릭 이벤트 처리
        sender = self.sender()
        text = sender.text()
        current_text = self.display.text()

        if text == 'C':
            self.display.setText(self.calculator.reset())
        elif text == '=':
            result = self.calculator.equal()
            self.display.setText(result)
            self.adjust_font_size(result)
        elif text in {'+', '-', '×', '÷'}:
            new_text = self.calculator.process_operation(current_text, text)
            self.display.setText(new_text)
            self.adjust_font_size(new_text)
        elif text == '±':
            try:
                value = float(current_text)
                new_value = self.calculator.negative_positive(value)
                self.display.setText(str(self.calculator.format_number(new_value)))
                self.calculator.current_value = new_value
            except ValueError:
                pass
        elif text == '%':
            try:
                value = float(current_text)
                new_value = self.calculator.percent(value)
                self.display.setText(str(self.calculator.format_number(new_value)))
                self.calculator.current_value = new_value
            except ValueError:
                pass
        else:  # 숫자와 소수점
            new_text = self.calculator.process_number(current_text, text)
            self.display.setText(new_text)
            self.adjust_font_size(new_text)

    def adjust_font_size(self, text):
        # 텍스트 길이에 따라 폰트 크기 조정
        length = len(text)
        font = QFont()

        if length > 12:
            font.setPointSize(20)
        elif length > 9:
            font.setPointSize(26)
        elif length > 7:
            font.setPointSize(30)
        else:
            font.setPointSize(36)

        self.display.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = CalculatorUI()
    calculator.resize(350, 500)
    calculator.show()
    sys.exit(app.exec_())
