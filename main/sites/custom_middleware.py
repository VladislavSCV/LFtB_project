from django.shortcuts import redirect


class ErrorHandlerMiddleware:
    """ Класс для обработки ошибки 500 """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            return redirect('http://127.0.0.1:8000/')
        return response