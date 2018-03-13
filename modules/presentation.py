from termcolor import colored


class Presentation(object):
    def __init__(self):
        return

    def print_footer(self):
        color = 'magenta'
        print('\n')
        print(colored(self.get_seperator(), color))
        print(colored(self.get_footer(), color))
        print(colored(self.get_seperator(), color))

    def print_header(self, version):
        color = 'magenta'
        print(colored(self.get_seperator(), color))
        print(colored(self.get_banner(), color))
        print(colored(self.get_seperator(), color))
        print(colored(self.get_version(version), color))

    @staticmethod
    def get_version(version):
        return '\nVersion: ' + version + '\n'

    @staticmethod
    def get_seperator():
        return '**************************************************************'

    @staticmethod
    def get_footer():
        footer = '* https://github.com/m4l1c3/url-checker                     *'
        return footer

    @staticmethod
    def get_banner():
        banner = '*               __           __              __              *\n'
        banner += '*   __  _______/ /     _____/ /_  ___  _____/ /_____  _____  *\n'
        banner += '*  / / / / ___/ /_____/ ___/ __ \/ _ \/ ___/ //_/ _ \/ ___/  *\n'
        banner += '* / /_/ / /  / /_____/ /__/ / / /  __/ /__/ ,< /  __/ /      *\n'
        banner += '* \__,_/_/  /_/      \___/_/ /_/\___/\___/_/|_|\___/_/       *\n'
        banner += '*                                                            *\n'
        banner += '*                                                by:  m4l1c3 *'
        return banner
