"""Product management routes for authorised administrators."""
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from ... import db

router = APIRouter(prefix="/api/v1/products", tags=["products"])


class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    category: str = Field(..., min_length=1, max_length=80)
    unit_price: float = Field(..., gt=0, le=1_000_000)


def _require_admin(request: Request) -> None:
    if request.state.user.get("role") != "Administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductIn, request: Request):
    """Create a product. This endpoint is restricted to administrators."""
    _require_admin(request)
    try:
        product_id = db.execute_write(
            """INSERT INTO products (product_name, category, unit_price, unit_cost, popularity_weight)
               VALUES (?, ?, ?, 0, 0)""",
            (product.name.strip(), product.category.strip(), product.unit_price),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to save product") from exc
    return {"product_id": product_id, "success": True}


@router.get("/", response_model=list[dict])
def list_products():
    """Return product records for the authenticated dashboard."""
    try:
        return db.query_rows("SELECT product_name, category, unit_price, unit_cost, popularity_weight FROM products")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to load products") from exc
