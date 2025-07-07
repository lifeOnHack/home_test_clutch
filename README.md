# GitHub - Okta Integration Script

## Requirements

- Python 3.8+
- Install dependencies:

## Configure Environment

Create a `.env` file with the following vars:

- GITHUB_TOKEN
- GITHUB_ORG
- OKTA_DOMAIN
- OKTA_API_TOKEN

run main.py and the script will print correlated users between GitHub and Okta.

----- PAT NOTES -------

- When using GitHub Enterprise SSO, you must authorize your Personal Access Token (PAT) for your organization under Developer Settings.
