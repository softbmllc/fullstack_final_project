from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import CarMake, CarModel
from .populate import initiate
import json, os, requests, traceback

# =======================
#  Utilidades internas
# =======================

def _json_or_400(request):
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None

# --- Cliente simple para el microservicio Node (opcional) ---
DEALER_API = os.environ.get("DEALER_API", "").rstrip("/")

def _api_url(path: str) -> str | None:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if DEALER_API:
        if not path.startswith("/"):
            path = "/" + path
        return DEALER_API + path
    return None

def api_get(path: str) -> dict | list:
    url = _api_url(path)
    if not url:
        return {}
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}

def api_post(path: str, payload: dict) -> dict:
    url = _api_url(path)
    if not url:
        return {"status": "stub", "detail": "No DEALER_API defined"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# =======================
#  Health / diagnóstico
# =======================

def health(request):
    try:
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)

# =======================
#  Autenticación API JSON
# =======================

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

# =======================
#  Páginas HTML
# =======================

def login_page(request):
    return render(request, "login.html")

def get_cars(request):
    """
    Devuelve CarModel + CarMake; si no hay datos ejecuta populate().
    Si algo falla, devolvemos el traceback como JSON (diagnóstico).
    """
    try:
        if CarMake.objects.count() == 0 or CarModel.objects.count() == 0:
            initiate()      # poblar si está vacío
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
    except Exception as e:
        return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)

def dealer_details_page(request, dealer_id: int):
    """Detalle del dealer + reviews (Render HTML)."""
    dealer = api_get(f"/fetchDealer/{dealer_id}") or {}
    reviews = api_get(f"/fetchReviews/dealer/{dealer_id}") or []
    return render(
        request,
        "dealer_details.html",
        {"dealer": dealer, "reviews": reviews, "dealer_id": dealer_id},
    )

def add_review_form(request, dealer_id: int):
    """Muestra el formulario para enviar la review."""
    dealer = api_get(f"/fetchDealer/{dealer_id}") or {}
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
    api_post("/insert_review", payload)   # si falla, igual redirigimos
    return redirect(f"/dealer/{dealer_id}")
