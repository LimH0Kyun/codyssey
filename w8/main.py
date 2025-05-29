#!/usr/bin/env python3
"""
화성 기지 Emergency Storage 해독 프로그램
6자리 숫자+소문자 알파벳 조합의 ZIP 파일 암호를 브루트포스로 해독
"""

import zipfile
import string
import time
import itertools
import multiprocessing as mp
from multiprocessing import Pool, Manager


def generate_password_batch(start_idx, batch_size, charset, length):
    """주어진 범위의 암호 조합을 생성하는 함수"""
    passwords = []
    total_combinations = len(charset) ** length
    
    for i in range(start_idx, min(start_idx + batch_size, total_combinations)):
        password = ''
        temp = i
        for _ in range(length):
            password = charset[temp % len(charset)] + password
            temp //= len(charset)
        passwords.append(password)
    
    return passwords


def try_passwords_batch(args):
    """배치로 암호를 시도하는 함수 (멀티프로세싱용)"""
    zip_filename, passwords, process_id = args
    
    for password in passwords:
        try:
            with zipfile.ZipFile(zip_filename, 'r') as zip_file:
                # 첫 번째 파일만 테스트로 읽어보기
                file_list = zip_file.namelist()
                if file_list:
                    # 실제로 파일을 읽어서 암호가 맞는지 확인
                    zip_file.read(file_list[0], pwd=password.encode('utf-8'))
                    return password, process_id
        except Exception:
            # 모든 종류의 오류를 무시하고 계속 진행
            continue
    
    return None, process_id


def unlock_zip():
    """Emergency Storage ZIP 파일의 암호를 해독하는 함수"""
    import os
    zip_filename = '/emergency_storage_key.zip'
    
    # 현재 디렉토리에서 파일 찾기
    if not os.path.exists(zip_filename):
        zip_filename = os.path.join('.', '/emergency_storage_key.zip')
    
    if not os.path.exists(zip_filename):
        print(f'현재 디렉토리: {os.getcwd()}')
        print(f'디렉토리 내용: {os.listdir(".")}')
    
    zip_filename = '/emergency_storage_key.zip'
    charset = string.digits + string.ascii_lowercase  # 0-9, a-z
    password_length = 6
    
    print('=' * 60)
    print('화성 기지 Emergency Storage 해독 시작!')
    print('=' * 60)
    print(f'대상 파일: {zip_filename}')
    print(f'암호 조건: {password_length}자리 숫자+소문자')
    print(f'문자셋: {charset}')
    print(f'총 경우의 수: {len(charset) ** password_length:,}')
    
    # ZIP 파일 존재 확인
    try:
        with zipfile.ZipFile(zip_filename, 'r') as test_zip:
            pass
    except FileNotFoundError:
        print(f'오류: {zip_filename} 파일을 찾을 수 없습니다!')
        return None
    except zipfile.BadZipFile:
        print(f'오류: {zip_filename}는 유효한 ZIP 파일이 아닙니다!')
        return None
    
    start_time = time.time()
    total_combinations = len(charset) ** password_length
    
    # CPU 코어 수 확인 및 프로세스 설정
    cpu_count = mp.cpu_count()
    process_count = min(cpu_count, 8)  # 최대 8개 프로세스
    batch_size = 1000  # 각 배치당 시도할 암호 개수
    
    print(f'CPU 코어 수: {cpu_count}')
    print(f'사용할 프로세스 수: {process_count}')
    print(f'배치 크기: {batch_size}')
    print('-' * 60)
    
    found_password = None
    attempts = 0
    
    try:
        with Pool(processes=process_count) as pool:
            # 작업을 배치 단위로 분할
            batch_start = 0
            
            while batch_start < total_combinations and found_password is None:
                # 각 프로세스에 할당할 작업 생성
                tasks = []
                
                for process_id in range(process_count):
                    if batch_start >= total_combinations:
                        break
                    
                    current_batch_size = min(batch_size, 
                                           total_combinations - batch_start)
                    passwords = generate_password_batch(batch_start, 
                                                     current_batch_size, 
                                                     charset, 
                                                     password_length)
                    
                    tasks.append((zip_filename, passwords, process_id))
                    batch_start += current_batch_size
                    attempts += current_batch_size
                
                if not tasks:
                    break
                
                # 병렬로 암호 시도
                results = pool.map(try_passwords_batch, tasks)
                
                # 결과 확인
                for result, process_id in results:
                    if result is not None:
                        found_password = result
                        break
                
                # 진행 상황 출력
                elapsed_time = time.time() - start_time
                progress = (attempts / total_combinations) * 100
                speed = attempts / elapsed_time if elapsed_time > 0 else 0
                
                print(f'진행률: {progress:.2f}% | '
                      f'시도: {attempts:,} | '
                      f'경과시간: {elapsed_time:.1f}초 | '
                      f'속도: {speed:.0f} 암호/초')
                
    except KeyboardInterrupt:
        print('\n해독 작업이 중단되었습니다.')
        return None
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print('-' * 60)
    
    if found_password:
        print(f'🎉 암호 해독 성공!')
        print(f'발견된 암호: {found_password}')
        print(f'총 시도 횟수: {attempts:,}')
        print(f'소요 시간: {elapsed_time:.2f}초')
        print(f'평균 속도: {attempts/elapsed_time:.0f} 암호/초')
        
        # 암호를 파일에 저장
        try:
            with open('password.txt', 'w', encoding='utf-8') as f:
                f.write(found_password)
            print(f'암호가 password.txt 파일에 저장되었습니다.')
        except IOError as e:
            print(f'파일 저장 오류: {e}')
        
        return found_password
    else:
        print('😞 암호를 찾지 못했습니다.')
        print(f'총 시도 횟수: {attempts:,}')
        print(f'소요 시간: {elapsed_time:.2f}초')
        return None


