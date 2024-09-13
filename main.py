import slack
import api_response_checker
import argparse


def main():
    # 명령줄 인자 처리
    parser = argparse.ArgumentParser(
        description="Check if a key value from API response is greater than or equal to 0.")

    parser.add_argument('webhook_url', type=str, help="The webhook key of messenger.")
    parser.add_argument('api_url', type=str, help="The API URL to send GET request.")
    parser.add_argument('landing_url', type=str, help="The landing page URL to display after checking.")
    parser.add_argument('key_path_to_check', type=str,
                        help="The key path to check in the API response (comma separated).")

    args = parser.parse_args()

    key_path_to_check = args.key_path_to_check.split(',')  # 리스트로 변환
    webhook_url = args.webhook_url
    api_url = args.api_url
    landing_url = args.landing_url

    messenger = slack.Slack(webhook_url)
    checker = api_response_checker.ApiResponseChecker(api_url, key_path_to_check)
    if checker.check_key_value():
        msg = "The key value is 0 or greater. 🙌" + "\n" + landing_url
    else:
        msg = "The key value is 0 or not a number. 😭"

    messenger.send_message(msg)


if __name__ == "__main__":
    main()
