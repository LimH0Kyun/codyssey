import os
import datetime
import wave
import pyaudio


def create_records_folder():
    """'records' 폴더가 없으면 생성하는 함수"""
    if not os.path.exists('records'):
        os.makedirs('records')


def get_current_timestamp():
    """현재 날짜와 시간을 'YYYYMMDD-HHMMSS' 형식의 문자열로 반환"""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')


def record_voice(duration=5):
    """시스템 마이크로 지정한 시간(초)만큼 음성을 녹음하는 함수"""
    chunk = 1024  # 한 번에 읽을 프레임 수
    format = pyaudio.paInt16  # 오디오 포맷(16비트)
    channels = 1  # 모노 녹음
    rate = 44100  # 샘플링 레이트(Hz)

    audio = pyaudio.PyAudio()  # PyAudio 객체 생성

    # 오디오 스트림 열기
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print('녹음을 시작합니다...')
    frames = []

    # 지정한 시간 동안 오디오 데이터 읽기
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print('녹음이 완료되었습니다.')

    # 스트림 종료 및 자원 해제
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 파일명에 타임스탬프 추가
    timestamp = get_current_timestamp()
    filename = 'records/' + timestamp + '.wav'

    # 녹음된 데이터를 WAV 파일로 저장
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print('파일 저장 완료:', filename)


def list_records_between(start_date, end_date):
    """시작일과 종료일 사이(포함)의 녹음 파일 목록을 반환하는 함수"""
    file_list = []
    for filename in os.listdir('records'):
        if filename.endswith('.wav'):
            date_str = filename.split('.')[0]  # 'YYYYMMDD-HHMMSS' 추출
            file_date = datetime.datetime.strptime(date_str, '%Y%m%d-%H%M%S').date()
            if start_date <= file_date <= end_date:
                file_list.append(filename)

    return sorted(file_list)


if __name__ == '__main__':
    create_records_folder()  # records 폴더 생성
    record_voice(5)  # 5초간 녹음

    # 보너스 과제: 특정 기간의 녹음 파일 목록 출력 예시
    # 시작일과 종료일 형식: datetime.date(YYYY, MM, DD)
    start = datetime.date(2025, 5, 1)
    end = datetime.date(2025, 5, 29)
    files = list_records_between(start, end)
    for f in files:
        print(f)
