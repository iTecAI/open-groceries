from . import GroceryItem, Store
from typing import Any

class GroceryAdapter:
    def __init__(self) -> None:
        pass
    
    def search_groceries(self, search: str) -> list[GroceryItem]:
        raise NotImplementedError
    
    def get_grocery_item(self, id: int) -> GroceryItem:
        raise NotImplementedError