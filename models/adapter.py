from . import GroceryItem, GroceryItemExpanded, Store
from typing import Any

class GroceryAdapter:
    def __init__(self) -> None:
        pass

    def stores(self) -> list[Store]:
        raise NotImplementedError
    
    def set_store(self, store: Any):
        raise NotImplementedError
    
    def search_groceries(self, search: str) -> list[GroceryItem]:
        raise NotImplementedError
    
    def get_grocery_item(self, id: int) -> GroceryItemExpanded:
        raise NotImplementedError