from datetime import datetime
from typing import List, Literal, Union

from pydantic import BaseModel

NOT_SUPPORTED = Literal["not_supported"]
NO_INFORMTION = Literal["no_information"]
NOT_APPLICABLE = Literal["N/A"]


class User(BaseModel):
    username: str
    arn: str
    user_creation_time: datetime
    password_enabled: Union[bool, NOT_SUPPORTED]
    password_last_used: Union[datetime, NOT_SUPPORTED, NO_INFORMTION, NOT_APPLICABLE]
    password_last_changed: Union[datetime, NOT_SUPPORTED, NOT_APPLICABLE]
    password_next_rotation: Union[datetime, NOT_SUPPORTED, NOT_APPLICABLE]
    mfa_active: bool
    access_key_1_active: bool
    access_key_1_last_rotated: Union[datetime, NOT_APPLICABLE]
    access_key_1_last_used_date: Union[datetime, NOT_APPLICABLE]
    access_key_1_last_used_region: str
    access_key_1_last_used_service: str
    access_key_2_active: bool
    access_key_2_last_rotated: Union[datetime, NOT_APPLICABLE]
    access_key_2_last_used_date: Union[datetime, NOT_APPLICABLE]
    access_key_2_last_used_region: str
    access_key_2_last_used_service: str
    cert_1_active: bool
    cert_1_last_rotated: Union[datetime, NOT_APPLICABLE]
    cert_2_active: bool
    cert_2_last_rotated: Union[datetime, NOT_APPLICABLE]


class CredentialReport(BaseModel):
    users: List[User]
