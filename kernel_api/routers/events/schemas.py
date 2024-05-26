from pydantic import BaseModel

class EventSchema(BaseModel):
    description: str
    max_participants: int
    status: str
    start_time: str
    type: str
    image_url: str

