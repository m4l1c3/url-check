import re
import urllib3
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored
import sys
import os
import argparse


class UrlChecker(object):
    def main(self, argv):
        self.word_list = []
        self.thread_pool = ThreadPool(4)
        self.verbose = False
        self.version = '0.0.1'
        self.errors = []
        self.website = 'https://github.com/m4l1c3/url-check'

        print_header(self.version)

        self.url_validation = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if len(sys.argv) < 1:
            sys.exit("Not enough args")
        if argv.threads is not None and str.isdigit(argv.threads):
            self.thread_pool = ThreadPool(int(argv.threads))
        if argv.url is not None and self.url_validation.match(argv.url):
            self.word_list.append(argv.url)
        if argv.wordlist is not None and os.path.isfile(argv.wordlist):
            try:
                with open(argv.wordlist, 'r') as word_list:
                    self.word_list = word_list.read().splitlines()

            except IOError as error:
                self.errors.append(error)
                print(error)

        if not self.word_list:
            print(colored('No URLs specified', 'red'))
        else:
            print(colored('Beginning URL Check', 'magenta'))
            self.thread_pool.map(request, self.word_list)

        print_footer()


def print_footer():
    color = 'magenta'
    print('\n')
    print(colored(get_seperator(), color))
    print(colored(get_footer(), color))
    print(colored(get_seperator(), color))


def print_header(version):
    color = 'magenta'
    print(colored(get_seperator(), color))
    print(colored(get_banner(), color))
    print(colored(get_seperator(), color))
    print(colored(get_version(version), color))


def get_version(version):
    return '\nVersion: ' + version + '\n'


def get_seperator():
    return '**************************************************************'


def get_footer():
    footer = '* https://github.com/m4l1c3/url-check                        *'
    return footer


def get_banner():
    banner = '*               __           __              __              *\n'
    banner += '*   __  _______/ /     _____/ /_  ___  _____/ /_____  _____  *\n'
    banner += '*  / / / / ___/ /_____/ ___/ __ \/ _ \/ ___/ //_/ _ \/ ___/  *\n'
    banner += '* / /_/ / /  / /_____/ /__/ / / /  __/ /__/ ,< /  __/ /      *\n'
    banner += '* \__,_/_/  /_/      \___/_/ /_/\___/\___/_/|_|\___/_/       *'

    return banner


def get_response_color(response):
    if not type(response) is urllib3.exceptions.MaxRetryError:
        if 200 <= response.status < 300:
            color = 'green'
        elif 300 <= response.status < 400:
            color = 'yellow'
        elif 400 <= response.status < 500:
            color = 'cyan'
        else:
            color = 'red'
    else:
        color = 'red'
    return color


def request(url):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        print(colored('* ' + url, get_response_color(response)))
    except Exception as ex:
        response = ex


def parse_args(arguments=''):
    try:
        parser = argparse.ArgumentParser(arguments)
        parser.add_argument('-u', '--url')
        parser.add_argument('-w', '--wordlist')
        parser.add_argument('-t', '--threads')
        parser.add_argument('-v', '--verbose')
        return parser.parse_args()
    except argparse.ArgumentError as er:
        print(er)


if __name__ == "__main__":
    try:
        args = parse_args()
        main = UrlChecker().main(args)
    except KeyboardInterrupt:
        sys.exit('Keyboard Interrupt by User!!')
    except argparse.ArgumentError as error:
        print(error)
