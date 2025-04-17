import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # UI 초기화

    def init_ui(self):
        self.setWindowTitle('아이폰 계산기')  # 창 제목 설정
        self.setStyleSheet('background-color: #000;')  # 배경색 설정

        main_layout = QVBoxLayout()  # 전체 수직 레이아웃

        # 계산 결과 및 입력 표시창 생성
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 입력창을 읽기 전용으로 설정
        self.display.setStyleSheet(
            'font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;'
        )
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        main_layout.addWidget(self.display)  # 메인 레이아웃에 추가

        button_layout = QGridLayout()  # 버튼 그리드 레이아웃

        # 버튼 텍스트, 위치(row, col), (선택적으로 span)
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼 생성 및 레이아웃에 추가
        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setStyleSheet(self.get_button_style(text))  # 버튼 스타일 지정
            button.clicked.connect(self.on_button_click)  # 클릭 시 이벤트 연결
            if span:
                button_layout.addWidget(button, row, col, *span)
            else:
                button_layout.addWidget(button, row, col)

        main_layout.addLayout(button_layout)  # 메인 레이아웃에 버튼 레이아웃 추가
        self.setLayout(main_layout)  # 위젯에 레이아웃 설정

        # 내부 상태 변수 초기화
        self.current_input = ''
        self.last_operator = ''
        self.reset_next = False

    def get_button_style(self, text):
        # 버튼별 스타일 반환
        if text in {'C', '±', '%'}:
            return 'font-size: 24px; background-color: #a5a5a5; color: #000; border-radius: 25px; height: 50px;'
        elif text in {'÷', '×', '-', '+', '='}:
            return 'font-size: 24px; background-color: #f09a36; color: #fff; border-radius: 25px; height: 50px;'
        else:
            return 'font-size: 24px; background-color: #333; color: #fff; border-radius: 25px; height: 50px;'

    def on_button_click(self):
        # 버튼 클릭 시 동작 처리
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.display.clear()  # 표시창 초기화
            self.current_input = ''
            self.last_operator = ''
            self.reset_next = False
        elif text == '=':
            self.calculate_result()  # 결과 계산
        elif text in {'+', '-', '×', '÷'}:
            self.input_operator(text)  # 연산자 입력
        elif text == '±':
            self.toggle_sign()  # 부호 변경
        elif text == '%':
            self.input_percent()  # 백분율 변환
        else:
            self.input_number(text)  # 숫자 및 소수점 입력

    def input_number(self, num):
        # 숫자 및 소수점 입력 처리
        if self.reset_next:
            self.display.clear()
            self.reset_next = False
        if num == '.' and '.' in self.get_last_number():
            return  # 이미 소수점이 있으면 무시
        self.display.setText(self.display.text() + num)

    def input_operator(self, op):
        # 연산자 입력 처리
        current = self.display.text()
        if not current:
            return
        if current[-1] in '+-×÷':
            self.display.setText(current[:-1] + op)  # 마지막 연산자 교체
        else:
            self.display.setText(current + op)
        self.reset_next = False

    def calculate_result(self):
        # 결과 계산 및 표시
        expr = self.display.text().replace('×', '*').replace('÷', '/')
        try:
            # eval은 위험할 수 있으나, 입력이 버튼으로만 제한되어 있어 사용
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)  # 정수로 변환
            self.display.setText(str(result))
            self.reset_next = True
        except Exception:
            self.display.setText('오류임')  # 오류 발생 시 메시지 표시
            self.reset_next = True

    def toggle_sign(self):
        # 마지막 숫자의 부호 변경
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
        # 마지막 숫자를 백분율로 변환
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
        # 연산자 기준으로 식을 분리
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
        # 식에서 마지막 숫자 추출
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
    calculator.resize(350, 500)  # 창 크기 설정
    calculator.show()
    sys.exit(app.exec_())  # 앱 실행