
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///products.db"
engine = create_engine(DATABASE_URL, echo=True)

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    price: float
    category: str
    image: str

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "MiniShop backend with SQLite is running 🚀"}

@app.get("/products")
def get_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

@app.post("/products")
def add_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return {"message": "Product added", "product": product}

@app.put("/products/{product_id}")
def update_product(product_id: int, new_data: Product):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.title = new_data.title
        product.price = new_data.price
        product.category = new_data.category
        product.image = new_data.image
        session.add(product)
        session.commit()
        session.refresh(product)
        return {"message": "Product updated", "product": product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return {"message": "Product deleted"}
