import random
import time

# 상수 정의
AVG_INTERVAL = 60  # 5분(5초 * 60회) 주기

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }

    def set_env(self):
        # 각 환경 변수에 대해 랜덤 값을 소수점 둘째 자리까지 할당
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2),
        }

    def log_env(self, timestamp):
        # 로그 메시지 생성 및 파일에 기록
        log_message = (
            f'[{timestamp}]\n'
            f'내부 온도: {self.env_values["mars_base_internal_temperature"]:.2f}\n'
            f'외부 온도: {self.env_values["mars_base_external_temperature"]:.2f}\n'
            f'내부 습도: {self.env_values["mars_base_internal_humidity"]:.2f}\n'
            f'외부 광량: {self.env_values["mars_base_external_illuminance"]:.2f}\n'
            f'내부 CO2: {self.env_values["mars_base_internal_co2"]:.2f}\n'
            f'내부 산소: {self.env_values["mars_base_internal_oxygen"]:.2f}\n\n'
        )
        try:
            with open('./w3/data/processed/mars_mission_log.txt', 'a') as log_file:
                log_file.write(log_message)
        except IOError as e:
            print(f'파일을 쓸 때 오류가 발생했습니다: {e}')

class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()  # DummySensor 객체 인스턴스 생성
        self.running = True      # 시스템 실행 상태 플래그
        self.data_history = []   # 5분 평균 계산을 위한 데이터 저장 리스트
        self.iteration = 0       # 반복 횟수 (5초마다 1회)

    def print_json(self, data):
        # JSON 형태로 데이터 출력
        print('{')
        for i, (key, value) in enumerate(data.items()):
            comma = ',' if i < len(data) - 1 else ''
            print(f'    "{key}": {value:.2f}{comma}')
        print('}')

    def delay(self):
        # time.sleep을 이용한 5초 지연 함수
        time.sleep(5)

    def calculate_averages(self):
        # 5분 평균 계산
        averages = {key: sum(item[key] for item in self.data_history) / len(self.data_history) for key in self.data_history[0]}
        return averages

    def update_data_history(self):
        # 데이터 히스토리에 현재 값 저장 (최대 AVG_INTERVAL 개)
        self.data_history.append(self.ds.env_values.copy())
        if len(self.data_history) > AVG_INTERVAL:
            self.data_history.pop(0)

    def get_sensor_data(self):
        print('환경 출력 중... 종료하려면 Ctrl+C를 누르세요.')
        try:
            while self.running:
                timestamp = f'T+{self.iteration * 5} sec'
                # 센서 데이터 갱신 및 로그 기록
                self.ds.set_env()
                self.ds.log_env(timestamp)

                # 데이터 히스토리 업데이트
                self.update_data_history()

                # 현재 센서 데이터를 JSON 형태로 출력
                self.print_json(self.ds.env_values)
                self.iteration += 1

                # 5분(AVG_INTERVAL 회)마다 5분 평균 출력
                if self.iteration % AVG_INTERVAL == 0:
                    averages = self.calculate_averages()
                    print('\n5분 평균:')
                    print('------------------')
                    self.print_json(averages)
                    print('------------------\n')

                # 5초 지연
                self.delay()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        print('System stopped.')

if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()