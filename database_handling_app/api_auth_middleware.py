from functools import wraps
from django.http import JsonResponse
from django.conf import settings


def api_key_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get("X-API-Key") or request.GET.get("key")
        if api_key is None:
            return JsonResponse({"error": "No API key provided"}, status=403)
        if api_key != settings.API_KEY:
            return JsonResponse({"error": "Invalid API key"}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapped_view
