"""
The MIT License (MIT)

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from requests_oauthlib import OAuth1, OAuth1Session

class OauthSession(OAuth1Session):
    def __init__(self, consumer_key: str, consumer_secret: str, callback=None):
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_secret
        self.access_token = None
        self.access_token_secret = None
        self.callback = callback

    @property
    def oauth1(self) -> OAuth1:
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_key_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            decoding=None,
        )

    def set_access_token(self, key, secret):
        self.access_token: str = key
        self.access_token_secret: str = secret
