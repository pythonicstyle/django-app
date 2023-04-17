from time import time

from django.http import HttpRequest, HttpResponse


def setup_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META.get("no user agent")
        response = get_response(request)
        return response

    return middleware


class CountRequestsMiddleware:
    LIMIT_TIME = 0.5

    def __init__(self, get_response: callable):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.last_request_data = {}

    def __call__(self, request: HttpRequest):
        user_ip = request.META.get("REMOTE_ADDR")
        if user_ip in self.last_request_data:
            if 0.2 < time() - self.last_request_data[user_ip] < self.LIMIT_TIME:
                return HttpResponse("Request limit exceeded")
        self.last_request_data[user_ip] = time()

        print(self.last_request_data)
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(f"got {self.exceptions_count} exceptions so far")
