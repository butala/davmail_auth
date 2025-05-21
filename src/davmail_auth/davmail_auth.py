#!/usr/bin/env python3

import time
import logging
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import sh
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger('davmail_auth')

DAVMAIL_BIN = '/usr/local/bin/davmail'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = ArgumentParser('Wrapper to davmail which, when required, opens Chrome and prompts the user for authentication.',
                            epilog='All remaining arguments are passed to davmail.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--timeout', type=float, default=300, help='Timeout for user react (in seconds)')
    parser.add_argument('--poll', type=float, default=0.1, help='Poll period to check for authentication completion (in seconds)')
    args, remaining_args = parser.parse_known_args(argv[1:])

    title_empty_condition = EC.title_is('')

    def interact(line, stdin):
        print(line, end='')
        if line.startswith('https://login.microsoftonline.com/common/oauth2'):
            driver = webdriver.Chrome()
            driver.get(line)
            current_url = None
            try:
                WebDriverWait(driver, poll_frequency=args.poll, timeout=args.timeout).until(title_empty_condition)
            except Exception as e:
                raise e
            finally:

                current_url = driver.current_url
                driver.quit()
            logger.info(f'RETURNED URL: {current_url}')
            assert current_url is not None
            stdin.put(current_url)
            stdin.put('\n')

    sh.davmail(*remaining_args, _out=interact, _tty_in=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
