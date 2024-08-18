import os
from datetime import datetime


class MiddlewareSaveFile:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        name = None
        method = request.method
        if request.user.is_authenticated:
            name = request.user.username
        ip = request.META.get('REMOTE_ADDR')
        url = request.path
        start = datetime.now()
        response = self._get_response(request)
        end = datetime.now()
        text = (f'Username = {name if name else 'Не зарегистрирован'}\nMethod = {method}\n'
                f'URL = {url}\nIp = {ip}\nRequest time = {start}\nResponse time = {end}\n\n')
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file = open(f"logs/{name if name else ip}.txt", "a")
        file.write(text)
        file.close()
        return response
