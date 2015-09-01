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

from __future__ import print_function, unicode_literals

import requests
import json
from .version import __version__


class Bitreserve(object):
    """
    Use this SDK to simplify interaction with the Bitreserve API
    """

    def __init__(self, host='api.bitreserve.org'):
        self.host = host
        self.version = 0
        self.session = requests.Session()
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'bitreserve-python-sdk/' + __version__
        }
        self.pat = None

    def auth(self, username, password):
        """
        Authenticates against the Bitreserve backend using a username and password. Bitreserve
        return an User Auth Token, which is persisted for the life of the session.

        :param String username A Bitreserve username or email address.

        :param String password The password corresponding to the specified username.

        :rtype:
          The user authentication token string.
        """

        params = {
            'client_id': 'BITRESERVE',
            'client_secret': 'secret',
            'grant_type': 'password',
            'username': username,
            'password': password
        }

        data = self._post('/oauth2/token', params)
        self.token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')
        self.headers['Authorization'] = 'Bearer ' + self.token
        return data

    def auth_pat(self, pat):
        self.pat = pat

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
        return self._get('/reserve')

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
          address, an email address, or a Bitreserve membername.

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
        Returns current market rates used by the Bitreserve platform when conducting
        exchanges. These rates do not include the commission Bitreserve applies to
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

    """
    HELPER FUNCTIONS
    """

    def _build_url(self, uri):
        if uri.startswith('/oauth2'):
            return uri
        return '/v' + str(self.version) + uri

    def _post(self, uri, params):
        """
        """
        url = 'https://' + self.host + self._build_url(uri)

        # You're ready to make verified HTTPS requests.
        try:
            if self.pat:
                response = self.session.post(url, data=params, headers=self.headers, auth=(self.pat, 'X-OAuth-Basic'))
            else:
                response = self.session.post(url, data=params, headers=self.headers)
        except requests.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            print("Failed certificate check")

        data = json.loads(response.text)
        return data

    def _get(self, uri):
        """
        """
        url = 'https://' + self.host + self._build_url(uri)

        # You're ready to make verified HTTPS requests.
        try:
            if self.pat:
                response = self.session.get(url, headers=self.headers, auth=(self.pat, 'X-OAuth-Basic'))
            else:
                response = self.session.get(url, headers=self.headers)
        except requests.exceptions.SSLError:
            # Handle incorrect certificate error.
            print("Failed certificate check")

        data = json.loads(response.text)
        return data
