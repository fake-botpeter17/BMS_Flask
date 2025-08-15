from .connection import getDB
from pickle import load
from bcrypt import hashpw

users = getDB()["users"]


def getUser(usr):
    user = users.find_one({"uid": usr}, {"_id": False})
    return user


def getUserSalt(salt_id):
    with open("db/BillingInfo.dat", "rb+") as f:
        data: dict[str, bytes] = load(f)
    salt = data.get(salt_id)
    print(f"{salt = }")
    return salt


def authenticated(user, password):
    salt = getUserSalt(user.get("salt"))
    pwd: bytes = hashpw(password.encode(), salt)
    if str(pwd) == user.get("hashed_pwd"):
        return True
    return False
