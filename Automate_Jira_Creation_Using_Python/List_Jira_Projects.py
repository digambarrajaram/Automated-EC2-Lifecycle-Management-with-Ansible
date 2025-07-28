# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import sys


url = "https://digambarrajaram2.atlassian.net/rest/api/3/project"

EMAIL = "digambarrajaram2@gmail.com"
API_TOKEN = "ATATT3xFfGF0t1dR4XNToaUsuyVyUsq3-ZUM1wgmRWnOEuA8d7vL4nUkPppTHYYLtAvZdtGHaezjxIM1NX-JnUxDcHJngxnQLb_ki4NujniLbuKh-EmEUBT1081CvN4Js8Ss7UDM8XeZhogvmmc_FWHMnK0e88J9oTxx9TvMcnKaHVz3Q-ZIU6Q=F44D34E7"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
  "Accept": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

output = json.loads(response.text)
for i in range(len(output)):
    project_name = output[i]["name"]
    print(f"{i+1})",project_name.encode(sys.stdout.encoding, errors='replace').decode())

