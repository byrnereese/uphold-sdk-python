import urllib3
import certifi
import json

"""
# these URLs work:
url = 'https://api.bitreserve.org/v1/me/contacts'
url = 'https://api.bitreserve.org/v1/me/phone_numbers'
url = 'https://api.bitreserve.org/v1/me/transactions'
url = 'https://api.bitreserve.org/v1/me/cards'
url = 'https://api.bitreserve.org/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3'
url = 'https://api.bitreserve.org/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3/transactions'
url = 'https://api.bitreserve.org/v1/ticker'
url = 'https://api.bitreserve.org/v1/ticker/USD'
url = 'https://api.bitreserve.org/v1/ticker/BTCUSD'
url = 'https://api.bitreserve.org/v1/reserve'
url = 'https://api.bitreserve.org/v1/reserve/ledger'
url = 'https://api.bitreserve.org/v1/reserve/transactions'
url = 'https://api.bitreserve.org/v1/reserve/transactions/a97bb994-6e24-4a89-b653-e0a6d0bcf634'

# these URLS don't work:
url = 'https://api.bitreserve.org/v1/users/byrnereese'
url = 'https://api.bitreserve.org/v1/me/addresses'
url = 'https://api.bitreserve.org/v1/me/addresses/145ZeN94MAtTmEgvhXEch3rRgrs7BdD2cY'
"""

class Bitreserve(object):
    """
    Use this SDK to simplify interaction with the Bitreserve API
    """
    
    def __init__(self, host='api.bitreserve.org'):
        self.host = host
        self.version = 0
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', # Force certificate check.
            ca_certs=certifi.where(),  # Path to the Certifi bundle.
            )
        self.headers = { 'Content-type' : 'application/x-www-form-urlencoded' }
        #self.headers = { 'Authorization':'Bearer ' + token }
        #self.headers = { 'Content-type' : 'application/x-www-form-urlencoded','Authorization':'Bearer '+token }
        
    def auth(self, username, password):
        """
        Authenticates against the Bitreserve backend using a username and password. Bitreserve
        return an User Auth Token, which is persisted for the life of the session.

        :param String username A Bitreserve username or email address.

        :param String password The password corresponding to the specified username.

        :rtype:
          The user authentication token string.
        """

        params = {'client_id'     : 'BITRESERVE',
                  'client_secret' : 'secret',
                  'grant_type'    : 'password',
                  'username'      : username,
                  'password'      : password }

        data = self._post('/oauth2/token', params)
        self.token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')
        self.headers['Authorization'] = 'Bearer ' + self.token
        return data

    def get_me(self):
        uri = self._build_url('/me')
        return self._get( uri )

    """
    def get_addresses(self):
        uri = self._build_url('/me/addresses')
        return self._get( uri )
    """
        
    def get_contacts(self):
        uri = self._build_url('/me/contacts')
        return self._get( uri )
        
    def get_cards(self):
        uri = self._build_url('/me/cards')
        return self._get( uri )

    def get_card(self, c):
        uri = self._build_url('/me/cards/' + c)
        return self._get( uri )

    def get_phones(self):
        uri = self._build_url('/me/phones')
        return self._get( uri )

    def get_reserve_status(self):
        uri = self._build_url('/reserve')
        return self._get( uri )

    def get_reserve_ledger(self):
        uri = self._build_url('/reserve/ledger')
        return self._get( uri )

    def get_reserve_chain(self):
        uri = self._build_url('/reserve/transactions')
        return self._get( uri )

    def prepare_txn(self, card, to, amount, denom):
        """
        """
        fields = {
            'denomination[currency]':'USD',
            'denomination[amount]':0.01,
            'destination':'byrne+13@bitreserve.org'}
        data = self._post('/me/cards/'+card+'/transactions/new', fields);
        fields["signature"] = data["signature"]
        return fields

    def execute_txn(self, card, to, amount, denom, sig):
        """
        """
        fields = {
            'denomination[currency]':'USD',
            'denomination[amount]':0.01,
            'destination':'byrne+13@bitreserve.org'}
        if sig:
            fields['signature'] = sig
        return self._post('/me/cards/'+card+'/transactions', fields);

    def get_ticker(self, t=''):
        if t:
            uri = self._build_url('/ticker/' + t )
        else:
            uri = self._build_url('/ticker')
        return self._get( uri )

    def _build_url(self, uri):
        return '/v' + str(self.version) + uri

    def _post(self, uri, params):
        """
        """
        url = 'https://' + self.host + uri

        # You're ready to make verified HTTPS requests.
        try:
            response = self.http.request_encode_body('POST', url, params, self.headers, False)
        except urllib3.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            print "Failed certificate check"

        data = json.loads(response.data)
        return data

    def _get(self, uri):
        """
        """
        url = 'https://' + self.host + uri
        print "GETting " + url
        # You're ready to make verified HTTPS requests.
        try:
            response = self.http.request('GET', url, headers=self.headers)
        except urllib3.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            print "Failed certificate check"

        data = json.loads(response.data)
        return data
