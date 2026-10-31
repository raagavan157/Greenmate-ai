from pydantic import BaseModel
from typing import Optional, List

class GuideResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    category: str
    read_time: str
    image_url: str
    summary: str
    content: str
