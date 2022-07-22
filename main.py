import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(url, token):
    headers = {
      'Authorization': f'Bearer {token}'
    }
    long_url = {"long_url": url}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=long_url
    )
    response.raise_for_status()
    short_link = response.json()
    return short_link['id']


def count_clicks(url, token):
    url = urlparse(url)
    url = f'{url.netloc}{url.path}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = (
        ('unit', 'day'),
        ('units', '-1'),

    )
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary',
        headers=headers,
        params=params
    )
    clicks_counter = response.json()
    response.raise_for_status()
    return clicks_counter['total_clicks']


def is_bitlink(url, token):
    url = urlparse(url)
    url = f'{url.netloc}{url.path}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=headers
    )
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='сокращение ссылок'
    )
    parser.add_argument('url', help='введите ссылку')
    args = parser.parse_args()
    url = args.url
    if is_bitlink(url, token):
        try:
            print('Clicks_count: ', count_clicks(url, token))
        except requests.exceptions.HTTPError as e:
            print('Error: ', e)
    else:
        try:
            print('Bitlink: ', shorten_link(url, token))
        except requests.exceptions.HTTPError as e:
            print('Error: ', e)


if __name__ == '__main__':
    main()
