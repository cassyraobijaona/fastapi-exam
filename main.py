from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml

app = FastAPI()

with open("main.yaml", "r") as f:
    main_yaml = yaml.safe_load(f)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = main_yaml
    return app.openapi_schema


app.openapi = custom_openapi


class Characteristics(Attribus):
    max_speed: float
    max_fuel_capacity: float

class Car(Attribus):
    id: str
    brand: str
    model: str
    characteristics: Characteristics

cars_db: Dict[str, Car] = {}

@app.get("/ping")
def ping():
    return "pong"

@app.post("/cars", status_code=201)
def create_car(car: Car):
    cars_db[car.id] = car
    return car

@app.get("/cars", response_model=List[Car])
def get_all_cars():
    return list(cars_db.values())

@app.get("/cars/{id}", response_model=Car)
def get_car_by_id(id: str):
    car = cars_db.get(id)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car with ID '{id}' not found.")
    return car

@app.put("/cars/{id}/characteristics", response_model=Car)
def update_characteristics(id: str, new_char: Characteristics):
    car = cars_db.get(id)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car with ID '{id}' not found.")
    car.characteristics = new_char
    cars_db[id] = car
    return car