import requests

class EveryoneApi():

    def __init__(self, phone=""):
        self.phone = phone
    
    def request_data(self):
        if self.phone:
            
            # Form the url with the given phone
            url = "https://api.everyoneapi.com/v1/phone/{0}".format(self.phone)

            # Form the dictionary with all the queries in the url
            querystring = {
                "account_sid":"",
                "auth_token":"",
                "data":"name,address,location,cnam,carrier,carrier_o,gender,linetype,image,line_provider,profile"
            }

            # Form the dictionary with all the headers
            headers = {
                'Cache-Control': "no-cache",
            }

            # Form the response with teh headers and query parameteres
            response = requests.request("GET", url, headers=headers, params=querystring)
            if(response.status_code == 200):
                try:
                    # Return response converted from json
                    response_parsed = response.json()
                    operator = self.get_operator(response_parsed)
                    name = self.get_name(response_parsed)
                    gender = self.get_gender(response_parsed)
                    return operator, name, gender
                except Exception as e:
                    print(f"Error en parseo everyoneapi --> {e}")
                    return ("", "", "")
            else:
                print(f"Error en response everyoneapi --> {response.status_code}")
                print("")
        return ("", "", "")
    
    def get_operator(self, response):
        operator = response.get("data", {}).get("carrier_o", {}).get("name", "Operator not found")
        return operator
    
    def get_name(self, response):
        name = response.get("data", {}).get("name", "")
        return name
    
    def get_gender(self, response):
        gender = response.get("data", {}).get("gender", "")
        return gender

