from pydantic import BaseModel

class EventSchema(BaseModel):
    description: str
    name: str
    max_participants: int
    status: str
    start_time: str
    type: str
    image_url: str

