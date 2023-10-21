from dataclasses import dataclass
from typing import Optional

@dataclass
class GroceryCategory:
    id: int
    name: str

    @classmethod
    def from_data(cls, data: dict) -> "GroceryCategory":
        return GroceryCategory(id=int(data["id"]), name=data["name"])
    
    @classmethod
    def all_from_data(cls, data: list[dict]) -> list["GroceryCategory"]:
        return [GroceryCategory.from_data(c) for c in data]
    
@dataclass
class GroceryImageType:
    large: str
    medium: str
    small: str

    @classmethod
    def from_data(cls, data: dict) -> "GroceryImageType":
        return GroceryImageType(
            **data
        )
    
@dataclass
class GroceryRatings:
    average: float
    count: int

    @classmethod
    def from_data(cls, data: dict) -> "GroceryRatings":
        return GroceryRatings(average=data["average_rating"], count=data["user_count"])
    
@dataclass
class GroceryPrice:
    base: float
    unit_price: Optional[float]
    unit_measurement: Optional[str]

    @classmethod
    def from_data(cls, data: dict) -> "GroceryPrice":
        return GroceryPrice(
            base=data["base_price"],
            unit_price=data["uom_price"]["price"] if "uom_price" in data.keys() else None,
            unit_measurement=data["uom_price"]["uom"] if "uom_price" in data.keys() else None
        )

@dataclass
class GroceryItem:
    id: int
    name: str
    brand: str
    aisle: str
    categories: list[GroceryCategory]
    images: list[GroceryImageType]
    tags: list[str]
    size: Optional[str]
    price: GroceryPrice
    ratings: GroceryRatings

    @classmethod
    def from_data(cls, data: dict) -> "GroceryItem":
        return GroceryItem(
            id=int(data["id"]),
            name=data["name"].lower().strip(),
            brand=data["brand_name"].lower().strip(),
            aisle=data.get("aisle", "").lower().strip(),
            categories=GroceryCategory.all_from_data(data["categories"]),
            images=[GroceryImageType.from_data(i) for i in data.get("images", {}).values()],
            tags=data.get("tags", []),
            size=data.get("size_string", None),
            price=GroceryPrice.from_data(data),
            ratings=GroceryRatings.from_data(data["product_rating"])
        )
