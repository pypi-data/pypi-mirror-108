import os
import sys

__version__ = '0.1.16.dev1'

def login(api_token=None):
    if api_token is None:
        try:
            from IPython.display import IFrame, display, clear_output
            iframe = IFrame('https://finlab-python.github.io/api_token', width=620, height=300)
            display(iframe)
            api_token = input('輸入驗證碼')
            clear_output()
            print('登入成功!')
        except:
            print('Go to this URL in a browser: https://finlab-python.github.io/api_token')
            api_token = input('Enter your api_token:\n')

    os.environ['finlab_id_token'] = api_token

def get_token():

    if 'finlab_id_token' not in os.environ:
        login()

    return os.environ['finlab_id_token']
