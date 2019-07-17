import requests
import json
import csv
import secrets
import re
import os
import pandas

# list variable to store data
issues = []
public_issues = []

public_columns = ["Park Maintenance", "Unmaintained Vegetation, Right of Way", "Dead Animal", "Blocked Storm Drain", "Pothole", "Sidewalk Repair", "Traffic Sign Down", "Roll Cart Left at Street", "Traffic Signal", "Post to Neighbors"]
to_drop = ["description", "internal_comments_url", "recategorize_url", "assignment_url", "mark_as_duplicate_url", "canonical_issue", "vote_count", "rating", "lat", "lng", "address", "reopened_at", "is_private", "shortened_url", "visibility", "comments_count", "html_url", "comment_url", "flag_url", "closing_questions_url", "closing_questions_pending", "sla_expires_at", "point", "transitions", "priority", "assignee", "active_service_request", "internal_comments", "reporter", "agent", "request_type", "media", "integrations", "integrations_url", "integration_categories_url", "questions", "comments", "duplicate_issues", "votes", "current_user_relationship"]

# function performs the GET requests to obtain the data from seeclickfix v2 API
def get_issues():
    
    # url with params included
    url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues?page=1&per_page=100&status=open,acknowledged,closed,archived&details=false"
   
    # setting headers, and authenticating
    headers = {
    'Authorization': secrets.seeclickkey,
    'Cache-Control': "no-cache",
    }
    
    # performs the first request to get 100 records
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    # loop through response and append desired content to issues list
    for i in data['issues']:
        issues.append(i)
    
    # page number variable to assist with pagination for subsequent GET requests
    page_number = 2

    # while loop to handle the parsing of GET requests
    # only 100 responses allowed per "page"
    while (len(data['issues']) != 0):
        # reset url to request next page
        url = "https://crm.seeclickfix.com/api/v2/organizations/1102/issues?page=" + str(page_number) + "&per_page=100&status=open,acknowledged,closed,archived&details=false"
        response = requests.get(url, headers=headers)
        # convert response to JSON
        try:
            data = json.loads(response.text)
        except:
            continue
        # loop though desired portion of JSON
        # store in "issues" list
        try:
            for i in data['issues']:
                issues.append(dict(i))
        except:
            write_scf(data)
        print(len(issues))
        # increment page number
        page_number += 1
    # calls the CSV writing function
    write_scf(data)

# Handles parsing the JSON and writing the CSV
def write_scf(data):
    
    # define "issues" as "global" (heh) to allow function to modify it
    global issues
    print(len(issues))
    # open the CSV
    with open("//CHFS/Shared Documents/OpenData/datasets/prestaging/seeclickfix_all.csv", "w+") as scf_headers:

        # loop through list and remove any fields that start with {
        # prevents processing issue on portal
        for entry in issues:
            for summary in public_columns:
                if entry['summary'] == summary:
                    scrubbed_value = re.sub('[^A-Za-z0-9_\-\.: ]', '', str(entry['description']))
                    entry['description'] = scrubbed_value
                    public_issues.append(entry)
                else:
                    continue

        # writes headers
        if os.stat('//CHFS/Shared Documents/OpenData/datasets/prestaging/seeclickfix_all.csv').st_size == 0:
            fieldnames = issues[0].keys()
            csv_writer = csv.DictWriter(scf_headers, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')
            csv_writer.writeheader()

        # writes initial raw file
        for entry in public_issues:
            if entry['report_method'] == "direct":
                csv_writer.writerow(entry)

        clean_scf()

def clean_scf():
    df = pandas.read_csv("//CHFS/Shared Documents/OpenData/datasets/prestaging/seeclickfix_all.csv", error_bad_lines=False, encoding="latin_1")
    df.drop(to_drop, axis=1, inplace=True)
    df.to_csv("//CHFS/Shared Documents/OpenData/datasets/staging/seeclickfix_clean.csv", encoding="utf-8", index=False)


# begins the program
get_issues()