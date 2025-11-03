from .models import CarMake, CarModel

def initiate():
    makes = [
        {"name": "NISSAN",  "description": "Great cars. Japanese technology"},
        {"name": "Mercedes","description": "Great cars. German technology"},
        {"name": "Audi",    "description": "Great cars. German technology"},
        {"name": "Kia",     "description": "Great cars. Korean technology"},
        {"name": "Toyota",  "description": "Great cars. Japanese technology"},
    ]
    m = [CarMake.objects.create(**x) for x in makes]

    models = [
        {"name":"Pathfinder","type":"SUV","year":2023,"car_make":m[0]},
        {"name":"Qashqai","type":"SUV","year":2023,"car_make":m[0]},
        {"name":"XTRAIL","type":"SUV","year":2023,"car_make":m[0]},
        {"name":"A-Class","type":"SUV","year":2023,"car_make":m[1]},
        {"name":"C-Class","type":"SUV","year":2023,"car_make":m[1]},
        {"name":"E-Class","type":"SUV","year":2023,"car_make":m[1]},
        {"name":"A4","type":"SUV","year":2023,"car_make":m[2]},
        {"name":"A5","type":"SUV","year":2023,"car_make":m[2]},
        {"name":"A6","type":"SUV","year":2023,"car_make":m[2]},
        {"name":"Sorrento","type":"SUV","year":2023,"car_make":m[3]},
        {"name":"Carnival","type":"SUV","year":2023,"car_make":m[3]},
        {"name":"Cerato","type":"Sedan","year":2023,"car_make":m[3]},
        {"name":"Corolla","type":"Sedan","year":2023,"car_make":m[4]},
        {"name":"Camry","type":"Sedan","year":2023,"car_make":m[4]},
        {"name":"Kluger","type":"SUV","year":2023,"car_make":m[4]},
    ]
    for x in models:
        CarModel.objects.create(dealer_id=0, **x)   # dealer_id dummy