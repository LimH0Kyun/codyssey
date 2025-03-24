def read_log_file(file_path):
    # 로그 파일을 읽고 헤더와 데이터를 반환
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                print("오류: 로그 파일이 비어 있습니다.")
                exit(1)
            header = lines[0].strip().split(",")
            data = []
            expected_fields = len(header)
            for i, line in enumerate(lines[1:], start=2):
                parts = line.strip().split(",")
                if len(parts) != expected_fields:
                    continue
                data.append(parts)
            return header, data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        exit(1)
    except PermissionError:
        print("파일을 읽을 권한이 없습니다.")
        exit(1)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
        exit(1)

def sort_lines_by_timestamp(lines):
    # 타임스탬프 기준으로 로그 라인을 정렬
    header = lines[0]
    data_lines = lines[1]  # 데이터 리스트를 직접 접근
    sorted_lines = sorted(data_lines, key=lambda x: x[0], reverse=True)
    return header, sorted_lines

def print_logs(header, sorted_lines):
    # 로그를 콘솔에 출력
    print(",".join(header))
    for line in sorted_lines:
        print(",".join(line))

def extract_problem_lines(lines, problem_messages):
    # 문제 메시지를 포함한 라인을 추출
    header, data_lines = lines
    return [
        line
        for line in data_lines
        if any(msg.lower() in ",".join(line).lower() for msg in problem_messages)
    ]

def save_problem_logs(header, problem_lines, output_file):
    # 문제 로그를 파일에 저장
    try:
        with open(output_file, "w", encoding="utf-8") as problem_file:
            problem_file.write(",".join(header) + "\n")
            for line in problem_lines:
                problem_file.write(",".join(line) + "\n")
        print(f"문제가 되는 부분을 {output_file} 파일에 저장했습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def main(log_file_path, output_file):
    # 메인 함수: 로그 파일 처리 및 문제 로그 저장
    lines = read_log_file(log_file_path)
    header, sorted_lines = sort_lines_by_timestamp(lines)
    print_logs(header, sorted_lines)

    problem_messages = ["oxygen tank unstable.", "oxygen tank explosion."]
    problem_lines = extract_problem_lines(lines, problem_messages)
    save_problem_logs(header, problem_lines, output_file)

# 실행
log_file_path = "./w1/logs/mission_computer_main.log"
output_file = "./w1/logs/problem_logs.log"
main(log_file_path, output_file)