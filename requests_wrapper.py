import requests

class GetRequest:
    def __init__(self, url, user_agent = "Your Name <youremail@example.com>"):
        response = requests.get(url, headers={"User-Agent": user_agent})
        response.encoding = 'utf-8'
        if response.status_code != requests.codes.ok:
            raise RequestException('{}: {}'.format(response.status_code, response.text))
        
        self.response = response

class RequestException(Exception):
    pass