import sys
import os
import struct


def read_csv_file(file_path):
    # CSV 파일을 읽고 헤더와 데이터를 리스트로 반환
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            # 첫 번째 줄은 헤더, 제거
            header = lines[0].strip().split(",")
            data = [line.strip().split(",") for line in lines[1:]]
            return header, data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        sys.exit(1)
    except PermissionError:
        print("파일을 읽을 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)


def sort_by_flammability(data):
    # 데이터를 인화성 지수(마지막 열) 기준으로 내림차순 정렬
    return sorted(data, key=lambda x: float(x[-1]), reverse=True)


def print_inventory(header, data):
    # 정렬된 인벤토리 데이터를 콘솔에 출력
    print(",".join(header))
    for item in data:
        print(",".join(item))


def extract_high_flammability(data, threshold=0.7):
    # 인화성 지수가 0.7 이상인 항목을 추출
    return [item for item in data if float(item[-1]) >= threshold]


def save_to_csv(header, data, output_file):
    # 데이터를 CSV 파일로 저장
    try:
        # 출력 파일의 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as file:
            file.write(",".join(header) + "\n")
            for item in data:
                file.write(",".join(item) + "\n")
        print(f"인화성 지수가 0.7 이상인 항목을 {output_file} 파일에 저장했습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")


def save_to_binary(data, binary_file):
    # 정렬된 데이터를 이진 파일로 저장
    try:
        with open(binary_file, "wb") as file:
            for item in data:
                line = ",".join(item).encode("utf-8")
                file.write(struct.pack("I", len(line)))
                file.write(line)
        print(f"정렬된 데이터를 {binary_file} 파일에 저장했습니다.")
    except Exception as e:
        print(f"이진 파일 저장 중 오류가 발생했습니다: {e}")


def read_from_binary(binary_file):
    # 이진 파일에서 데이터를 읽어 콘솔에 출력
    try:
        with open(binary_file, "rb") as file:
            print("\n이진 파일에서 읽은 데이터:")
            while True:
                length_data = file.read(4)
                if not length_data:
                    break
                length = struct.unpack("I", length_data)[0]
                line_data = file.read(length)
                print(line_data.decode("utf-8"))
    except Exception as e:
        print(f"이진 파일 읽기 중 오류가 발생했습니다: {e}")


def main(input_file, danger_file, binary_file):
    # 메인 함수: 인벤토리 데이터를 처리하고 결과를 출력 및 저장

    # 1. CSV 파일 읽기
    header, data = read_csv_file(input_file)

    # 2. 인화성 지수로 정렬
    sorted_data = sort_by_flammability(data)

    # 3. 정렬된 데이터 출력
    print_inventory(header, sorted_data)

    # 4. 인화성 지수가 0.7 이상인 항목 추출 및 출력
    high_flammability = extract_high_flammability(sorted_data)
    print("\n인화성 지수가 0.7 이상인 항목:")
    for item in high_flammability:
        print(",".join(item))

    # 5. 추출한 항목을 CSV로 저장
    save_to_csv(header, high_flammability, danger_file)

    # 6. 이진 파일 저장 및 읽기
    save_to_binary(sorted_data, binary_file)
    read_from_binary(binary_file)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        # python .\w2\src\main.py .\w2\data\raw\Mars_Base_Inventory_List.csv .\w2\data\processed\Mars_Base_Inventory_danger.csv .\w2\data\processed\Mars_Base_Inventory_List.bin
        print("사용법: python main.py <input_file> <danger_file> <binary_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

# 텍스트 파일과 이진 파일 형태의 차이점과 장단점
"""
텍스트 파일은 가독성과 편집 용이성이 뛰어나 설정 파일이나 로그 기록처럼 사람이 자주 다뤄야 하는 경우에 적합
하지만 용량이 크고 복잡한 데이터를 다루기 어렵고,

이진 파일은 크기 효율성과 데이터 정밀도가 높아
이미지, 오디오, 대용량 데이터 저장에 유리하지만
사람이 직접 다루기 어렵고 호환성 문제가 생길 수 있다.
"""
