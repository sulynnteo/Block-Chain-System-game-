from hashlib import sha256
from json import dumps


def encrypt_sha256(data: dict[str, any]) -> str:

    json_string = dumps(data, indent=4, separators=(',', ': '))
    return sha256(json_string.encode()).hexdigest()