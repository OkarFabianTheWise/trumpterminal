import aimod
from requests_oauthlib import OAuth1Session
import os
import json
import time
import random

# Load your environment variables
consumer_key = os.environ.get("X_API_KEY")
consumer_secret = os.environ.get("X_API_SECRET")

# File to store OAuth tokens
TOKEN_FILE = 'tokens.json'

def load_tokens():
    """Load OAuth tokens from a JSON file if they exist."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None

def save_tokens(tokens):
    """Save OAuth tokens to a JSON file."""
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

def get_oauth_tokens():
    """Get OAuth tokens, authorize if they do not exist."""
    tokens = load_tokens()

    if tokens:
        print("Loaded existing tokens.")
        return tokens['oauth_token'], tokens['oauth_token_secret']
    
    # OAuth process
    try:
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Save the tokens for future use
        save_tokens({
            'oauth_token': access_token,
            'oauth_token_secret': access_token_secret
        })

        return access_token, access_token_secret

    except Exception as e:
        print("Error during OAuth process: {}".format(e))
        raise

def make_tweet(text):
    """Post a tweet with the provided text."""
    try:
        access_token, access_token_secret = get_oauth_tokens()

        # Create an OAuth session with the access tokens
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Post the tweet
        response = oauth.post("https://api.twitter.com/2/tweets", json={"text": text})

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Tweet posted successfully with response code: {}".format(response.status_code))
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))

    except Exception as error:
        print("Error in make_tweet:", error)

if __name__ == "__main__":
    try:
        responder = aimod.AIResponder()
        
        # Interval options in seconds (25 mins, 30 mins, 35 mins, 40 mins)
        intervals = [1500, 1800, 2100, 2400]
        
        while True:
            # Sleep for a random interval from the list
            wait_time = random.choice(intervals)
            print(f"Waiting for {wait_time // 60} minutes before next tweet.")
            time.sleep(wait_time)

            # Generate a new quote
            quote = responder.generate_response("Generate a quote")

            # Post the tweet
            print("Tweeting: ", quote)
            make_tweet(quote)
    except Exception as error:
        print("Error::runner:", error)
            
