from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from orderlab.pricing import subtotal


class OrderIn(BaseModel):
    price: int = Field(ge=0)
    quantity: int = Field(gt=0)


def create_app() -> FastAPI:
    app = FastAPI(title="OrderLab")
    orders: dict[int, int] = {}

    @app.post("/orders", status_code=201)
    async def create_order(order: OrderIn):
        order_id = len(orders) + 1
        amount = subtotal(order.price, order.quantity)
        orders[order_id] = amount
        return {"id": order_id, "subtotal": amount}

    @app.get("/orders/{order_id}")
    async def get_order(order_id: int):
        if order_id not in orders:
            raise HTTPException(status_code=404, detail="Not found")
        return {"id": order_id, "subtotal": orders[order_id]}

    return app
