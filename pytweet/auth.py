from requests_oauthlib import OAuth1, OAuth1Session

class OauthSession(OAuth1Session):
    def __init__(self, consumer_key : str, consumer_secret: str, callback=None):
        super().__init__(consumer_key, client_secret=consumer_secret,callback_uri=callback)
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_secret
        self.access_token = None
        self.access_token_secret = None
        self.callback = callback
        

    @property
    def oauth1(self):
        return OAuth1(self.consumer_key,
        client_secret=self.consumer_key_secret,
        resource_owner_key=self.access_token,
        resource_owner_secret=self.access_token_secret,
        decoding=None)

    def set_access_token(self, key, secret):
        self.access_token = key
        self.access_token_secret = secret