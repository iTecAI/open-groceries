from typing import Union
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Ratings:
    average: int
    count: int

@dataclass
class GroceryItem:
    type: str
    id: Union[str, int]
    name: str
    location: Optional[str]
    images: list[str]
    tags: list[str]
    categories: list[str]
    price: float
    ratings: Ratings
    metadata: dict[str, Any]