import requests

API_URLS = ["https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"]

class API_util():
    def __init__(self):
        pass
    
    def extract(self):
        parsed_dict = {}
        for url in API_URLS:
            response = requests.get(url).json()
            text = url.split(".")[-2]
            table_name = "CDW_SAPP_" + text.split("/")[-1].upper()
            parsed_dict[table_name] = response
        return parsed_dict
