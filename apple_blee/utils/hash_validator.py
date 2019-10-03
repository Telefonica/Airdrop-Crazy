import requests

def check_hash(hash):
    url = "http://172.16.0.218:5000/api/search"
    querystring = {"hash": hash}
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTg0MjIxMjMsIm5iZiI6MTU1ODQyMjEyMywianRpIjoiZTE2ZmFjYzQtZGU4OS00NWY1LWI3MjQtM2YxODM4NjQxZGUwIiwiaWRlbnRpdHkiOiJrX21pdG5pYyIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.BPXKILXs0vDGRRe5svcxlAGJUFMI_gCgX4Y2Xh2B_h0",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get("phone", "None")
    return "None"

if __name__ == "__main__":

    response = check_hash("3904ce0b7da5df62cae348a3010d35ca95a4653d28fb5b39534d9ec76a5932a9")
    print(response)
    print(type(response))
    if(response != "None"):
        print("good")
    else:
        print("none")
