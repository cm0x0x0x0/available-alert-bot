import time
import slack
import api_response_checker
import argparse
import threading


def check_every_interval(checker, messenger, landing_url, interval):
    while True:
        if checker.check_key_value():
            msg = "The key value is 0 or greater. 🙌" + "\n" + landing_url
            messenger.send_message(msg)
        time.sleep(interval)


def send_message_every_interval(messenger, text, interval):
    while True:
        messenger.send_message(text)
        time.sleep(interval)


def main():
    # 명령줄 인자 처리
    parser = argparse.ArgumentParser(
        description="Check if a key value from API response is greater than or equal to 0.")

    parser.add_argument('webhook_url', type=str, help="The webhook key of messenger.")
    parser.add_argument('api_url', type=str, help="The API URL to send GET request.")
    parser.add_argument('landing_url', type=str, help="The landing page URL to display after checking.")
    parser.add_argument('key_path_to_check', type=str,
                        help="The key path to check in the API response (comma separated).")
    parser.add_argument('interval', type=int, help="The interval (in seconds) at which the task will be repeated.")

    parse_args = parser.parse_args()

    key_path_to_check = parse_args.key_path_to_check.split(',')  # 리스트로 변환
    webhook_url = parse_args.webhook_url
    api_url = parse_args.api_url
    landing_url = parse_args.landing_url
    interval = parse_args.interval

    messenger = slack.Slack(webhook_url)
    checker = api_response_checker.ApiResponseChecker(api_url, key_path_to_check)


    check_thread = threading.Thread(target=check_every_interval, args=(checker, messenger, landing_url, interval))
    check_thread.daemon = True
    check_thread.start()

    liveness_msg = "App is still living ! 😎"
    liveness_check_interval = 3600
    liveness_thread = threading.Thread(target=send_message_every_interval, args=(messenger, liveness_msg, liveness_check_interval))
    liveness_thread.daemon = True
    liveness_thread.start()

    check_thread.join()
    liveness_thread.join()

if __name__ == "__main__":
    main()
