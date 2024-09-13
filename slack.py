import requests
import json

class Slack:
    def __init__(self, webhook_url):
        """
        Slack 클래스 생성자. Webhook URL을 설정합니다.
        :param webhook_url: Slack에서 제공한 Incoming Webhook URL
        """
        self.webhook_url = webhook_url

    def send_message(self, message):
        """
        Slack 채널로 메시지를 전송하는 함수.
        :param message: 보낼 메시지 내용
        :return: 응답 성공 여부를 반환
        """
        message_data = {
            'text': message,
        }

        # Webhook으로 HTTP POST 요청을 보냅니다.
        response = requests.post(
            self.webhook_url,
            data=json.dumps(message_data),
            headers={'Content-Type': 'application/json'}
        )

        # 응답을 확인하고 성공 여부를 반환
        if response.status_code == 200:
            print('Message sent successfully!')
            return True
        else:
            print(f'Failed to send message: {response.status_code}, {response.text}')
            return False

# 사용 예시
if __name__ == '__main__':
    # Slack에서 제공받은 Webhook URL을 입력
    webhook_url = 'https://hooks.slack.com/services/###'

    # Slack 객체 생성
    slack = Slack(webhook_url)

    # 메시지 전송
    slack.send_message(
        message="Hello, Slack! This is a test message.",
    )
