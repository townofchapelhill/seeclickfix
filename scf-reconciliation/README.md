# scf-reconciliation
Custom reconciliation report for the Town of Chapel Hill Public Works department. SeeClickFix data is retrieved from the v2 API and copied locally using a Python script. The data is displayed on an HTML page with filtering an export functions. 

This makes use of positional data in the answers JSON array to retrieve secondary question answers for each request type.

How to use:

1. Put the ID of the request type you want in config_getJSON.txt. It is a comma-separated list.
2. Generate a compatible JSON file using "getJSON script.py". This script generates a JSON file for every request type specified in config_getJSON.txt, in the format "seeclickfix_[ID number].json". These can be found in the "data" folder.
3. Create a config file for the request type you're using-- it can be named whatever you want, as long as it is in the root folder. This file contains the questions from the "questions" field of SeeClickFix that you would like displayed in the HTML table. Each question must be written exactly as formatted in the SeeClickFix API, and are separated by newlines.

# We keep changing what happens after this part. Will be added soon.
