import os
import csv
import speech_recognition as sr


def get_audio_file_list(folder_path):
    """지정된 폴더에서 .wav 확장자의 음성파일 목록을 반환한다."""
    file_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_list.append(os.path.join(folder_path, file_name))
    return file_list


def convert_audio_to_text(audio_file):
    """음성파일을 텍스트로 변환한다 (STT 기능 사용)."""
    recognizer = sr.Recognizer()
    text_list = []

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            # 시간 정보는 기본 STT에서 제공되지 않으므로 전체 텍스트만 저장
            text_list.append(("0:00", text))
        except sr.UnknownValueError:
            print(f"음성 인식 실패: {audio_file}")
        except sr.RequestError as e:
            print(f"API 요청 실패: {e}")

    return text_list


def save_text_to_csv(audio_file, text_list):
    """변환된 텍스트를 CSV 파일로 저장한다."""
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    csv_file = base_name + ".csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Text"])

        for time_stamp, text in text_list:
            writer.writerow([time_stamp, text])

    print(f"CSV 저장 완료: {csv_file}")


def search_keyword_in_csv(keyword):
    """CSV 파일에서 특정 키워드를 검색한다 (보너스 과제)."""
    csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]

    for csv_file in csv_files:
        print(f"--- {csv_file} ---")
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 스킵

            for row in reader:
                time_stamp, text = row
                if keyword in text:
                    print(f"{time_stamp}: {text}")


def main():
    """전체 흐름 실행."""
    folder_path = "/Users/cheon-yechan/Desktop/workspace/ia-codyseeay/records"  # 음성파일 폴더 경로로 수정
    audio_files = get_audio_file_list(folder_path)

    for audio_file in audio_files:
        print(f"처리중: {audio_file}")
        text_list = convert_audio_to_text(audio_file)
        save_text_to_csv(audio_file, text_list)

    # 보너스 테스트 (원할 경우 주석 해제)
    # keyword = input('검색할 키워드를 입력하세요: ')
    # search_keyword_in_csv(keyword)


if __name__ == "__main__":
    main()
