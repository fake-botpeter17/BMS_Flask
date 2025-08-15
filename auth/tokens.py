from utils.types import User
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from uuid import uuid4
from typing import Optional
from datetime import datetime, timezone, timedelta
import base64


generated_keys = {}


def generate_rsa_keys() -> tuple[bytes, bytes]:
    """
    Generates an RSA key pair.

    Returns:
        A tuple containing the private key (bytes) and the public key (bytes).
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def decrypt_with_private_key(private_key_pem: bytes, encrypted_data_b64: str) -> str:
    """
    Decrypts data using a private key.

    Args:
        private_key_pem (bytes): The private key in PEM format.
        encrypted_data_b64 (str): The base64-encoded encrypted data.

    Returns:
        str: The decrypted data as a string.
    """
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    return cipher.decrypt(encrypted_data).decode()


def getKey(expiry_minutes=5):
    """
    Generates a new RSA key pair and stores it in the generated_keys dictionary.

    Args:
        expiry_minutes (int, optional): The expiry time of the key in minutes. Defaults to 5.

    Returns:
        tuple: A tuple containing the kid (str) and public key (bytes).
    """
    global generated_keys
    kid = str(uuid4())
    private_key, public_key = generate_rsa_keys()
    generated_keys[kid] = {
        "private_key": private_key,
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes),
    }
    return kid, public_key


def getPrivateKey(kid: str) -> Optional[bytes]:
    """
    Retrieves the private key associated with a given kid (key ID).

    Args:
        kid (str): The key ID.

    Returns:
        Optional[bytes]: The private key if it exists and has not expired, None otherwise.
    """
    key_data = generated_keys.get(kid)
    if not key_data:
        return None
    if datetime.now(timezone.utc) > key_data["expires_at"]:
        del generated_keys[kid]
        return None
    return key_data["private_key"]


def revokeKey(kid: str) -> bool:
    if generated_keys.pop(kid, None):
        return True
    return False


def generate_refresh_access_tokens(user: User) -> dict[str, str]:
    raise NotImplementedError
