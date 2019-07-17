# seeclickfix

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/26b0d186d3c1424fa1a240c083c3f5df)](https://app.codacy.com/app/TownofChapelHill/seeclickfix?utm_source=github.com&utm_medium=referral&utm_content=townofchapelhill/seeclickfix&utm_campaign=Badge_Grade_Settings)

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


