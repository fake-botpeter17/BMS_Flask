from collections.abc import Generator
from typing import Any, Union
from requests import Response, Timeout, get
from datetime import datetime, date
from threading import Thread
from pydantic import BaseModel, PrivateAttr


class User(BaseModel):
    """
    Stores the current user's info
    """

    name: str = str()
    designation: str = str()
    uid: str = str()
    __Logging_Out: bool = PrivateAttr(False)

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

    def isAdmin(self) -> bool:
        """Checks if the current user is an Admin"""
        return self.designation.casefold() == "Admin".casefold()

    def isLoggingOut(self) -> bool:
        """Checks if the current user is logging out"""
        return self.__Logging_Out

    def toggleLoggingOut(self) -> None:
        """Toggles the logging out status of the current user"""
        self.__Logging_Out = True
        self.resetUser()

    def resetUser(self) -> None:
        """Resets the current user's info"""
        self.name: str = str()
        self.designation: str = str()
        self.uid: str = str()
        self.__Logging_Out: bool = False


class Bill_:
    __Bill_No_Gen: Generator
    __Bill_No: int = int()
    __Items: dict = dict()
    __Cart: dict = dict()  # {id:row}
    __Row_Lookup: dict = dict()  # {row:id}

    @staticmethod
    def getItems():
        try:
            req: Response = get(get_Api(testing=False) + "//get_stock", timeout=15)
            items_cache = req.json()
        except Timeout:
            return
        if not items_cache:
            return {}
        tmp = dict()
        for item in items_cache:
            tmp[item["id"]] = item
        return tmp

    @classmethod
    def contains(cls, item_id: int) -> bool:
        """Checks if the given item ID is in the cart"""
        return item_id in cls.__Cart

    @staticmethod
    def __Bill_Number(testing: bool = False) -> Generator:
        """Retreives the latest Bill Number"""
        Latest_Bill: int | None = get(f"{get_Api(testing)}/getLastBillNo").json()
        if not Latest_Bill:
            Latest_Bill = 10001
        for Bill_Number in range(Latest_Bill + 1, 100000):
            yield Bill_Number

    @staticmethod
    def Get_Date() -> str:
        """Returns the current date."""
        return date.today().strftime("%B %d, %Y")

    @staticmethod
    def Get_Time() -> str:
        """Returns the current time."""
        return datetime.now().time().strftime("%H:%M:%S")

    @classmethod
    def Init(cls: "Bill_") -> None:
        """Initializes the bill"""
        cls.__Bill_No_Gen = cls.__Bill_Number()
        cls.__Bill_No = next(cls.__Bill_No_Gen)
        Thread(target=cls.Items_Cacher).start()

    @classmethod
    def Get_Bill_No(cls: "Bill_") -> int:
        """Returns the current bill number"""
        return cls.__Bill_No

    @classmethod
    def Get_Item(cls: "Bill_", Item_ID: int) -> dict[int | str : int | str]:
        return cls.__Items.get(Item_ID)

    @classmethod
    def Increment_Bill_No(cls: "Bill_") -> None:
        """Increments the bill number"""
        cls.__Bill_No = next(cls.__Bill_No_Gen)

    @classmethod
    def getCartItems(cls: "Bill_"):
        return cls.__Cart.keys()

    @classmethod
    def getRowNumber(cls: "Bill_", Item_ID: int):
        return cls.__Cart.get(Item_ID)

    @classmethod
    def isEmpty(cls: "Bill_") -> bool:
        return len(cls.__Cart) == 0

    @classmethod
    def remove_row_item(cls: "Bill_", row_number: int) -> None:
        item = cls.__Row_Lookup.get(row_number)
        if item in cls.__Cart:
            del cls.__Cart[item]
        cls.__Row_Lookup.pop(row_number)

    @classmethod
    def isDuplicateRow(cls: "Bill_", row_number: int) -> bool:
        return row_number in cls.__Row_Lookup

    @classmethod
    def addItem(cls: "Bill_", item_id: int, row: int) -> None:
        cls.__Cart[item_id] = row
        cls.__Row_Lookup[row] = item_id

    @classmethod
    def getCart(cls: "Bill_") -> dict[int, int | str]:
        return cls.__Cart

    @classmethod
    def nextBillPrep(cls: "Bill_"):
        cls.__Cart.clear()
        cls.__Row_Lookup.clear()
        cls.Increment_Bill_No()

    # @classmethod
    # def remove_row_item(cls : "Bill_", row_number : int) -> None:
    #     if cls.__Row_Lookup(row_number) in cls.__Cart:
    #         del cls.__Cart[cls.get_row_item(row_number)]
    #     ...

    # @classmethod
    # def get_row_item(cls: "Bill_", row_number: int) -> int:
    #     return cls.__Row_Lookup.get(row_number)

    @classmethod
    def Items_Cacher(cls: "Bill_") -> None:
        """Caches the items"""
        try:
            req: Response = get(get_Api(testing=False) + "//get_items", timeout=15)
            items_cache = req.json()
        except Timeout:
            return
        if not items_cache:
            return
        for item in items_cache:
            cls.__Items[item["id"]] = item


class Item(BaseModel):
    id: int
    name: str
    cost_price: Union[int, float]
    selling_price: Union[int, float]
    qnty: int   


    def getObj(self):
        obj = {
            "id": self.id,
            "name": f"{self.name}",
            "cp": self.cost_price,
            "qnty": self.qnty,
            "added": round(self.cost_price * 1.08, 2),
            "sp": self.selling_price,
        }
        return obj

    def isValid(self) -> bool:
        if (
            self.id is None
            or not self.name
            or self.cost_price is None
            or self.selling_price is None
            or self.qnty is None
        ):
            logger.warning(f"Invalid item data for ID {self.id}")
            return False
        return True
