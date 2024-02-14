#!/usr/bin/env python3
import requests

response = requests.get('https://api.git.com/user')

cookies = response.cookies

for cookie in cookies:
    print(f'{cookie.name}={cookie.value}')
