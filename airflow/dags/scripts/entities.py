# Third-party imports
from pydantic import BaseModel
from typing import Optional

# define the RequestStreamModel class
class RequestStreamModel(BaseModel):
    request_id: str
    requested_datetime: str
    updated_datetime: str
    status_description: Optional[str] = None
    agency_responsible: Optional[str] = None
    service_type: Optional[str] = None
    service_subtype: Optional[str] = None
    address: Optional[str] = None
    street: Optional[str] = None
    supervisor_district: Optional[str] = None
    neighborhood: Optional[str] = None
    police_district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: Optional[str] = None