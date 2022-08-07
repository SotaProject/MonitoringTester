import requests
import time
import json
import os


VERSION = '0.1'


def send_report(results: dict) -> int:
    payload = {
        'token': os.environ.get('TOKEN'),
        'results': results,
        'version': VERSION
    }
    r = requests.post(f'{os.environ.get("SERVER")}/send_result/', data=json.dumps(payload))
    return r.status_code


def run_test(test_type: str, domain: str, path: str, value: str) -> (bool, str):
    r = requests.get(domain + path)

    match test_type:
        case "text_on_page":
            if value not in r.text:
                return False, 'Text not on page'
            return True, 'Success'
        case "content_type":
            if r.headers['Content-Type'] != value:
                return False, f'Content-Type {r.headers["Content-Type"]}'
            return True, 'Success'
        case _:
            print(f'Unsupported test type {{ test_type }}')
            return False, f'Unsupported test type {{ test_type }}'


def main():
    while True:
        try:
            r = requests.get(f'{os.environ.get("SERVER")}/tests/')
            domains = r.json()['domains']
            tests = r.json()['tests']
            results = {}
            for domain in domains:
                for test_id, test in tests.items():
                    success, result = run_test(test['type'], domain, test['path'], test['value'])
                    results[test_id] = {'domain': domain, 'success': success, 'result': result}
            status_code = 0
            while status_code != 200:
                status_code = send_report(results)
                time.sleep(60)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()

