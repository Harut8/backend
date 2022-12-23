from pydantic import BaseModel


class test(BaseModel):
    id: int | None = None
    name: str|None = None

