import requests
import json
def add(a:int,b:int)->int:
    return a+b

def get_for_request(url):
    result = requests.get(url)
    if result.status_code != 200:
        return "error"
    else:
        return result.text