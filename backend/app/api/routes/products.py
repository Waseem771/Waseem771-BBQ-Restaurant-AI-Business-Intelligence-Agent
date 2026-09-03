# app/api/routes/products.py
"""Product CRUD API routes.

Provides endpoint to add a new product to the SQLite database and list all products.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ... import db

router = APIRouter(prefix="/api/v1/products", tags=["products"])

class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, description="Product name")
    category: str = Field(..., min_length=1, description="Product category")
    unit_price: float = Field(..., gt=0, description="Unit price in PKR")

@router.post("/", response_model=dict)
def add_product(product: ProductIn):
    """Insert a new product record.

    Returns the newly created product_id.
    """
    # Basic validation – ensure price is non‑negative (already enforced by Pydantic)
    sql = """
        INSERT INTO products (product_name, category, unit_price, unit_cost, popularity_weight)
        VALUES (?, ?, ?, 0, 0)
    """
    try:
        product_id = db.execute_write(sql, (product.name, product.category, product.unit_price))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to insert product: {exc}")

    return {"product_id": product_id, "success": True}

@router.get("/", response_model=list[dict])
def list_products():
    """Return all products.

    The frontend uses this for the detailed product breakdown.
    """
    sql = "SELECT product_name, category, unit_price, unit_cost, popularity_weight FROM products"
    try:
        rows = db.query_rows(sql)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {exc}")
    return rows

"""Product CRUD API routes.

Provides endpoint to add a new product to the SQLite database.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ... import db

router = APIRouter(prefix="/api/v1/products", tags=["products"])

class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, description="Product name")
    category: str = Field(..., min_length=1, description="Product category")
    unit_price: float = Field(..., gt=0, description="Unit price in PKR")

@router.post("/", response_model=dict)
def add_product(product: ProductIn):
    """Insert a new product record.

    Returns the newly created product_id.
    """
    # Basic validation – ensure price is non‑negative (already enforced by Pydantic)
    sql = """
        INSERT INTO products (product_name, category, unit_price, unit_cost, popularity_weight)
        VALUES (?, ?, ?, 0, 0)
    """
    try:
        product_id = db.execute_write(sql, (product.name, product.category, product.unit_price))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to insert product: {exc}")

    return {"product_id": product_id, "success": True}
