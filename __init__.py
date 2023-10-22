import requests
from dataclasses import dataclass
from typing import Any, Union
from models import *
from exceptions import *
from adapters import *


if __name__ == "__main__":
    weg = Wegmans()
    print(weg.get_locations("Rochester Institute Of Technology"))
