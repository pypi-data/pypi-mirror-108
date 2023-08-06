import requests
import json
def add(a:int,b:int)->int:
    return a+b

def get_for_request(url,session=None):
    result = "error"
    if session is None:
        result = requests.get(url)
    else:
        result = session.get(url)
    if result.status_code != 200:
        return "error"
    else:
        return result.text
def post_for_request(url,requestbody,session=None):
    result = "error"
    if session is None:
        result = requests.post(url,json=requestbody)
    else:
        result = session.post(url,json=requestbody)
    if result.status_code != 200:
        return "error"
    else:
        return json.loads(result.text)