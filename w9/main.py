def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 모든 가능한 시프트(0-25)로 해독하는 함수
    
    Args:
        target_text (str): 해독할 암호화된 텍스트
    """
    print('=== 카이사르 암호 해독 시작 ===')
    print(f'원본 암호문: {target_text}')
    print('-' * 50)
    
    # 각 시프트별 해독 결과 저장
    decoded_results = {}
    
    for shift in range(26):
        decoded_text = ''
        
        for char in target_text:
            if char.isalpha():
                # 대문자 처리
                if char.isupper():
                    decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                # 소문자 처리
                else:
                    decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decoded_text += decoded_char
            else:
                # 알파벳이 아닌 문자는 그대로 유지
                decoded_text += char
        
        decoded_results[shift] = decoded_text
        print(f'시프트 {shift:2d}: {decoded_text}')
    
    print('-' * 50)
    return decoded_results


def load_password_file():
    """password.txt 파일을 읽어오는 함수"""
    try:
        with open('9week/password.txt', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            print(f'password.txt 파일을 성공적으로 읽었습니다.')
            return content
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
        print('테스트용 암호문을 사용합니다: "Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj"')
        return 'Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj'
    except Exception as e:
        print(f'파일 읽기 중 오류가 발생했습니다: {e}')
        return None


def save_result(shift_number, decoded_text):
    """해독 결과를 result.txt에 저장하는 함수"""
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(f'시프트 번호: {shift_number}\n')
            file.write(f'해독된 텍스트: {decoded_text}\n')
        print(f'결과가 result.txt에 저장되었습니다.')
        return True
    except Exception as e:
        print(f'파일 저장 중 오류가 발생했습니다: {e}')
        return False


def create_dictionary():
    """텍스트 사전을 만드는 함수 (보너스 과제)"""
    # 일반적인 영어 단어들
    common_words = [
        'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with',
        'for', 'as', 'was', 'on', 'are', 'you', 'this', 'be', 'at', 'or',
        'have', 'from', 'an', 'they', 'which', 'one', 'had', 'by', 'words',
        'but', 'not', 'what', 'all', 'were', 'when', 'we', 'there', 'can',
        'said', 'each', 'she', 'do', 'how', 'their', 'if', 'will', 'up',
        'other', 'about', 'out', 'many', 'then', 'them', 'these', 'so',
        'some', 'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two',
        'more', 'very', 'after', 'use', 'our', 'way', 'than', 'first',
        'water', 'been', 'call', 'who', 'its', 'now', 'find', 'long', 'down',
        'day', 'did', 'get', 'come', 'made', 'may', 'part', 'over', 'new',
        'sound', 'take', 'only', 'little', 'work', 'know', 'place', 'year',
        'live', 'me', 'back', 'give', 'most', 'very', 'after', 'things',
        'our', 'just', 'name', 'good', 'sentence', 'man', 'think', 'say',
        'great', 'where', 'help', 'through', 'much', 'before', 'line',
        'right', 'too', 'means', 'old', 'any', 'same', 'tell', 'boy',
        'follow', 'came', 'want', 'show', 'also', 'around', 'form', 'three',
        'small', 'set', 'put', 'end', 'why', 'again', 'turn', 'here',
        'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog'
    ]
    return set(word.lower() for word in common_words)


def find_meaningful_text(decoded_results, dictionary):
    """사전의 단어들과 매칭되는 해독문을 찾는 함수 (보너스 과제)"""
    print('\n=== 자동 의미 있는 텍스트 탐지 ===')
    
    best_matches = []
    
    for shift, text in decoded_results.items():
        words = text.lower().split()
        matches = 0
        
        for word in words:
            # 구두점 제거
            clean_word = ''.join(char for char in word if char.isalpha())
            if clean_word in dictionary:
                matches += 1
        
        if matches > 0:
            match_ratio = matches / len(words) if words else 0
            best_matches.append((shift, text, matches, match_ratio))
            print(f'시프트 {shift:2d}: {matches}개 단어 매칭 ({match_ratio:.2%}) - {text}')
    
    if best_matches:
        # 매칭 비율이 가장 높은 것을 찾기
        best_match = max(best_matches, key=lambda x: x[3])
        print(f'\n가장 유력한 해독문: 시프트 {best_match[0]} ({best_match[3]:.2%} 매칭)')
        return best_match[0], best_match[1]
    
    return None, None


def main():
    """메인 실행 함수"""
    print('화성 기지 비상 저장소 암호 해독 프로그램')
    print('=' * 50)
    
    # 1. password.txt 파일 읽기
    password_text = load_password_file()
    if password_text is None:
        return
    
    # 2. 카이사르 암호 해독
    decoded_results = caesar_cipher_decode(password_text)
    
    # 3. 보너스 과제: 자동으로 의미 있는 텍스트 찾기
    dictionary = create_dictionary()
    auto_shift, auto_text = find_meaningful_text(decoded_results, dictionary)
    
    if auto_shift is not None:
        print(f'\n자동 탐지된 해독문을 result.txt에 저장할까요? (y/n): ', end='')
        choice = input().lower()
        if choice == 'y':
            save_result(auto_shift, auto_text)
            print('자동 탐지 완료!')
            return
    
    # 4. 수동으로 시프트 번호 선택
    print('\n어떤 시프트 번호의 결과가 올바른 해독문인가요?')
    print('(0-25 사이의 숫자를 입력하세요, 종료하려면 -1)')
    
    while True:
        try:
            shift_choice = int(input('시프트 번호: '))
            
            if shift_choice == -1:
                print('프로그램을 종료합니다.')
                break
            
            if 0 <= shift_choice <= 25:
                selected_text = decoded_results[shift_choice]
                print(f'선택된 해독문: {selected_text}')
                
                confirm = input('이 결과를 result.txt에 저장하시겠습니까? (y/n): ').lower()
                if confirm == 'y':
                    if save_result(shift_choice, selected_text):
                        print('성공적으로 저장되었습니다!')
                    break
            else:
                print('0부터 25 사이의 숫자를 입력해주세요.')
                
        except ValueError:
            print('올바른 숫자를 입력해주세요.')
        except KeyboardInterrupt:
            print('\n프로그램을 종료합니다.')
            break


if __name__ == '__main__':
    main()