from time import time

from django.http import HttpRequest, HttpResponse


def setup_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        return response

    return middleware


class CountRequestsMiddleware:
    LIMIT_TIME = 3

    def __init__(self, get_response: callable):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.last_request_data = {}

    # def __call__(self, request: HttpRequest):
    #     if self.last_request_data:
    #         if request.META.get("REMOTE_ADDR") == self.last_request_data["user_ip"]:
    #             if time() - self.last_request_data["last_request_time"] < self.LIMIT_TIME:
    #                 return HttpResponse("Request limit exceeded")
    #     self.last_request_data["user_ip"] = request.META.get("REMOTE_ADDR")
    #     self.last_request_data["last_request_time"] = time()
    #     self.requests_count += 1
    #     print("requests count", self.requests_count)
    #     response = self.get_response(request)
    #     self.responses_count += 1
    #     print("responses count", self.responses_count)
    #     return response

    # TODO Если два пользователя (или больше) будет поочереди заходить на страницу, то ограничения не будет работать
    #  совсем.
    #  Попробуйте сделать так:
    #  - храним данные по посещениях в словаре вида: {ip: visit_time}, где ip это реальный адрес пользователя.
    #  То есть в словаре будут все посетители сайта и время когда они посещали сайт вне ограничений.
    #  - при запросе смотрим в словарь по ключу с ip, если его нет, создаём запись вида "ip: время доступа", и всё, а если
    #  ключ есть, то получаем время прошлого доступа
    #  - сравниваем текущее время и время последнего запроса, если разница меньше допустимого - возвращаем страницу
    #  с ошибкой. Если разница допустима - обновляем время доступа для этого ip.

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(f"got {self.exceptions_count} exceptions so far")
