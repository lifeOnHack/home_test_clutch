import os, requests
from typing import Dict,List
from dotenv import load_dotenv

load_dotenv()  # טען משתני סביבה מ-.env
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
    
def get_org_members(url: str = f"{GITHUB_API_URL}/orgs/{os.getenv('GITHUB_ORG')}/members") -> List[Dict]:
    """Fetch all members in the GitHub organization.

    Args:
        url (str): the url to fetch the members. Defaults to f"{GITHUB_API_URL}/orgs/{os.getenv('GITHUB_ORG')}/members".

    Returns:
        List[Dict]: list of members
    """
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
    """get user's tokens from github api

    Returns:
        List[Dict]: list of all PATs of the user
    """
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, headers=get_github_headers())
    response.raise_for_status()
    return response.json()

def get_PAT_events(url:str = f"{GITHUB_API_URL}/orgs/{os.getenv('GITHUB_ORG')}/audit-log",
                   headers:dict = get_github_headers(),params={"per_page": 50}):
    """Get all PATs events filtered by params from the 'api' Audit Log with pagination.

    Args:
        url (str, optional): url to fetch PATs from. Defaults to f"{GITHUB_API_URL}/orgs/{os.getenv('GITHUB_ORG')}/audit-log".
        headers (dict, optional): for url. Defaults to get_github_headers().
        params (dict, optional): for url. Defaults to {}.

    Returns:
        _type_: all the PAT events filtered
    """

    results = []
    while url:
        response = requests.get(url, headers=headers ,params=params)
        response.raise_for_status()
        page_results = response.json()
        results.extend(page_results)

        # Handle pagination: look for 'Link' header
        links = response.links
        if 'next' in links:
            url = links['next']['url']
            params = {}  # params כבר בפנים בקישור
        else:
            url = None

    return results




def test_get_org_members():
    org = os.getenv("GITHUB_ORG")
    members = get_org_members(f"{GITHUB_API_URL}/orgs/{org}/members")
    print(f"✅ Found {len(members)} members in org '{org}'")
    for member in members:
        print(f"- {member.get('login')} | {member.get('id')}")

def test_get_user_tokens():
    # דוגמת משתמש לבדיקה
    username = "bigbrolinus"  # החלף בשם משתמש קיים בארגון שלך
    user_info = get_user_tokens(username)
    print(f"✅ Info for '{username}':")
    print(user_info)
    
if __name__ == "__main__":
    test_get_org_members()
    test_get_user_tokens()
    #events = get_PAT_events()
    #print(len(events))
    #[print(event) for event in events]
