from pydantic import BaseModel


class Track(BaseModel):
    name: str
    artists: str
    link: str
