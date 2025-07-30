from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

EMAIL = ""
API_TOKEN = ""
PROJECT_KEY = ""
ISSUE_TYPE_ID = ""

# Mapping of GitHub issue ID (as string) -> Jira issue key
GITHUB_TO_JIRA = {}

@app.route("/createJira", methods=['POST'])
def handle_github_webhook():
    payload = request.get_json()
    action = payload.get("action")
    issue_data = payload.get("issue", {})
    comment_data = payload.get("comment", {})
    github_issue_id = str(issue_data.get("id"))  # Store as string for mapping consistency
    issue_title = issue_data.get("title")
    issue_body = issue_data.get("body", "")

    # 🔹 Create new Jira issue if GitHub issue opened and contains "/jira"
    if action == "opened" and "/jira" in issue_body.lower():
        url = "https://digambarrajaram2.atlassian.net/rest/api/3/issue"
        auth = HTTPBasicAuth(EMAIL, API_TOKEN)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        jira_payload = {
            "fields": {
                "project": {
                    "key": PROJECT_KEY
                },
                "summary": f"{issue_title}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": issue_body
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "id": ISSUE_TYPE_ID
                }
            }
        }

        response = requests.post(url, headers=headers, json=jira_payload, auth=auth)
        response_data = response.json()

        jira_issue_key = response_data.get("key")
        if jira_issue_key:
            GITHUB_TO_JIRA[github_issue_id] = jira_issue_key

        return jsonify({
            "message": "Jira issue created",
            "jira_issue": jira_issue_key
        }), response.status_code

    # 🔹 Add comment to existing Jira issue if comment is added on GitHub
    elif action == "created" and "comment" in payload and "/jira" in issue_body.lower():
        comment_body = comment_data.get("body", "")
        jira_issue_key = GITHUB_TO_JIRA.get(github_issue_id)

        if not jira_issue_key:
            return jsonify({"error": "Jira issue not found for GitHub issue"}), 404

        url = f"https:///rest/api/3/issue/{jira_issue_key}/comment"
        auth = HTTPBasicAuth(EMAIL, API_TOKEN)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        comment_payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment_body
                            }
                        ]
                    }
                ]
            }
        }

        response = requests.post(url, headers=headers, json=comment_payload, auth=auth)
        return jsonify({
            "message": "Comment added to Jira issue",
            "jira_issue": jira_issue_key
        }), response.status_code

    return jsonify({"message": "No action taken"}), 200

# Start Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
