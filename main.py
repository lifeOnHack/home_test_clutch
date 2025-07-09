import json
from github_api import get_PAT_events
from okta_api import get_okta_users
from correlate import correlate_github_okta,filter_pat_events,save_data_to_file

def main(user_api_args:dict = {},
    pats_api_args:dict = {},
    filter = lambda pat: True,
    corr_func = correlate_github_okta, 
    save_func = lambda data:None):
    """the main function with all the inputs the users need to run
    one can add his own filter, file saving and correlation function

    Args:
        user_api_url (dict): args for the usersfetch request
        pats_api_args (dict): args for the pats fetch request
        filter (_type_, optional): filter data after correlation if needed. Defaults to lambdapat:True.
        corr_func (_type_, optional): the correlation function gets the PATs and the users. Defaults to correlate_github_okta.
        save_to_file (_type_, optional): function to save the data gets the data and the file opend. Defaults to lambdadata:None.
    """
    print("Fetching GitHub PAT events...")
    pats = get_PAT_events(**pats_api_args)
    print(f"Found {len(pats)} PAT events.")

    print("Fetching Okta users...")
    okta_users = get_okta_users(**user_api_args)
    print(f"Found {len(okta_users)} Okta users.")

    print("Correlating data...")
    correlations = corr_func(pats, okta_users)

    print("Filtering data...")
    filtered_correlations = filter_pat_events(correlations, filter)

    print(f"✅ {len(filtered_correlations)} correlations left after filtering")
    # Save to JSON file
    output_file = "pat_okta_correlation.json"
    save_data_to_file(filtered_correlations, save_func, output_file)

    print(f"✅ Correlation data saved to {output_file}")
    print("\n\n",filtered_correlations)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main(
        filter=lambda pat: (pat["github_token_id"] != None and pat["github_actor"] != None),
        save_func=lambda data,f: json.dump(data, f, indent=4) 
        )
