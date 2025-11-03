from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import CarMake, CarModel
from .populate import initiate
import json


# ---------- utilidades ----------
def _json_or_400(request):
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None


# ---------- autenticación (API JSON) ----------
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


# ---------- página de login (HTML) ----------
def login_page(request):
    """
    Renderiza una página simple de login para el despliegue.
    El formulario llama al endpoint /djangoapp/login.
    """
    return render(request, "login.html")


# ---------- proyecto 4: endpoint get_cars ----------
def get_cars(request):
    """
    Devuelve todos los CarModel junto con su CarMake.
    Si la tabla está vacía, se ejecuta populate.initiate() automáticamente.
    """
    if CarMake.objects.count() == 0 or CarModel.objects.count() == 0:
        initiate()

    cars = CarModel.objects.select_related("car_make").all()
    data = [
        {
            "CarMake": car.car_make.name,
            "CarModel": car.name,
            "Type": car.type,
            "Year": car.year,
        }
        for car in cars
    ]
    return JsonResponse({"CarModels": data})
