from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .models import models, schemas
from .controllers import orders
from .controllers import sandwiches
from .controllers import resources
from .controllers import recipes
from .controllers import order_detail
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)

@app.post("/sandwiches/", response_model=schemas.Sandwich)
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)

@app.get("/sandwiches/", response_model=list[schemas.Sandwich])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    return sandwiches.update(db=db, sandwich_id=sandwich_id, sandwich=sandwich)

@app.delete("/sandwiches/{sandwich_id}")
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwiches.delete(db=db, sandwich_id=sandwich_id)
    return {"detail": "Sandwich deleted"}


# Create Resource
@app.post("/resources/", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(db=db, resource=resource)

# Read All Resources
@app.get("/resources/", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

# Read One Resource
@app.get("/resources/{resource_id}", response_model=schemas.Resource)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

# Update Resource
@app.put("/resources/{resource_id}", response_model=schemas.Resource)
def update_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    return resources.update(db=db, resource_id=resource_id, resource=resource)

# Delete Resource
@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resources.delete(db=db, resource_id=resource_id)
    return {"detail": "Resource deleted"}

# Create Recipe
@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipes.create(db=db, recipe=recipe)

# Read All Recipes
@app.get("/recipes/", response_model=list[schemas.Recipe])
def read_recipes(db: Session = Depends(get_db)):
    return recipes.read_all(db)

# Read One Recipe
@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipes.read_one(db, recipe_id=recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# Update Recipe
@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    return recipes.update(db=db, recipe_id=recipe_id, recipe=recipe)

# Delete Recipe
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipes.delete(db=db, recipe_id=recipe_id)
    return {"detail": "Recipe deleted"}


# Create OrderDetail
@app.post("/order_details/", response_model=schemas.OrderDetail)
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return order_detail.create(db=db, order_detail=order_detail)

# Read All OrderDetails
@app.get("/order_details/", response_model=list[schemas.OrderDetail])
def read_order_details(db: Session = Depends(get_db)):
    return order_detail.read_all(db)

# Read One OrderDetail
@app.get("/order_details/{order_detail_id}", response_model=schemas.OrderDetail)
def read_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_detail.read_one(db, order_detail_id=order_detail_id)
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    return order_detail

# Update OrderDetail
@app.put("/order_details/{order_detail_id}", response_model=schemas.OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    return order_detail.update(db=db, order_detail_id=order_detail_id, order_detail=order_detail)

# Delete OrderDetail
@app.delete("/order_details/{order_detail_id}")
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail.delete(db=db, order_detail_id=order_detail_id)
    return {"detail": "Order detail deleted"}


