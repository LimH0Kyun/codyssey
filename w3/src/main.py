import random
import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }

    def set_env(self):
        # 환경 값을 랜덤으로 생성하여 env_values에 저장
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)

    def get_env(self):
        # env_values를 반환하고 로그 파일에 기록
        # 현재 날짜와 시간
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # 로그 메시지 생성
        log_message = (
            f'[{timestamp}] 내부 온도: {self.env_values["mars_base_internal_temperature"]:.2f}, '
            f'외부 온도: {self.env_values["mars_base_external_temperature"]:.2f}, '
            f'내부 습도: {self.env_values["mars_base_internal_humidity"]:.2f}, '
            f'외부 광량: {self.env_values["mars_base_external_illuminance"]:.2f}, '
            f'내부 CO2: {self.env_values["mars_base_internal_co2"]:.2f}, '
            f'내부 산소: {self.env_values["mars_base_internal_oxygen"]:.2f}\n'
        )

        # 로그 파일에 추가
        with open("./w3/data/processed/mars_mission_log.txt", "a") as log_file:
            log_file.write(log_message)

        return self.env_values


ds = DummySensor()
ds.set_env()
env_data = ds.get_env()
print(env_data)
