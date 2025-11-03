from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def _json_or_400(request):
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    data = _json_or_400(request)
    if data is None:
        return JsonResponse({"error": "Bad JSON"}, status=400)
    username = data.get("userName")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Failed"})

def logout_user(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    data = _json_or_400(request)
    if data is None:
        return JsonResponse({"error": "Bad JSON"}, status=400)

    username = data.get("userName")
    if not username:
        return JsonResponse({"error": "Missing username"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        password=data.get("password") or "",
        email=data.get("email") or "",
        first_name=data.get("firstName") or "",
        last_name=data.get("lastName") or "",
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": True})