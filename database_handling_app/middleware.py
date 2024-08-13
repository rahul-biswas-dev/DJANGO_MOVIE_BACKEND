import logging
from django.http import JsonResponse
from django_ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, Ratelimited):
        request = context["request"]
        limited = getattr(request, "limited", None)
        logger.debug(f"Rate limit exceeded. Request limited: {limited}")
        logger.debug(f"Request META: {request.META}")

        if isinstance(limited, bool):
            logger.info("Generic rate limit exceeded")
            return JsonResponse(
                {"error": "API Rate limit exceeded. Please try again later."},
                status=429,
            )
        elif isinstance(limited, str):
            if "per_second" in limited:
                logger.info("Per-second rate limit exceeded")
                return JsonResponse(
                    {"error": "API Per-second rate limit exceeded. Please slow down."},
                    status=429,
                )
            elif "per_day" in limited:
                logger.info("Daily rate limit exceeded")
                return JsonResponse(
                    {
                        "error": "API Daily rate limit exceeded. Please try again tomorrow."
                    },
                    status=429,
                )

        logger.info("Unspecified rate limit exceeded")
        return JsonResponse(
            {"error": "API Rate limit exceeded. Please try again later."}, status=429
        )
    return exception_handler(exc, context)


class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("Request passing through RatelimitMiddleware")
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.debug(f"Exception caught in middleware: {type(exception)}")
        if isinstance(exception, Ratelimited):
            logger.info("API Rate limit exceeded in process_exception")
            return JsonResponse(
                {"error": "API Rate limit exceeded. Please try again later."},
                status=429,
            )
