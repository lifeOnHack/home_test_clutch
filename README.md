# GitHub - Okta Integration Script

## 🗂️ What This Does

- Fetches GitHub PAT events (SSO grants)
- Fetches Okta user information
- Correlates them to show which Okta user created which PAT

# Requirements

- Python 3.8+
- Install dependencies:

## Configure Environment

Create a `.env` file with the following vars:

- GITHUB_TOKEN
- GITHUB_ORG
- OKTA_DOMAIN
- OKTA_API_TOKEN

authorize the github token with the github organization
run main.py and the script will print correlated users between GitHub and Okta.

----- PAT NOTES -------

- When using GitHub Enterprise SSO, you must authorize your Personal Access Token (PAT) for your organization under Developer Settings.

- GitHub REST API does NOT expose PATs directly for security.
  In practice, you'd use the Audit Log API or GitHub Advanced Security.

------- Scalability ---------
the main function gets parameters you can modify to fetch data
from others APIs, notice you need to match the .env variables to the correct tokens
needed for the platform you are using
