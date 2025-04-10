import random
import time
import platform
import os
import sys
import psutil  # 실시간 부하 정보를 가져오기 위해 추가

# 상수 정의
AVG_INTERVAL = 60  # 5분(5초 * 60회) 주기
LOG_FILE_PATH = './w5/data/processed/mars_mission_log.txt'

class DummySensor:
    """화성 기지 환경 데이터를 생성하고 로깅하는 클래스"""
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
        """환경 변수에 랜덤 값을 설정"""
        self.env_values.update({
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2),
        })

    def log_env(self, timestamp):
        """환경 데이터를 로그 파일에 기록"""
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
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(log_message)
        except IOError as e:
            print(f'파일을 쓸 때 오류가 발생했습니다: {e}')

class MissionComputer:
    """화성 미션 컴퓨터의 상태와 환경 데이터를 관리하는 클래스"""
    def __init__(self):
        self.sensor = DummySensor()
        self.running = True
        self.data_history = []
        self.iteration = 0

    def print_json(self, data, title=''):
        """데이터를 JSON 형식으로 출력"""
        if title:
            print(f'{title}:')
        print('{')
        for i, (key, value) in enumerate(data.items()):
            comma = ',' if i < len(data) - 1 else ''
            if isinstance(value, (int, float)):
                print(f'    "{key}": {value:.2f}{comma}')
            else:
                print(f'    "{key}": "{value}"{comma}')
        print('}')

    def delay(self, seconds=5):
        """지정된 시간만큼 대기"""
        time.sleep(seconds)

    def calculate_averages(self):
        """5분 평균 계산"""
        if not self.data_history:
            return {}
        return {key: sum(item[key] for item in self.data_history) / len(self.data_history) for key in self.data_history[0]}

    def update_data_history(self):
        """데이터 히스토리 업데이트"""
        self.data_history.append(self.sensor.env_values.copy())
        if len(self.data_history) > AVG_INTERVAL:
            self.data_history.pop(0)

    def get_sensor_data(self):
        """센서 데이터 수집 및 출력"""
        print('환경 출력 중... 종료하려면 Ctrl+C를 누르세요.')
        try:
            while self.running:
                timestamp = f'T+{self.iteration * 5} sec'
                self.sensor.set_env()
                self.sensor.log_env(timestamp)
                self.update_data_history()

                self.print_json(self.sensor.env_values, '현재 환경 데이터')
                self.iteration += 1

                if self.iteration % AVG_INTERVAL == 0:
                    averages = self.calculate_averages()
                    print('\n5분 평균:')
                    print('------------------')
                    self.print_json(averages)
                    print('------------------\n')

                self.delay()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """시스템 종료"""
        self.running = False
        print('System stopped.')

    def get_mission_computer_info(self):
        """시스템 정보 가져오기"""
        try:
            system_info = {
                'operating_system': platform.system(),
                'os_version': platform.release(),
                'cpu_type': platform.processor() or 'unknown',
                'cpu_cores': os.cpu_count() or 0,
                'memory_size_mb': round(psutil.virtual_memory().total / (1024 * 1024), 2),  # psutil로 정확한 메모리 크기
            }
            self.print_json(system_info, '미션 컴퓨터 시스템 정보')
            return system_info
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')
            return {}

    def get_mission_computer_load(self):
        """실시간 부하 정보 가져오기"""
        try:
            load_info = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),  # 1초 간격으로 CPU 사용량 측정
                'memory_usage_percent': psutil.virtual_memory().percent,  # 메모리 사용량 퍼센트
            }
            self.print_json(load_info, '미션 컴퓨터 실시간 부하')
            return load_info
        except Exception as e:
            print(f'부하 정보를 가져오는 중 오류 발생: {e}')
            return {}

    def load_settings(self):
        """setting.txt에서 출력 항목 설정 로드"""
        settings = {
            'operating_system': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_cores': True,
            'memory_size_mb': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True,
        }
        try:
            with open('setting.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    settings[key] = value.lower() == 'true'
        except FileNotFoundError:
            print('setting.txt 파일이 없습니다. 기본 설정을 사용합니다.')
        except Exception as e:
            print(f'setting.txt 로드 중 오류 발생: {e}')
        return settings

    def get_filtered_info(self):
        """설정에 따라 필터링된 정보 출력"""
        settings = self.load_settings()
        try:
            filtered_info = {}
            system_info = self.get_mission_computer_info()
            load_info = self.get_mission_computer_load()

            for key in system_info:
                if settings.get(key, False):
                    filtered_info[key] = system_info[key]
            for key in load_info:
                if settings.get(key, False):
                    filtered_info[key] = load_info[key]

            if filtered_info:
                self.print_json(filtered_info, '필터링된 미션 컴퓨터 정보')
        except Exception as e:
            print(f'필터링된 정보를 가져오는 중 오류 발생: {e}')

if __name__ == '__main__':
    run_computer = MissionComputer()
    run_computer.get_mission_computer_info()
    run_computer.get_mission_computer_load()
    run_computer.get_filtered_info()
    run_computer.get_sensor_data()