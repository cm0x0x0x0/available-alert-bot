import requests

class ApiResponseChecker:
    def __init__(self, url, key_path):
        """
        ApiResponseChecker 클래스 생성자.
        :param url: GET 요청을 보낼 API의 URL
        :param key_path: 확인하고자 하는 응답 JSON의 특정 키 경로 (리스트 형태, 예: ['data', 'value'])
        """
        self.url = url
        self.key_path = key_path

    def send_request(self):
        """
        API에 GET 요청을 보내고 응답을 반환합니다.
        :return: JSON 형식의 응답 또는 None (실패 시)
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
            return response.json()  # JSON 응답을 반환
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_nested_value(self, data, keys):
        """
        중첩된 JSON에서 특정 키 경로를 따라 값을 찾는 함수.
        :param data: JSON 응답 데이터
        :param keys: 확인하고자 하는 키 경로 (리스트 형태)
        :return: 찾은 값 또는 None
        """
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def check_key_value(self):
        """
        특정 키 경로에 해당하는 값이 0 이상인지 확인하는 함수.
        :return: True (키 값이 0 이상일 때), False (그 외)
        """
        response_data = self.send_request()

        if response_data is None:
            print("No response or failed to fetch the response.")
            return False

        print(response_data)

        # 중첩된 키 경로를 따라 값 찾기
        value = self.get_nested_value(response_data, self.key_path)

        if value is not None:
            if isinstance(value, (int, float)) and value > 0:
                print(f"Key path '{' -> '.join(self.key_path)}' value is {value}, which is greater than 0.")
                return True
            else:
                print(f"Key path '{' -> '.join(self.key_path)}' value is {value}, which is not more than 0 or not a number.")
                return False
        else:
            print(f"Key path '{' -> '.join(self.key_path)}' not found in the response.")
            return False

# 사용 예시
if __name__ == '__main__':
    # 확인하고 싶은 API URL과 중첩된 key 경로
    api_url = 'https://api.example.com/data'
    key_path_to_check = ['data', 'details', 'value']  # 중첩된 키 경로

    # ApiResponseChecker 객체 생성
    checker = ApiResponseChecker(api_url, key_path_to_check)

    # 특정 키 값이 0 이상인지 확인
    if checker.check_key_value():
        print("The key value is 0 or greater.")
    else:
        print("The key value is not more than 0 or not a number")
