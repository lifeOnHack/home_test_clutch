"""
correlate.py

Contains logic to correlate GitHub PATs to Okta users.
"""

from typing import List, Dict

def correlate_github_okta(
    pat_events: List[Dict],
    okta_users: List[Dict],
) -> List[Dict]:
    """
    Correlate PAT events with Okta users based on email.

    Args:
        pat_events (List[Dict]): all pat events
        okta_users (List[Dict]): users on okta organization

    Returns:
        List[Dict]: _description_
    """
    results = []

    # Create a dictionary of Okta users by email- email:user_data
    okta_email_map = {
        u['profile']['email'].lower(): u for u in okta_users if u['profile']['email']
    }
    
    for pat in pat_events:
        actor = pat.get('actor')
        actor_email = pat.get('external_identity_nameid')
        okta_user = None
        if actor_email is not None: #mail dont alaeays exist
            okta_user = okta_email_map.get(actor_email.lower())

        results.append({
            "github_actor": actor,
            "action": pat.get('action'),
            "github_token_id": pat.get('token_id'),
            "github_scopes": pat.get('token_scopes'),
            "github_created_at": pat.get('created_at'),
            "okta_email": actor_email if okta_user else None,
            "okta_firstName": okta_user['profile']['firstName'] if okta_user else None,
            "okta_lastName": okta_user['profile']['lastName'] if okta_user else None,
            "okta_status": okta_user['status'] if okta_user else None,
        })
    results.sort(key=lambda x: x["github_actor"] if x["github_actor"] else "zzz")#zzz for end

    return results


def filter_pat_events(corrlations: List[Dict], filter_func) -> List[Dict]:
    """
    Filters PAT events based on a provided filter function.

    Args:
        corrlations (List[Dict]): List of corrlations between PAT events and okta users to filter.
        filter_func (Callable[[Dict], bool]): A function that takes a PAT event
            as input and returns a boolean indicating whether the event should
            be included in the result.

    Returns:
        List[Dict]: A list of filtered PAT events.
    """
    return [pat for pat in corrlations if filter_func(pat)]


if __name__ == "__main__":
    from github_api import get_PAT_events
    from okta_api import get_okta_users
    
    cor = correlate_github_okta(get_PAT_events(), get_okta_users())
    for c in cor:
        print(c)