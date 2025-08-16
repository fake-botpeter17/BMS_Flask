from utils.types import User
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from uuid import uuid4
from db.redis_client import delete_key, set_key, get_key
from typing import Optional
import base64


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
    kid = str(uuid4())
    private_key, public_key = generate_rsa_keys()
    set_key(key=kid, value=private_key.decode(), expire=expiry_minutes * 60)
    return kid, public_key


def getPrivateKey(kid: str) -> Optional[bytes]:
    """
    Retrieves the private key associated with a given kid (key ID).

    Args:
        kid (str): The key ID.

    Returns:
        Optional[bytes]: The private key if it exists and has not expired, None otherwise.
    """
    key_data = get_key(kid)
    if not key_data:
        return None
    delete_key(kid)
    return key_data.encode()


def revokeKey(kid: str) -> None:
    delete_key(kid)


def generate_refresh_access_tokens(user: User) -> dict[str, str]:
    raise NotImplementedError
