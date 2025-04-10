# 스토리
지금 생각해도 화성 기지가 왜 폭발 했는지 아직 잘 모르겠다.
어쩌면 한낯 식물학자 따위가 알기에는 시작부터 뭐가 잘못된 것인지 알 수도 없다.
하지만 지금 주위에는 아무도 없고 나머지 사람들의 생사는 알 수도 없고 알 수 있는 방법도 없었다.
잠깐 멘탈이 나가 있었지만 냉정하게 지금 당장 할 수 있는 일과 할 수 없는 일 그리고 가장 먼저 해야 할 일 들을 정리했다.

지구에서 가장 가까울 때라도 54.6백만 Km 떨어진 화성에 홀로 남겨진 식물학자 가장 먼저 해야 할 일은 바로 눈앞에 차갑게 말없이 있는 미션 컴퓨터를 깨우는 일이었다.
미션 컴퓨터의 전원을 넣자 반가운 짧은 비프음과 함께 화면이 밝아지기 시작했다.
컴퓨터를 조용히 살펴보던 그녀는 잠시 뒤 운영체제를 제외하고 모든 소프트웨어가 지난 사고 때문에 삭제 되어 버린 것을 알게 되었다.

망연자실해서 몇 분을 그 자세로 앉아있다가.
우연히 컴퓨터 옆에 보니 ‘미션 컴퓨터 쿡북(Mission Computer Cookbook)’라는 책자가 한 권 남아 있는 것을 알게 되었다.
미션 컴퓨터 쿡북에서는 미션 컴퓨터의 기능들과 동작 그리고 활용법에 대한 자세한 내용들이 기술되어 있었다.

한 박사는 지금은 먼저 사고 원인을 이해하고 화성 기지를 재건하는 것이 급선무라는 생각이 들자 마자 쿡북을 집어 들고 일기 시작했다.
쿡북에 따르면 미션 컴퓨터는 mission_computer_main.log 파일에 주요 동작들에 대한 기록들이 남겨져 있다는 것을 알게 되었다.
얼른 미션 컴퓨터를 다시 살펴 보니 별도의 드라이브에 저장되던 로그 파일과 일부 데이터 파일들이 남아 있었다.

이제 로그 파일을 읽어 들이고 분석한다면 사고의 원인을 알아 낼 수 있을 것이다.
비록 로그 분석을 위한 그 흔한 소프트웨어 하나 없는 상황이긴 하지만 인간은 늘 방법을 찾아내왔고 그리고 오늘 나도 그 방법을 찾아 낼 것이다.

# 수행과제
로그 분석을 위해 Python으로 소프트웨어를 개발해야 한다. 이를 위해서 먼저 Python을 설치해야 한다.
빠른 개발을 위해 Python 개발 도구들을 알아보고 비교해서 하나의 도구를 선정해서 설치한다.
설치가 잘 되었는지 확인 하기 위해서 ‘Hello Mars’를 출력해 본다.
본격적으로 로그를 분석하기 위해서 mission_computer_main.log 파일을 열고 전체 내용을 화면에 출력해 본다.
이때 코드는 main.py 파일로 저장한다. (로그 데이터는 별도 제공)
파일을 처리 할 때에 발생할 수 있는 예외를 처리한다.
mission_computer_main.log의 내용을 통해서 사고의 원인을 분석하고 정리해서 보고서(log_analysis.md)를 Markdown 형태로 를 작성해 놓는다.

# 개발환경
Python 버전은 3.x 버전으로 한다.
Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다.
Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다. (PEP 8 – 파이썬 코드 스타일 가이드 | peps.python.org)
문자열을 표현 할 때에는 ‘ ’을 기본으로 사용한다.
다만 문자열 내에서 ‘을 사용할 경우와 같이 부득이한 경우에는 “ “를 사용한다.
foo = (0,) 와 같이 대입문의 = 앞 뒤로는 공백을 준다.
들여 쓰기는 공백을 기본으로 사용합니다.

# 제약사항
보고서는 UTF8 형태의 encoding을 사용해서 저장한다.
수행 과제에 지시된 파일 이름을 준수한다.

# 보너스 과제
출력 결과를 시간의 역순으로 정렬해서 출력한다.
출력 결과 중 문제가 되는 부분만 따로 파일로 저장한다.
