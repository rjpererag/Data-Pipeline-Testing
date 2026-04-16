from pydantic import BaseModel

class Price(BaseModel):
    symbol: str
    price: float
    currency: str | None = None
    time: str | None = None
    status: str | None = None