# server/djangoproj/diagnostic_middleware.py
import traceback
from django.http import JsonResponse

class JsonErrorMiddleware:
    """
    Middleware temporal de diagnóstico: captura cualquier excepción
    y devuelve JSON con el traceback (en lugar de la página HTML 500).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            return JsonResponse(
                {"error": str(e), "trace": traceback.format_exc()},
                status=500
            )
