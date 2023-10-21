from dataclasses import dataclass
from typing import Any, Optional, Union

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
    instance: Any
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
    def from_data(cls, instance: Any, data: dict) -> "GroceryItem":
        return GroceryItem(
            instance=instance,
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
    
    @property
    def expanded(self) -> "GroceryItemExpanded":
        return self.instance.get_grocery_item(self.id)
    
@dataclass
class NutritionField:
    name: str
    amount: float
    daily_amount: float
    units: Optional[str]
    children: list["NutritionField"]

    @classmethod
    def from_field(cls, field: dict) -> "NutritionField":
        amt, amt_unit = field["amount"].split(" ")
        daily = float(field["daily_value"].strip())
        return NutritionField(
            name=field["name"].strip(),
            amount=float(amt),
            daily_amount=daily,
            units=amt_unit if len(amt_unit) > 0 else None,
            children=[NutritionField.from_field(c) for c in field.get("children", [])]
        )
    
@dataclass
class GroceryItemNutrition:
    serving_size: str
    servings_per_container: str
    fields: list[NutritionField]
    secondary_fields: list[NutritionField]

    @classmethod
    def from_data(cls, data: dict) -> "GroceryItemNutrition":
        return GroceryItemNutrition(
            serving_size=data["data"]["amount"].strip(),
            servings_per_container=data["data"]["per_container"].strip(),
            fields=[NutritionField.from_field(f) for f in data["data"]["fields"]],
            secondary_fields=[NutritionField.from_field(f) for f in data["data"]["secondary_fields"]]
        )

    
@dataclass
class GroceryItemExpanded:
    instance: Any
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
    description: Optional[str]
    ingredients: Optional[str]
    instructions: Optional[str]
    nutrition_facts: Optional[GroceryItemNutrition]

    @classmethod
    def from_data(cls, instance: Any, data: dict) -> "GroceryItemExpanded":
        return GroceryItemExpanded(
            instance=instance,
            id=int(data["id"]),
            name=data["name"].lower().strip(),
            brand=data["brand_name"].lower().strip(),
            aisle=data.get("aisle", "").lower().strip(),
            categories=GroceryCategory.all_from_data(data["categories"]),
            images=[GroceryImageType.from_data(i) for i in data.get("images", {}).values()],
            tags=data.get("tags", []),
            size=data.get("size_string", None),
            price=GroceryPrice.from_data(data),
            ratings=GroceryRatings.from_data(data["product_rating"]),
            description=data.get("description"),
            ingredients=data.get("ingredients"),
            instructions=data.get("instructions"),
            nutrition_facts=GroceryItemNutrition.from_data(data["nutrition"]) if "nutrition" in data.keys() and data["nutrition"] and "data" in data["nutrition"].keys() else None
        )
    

