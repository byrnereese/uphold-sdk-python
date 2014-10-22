"""
Bitreserve Python SDK
This is a python module to ease integration between python apps and the Bitreserve API.

Repo: http://github.com/byrnereese/bitreserve-python-sdk

TODO
* Create custom exceptions for common errors
* Add support for updating records
* Turn off authentication/authorization for public transactions (or make that optional)
* Transmit a User-Agent field

METHODS TO ADD SUPPORT FOR
url = 'https://api.bitreserve.org/v1/me/transactions'
url = 'https://api.bitreserve.org/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3'
url = 'https://api.bitreserve.org/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3/transactions'
url = 'https://api.bitreserve.org/v1/reserve/transactions/a97bb994-6e24-4a89-b653-e0a6d0bcf634'
"""

import urllib3
import certifi
import json
import version

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
        self.headers = { 'Content-type' : 'application/x-www-form-urlencoded',
                         'User-Agent' : 'bitreserve-python-sdk/' + version.__version__ }

        
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
        """
        Returns a hash containing a comprehensive summary of the current user in content. The data
        returned contains profile data, a list of the users cards, recent transactions and more. 

        :rtype:
          A hash containing all user's properties.
        """
        uri = self._build_url('/me')
        return self._get( uri )

    """
    def get_addresses(self):
        uri = self._build_url('/me/addresses')
        return self._get( uri )
    """
        
    def get_contacts(self):
        """
        Returns all of the contacts associated with the current users.

        :rtype:
          An array of hashes containing all the contacts of the current user's properties.
        """
        uri = self._build_url('/me/contacts')
        return self._get( uri )
        
    def get_cards(self):
        """
        Returns all of the cards associated with the current users.

        :rtype:
          An array of hashes containing all the cards of the current user.
        """
        uri = self._build_url('/me/cards')
        return self._get( uri )

    def get_card(self, c):
        """
        Return the details of a single card belonging to the current user.

        :param String card_id The card ID of the card you wish to retrieve.

        :rtype:
          An array of hashes containing all the cards of the current user.
        """
        uri = self._build_url('/me/cards/' + c)
        return self._get( uri )

    def get_phones(self):
        """
        Returns all of the phone numbers associated with the current user.

        :rtype:
          An array of hashes containing all the phone numbers of the current user.
        """
        uri = self._build_url('/me/phones')
        return self._get( uri )

    def get_reserve_status(self):
        """
        Returns the current status of the reserve. The current status summarized
        the liabilities and assets currently held in the reserve, indexed by the
        asset type. Furthermore, the value of each asset and liability is 
        represented in all supported fiat currencies allowing developers to quickly
        show the value of the reserve in US Dollars, or Euros, etc.

        :rtype:
          An array of hashes summarizing the reserve.
        """
        uri = self._build_url('/reserve')
        return self._get( uri )

    def get_reserve_ledger(self):
        """
        Returns all the rows belowing to the ledger. Each row documents a change in
        the reserve's assets or its liabilities. 

        :rtype:
          An array of ledger entries.
        """
        uri = self._build_url('/reserve/ledger')
        return self._get( uri )

    def get_reserve_chain(self):
        """
        Returns the entire Reservechain consisting of all of the transactions conducted
        by its members. These transactions are 100% anonymous. 

        :rtype:
          An array of transactions.
        """
        uri = self._build_url('/reserve/transactions')
        return self._get( uri )

    def prepare_txn(self, card, to, amount, denom):
        """
        Developers can optionally prepare a transaction in order to preview a transaction
        prior to it being executed. A prepared transaction has a TTL (time-to-live) of 30
        seconds. Within that time, the transaction can be executed at a guaranteed price.

        :param String card_id The card ID from which to draw funds.

        :param String to The recipient of the funds. Can be in the form of a bitcoin 
          address, an email address, or a Bitreserve membername.
        
        :param Float amount The amount to send.

        :param String denom The denomination to send. Permissible values are USD, GBP,
          CNY, JPY, EUR, and BTC.

        :rtype:
          A string representing a handle to a transaction promise.
        """
        fields = {
            'denomination[currency]':'USD',
            'denomination[amount]':0.01,
            'destination':'byrne+13@bitreserve.org'}
        data = self._post('/me/cards/'+card+'/transactions/new', fields);
        fields["signature"] = data["signature"]
        return data["signature"]

    def execute_txn(self, card, to, amount, denom, sig=''):
        """
        Executes a transaction. This is an atomic operation and cannot be reversed.
        When an optional sig parameter is provided a previously quoted market rate
        will be honored when conducting any resulting exchanges. When an optional
        sig parameter is provided, all of the values (card, to, amount and denom)
        must agree and correspond to the originally submitted values.

        :param String card_id The card ID from which to draw funds.

        :param String to The recipient of the funds. Can be in the form of a bitcoin 
          address, an email address, or a Bitreserve membername.
        
        :param Float amount The amount to send.

        :param String denom The denomination to send. Permissible values are USD, GBP,
          CNY, JPY, EUR, and BTC.

        :param String promise (optional) The promise handle guaranteeing a previously
          quoted market rate for the values specified.

        :rtype:
          A string representing a handle to a transaction promise.
        """
        fields = {
            'denomination[currency]':'USD',
            'denomination[amount]':0.01,
            'destination':'byrne+13@bitreserve.org'}
        if sig != '':
            fields['signature'] = sig
        return self._post('/me/cards/'+card+'/transactions', fields);

    def get_ticker(self, t=''):
        """
        Returns current market rates used by the Bitreserve platform when conducting
        exchanges. These rates do not include the commission Bitreserve applies to 
        exchanges. 

        :param String ticker (optional) A specific currency to retrieve quotes for.

        :rtype:
          An array of market rates indexed by currency.
        """
        if t:
            uri = self._build_url('/ticker/' + t )
        else:
            uri = self._build_url('/ticker')
        return self._get( uri )

    """
    HELPER FUNCTIONS
    """

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

        # You're ready to make verified HTTPS requests.
        try:
            response = self.http.request('GET', url, headers=self.headers)
        except urllib3.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            print "Failed certificate check"

        data = json.loads(response.data)
        return data
