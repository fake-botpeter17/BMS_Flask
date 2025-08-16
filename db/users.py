from .connection import getDB
from pickle import load
from bcrypt import hashpw
from utils.types import User

users = getDB()["users"]


def getUser(usr, obj = False):
    user = users.find_one({"uid": usr}, {"_id": False})
    if obj:
        return User(**user) if user else None
    return user 


def getUserSalt(salt_id):
    with open("db/BillingInfo.dat", "rb+") as f:
        data: dict[str, bytes] = load(f)
    salt = data.get(salt_id)
    return salt

def userIsAdmin(uid: str) -> bool:
    user = getUser(uid)
    role = user.get('designation')
    if not user: 
        return False
    return role.casefold() == "Admin".casefold()

def authenticated(user, password):
    salt = getUserSalt(user.get("salt"))
    pwd: bytes = hashpw(password.encode(), salt)
    if str(pwd) == user.get("hashed_pwd"):
        return True
    return False
