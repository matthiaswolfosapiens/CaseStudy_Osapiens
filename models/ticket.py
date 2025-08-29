from datetime import datetime
from typing import Optional, Union
from pydantic import Field
from beanie import Document

class Ticket(Document):
    # Field aliases are used to keep the desired JSON key names ("Create Date")
    create_date: Union[datetime, int] = Field(..., alias="Create Date")
    status: str = Field(..., alias="Status")
    resolved_date: Optional[Union[datetime, int]] = Field(None, alias="Resolved Date")
    agent: str = Field(..., alias="Agent")
    csat: Optional[str] = Field(None, alias="CSAT")
    description: str = Field(..., alias="Description")
    subject: str = Field(..., alias="Subject")
    customer_email: str = Field(..., alias="Customer Email")

    endpoint_version: str = Field(..., index=True)

    class Settings:
        name = "tickets"
        use_state_management = True
        state_management_save_previous = False
        validate_on_save = True
        bson_encoders = {
            datetime: lambda dt: dt,
        }