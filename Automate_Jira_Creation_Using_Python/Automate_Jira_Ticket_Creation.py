# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://digambarrajaram2.atlassian.net/rest/api/3/issue"

EMAIL = "digambarrajaram2@gmail.com"
API_TOKEN = "ATATT3xFfGF0t1dR4XNToaUsuyVyUsq3-ZUM1wgmRWnOEuA8d7vL4nUkPppTHYYLtAvZdtGHaezjxIM1NX-JnUxDcHJngxnQLb_ki4NujniLbuKh-EmEUBT1081CvN4Js8Ss7UDM8XeZhogvmmc_FWHMnK0e88J9oTxx9TvMcnKaHVz3Q-ZIU6Q=F44D34E7"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "fields": {

    "description": {
      "content": [
        {
          "content": [
            {
              "text": "My first JIRA Ticket",
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "issuetype": {
      "id": "10011"
    },
    "project": {
      "key": "SCRUM"
    },
    "summary": "First Jira Ticket",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))