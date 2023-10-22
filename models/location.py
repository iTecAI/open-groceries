from dataclasses import dataclass

@dataclass
class LatLong:
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: dict) -> "LatLong":
        return LatLong(latitude=float(data["latitude"]), longitude=float(data["longitude"]))
    
    @classmethod
    def from_list(cls, data: list, longitude_first: bool = False) -> "LatLong":
        if longitude_first:
            return LatLong(latitude=float(data[1]), longitude=float(data[0]))
        else:
            return LatLong(latitude=float(data[0]), longitude=float(data[1]))
        
@dataclass
class Address:
    lines: list[str]
    city: str
    country: str
    zip_code: str
    province: str

@dataclass
class Location:
    type: str
    id: str
    name: str
    location: LatLong
    address: Address
    phone: str
    features: list[str]

