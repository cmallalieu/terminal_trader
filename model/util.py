import requests

APIURL = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol={ticker}"
APIURL2 = "http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input={company_name}"

FAKEDATA = {
        "stok": 3.50
        }

def get_price(ticker):
    if ticker in FAKEDATA:
        return FAKEDATA[ticker]
    
    response = requests.get(APIURL.format(ticker=ticker))
    if response.status_code == 200:
        data = response.json()
        if data.get("Status") == "SUCCESS":
            return data["LastPrice"]
        else:
            return None
    return None

def get_ticker(company_name):
    response = requests.get(APIURL2.format(company_name=company_name))
    if response.status_code == 200:
        data = response.json()
        if len(data) == 0:
            return None
        else:
            return data[0]["Symbol"]
    return None
