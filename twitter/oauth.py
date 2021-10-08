from requests_oauthlib import OAuth1Session

class Oauth:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def session(self, client_key, *,client_secret, resource_owner_key, resource_owner_secret):
        return OAuth1Session(client_key, client_secret=client_secret, resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)

    def requests_oauth(self):
        request_token_url = "https://api.twitter.com/oauth/request_token"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)
        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except Exception as e:
            raise e

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret") 

     # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go authorize here in get PIN in the website: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

      # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )

        oauth_tokens = oauth.fetch_access_token(access_token_url)
        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]
        return self.consumer_key, self.consumer_secret, access_token, access_token_secret