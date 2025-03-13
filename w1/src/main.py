import sys
import os

def read_log_file(file_path):
    #로그 파일을 읽고 라인 리스트를 반환
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다.')
        sys.exit(1)
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')
        sys.exit(1)

def sort_lines_by_timestamp(lines):
    #타임스탬프 기준으로 로그 라인을 정렬
    header = lines[0]
    data_lines = lines[1:]
    sorted_lines = sorted(data_lines, key=lambda x: x.split(',')[0], reverse=True)
    return header, sorted_lines

def print_logs(header, sorted_lines):
    #로그를 콘솔에 출력
    print(header.strip())
    for line in sorted_lines:
        print(line.strip())

def extract_problem_lines(lines, problem_messages):
    #문제 메시지를 포함한 라인을 추출
    data_lines = lines[1:]
    return [line for line in data_lines if any(msg.lower() in line.lower() for msg in problem_messages)]

def save_problem_logs(header, problem_lines, output_file):
    #문제 로그를 파일에 저장
    try:
        # 출력 파일의 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as problem_file:
            problem_file.write(header.strip() + '\n')
            for line in problem_lines:
                problem_file.write(line.strip() + '\n')
        print(f'문제가 되는 부분을 {output_file} 파일에 저장했습니다.')
    except Exception as e:
        print(f'파일 저장 중 오류가 발생했습니다: {e}')

def main(log_file_path, output_file):
    #메인 함수: 로그 파일 처리 및 문제 로그 저장
    lines = read_log_file(log_file_path)
    header, sorted_lines = sort_lines_by_timestamp(lines)
    print_logs(header, sorted_lines)
    
    problem_messages = ['oxygen tank unstable.', 'oxygen tank explosion.']
    problem_lines = extract_problem_lines(lines, problem_messages)
    save_problem_logs(header, problem_lines, output_file)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('사용법: python main.py <log_file_path> <output_file_path>')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])