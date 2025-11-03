from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review  # <─ usamos tu cliente REST
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
    return render(request, "login.html")


# ---------- proyecto 4: endpoint get_cars ----------
def get_cars(request):
    """Devuelve CarModel + CarMake; si no hay datos ejecuta populate()."""
    if CarMake.objects.count() == 0 or CarModel.objects.count() == 0:
        initiate()

    cars = CarModel.objects.select_related("car_make").all()
    data = [
        {
            "CarMake": c.car_make.name,
            "CarModel": c.name,
            "Type": c.type,
            "Year": c.year,
        }
        for c in cars
    ]
    return JsonResponse({"CarModels": data})


# ---------- Páginas dinámicas para el despliegue ----------
def dealer_details_page(request, dealer_id: int):
    """Detalle del dealer + reviews (Render HTML)."""
    dealer = get_request(f"/fetchDealer/{dealer_id}") or {}
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}") or []
    return render(
        request,
        "dealer_details.html",
        {"dealer": dealer, "reviews": reviews, "dealer_id": dealer_id},
    )


def add_review_form(request, dealer_id: int):
    """Muestra el formulario para enviar la review."""
    dealer = get_request(f"/fetchDealer/{dealer_id}") or {}
    return render(
        request,
        "add_review.html",
        {"dealer": dealer, "dealer_id": dealer_id},
    )


def post_review_view(request, dealer_id: int):
    """Recibe el form, envía al backend Node y redirige al detalle."""
    if request.method != "POST":
        return redirect(f"/dealer/{dealer_id}")

    payload = {
        "name": request.user.username if request.user.is_authenticated else "guest",
        "dealership": dealer_id,
        "review": request.POST.get("review", ""),
        "purchase": request.POST.get("purchase") == "on",
        "purchase_date": request.POST.get("purchase_date", ""),
        "car_make": request.POST.get("car_make", ""),
        "car_model": request.POST.get("car_model", ""),
        "car_year": int(request.POST.get("car_year") or 0),
    }
    try:
        post_review(payload)
    except Exception:
        pass  # si falla, igual redirigimos al detalle

    return redirect(f"/dealer/{dealer_id}")