def unlock_zip_simple():
    """단순한 브루트포스 방식 (단일 프로세스)"""
    import os
    zip_filename = '/emergency_storage_key.zip'
    
    # 현재 디렉토리에서 파일 찾기
    if not os.path.exists(zip_filename):
        zip_filename = os.path.join('.', '/emergency_storage_key.zip')
    
    if not os.path.exists(zip_filename):
        print(f'현재 디렉토리: {os.getcwd()}')
        print(f'디렉토리 내용: {os.listdir(".")}')
    
    zip_filename = '/emergency_storage_key.zip'
    charset = string.digits + string.ascii_lowercase
    password_length = 6
    
    print('=' * 60)
    print('단순 브루트포스 해독 시작 (단일 프로세스)')
    print('=' * 60)
    
    # ZIP 파일 존재 확인
    try:
        with zipfile.ZipFile(zip_filename, 'r') as test_zip:
            pass
    except FileNotFoundError:
        print(f'오류: {zip_filename} 파일을 찾을 수 없습니다!')
        return None
    except zipfile.BadZipFile:
        print(f'오류: {zip_filename}는 유효한 ZIP 파일이 아닙니다!')
        return None
    
    start_time = time.time()
    attempts = 0
    
    try:
        # 모든 가능한 암호 조합 생성 및 시도
        for password_tuple in itertools.product(charset, repeat=password_length):
            password = ''.join(password_tuple)
            attempts += 1
            
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zip_file:
                    # 첫 번째 파일만 읽어서 테스트
                    file_list = zip_file.namelist()
                    if file_list:
                        zip_file.read(file_list[0], pwd=password.encode('utf-8'))
                
                # 성공한 경우
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                print(f'🎉 암호 해독 성공!')
                print(f'발견된 암호: {password}')
                print(f'총 시도 횟수: {attempts:,}')
                print(f'소요 시간: {elapsed_time:.2f}초')
                
                # 암호를 파일에 저장
                try:
                    with open('password.txt', 'w', encoding='utf-8') as f:
                        f.write(password)
                    print(f'암호가 password.txt 파일에 저장되었습니다.')
                except IOError as e:
                    print(f'파일 저장 오류: {e}')
                
                return password
                
            except Exception:
                # 모든 ZIP 관련 오류를 무시하고 계속 진행
                if attempts % 10000 == 0:
                    elapsed_time = time.time() - start_time
                    speed = attempts / elapsed_time if elapsed_time > 0 else 0
                    print(f'시도: {attempts:,} | '
                          f'경과시간: {elapsed_time:.1f}초 | '
                          f'속도: {speed:.0f} 암호/초')
                continue
    
    except KeyboardInterrupt:
        print('\n해독 작업이 중단되었습니다.')
        return None
    
    print('😞 암호를 찾지 못했습니다.')
    return None


def create_test_zip():
    """테스트용 ZIP 파일 생성 함수"""
    test_password = 'test01'
    zip_filename = '/emergency_storage_key.zip'
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 파일 내용을 ZIP에 추가
            zip_file.writestr('emergency_supplies.txt', 
                            '비상 물품 목록:\n- 산소 캔슐 x5\n- 응급 식량 x10\n- 커피 x3\n- 정수 필터 x2\n- 의료용품 세트 x1')
        
        # 암호 설정을 위해 다시 열기
        with zipfile.ZipFile(zip_filename, 'a') as zip_file:
            zip_file.setpassword(test_password.encode('utf-8'))
        
        print(f'테스트 ZIP 파일이 생성되었습니다: {zip_filename}')
        print(f'테스트 암호: {test_password}')
        
    except Exception as e:
        print(f'테스트 파일 생성 오류: {e}')
        
        # 대안: 외부 명령어 없이 간단한 ZIP 생성
        try:
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write('비상 물품 목록:\n- 산소 캔슐 x5\n- 응급 식량 x10\n- 커피 x3')
                temp_filename = temp_file.name
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(temp_filename, 'emergency_supplies.txt')
                zip_file.setpassword(test_password.encode('utf-8'))
            
            os.unlink(temp_filename)
            print(f'대안 방법으로 테스트 ZIP 파일 생성 완료')
            
        except Exception as e2:
            print(f'대안 방법도 실패: {e2}')


if __name__ == '__main__':
    print('화성 기지 Emergency Storage 해독 프로그램')
    print('=' * 60)
    
    # 메뉴 선택
    print('1. 멀티프로세싱 해독 (권장)')
    print('2. 단일 프로세스 해독')
    print('3. 테스트 ZIP 파일 생성')
    
    try:
        choice = input('\n선택하세요 (1-3): ').strip()
        
        if choice == '1':
            unlock_zip()
        elif choice == '2':
            unlock_zip_simple()
        elif choice == '3':
            create_test_zip()
        else:
            print('잘못된 선택입니다. 멀티프로세싱 해독을 실행합니다.')
            unlock_zip()
            
    except KeyboardInterrupt:
        print('\n프로그램이 종료되었습니다.')
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')