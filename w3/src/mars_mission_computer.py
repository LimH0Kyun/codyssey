import random

# import datetime

# 로그 파일 경로
LOG_FILE_PATH = "./w3/data/processed/mars_mission_log.txt"


class DummySensor:
    def __init__(self):
        # 환경 변수 초기화
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0,
        }

    def set_env(self):
        # 환경 변수에 랜덤 값 설정 (round 추가)
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 2)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self, timestamp):
        # 로그 메시지 생성
        log_message = (
            f"[{timestamp}]\n"
            f'내부 온도: {self.env_values["mars_base_internal_temperature"]:.2f}\n'
            f'외부 온도: {self.env_values["mars_base_external_temperature"]:.2f}\n'
            f'내부 습도: {self.env_values["mars_base_internal_humidity"]:.2f}\n'
            f'외부 광량: {self.env_values["mars_base_external_illuminance"]:.2f}\n'
            f'내부 CO2: {self.env_values["mars_base_internal_co2"]:.2f}\n'
            f'내부 산소: {self.env_values["mars_base_internal_oxygen"]:.2f}\n\n'
        )

        # 로그 파일에 메시지 추가
        try:
            with open(LOG_FILE_PATH, "a") as log_file:
                log_file.write(log_message)
        # 예외처리
        except IOError as e:
            print(f"파일을 쓸 때 오류가 발생했습니다: {e}")

        return self.env_values


def get_valid_timestamp():
    # 사용자로부터 시간 입력 받기
    while True:
        user_input = input("시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 입력하세요: ")
        try:
            # 입력된 시간의 유효성 검사
            year, month, day = (
                int(user_input[0:4]),
                int(user_input[5:7]),
                int(user_input[8:10]),
            )
            hour, minute, second = (
                int(user_input[11:13]),
                int(user_input[14:16]),
                int(user_input[17:19]),
            )
            if (
                0 <= year < 10000
                and 1 <= month <= 12
                and 1 <= day <= 31
                and 0 <= hour < 24
                and 0 <= minute < 60
                and 0 <= second < 60
            ):
                return user_input
            else:
                print("잘못된 시간 형식입니다. 다시 입력하세요.")
        # 예외처리
        except (ValueError, IndexError):
            print("잘못된 형식입니다. 다시 입력하세요.")


def sort_log_file():
    # 로그 파일 정렬
    try:
        # 로그 파일 읽기
        with open(LOG_FILE_PATH, "r") as log_file:
            log_entries = log_file.read().strip().split("\n\n")

        # 시간순으로 정렬
        log_entries.sort(key=lambda entry: entry.split("\n")[0].strip("[]"))

        # 정렬된 로그 파일 쓰기
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write("\n\n".join(log_entries) + "\n\n")
    # 예외처리
    except IOError as e:
        print(f"파일을 읽거나 쓸 때 오류가 발생했습니다: {e}")


# DummySensor
ds = DummySensor()
ds.set_env()

# 시간 입력 받기

# datetime 사용
# now = datetime.datetime.now()
# timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# 제약사항에서 datetime을 사용해도 된다고 명시하지 않아서 고정값으로 설정
# timestamp = "2025-03-27 00:00:00"

# 고정값보다 사용자에게 입력받도록 리팩토링
timestamp = get_valid_timestamp()

# 환경 변수와 로그 메시지 출력
env_data = ds.get_env(timestamp)
print(env_data)

# 로그 파일 정렬
sort_log_file()
