import requests
from dataclasses import dataclass
from typing import Any, Union
from models import *
from exceptions import *
from adapters import *


if __name__ == "__main__":
    weg = Wegmans()
    print([i.name for i in weg.search_groceries("meatballs")])
