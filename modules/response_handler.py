import urllib3


class ResponseHandler(object):
    def __init__(self):
        return

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