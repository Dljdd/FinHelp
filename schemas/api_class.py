from pydantic import BaseModel
from typing import Optional, Dict, Union

class stock(BaseModel):
    symbol: str
    range: str
    interval: str

class article(BaseModel):
    symbol: str


class balancing(BaseModel):
    amount: int