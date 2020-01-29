import requests
import json
import csv
import secrets, filename_secrets
import os

dataset_columns = ['id', 'status', 'summary', 'description', 'rating', 'lat', 'lng', 'address', 'created_at', 'acknowledged_at', 'closed_at', 'reopened_at', 'updated_at', 'url']

# function performs the GET requests to obtain the data from seeclickfix v2 API
def get_issues(csvFile):
    global dataset_columns
    # page number variable to assist with pagination for subsequent GET requests
    page_number = 1
    items_per_page = 50
    # retrieval URL
    url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues?page=" + str(page_number) + "&per_page=" + str(items_per_page) + "&status=open,acknowledged,closed,archived&details=false"
    # setting headers, and authorization
    headers = {
    'Authorization': secrets.seeclickkey,
    'Cache-Control': "no-cache",
    #'If-Modified-Since': "Wed, 01 Jan 2020 00:00:00 GMT"
    }
    
    # while loop to handle the parsing of GET requests
    while True:
        # retrieval URL
        url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues?page=" + str(page_number) + "&per_page=" + str(items_per_page) + "&status=open,acknowledged,closed,archived&details=false"
        # request next page
        # print(url)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f'API call failed: {response.status_code}')
            raise RuntimeError
            # break
        # convert response to JSON
        data = json.loads(response.text)
        if len(data['issues']) == 0:
            # all issues retrieved
            break
        # loop though desired portion of JSON
        for i in data['issues']:
            row_data = {}
            # select specific columns to append
            for element in dataset_columns:
                row_data[element] = dict(i)[element]
            csvFile.writerow(row_data)
        print(f'Records processed: {page_number*items_per_page}')
        # increment page number
        page_number += 1
    return

# Main
if __name__ == '__main__':
    output_filename = os.path.join(filename_secrets.preStaging, "seeclickfix_all.csv")
    outputFile = open(output_filename, 'w', encoding='utf-8')
    csvFile = csv.DictWriter(outputFile, fieldnames=dataset_columns)
    if os.stat(output_filename).st_size == 0:
          # write the header if the file is empty
          csvFile.writeheader()
    get_issues(csvFile)
    outputFile.close()