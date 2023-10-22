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
    
    def stores(self) -> list[Store]:
        result = self.session.get(self.url("/api/v2/stores"))
        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return [Store.from_data(self, item) for item in data["items"]]
    
    def set_store(self, store: Union[int, Store]):
        if type(store) == int:
            self.store = store
        else:
            self.store == int(store.id)
        
        self.session.cookies.set("wfmStoreId", str(self.store))

    def search_groceries(self, search: str) -> list[GroceryItem]:
        result = self.session.get(self.url("/api/v2/store_products"), params={
            "search_term": search
        })
        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return [GroceryItem.from_data(self, item) for item in data["items"]]
    
    def get_grocery_item(self, id: int):
        result = self.session.get(self.url(f"/api/v2/store_products/{id}"), params={"require_storeproduct": "true"})

        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return GroceryItemExpanded.from_data(self, data)