"""
Uphold Python SDK
This is a python module to ease integration between python apps and the Uphold API.

Repo: http://github.com/byrnereese/uphold-python-sdk

TODO
* Create custom exceptions for common errors
* Add support for updating records
* Turn off authentication/authorization for public transactions (or make that optional)
* Transmit a User-Agent field

METHODS TO ADD SUPPORT FOR
url = 'https://api.uphold.com/v1/me/transactions'
url = 'https://api.uphold.com/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3'
url = 'https://api.uphold.com/v1/me/cards/2b2eb351-b1cc-48f7-a3d0-cb4f1721f3a3/transactions'
url = 'https://api.uphold.com/v1/reserve/transactions/a97bb994-6e24-4a89-b653-e0a6d0bcf634'
"""

from __future__ import print_function, unicode_literals

import urllib3
import requests
import json
import ssl
from .version import __version__

class VerificationRequired(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RateLimitError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NotSupportedInProduction(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Uphold(object):
    """
    Use this SDK to simplify interaction with the Uphold API
    """
    
    def __init__(self, sandbox=False):
        if sandbox:
            self.host = 'api-sandbox.uphold.com'
        else:
            self.host = 'api.uphold.com'
        self.in_sandbox = sandbox
        self.debug   = False
        self.version = 0
        self.session = requests.Session()
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'uphold-python-sdk/' + __version__
            }
        self.pat = None
        self.otp = None

    def _debug(self, s):
        if self.debug:
            print(s)
        
    def verification_code(self, code):
        self.otp = code

    def auth_basic(self, username, password):
        """
        Authenticates against the Uphold backend using a username and password. Uphold
        return an User Auth Token, which is persisted for the life of the session.
        
        :param String username An Uphold username or email address.
        
        :param String password The password corresponding to the specified username.
        
        """
        self.username = username
        self.password = password
        self.pat = None
        
    def auth_pat(self, pat):
        """
        Sets the authentication method to PAT, or "Personal Access Token." Before calling this
        method, a PAT needs to be created using the create_path() method. 

        :param String pat The personal access token

        """
        self.username = None
        self.password = None
        self.pat = pat

    def create_pat(self, desc):
        """
        Creates a personal access token.

        :param String desc A description for the token
        
        :rtype:
          A string representing the Personal Access Token
        """
        params = {
            'description': desc
        }
        self.headers['Content-Type'] = 'application/json'
        data = self._post('/me/tokens', params)
        return data.get('accessToken')

    def get_pats(self):
        """
        Returns a list of personal access tokens.

        :rtype:
          A list of personal access tokens
        """
        self.headers['Content-Type'] = 'application/json'
        data = self._get('/me/tokens')
        return data

    def get_me(self):
        """
        Returns a hash containing a comprehensive summary of the current user in content. The data
        returned contains profile data, a list of the users cards, recent transactions and more.

        :rtype:
          A hash containing all user's properties.
        """
        return self._get('/me')

    def get_contacts(self):
        """
        Returns all of the contacts associated with the current users.

        :rtype:
          An array of hashes containing all the contacts of the current user's properties.
        """
        return self._get('/me/contacts')

    def get_contact(self, contact):
        """
        Returns the contact associated with the contact id.

        :rtype:
          An hash containing the contact requested.
        """
        return self._get('/me/contacts/{}'.format(contact))

    def create_contact(self, first_name, last_name, company, emails=[], bitcoin_addresses=[]):
        fields = {
            'firstName': first_name,
            'lastName': last_name,
            'company': company,
            'emails': emails,
            'addresses': bitcoin_addresses
        }
        return self._post('/me/contacts', fields)

    def get_cards(self):
        """
        Returns all of the cards associated with the current users.

        :rtype:
          An array of hashes containing all the cards of the current user.
        """
        return self._get('/me/cards')

    def get_card(self, c):
        """
        Return the details of a single card belonging to the current user.

        :param String card_id The card ID of the card you wish to retrieve.

        :rtype:
          An array of hashes containing all the cards of the current user.
        """
        return self._get('/me/cards/' + c)

    def get_card_transactions(self, card):
        """
        Requests a list of transactions associated with a specific card.

        :rtype:
          An array of hashes containing all the card transactions.
        """
        return self._get('/me/cards/{}/transactions'.format(card))

    def get_phones(self):
        """
        Returns all of the phone numbers associated with the current user.

        :rtype:
          An array of hashes containing all the phone numbers of the current user.
        """
        return self._get('/me/phones')

    def get_reserve_statistics(self):
        return self._get('/reserve/statistics')

    def get_reserve_ledger(self):
        """
        Returns all the rows belowing to the ledger. Each row documents a change in
        the reserve's assets or its liabilities.

        :rtype:
          An array of ledger entries.
        """
        return self._get('/reserve/ledger')

    def get_reserve_chain(self):
        """
        Returns the entire Reservechain consisting of all of the transactions conducted
        by its members. These transactions are 100% anonymous.

        :rtype:
          An array of transactions.
        """
        return self._get('/reserve/transactions')

    def get_reserve_transaction(self, transaction):
        """
        Returns a public transaction from the Reservechain. These transactions are 100% anonymous.

        :rtype:
          An array with the transaction.
        """
        return self._get('/reserve/transactions/{}'.format(transaction))

    def get_transactions(self):
        """
        Requests a list of transactions associated with the current user.

        :rtype:
          An array of hashes containing all the current user's transactions.
        """
        return self._get('/me/transactions')

    def prepare_txn(self, card, to, amount, denom):
        """
        Developers can optionally prepare a transaction in order to preview a transaction
        prior to it being executed. A prepared transaction has a TTL (time-to-live) of 30
        seconds. Within that time, the transaction can be executed at a guaranteed price.

        :param String card_id The card ID from which to draw funds.

        :param String to The recipient of the funds. Can be in the form of a bitcoin
          address, an email address, or an Uphold username.

        :param Float/Decimal amount The amount to send.

        :param String denom The denomination to send. Permissible values are USD, GBP,
          CNY, JPY, EUR, and BTC.

        :rtype:
          A transaction object.
        """
        fields = {
            'denomination[currency]': denom,
            'denomination[amount]': str(amount),
            'destination': to
        }
        data = self._post('/me/cards/' + card + '/transactions', fields)
        return data['id']

    def execute_txn(self, card, transaction, message=''):
        """
        Executes a transaction. This is an atomic operation and cannot be reversed.
        When an optional sig parameter is provided a previously quoted market rate
        will be honored when conducting any resulting exchanges. When an optional
        sig parameter is provided, all of the values (card, to, amount and denom)
        must agree and correspond to the originally submitted values.

        :param String card_id The card ID from which to draw funds.

        :param String transaction Id of the transaction as returned by prepare_txn.

        :rtype:
          A transaction object
        """
        fields = {}
        if message:
            fields['message'] = message
        return self._post('/me/cards/' + card + '/transactions/' + transaction + '/commit', fields)

    def cancel_txn(self, card, transaction):
        """
        Cancels a transaction that has not yet been redeemed.

        :param String card_id The card ID from which to draw funds.

        :param String transaction Id of the transaction as returned by prepare_txn.

        :rtype:
          A transaction object
        """
        fields = {}
        return self._post('/me/cards/' + card + '/transactions/' + transaction + '/cancel', fields)

    def resend_txn(self, card, transaction):
        """
        Triggers a reminder for a transaction that hasn't been redeemed yet.

        :param String card_id The card ID from which to draw funds.

        :param String transaction Id of the transaction as returned by prepare_txn.

        :rtype:
          A transaction object
        """
        fields = {}
        return self._post('/me/cards/' + card + '/transactions/' + transaction + '/resend', fields)

    def get_ticker(self, t=''):
        """
        Returns current market rates used by the Uphold platform when conducting
        exchanges. These rates do not include the commission Uphold applies to
        exchanges.

        :param String ticker (optional) A specific currency to retrieve quotes for.

        :rtype:
          An array of market rates indexed by currency.
        """
        if t:
            uri = '/ticker/' + t
        else:
            uri = '/ticker'
        return self._get(uri)

    def get_vouchers(self):
        """
        Returns a list of all vouchers in one's account.

        :rtype:
          An array of vouchers
        """
        if not self.in_sandbox:
            raise NotSupportedInProduction()
        return self._get('/vouchers')

    def get_voucher(self, id):
        """
        Returns all the information associated with a single voucher.

        :param String id The ID of a specific voucher

        :rtype:
          A single voucher
        """
        if not self.in_sandbox:
            raise NotSupportedInProduction()
        return self._get('/vouchers/' + id)

    def redeem_voucher(self, id):
        """
        Redeems a voucher

        :param String id The ID of a specific voucher
        """
        if not self.in_sandbox:
            raise NotSupportedInProduction()
        return self._get('/vouchers/' + id + '/redeem')

    def revert_voucher(self, id):
        """
        Reverts or reverses a voucher that has been previously redeemed

        :param String id The ID of a specific voucher
        """
        if not self.in_sandbox:
            raise NotSupportedInProduction()
        return self._get('/vouchers/' + id + '/revert')

    """
    HELPER FUNCTIONS
    """
    def _build_url(self, uri):
        if uri.startswith('/oauth2'):
            return uri
        return '/v' + str(self.version) + uri

    def _update_rate_limit(self, headers):
        if 'X-RateLimit-Limit' in headers:
            self.limit     = headers['X-RateLimit-Limit']
            self.remaining = headers['X-RateLimit-Remaining']
            self.reset     = headers['X-RateLimit-Reset']
        else:
            self.limit = self.remaining = self.reset = ""
        
    def _post(self, uri, params):
        """
        """
        url = 'https://' + self.host + self._build_url(uri)

        try:
            if self.pat:
                self._debug("Using PAT")
                response = self.session.post(url, data=params, headers=self.headers, auth=(self.pat, 'X-OAuth-Basic'))
            elif self.username:
                self._debug("Using Basic Auth")
                self.session.auth = ( self.username, self.password )
                if self.otp:
                    self._debug("Using verification code: " + self.otp)
                    self.headers['X-Bitreserve-OTP'] = self.otp
                self._debug(self.headers)
                response = self.session.post(url, data=params, headers=self.headers)
            else:
                response = self.session.post(url, data=params, headers=self.headers)

            self._update_rate_limit( response.headers )

            if 'X-Bitreserve-OTP' in response.headers:
                self._debug("OTP Required!")
                raise VerificationRequired("OTP Required")
            elif response.status_code == 429:
                self._debug("Rate Limit Error!")
                raise RateLimitError(response.headers)

        except requests.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            self._debug("Failed certificate check: " + str(e))
            exit()

        data = json.loads(response.text)
        if 'X-Bitreserve-OTP' in self.headers:
            del self.headers['X-Bitreserve-OTP']
        return data

    def _get(self, uri):
        """
        """
        url = 'https://' + self.host + self._build_url(uri)

        # You're ready to make verified HTTPS requests.
        try:
            if self.pat:
                self._debug("Using PAT")
                response = self.session.get(url, headers=self.headers, auth=(self.pat, 'X-OAuth-Basic'))
            elif self.username:
                self._debug("Using Basic Auth")
                self.session.auth = ( self.username, self.password )
                if self.otp:
                    self._debug("Using verification code: " + self.otp)
                    self.headers['X-Bitreserve-OTP'] = self.otp
                self._debug(self.headers)
                response = self.session.get(url, headers=self.headers)
            else:
                response = self.session.get(url, headers=self.headers)

            self._update_rate_limit( response.headers )

            if 'X-Bitreserve-OTP' in response.headers:
                self._debug("OTP Required!")
                raise VerificationRequired("OTP Required")
            elif response.status_code == 429:
                self._debug("Rate Limit Error!")
                raise RateLimitError(response.headers)

        except requests.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            self._debug("Failed certificate check: " + str(e))
            exit()

        data = json.loads(response.text)
        if 'X-Bitreserve-OTP' in self.headers:
            del self.headers['X-Bitreserve-OTP']
        return data

