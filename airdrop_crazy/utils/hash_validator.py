import requests

def check_hash(hash):
    """Check the hash to the endpoint were the api Docker has been deployed
    
    Args:
        hash (str): Hash string obtained with airdrop_leak script
    
    Returns:
        str: Phone received or "None"
    """

    url = "http://172.16.0.218:5000/api/search"
    querystring = {"hash": hash}
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTg0MjIxMjMsIm5iZiI6MTU1ODQyMjEyMywianRpIjoiZTE2ZmFjYzQtZGU4OS00NWY1LWI3MjQtM2YxODM4NjQxZGUwIiwiaWRlbnRpdHkiOiJrX21pdG5pYyIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.BPXKILXs0vDGRRe5svcxlAGJUFMI_gCgX4Y2Xh2B_h0",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get("phone", "None")
    return "None"

