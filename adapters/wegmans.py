from dataclasses import dataclass
from typing import Any, Union
import requests
from models import *
from exceptions import *


@dataclass
class SessionContext:
    cookies: dict[str, str]
    user_agent: str


class Wegmans(GroceryAdapter):
    def __init__(
        self,
        base_url: str = "https://shop.wegmans.com",
        user_agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
        environment: dict[str, Any] = {
            "binary": "web-ecom",
            "binary_version": "4.33.26",
            "is_retina": False,
            "os_version": "Linux x86_64",
            "pixel_density": "1.0",
            "push_token": "",
            "screen_height": 1080,
            "screen_width": 1920,
        },
        store_id: int = 1
    ) -> None:
        self.base = base_url
        self.context = self._get_session_context(user_agent, environment)
        self.session = requests.Session()
        self.session.headers = {"User-Agent": self.context.user_agent}
        self.session.cookies.update(self.context.cookies)
        self.session.cookies.set("wfmStoreId", str(store_id))
        self.store = store_id

    def _get_session_context(
        self, user_agent: str, environment: dict[str, Any]
    ) -> SessionContext:
        first_pass = requests.get(self.base)
        cookies = dict(first_pass.cookies)
        second_pass = requests.post(
            self.base + "/api/v3/user_init",
            json=environment,
            headers={"User-Agent": user_agent},
            cookies=cookies,
        )
        cookies = dict(second_pass.cookies)
        return SessionContext(cookies=cookies, user_agent=user_agent)

    def url(self, path: str):
        return self.base.rstrip("/") + "/" + path.lstrip("/")

    def search_groceries(self, search: str) -> list[GroceryItem]:
        result = self.session.get(self.url("/api/v2/store_products"), params={
            "search_term": search
        })
        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return [self.build_wegmans_grocery_item(item) for item in data["items"]]
    
    def build_wegmans_grocery_item(self, data: dict) -> GroceryItem:

        return GroceryItem(
            type="wegmans",
            id=int(data["id"]),
            name=data["name"].lower().strip(),
            location=data.get("aisle").lower().strip() if data.get("aisle") else None,
            images=list(data.get("images", {"tile": {}})["tile"].values()),
            tags=data.get("tags", []),
            price=data.get("base_price", 0),
            ratings=Ratings(average=data["product_rating"]["average_rating"], count=data["product_rating"]["user_count"]),
            metadata={
                "brand": data.get("brand_name").lower().strip() if "brand_name" in data.keys() else None,
                "categories": [c["name"] for c in data["categories"]],
                "size": data.get("size_string", None)
            }
        )
    
    def get_grocery_item(self, id: str):
        result = self.session.get(self.url(f"/api/v2/store_products/{id}"), params={"require_storeproduct": "true"})

        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return self.build_wegmans_grocery_item(data)