import hashlib


def get_name_md5(name: str):
    hashed_str = hashlib.md5(name.encode("utf-8")).hexdigest()
    return hashed_str
