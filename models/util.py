from dataclasses import dataclass


@dataclass
class Address:
    lines: list[str]
    city: str
    country: str
    zip_code: str
    province: str

    @classmethod
    def from_data(cls, data: dict) -> "Address":
        return Address(
            lines=[
                data[f"address{i}"]
                for i in range(1, 3)
                if f"address{i}" in data.keys() and data[f"address{i}"]
            ],
            city=data.get("city", "").lower(),
            country=data.get("country", "").lower(),
            zip_code=data.get("postal_code", ""),
            province=data.get("province", "").lower()
        )
    
@dataclass
class Location:
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: dict) -> "Location":
        return Location(latitude=float(data["latitude"]), longitude=float(data["longitude"]))
    
    @classmethod
    def from_list(cls, data: list, longitude_first: bool = False) -> "Location":
        if longitude_first:
            return Location(latitude=float(data[1]), longitude=float(data[0]))
        else:
            return Location(latitude=float(data[0]), longitude=float(data[1]))