from django.http import JsonResponse
from django_ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, Ratelimited):
        request = context["request"]
        if hasattr(request, "limited"):
            if request.limited == "per_second":
                return JsonResponse(
                    {
                        "error": "You've exceeded the per-second rate limit. Please slow down your requests."
                    },
                    status=429,
                )
            elif request.limited == "per_day":
                return JsonResponse(
                    {
                        "error": "You've reached the daily request limit. Please try again tomorrow."
                    },
                    status=429,
                )
        return JsonResponse(
            {"error": "Rate limit exceeded. Please try again later."}, status=429
        )
    return exception_handler(exc, context)


class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Request passing through RatelimitMiddleware")
        return self.get_response(request)

    def process_exception(self, request, exception):
        print(f"Exception caught in middleware: {type(exception)}")
        if isinstance(exception, Ratelimited):
            print("Rate limit exceeded")
            return JsonResponse(
                {"error": "Rate limit exceeded. Please try again later."}, status=429
            )
