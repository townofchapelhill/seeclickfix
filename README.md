# seeclickfix

## Gather reported events and status from the SeeClickFix portal
## Reporting tables for private & internal issues using the SeeClickFix v2 organization API

### Goal 
Access the [See Click Fix]( https://seeclickfix.com/chapel-hill?locale=en) API to download all reported requests.

### Purpose 
See Click Fix is a portal to report maintenace requests from citizens to the town.

### Methodology 
Python script all-scf.py accesses the API to pull requests.

### Data Source
SeeClickFix API v2

### Output 
seeclickfix_all.csv - raw output from API calls

seeclickfix_clean - sanitized content via pandas

### Transformations
uses Pandas to remove unwanted columns and regex to clean fields


