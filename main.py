import requests
import time
import json
import os


def send_report(tests: list):
    payload = {'token': os.environ.get('TOKEN'), "tests": tests}
    r = requests.post(f'{os.environ.get("SERVER")}/send_result/', data=payload)

    time.sleep(300)


def test(domain: str):
    tests_failed = []

    # Страница Донатов
    r = requests.get(f'{domain}/donate')
    if 'bc1q95nlgsmz88qw3zluns76q2cv5r400lrtrq32m6' not in r.text:
        tests_failed.append(f'{domain}/donate bitcoin адрес')

    # Контакты
    r = requests.get(f'{domain}/contact')
    if 'https://t.me/s_nami_bot' not in r.text:
        tests_failed.append(f'{domain}/contact бот связи')

    # Расследование
    r = requests.get(f'{domain}/investigation/roskosmos-delo-na-milliard')
    if 'Роскосмос: дело на миллиард' not in r.text:
        tests_failed.append(f'{domain}/investigation/roskosmos-delo-na-milliard заголовок не совпадает')

    # /uploads
    r = requests.get(f'{domain}/uploads/64f0f340e322a656c737f_5d01eb5171.jpg')
    if r.headers['Content-Type'] != 'image/jpeg':
        tests_failed.append(f'{domain}/uploads/64f0f340e322a656c737f_5d01eb5171.jpg не image/jpeg')

    if tests_failed:
        send_report(tests_failed)


def main():
    while True:
        try:
            r = requests.get(f'{os.environ.get("SERVER")}/domains/')
            for domain in r.json()['domains']:
                test(domain)

        except Exception as e:
            print(e)

        time.sleep(60)


if __name__ == '__main__':
    main()

