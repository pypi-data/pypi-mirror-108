from .qradarmodel import QRadarModel
import json


class NetworkHierarchy(QRadarModel):
    def __init__(self, *, id: int = None, network_id: int = None, group: str = None, name: str = None, cidr: str = None, description: str = None, domain_id: int = None, location: str = None, country_code: str = None) -> None:
        self.id = id
        self.network_id = network_id
        self.group = group
        self.name = name
        self.cidr = cidr
        self.description = description
        self.domain_id = domain_id
        self.location = location
        self.country_code = country_code

    def to_json(self):
        message = {k: v for k, v in self.__dict__.items() if v is not None}
        return json.dumps(message)
