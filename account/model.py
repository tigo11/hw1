from dataclasses import dataclass
from enum import Enum
import json


class AccountStatus(Enum):
    BLOCKED = 'blocked'
    PENDING = 'pending'
    PROCESSING = 'processing'


@dataclass
class Account:
    id: int
    phone_number: str
    password: str
    status: AccountStatus = AccountStatus.PENDING

    def as_dict(self):
        return {"id": self.id,
                "phone_number": self.phone_number,
                "password": self.password,
                "status": self.status.value}

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):

        if not isinstance(data["id"], int):
            raise ValueError("Invalid id, must be integer")
        if not isinstance(data["phone_number"], str):
            raise ValueError("Invalid id, must be integer")
        if not isinstance(data["password"], str):
            raise ValueError("Invalid password, must be string")
        try:
            status = AccountStatus(data["status"])
        except ValueError:
            raise ValueError("Invalid status, must be from AccountStatus")
        if len(data.keys()) != 4:
            raise ValueError("Invalid dictionary, it must contain only for keys")

        return cls(id=data["id"],
                   phone_number=data["phone_number"],
                   password=data["password"],
                   status=status)

    @classmethod
    def from_json(cls, data: json):
        return cls.from_dict(json.loads(data))
