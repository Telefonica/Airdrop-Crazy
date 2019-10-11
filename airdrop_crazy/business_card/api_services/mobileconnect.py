import requests

class MobileConnect():

    def __init__(self, phone=""):
        self.phone = phone
    
    def request_data(self):
        if (self.phone):
            # Form the url with the given phone
            url = "https://discover.mobileconnect.io/gsma/v2/discovery"

            payload = f""
            headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'Authorization': "",
                'cache-control': "no-cache",
                }

            response = requests.request("POST", url, data=payload, headers=headers)
            response_proc = response.json()
            if(response_proc.get("error") == None): 
                try:
                    operator = self.transform_operator(response_proc)
                    country = response_proc.get("response", {}).get("country", "")
                    currency = response_proc.get("response", {}).get("currency", "")
                    return operator, country, currency
                except Exception as e:
                    print(f"no operator found {e}")
            else:
                error = response_proc.get("error", "")
                print(f"Error en response mobileconnect --> {error}")
        return "", "", ""

    def transform_operator(self, response):
        operator = response.get("response", {}).get("serving_operator", "Operator not found")
        operators_tras = {"telefonica_spain" : "Telefonica",  "vodafone_spain" : "Vodafone", "orange_spain" : "Orange"}
        return operators_tras.get(operator)


if __name__ == "__main__":
    print("Entramos en mobileconnect")
    mobileconnect = MobileConnect(phone="+34686522321")
    operator, country, currency = mobileconnect.request_data()
    print(f"{operator}  {country} {currency}")

