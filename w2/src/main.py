def read_csv_file(file_path):
    # 주어진 파일 경로에서 CSV 파일을 읽어 헤더와 데이터를 반환
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            header = lines[0].strip().split(",")
            data = [line.strip().split(",") for line in lines[1:]]
            return header, data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None, None
    except PermissionError:
        print("파일을 읽을 권한이 없습니다.")
        return None, None
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
        return None, None


def sort_by_flammability(data):
    # 데이터 리스트를 마지막 열(인화성 지수)을 기준으로 내림차순 정렬
    try:
        return sorted(data, key=lambda x: float(x[-1]), reverse=True)
    except ValueError:
        print("인화성 지수를 숫자로 변환할 수 없습니다.")
        return None


def print_inventory(header, data):
    # 헤더와 데이터를 콘솔에 출력
    print(",".join(header))
    for item in data:
        print(",".join(item))


def extract_high_flammability(data, threshold=0.7):
    # 데이터에서 인화성 지수가 threshold 이상인 항목을 추출
    try:
        return [item for item in data if float(item[-1]) >= threshold]
    except ValueError:
        print("인화성 지수를 숫자로 변환할 수 없습니다.")
        return None


def save_to_csv(header, data, output_file):
    # 헤더와 데이터를 지정된 output_file에 CSV 형식으로 저장
    try:
        with open(output_file, "w") as file:
            file.write(",".join(header) + "\n")
            for item in data:
                file.write(",".join(item) + "\n")
        print(f"인화성 지수가 0.7 이상인 항목을 {output_file} 파일에 저장했습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")


def save_to_binary(data, binary_file):
    # 데이터를 이진 파일로 저장, 각 항목의 길이를 4바이트로 기록한 후 데이터를 기록
    try:
        with open(binary_file, "wb") as file:
            for item in data:
                line = ",".join(item).encode("utf-8")
                length = len(line)
                file.write(length.to_bytes(4, byteorder="big"))
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
                length = int.from_bytes(length_data, byteorder="big")
                line_data = file.read(length)
                print(line_data.decode("utf-8"))
    except Exception as e:
        print(f"이진 파일 읽기 중 오류가 발생했습니다: {e}")


def main():
    # 고정된 파일 경로 설정
    input_file = "./w2/data/raw/Mars_Base_Inventory_List.csv"
    danger_file = "./w2/data/processed/Mars_Base_Inventory_danger.csv"
    binary_file = "./w2/data/processed/Mars_Base_Inventory_List.bin"

    # CSV 파일 읽기
    header, data = read_csv_file(input_file)
    if header is None or data is None:
        return

    # 인화성 지수로 정렬
    sorted_data = sort_by_flammability(data)
    if sorted_data is None:
        return

    # 인벤토리 출력
    print_inventory(header, sorted_data)

    # 인화성 지수가 높은 항목 추출
    high_flammability = extract_high_flammability(sorted_data)
    if high_flammability is None:
        return

    # 결과 출력
    print("\n인화성 지수가 0.7 이상인 항목:")
    for item in high_flammability:
        print(",".join(item))

    # CSV 파일로 저장
    save_to_csv(header, high_flammability, danger_file)

    # 바이너리 파일로 저장
    save_to_binary(sorted_data, binary_file)

    # 바이너리 파일 읽기
    read_from_binary(binary_file)


# 실행
if __name__ == "__main__":
    main()
