import requests
from dataclasses import dataclass
from typing import Any, Union
from models import *
from exceptions import *
from adapters import *


if __name__ == "__main__":
    costco = Costco()
    print(costco.suggest("beans"))
