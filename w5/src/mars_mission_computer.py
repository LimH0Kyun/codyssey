import random
import time
import platform
import os
import sys

AVG_INTERVAL = 60  # 5초 * 60 = 5분
LOG_PATH = './w5/data/processed/mars_mission_log.txt'
SETTING_PATH = './w5/setting.txt'

class DummySensor:
    def __init__(self):
        self.env_values = {}

    def set_env(self):
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2),
        }

    def log_env(self, timestamp):
        log_message = f"[{timestamp}]\n" + "\n".join([
            f"{key.replace('mars_base_', '').replace('_', ' ').capitalize()}: {value:.2f}"
            for key, value in self.env_values.items()
        ]) + "\n\n"
        try:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            with open(LOG_PATH, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
        except IOError as e:
            print(f'파일을 쓸 때 오류가 발생했습니다: {e}')

class MissionComputer:
    def __init__(self):
        self.sensor = DummySensor()
        self.running = True
        self.history = []
        self.iteration = 0
        self.setting_keys = self._load_settings()

    def _load_settings(self):
        if not os.path.exists(SETTING_PATH):
            print('setting.txt 파일이 없습니다. 기본 파일을 생성합니다.')
            self._create_default_setting_file()
            return []
        try:
            with open(SETTING_PATH, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f'setting.txt 파일을 읽는 중 오류 발생: {e}')
            return []

    def _create_default_setting_file(self):
        try:
            os.makedirs(os.path.dirname(SETTING_PATH), exist_ok=True)
            with open(SETTING_PATH, 'w', encoding='utf-8') as f:
                f.write("# 센서 데이터 항목:\n")
                f.write("mars_base_internal_temperature\n")
                f.write("mars_base_external_temperature\n")
                f.write("mars_base_internal_humidity\n")
                f.write("# 시스템 정보 항목:\n")
                f.write("os\n")
                f.write("cpu_core_count\n")
                f.write("memory_total_bytes\n")
                f.write("# 부하 정보 항목:\n")
                f.write("cpu_usage_percent\n")
                f.write("memory_usage_percent\n")
            print('기본 setting.txt 파일이 생성되었습니다.')
        except Exception as e:
            print(f'setting.txt 기본 생성 실패: {e}')

    def _print_json(self, data):
        print('{')
        keys = self.setting_keys if self.setting_keys else data.keys()
        shown = 0
        for key in keys:
            if key in data:
                shown += 1
                comma = ',' if shown < len([k for k in keys if k in data]) else ''
                print(f'    "{key}": {data[key]}{comma}')
        print('}')

    def _calculate_averages(self):
        return {
            key: round(sum(item[key] for item in self.history) / len(self.history), 2)
            for key in self.history[0]
        } if self.history else {}

    def _update_history(self):
        self.history.append(self.sensor.env_values.copy())
        if len(self.history) > AVG_INTERVAL:
            self.history.pop(0)

    def _delay(self):
        time.sleep(5)

    def get_sensor_data(self):
        print('환경 출력 중... 종료하려면 Ctrl+C를 누르세요.')
        try:
            while self.running:
                timestamp = f'T+{self.iteration * 5} sec'
                self.sensor.set_env()
                self.sensor.log_env(timestamp)
                self._update_history()
                self._print_json(self.sensor.env_values)
                self.iteration += 1

                if self.iteration % AVG_INTERVAL == 0:
                    print('\n5분 평균:')
                    print('------------------')
                    self._print_json(self._calculate_averages())
                    print('------------------\n')

                self._delay()
        except KeyboardInterrupt:
            self.stop()

    def get_mission_computer_info(self):
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_core_count': os.cpu_count(),
                'memory_total_bytes': self._get_total_memory()
            }
            print('\n미션 컴퓨터 시스템 정보:')
            self._print_json(info)
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')

    def get_mission_computer_load(self):
        try:
            cpu_usage = 0.0
            mem_usage = 0.0

            if sys.platform.startswith('linux'):
                with open('/proc/stat') as f:
                    cpu1 = list(map(int, f.readline().split()[1:]))
                time.sleep(0.1)
                with open('/proc/stat') as f:
                    cpu2 = list(map(int, f.readline().split()[1:]))

                idle1, total1 = cpu1[3], sum(cpu1)
                idle2, total2 = cpu2[3], sum(cpu2)

                idle_delta = idle2 - idle1
                total_delta = total2 - total1

                cpu_usage = round((1 - idle_delta / total_delta) * 100, 2)

                with open('/proc/meminfo') as f:
                    meminfo = f.read()
                total = int(next(l for l in meminfo.splitlines() if 'MemTotal' in l).split()[1])
                avail = int(next(l for l in meminfo.splitlines() if 'MemAvailable' in l).split()[1])
                mem_usage = round((total - avail) / total * 100, 2)

            load = {
                'cpu_usage_percent': cpu_usage,
                'memory_usage_percent': mem_usage
            }
            print('\n미션 컴퓨터 부하 정보:')
            self._print_json(load)
        except Exception as e:
            print(f'부하 정보를 가져오는 중 오류 발생: {e}')

    def _get_total_memory(self):
        if sys.platform == 'win32':
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            status = MEMORYSTATUSEX()
            status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return status.ullTotalPhys
        elif sys.platform.startswith('linux'):
            try:
                with open('/proc/meminfo') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            return int(line.split()[1]) * 1024
            except Exception as e:
                print(f'/proc/meminfo 읽기 실패: {e}')
        return 0

    def stop(self):
        self.running = False
        print('System stopped.')

if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
