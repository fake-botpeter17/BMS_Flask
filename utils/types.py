from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    """
    Stores the current user's info
    """

    name: str
    designation: str
    uid: str


class Item(BaseModel):
    id: int
    name: str
    cp: Union[int, float]
    sp: Union[int, float]
    qnty: int
