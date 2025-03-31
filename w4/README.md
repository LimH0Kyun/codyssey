# 스토리 
더미 센서를 만들어 놓고 나니 이제는 미션 컴퓨터에서 직접 센서 데이터의 결과를 출력하고 내용을 확인할 수 있게 구성하는게 필요했다.
화성에서 사람이 살아가는데 필수적인 기지 내외부의 온도 그리고 광량, 이산화탄소의 농도와 산소 농도등을 확인 할 수 있게 구성해야 했다. 
지구에서라면 수치 하나 하나가 실험실의 결과일 수도 있지만 여기서는 모두 생존과 관련되어 있어서 심각한 표정으로 한송희 박사는 코드를 들여다 보기 시작했다. 

# 수행과제 
미션 컴퓨터에 해당하는 클래스를 생성한다.
클래스의 이름은 MissionComputer로 정의한다. 
미션 컴퓨터에는 화성 기지의 환경에 대한 값을 저장할 수 있는 사전(Dict) 객체가 env_values라는 속성으로 포함되어야 한다. 
env_values라는 속성 안에는 다음과 같은 내용들이 구현 되어야 한다. 
화성 기지 내부 온도 (mars_base_internal_temperature)
화성 기지 외부 온도 (mars_base_external_temperature)
화성 기지 내부 습도 (mars_base_internal_humidity)
회성 기지 외부 광량 (mars_base_external_illuminance)
화성 기지 내부 이산화탄소 농도 (mars_base_internal_co2)
화성 기지 내부 산소 농도 (mars_base_internal_oxygen)
문제 3에서 제작한 DummySensor 클래스를 ds라는 이름으로 인스턴스화 시킨다. 
MissionComputer에 get_sensor_data() 메소드를 추가한다. 
get_sensor_data() 메소드에 다음과 같은 세 가지 기능을 추가한다. 
센서의 값을 가져와서 env_values에 담는다. 
env_values의 값을 출력한다. 이때 환경 정보의 값은 json 형태로 화면에 출력한다. 
위의 두 가지 동작을 5초에 한번씩 반복한다. 
MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화 한다.  
RunComputer 인스턴스의 get_sensor_data() 메소드를 호출해서 지속적으로 환경에 대한 값을 출력 할 수 있도록 한다.
전체 코드를 mars_mission_computer.py 파일로 저장한다. 

# 개발환경	
Python 버전은 3.x 버전으로 한다. 
Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다. 
Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다. (PEP 8 – 파이썬 코드 스타일 가이드 | peps.python.org)
문자열을 표현 할 때에는 ‘ ’을 기본으로 사용한다.
다만 문자열 내에서 ‘을 사용할 경우와 같이 부득이한 경우에는 “ “를 사용한다. 
foo = (0,) 와 같이 대입문의  = 앞 뒤로는 공백을 준다. 
들여 쓰기는 공백을 기본으로 사용합니다. 

# 제약사항
Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다. 
단 시간을 다루는 라이브러리는 사용 가능하다. 
Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다. 
경고 메시지 없이 모든 코드는 실행 되어야 한다. 

# 보너스 과제
특정 키를 입력할 경우 반복적으로 출력되던 화성 기지의 환경에 대한 출력을 멈추고 ‘Sytem stoped….’ 를 출력 할 수 있어야 한다. 
5분에 한번씩 각 환경값에 대한 5분 평균 값을 별도로 출력한다. 