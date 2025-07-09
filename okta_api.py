import os, requests
from typing import List, Dict

OKTA_API_URL = f"https://{os.getenv('OKTA_DOMAIN')}/api/v1"


def get_okta_headers() -> Dict[str, str]:
    """
    Returns headers for Okta API requests.
    """
    return {
        "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}",
        "Accept": "application/json"
    }


def get_okta_users(url = f"{OKTA_API_URL}/users", headers=get_okta_headers()) -> List[Dict]:
    """Fetch all users in the Okta org.

    Args:
        url (str, optional): the url to fetch the usres. Defaults to f"{OKTA_API_URL}/users".
        headers ([dict], optional): the headers one wants to add. Defaults to get_okta_headers().

    Returns:
        List[Dict]: list of okta users
    """
    results = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results.extend(response.json())
        links = response.links
        if 'next' in links:
            url = links['next']['url']
        else:
            url = None
    return results

if __name__ == "__main__":
    users = get_okta_users()
    print(f"✅ Found {len(users)} users in Okta\n\n")
    print(users)
    
    
    