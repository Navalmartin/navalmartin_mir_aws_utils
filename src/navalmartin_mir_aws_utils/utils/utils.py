import base64
import hmac
import hashlib


def get_secret_hash(username: str, client_id: str,
                    client_secret: str) -> str:
    """Calculate a secret hash  for the given username on the
    given client id
    It uses the SHA256 algorithm

    Parameters
    ----------
    username: The username
    client_id: The client id
    client_secret: The client secret

    Returns
    -------

    A string representing the hash
    """
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode("utf-8"),
                   msg=str(msg).encode("utf-8"),
                   digestmod=hashlib.sha256, ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
