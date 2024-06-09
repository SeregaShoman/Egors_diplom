from pydantic import BaseModel
from datetime import datetime

class EventSchema(BaseModel):
    description: str
    name: str
    max_participants: int
    status: str
    start_time: datetime
    type: str
    image_url: str

