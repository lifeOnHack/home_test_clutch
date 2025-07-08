import json
from github_api import get_PAT_events
from okta_api import get_okta_users
from correlate import correlate_github_okta,filter_pat_events

def main(filter = lambda pat: True):
    print("Fetching GitHub PAT events...")
    pats = get_PAT_events()
    print(f"Found {len(pats)} PAT events.")

    print("Fetching Okta users...")
    okta_users = get_okta_users()
    print(f"Found {len(okta_users)} Okta users.")

    print("Correlating data...")
    correlations = correlate_github_okta(pats, okta_users)

    print("Filtering data...")
    filtered_correlations = filter_pat_events(correlations, filter)

    print(f"✅ {len(filtered_correlations)} correlations left after filtering")
    # Save to JSON file
    output_file = "pat_okta_correlation.json"
    with open(output_file, "w") as f:
        json.dump(filtered_correlations, f, indent=4)

    print(f"✅ Correlation data saved to {output_file}")
    print("\n\n",filtered_correlations)

if __name__ == "__main__":
    main(lambda pat: (
        pat["github_token_id"] != None and pat["github_actor"] != None
        ))
