import os, requests
from typing import Dict,List

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_headers() -> Dict[str, str]:
    """
    Returns headers for GitHub API requests.
    """
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
def get_org_members(org: str) -> List[Dict]:
    """
    Fetch all members in the GitHub organization.
    """
    url = f"{GITHUB_API_URL}/orgs/{org}/members"
    response = requests.get(url, headers=get_github_headers())
    response.raise_for_status()
    return response.json()

def get_user_tokens(username: str) -> List[Dict]:
    """
    NOTE: GitHub REST API does NOT expose PATs directly for security.
    This is just a placeholder to illustrate the idea.
    In practice, you'd use the Audit Log API or GitHub Advanced Security.

    So here, we demonstrate a generic user info call.
    """
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, headers=get_github_headers())
    response.raise_for_status()
    return response.json()