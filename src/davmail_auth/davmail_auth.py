#!/usr/bin/env python3

import time
from sys import stdin

import sh
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    title_empty_condition = EC.title_is('')

    def interact(line, stdin):
        print(line, end='')
        if line.startswith('https://login.microsoftonline.com/common/oauth2'):
            driver = webdriver.Chrome()
            driver.get(line)
            current_url = None
            try:
                WebDriverWait(driver, poll_frequency=0.1, timeout=300).until(title_empty_condition)
            except Exception as e:
                raise e
            finally:

                current_url = driver.current_url
                driver.quit()
            print(f'RETURNED URL: {current_url}')
            assert current_url is not None
            stdin.put(current_url)
            stdin.put('\n')

    sh.davmail('/Users/butala/.davmail.properties', _out=interact, _tty_in=True)
