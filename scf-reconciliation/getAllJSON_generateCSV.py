import requests
import json
import csv
     
with open("secrets.txt") as f:
    secrets = f.read()

#Gets list of issue type IDs
url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues"
headers = {
    'Authorization': secrets,
    'Cache-Control': "no-cache",
}

response = requests.request("GET", url, headers=headers)
issueTypes = response.json()["metadata"]["query"]["request_types"].split(",")

#Gets actual issue JSONs
url = "https://seeclickfix.com/api/v2/issues/"

with open("seeclickfix_all.json", "w+") as f:
    querystring = {"request_types":issueTypes[0],"status":"open,acknowledged,closed,archived"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = {}
    data["issues"] = []
    for i in issueTypes:
        page = response.json()["metadata"]["pagination"]["page"]
        while(page != None):
            querystring = {"request_types":i,"page":page,"status":"open,acknowledged,closed,archived","per_page":"100"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            data["issues"] += response.json()["issues"]
            page = response.json()["metadata"]["pagination"]["next_page"]
    f.write(json.dumps(data))

with open("seeclickfix_all.json") as f:
    data = json.load(f)
    for item in data["issues"]:
        item["request_type"] = item["request_type"]["title"]

with open("seeclickfix_all.csv", "w+") as f:
    #All fields that start with a '{' are removed from the dictionary
    for item in list(data["issues"][0]):
        if str(data["issues"][0][item])[0] == "{":
            for issue in data["issues"]:
                del issue[item]
    fieldnames = list(data["issues"][0].keys())
    csv_writer = csv.DictWriter(f, fieldnames = fieldnames, lineterminator = "\n")
    csv_writer.writeheader()
    for item in data["issues"]:
        csv_writer.writerow(item)
