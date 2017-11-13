import re
import urllib3
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored
import sys
import os
import argparse
from itertools import product

from modules.files import Files
from modules.presentation import Presentation
from modules.response_handler import  ResponseHandler


urls = []

class UrlChecker(object):
    def __init__(self, argv):
        self.word_list = []
        self.thread_pool = ThreadPool(4)
        self.verbose = False
        self.version = '0.0.1'
        self.errors = []
        self.website = 'https://github.com/m4l1c3/url-check'
        self.urls = []
        self.out_file = ''
        self.presentation = Presentation()
        self.response_handler = ResponseHandler()
        self.files = Files()
        self.source_word_list = argv.wordlist
        self.url_validation = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.parse_arguments(argv)
        self.main()

    def main(self):
        self.presentation.print_header(self.version)

        if self.source_word_list is not None and os.path.isfile(self.source_word_list):
            try:
                with open(self.source_word_list, 'r') as word_list:
                    self.word_list = word_list.read().splitlines()

            except IOError as error:
                self.errors.append(error)
                print(error)

        if not self.word_list:
            print(colored('No URLs specified', 'red'))
        else:
            print(colored('Beginning URL Check', 'magenta'))
            self.thread_pool.map(self.request, self.word_list)

        if self.out_file is not '':
            self.files.save_output(self.out_file, urls)
        self.presentation.print_footer()

    def parse_arguments(self, argv):
        if len(sys.argv) < 1:
            sys.exit("Not enough args")
        if argv.output is not None:
            self.out_file = argv.output
        if argv.threads is not None and str.isdigit(argv.threads):
            self.thread_pool = ThreadPool(int(argv.threads))
        if argv.url is not None and self.url_validation.match(argv.url):
            self.word_list.append(argv.url)


    @staticmethod
    def request(url):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            print(colored('* ' + url + ' ' + str(response.status), get_response_color(response)))
            urls.append(url + ' ' + str(response.status))
        except Exception as ex:
            response = ex


def get_response_color(response):
    if not type(response) is urllib3.exceptions.MaxRetryError:
        if response.status < 300:
            color = 'green'
        elif response.status < 400:
            color = 'yellow'
        elif response.status < 500:
            color = 'cyan'
        else:
            color = 'red'
    else:
        color = 'red'
    return color


def parse_args(arguments=''):
    try:
        parser = argparse.ArgumentParser(arguments)
        parser.add_argument('-u', '--url')
        parser.add_argument('-w', '--wordlist')
        parser.add_argument('-t', '--threads')
        parser.add_argument('-v', '--verbose')
        parser.add_argument('-o', '--output')
        return parser.parse_args()
    except argparse.ArgumentError as er:
        print(er)


if __name__ == "__main__":
    try:
        args = parse_args()
        main = UrlChecker(args)
    except KeyboardInterrupt:
        sys.exit('Keyboard Interrupt by User!!')
    except argparse.ArgumentError as error:
        print(error)
