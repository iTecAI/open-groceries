import requests
from dataclasses import dataclass
from typing import Any, Union
from models import *
from exceptions import *
from adapters import *


if __name__ == "__main__":
    """weg = Wegmans()
    print(weg.search_groceries("meatballs"))"""

    costco = Costco()
    print(costco.search_groceries("meatballs"))
