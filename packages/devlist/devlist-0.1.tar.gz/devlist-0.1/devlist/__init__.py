import requests

def profile(id:int):
    api = requests.get(f"https://devlist.dev/api/user/{id}")
    return api.json()

def bio(id:int):
    api = requests.get(f"https://devlist.dev/api/user/{id}")
    if "bio" in api.json():
        return api.json()["bio"]
    else:
        return f"No bio in {id} account"

def username(id:int):
    api = requests.get(f"https://devlist.dev/api/user/{id}")
    return api.json()["username"]


def tag(id:int):
    api = requests.get(f"https://devlist.dev/api/user/{id}")
    return api.json()["tag"]

def discriminator(id:int):
    api = requests.get(f"https://devlist.dev/api/user/{id}")
    return api.json()["discriminator"]