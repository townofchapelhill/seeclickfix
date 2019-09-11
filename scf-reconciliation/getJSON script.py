import requests
import json
     
with open("secrets.txt") as f:
    secrets = f.read()

url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues"
headers = {
    'Authorization': secrets,
    'Cache-Control': "no-cache",
}

response = requests.request("GET", url, headers=headers)
config = response.json()["metadata"]["query"]["request_types"].split(",")

querystring = {"request_types":config[0],"details":"true","status":"archived"}

response = requests.request("GET", url, headers=headers, params=querystring)

for c in config:
    querystring = {"request_types":c,"details":"true","status":"archived"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    with open("data/config_" + c + ".json", "w+") as f:
        if response.json()["issues"] != [] and response.json()["issues"][0]["questions"] != None:
            for q in response.json()["issues"][0]["questions"]:
                f.write(q["question"] + "\n")
    with open("data/seeclickfix_" + c + ".json", "w+") as f:
        data = {}
        data["issues"] = []
        page = response.json()["metadata"]["pagination"]["page"]
        while(page != None):
            querystring = {"request_types":c,"page":page,"details":"true","status":"archived"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            data["issues"] += response.json()["issues"]
            page = response.json()["metadata"]["pagination"]["next_page"]
        f.write(json.dumps(data))
