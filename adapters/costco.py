from models import GroceryAdapter, GroceryItem, Ratings
import requests
from bs4 import BeautifulSoup
import esprima


class Costco(GroceryAdapter):
    def __init__(
        self,
        user_agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    ) -> None:
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": user_agent,
            "Host": "www.costco.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5"
        }
        self.base_url = "https://www.costco.com/"

    def search_groceries(self, search: str) -> list[GroceryItem]:
        req = self.session.get(
            self.base_url + "CatalogSearch", params={"dept": "All", "keyword": search}
        )
        soup = BeautifulSoup(req.text, features="html.parser")
        results = []
        for product in soup.select(".product"):
            data_script = product.select("script")[1]
            sc_tokens = esprima.tokenize(data_script.contents[0])
            data_mapping = {}
            for token in range(len(sc_tokens)):
                try:
                    if sc_tokens[token].type == "Identifier" and sc_tokens[token + 1].type == "Punctuator" and sc_tokens[token + 2].type in ["String", "Numeric"]:
                        data_mapping[sc_tokens[token].value] = sc_tokens[token + 2].value
                except:
                    pass

            metas = {i.attrs["itemprop"]:i.attrs["content"] for i in product.select("meta")}
            results.append(GroceryItem(
                type="costco",
                id=int(data_mapping["SKU"].strip("'")),
                name=data_mapping["name"].strip("'").replace("\\", ""),
                location=None,
                images=[data_mapping["productImageUrl"].strip("'").replace("\\", "")],
                tags=[i.contents[0].replace("\\", "") for i in product.select(".product-features li") if i.contents and len(i.contents) > 0],
                price=float(data_mapping["priceTotal"]),
                ratings=Ratings(average=float(metas.get("ratingValue", "0")), count=int(metas.get("reviewCount", "0"))),
                metadata={}
            ))
        
        return results
