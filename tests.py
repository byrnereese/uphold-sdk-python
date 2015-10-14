# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from unittest import TestCase, main, skip
from mock import Mock, patch
from decimal import Decimal

from uphold import Uphold


class FakeResponse(object):
    status = 200
    text = ''


class TestAuthentication(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestCurrencies(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestTicker(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestCard(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestContact(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestCurrencyPair(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


fake_transaction_response = FakeResponse()
fake_transaction_response.text = '''{
  "id": "7c377eba-cb1e-45a2-8c13-9807b4139bec",
  "type": "transfer",
  "message": null,
  "status": "pending",
  "RefundedById":null,
  "createdAt": "2014-08-27T00:01:11.616Z",
  "denomination": {
    "amount": "0.1",
    "currency": "BTC",
    "pair": "BTCBTC",
    "rate": "1.00"
  },
  "origin": {
    "CardId": "66cf2c86-8247-4094-bbec-ca29cea8220f",
    "amount": "0.1",
    "base": "0.1",
    "commission": "0.00",
    "currency": "BTC",
    "description": "John Doe",
    "fee": "0.00",
    "rate": "1.00",
    "type": "card",
    "username": "johndoe"
  },
  "destination": {
    "amount": "0.1",
    "base": "0.1",
    "commission": "0.00",
    "currency": "BTC",
    "description": "foo@bar.com",
    "fee": "0.00",
    "rate": "1.00",
    "type": "email"
  },
  "params": {
    "currency": "BTC",
    "margin": "0.00",
    "pair": "BTCBTC",
    "rate": "1.00",
    "ttl": 30000,
    "type": "invite"
  }
}'''

    
class TestTransaction(TestCase):
    def setUp(self):
        self.api = Bitreserve()
        #self.api.auth('user', 'password')

    @patch('requests.Session.post', Mock(return_value=fake_transaction_response))
    def test_prepare_txn(self):
        res = self.api.prepare_txn(
            '66cf2c86-8247-4094-bbec-ca29cea8220f',
            'foo@bar.com',
            Decimal('1.00'),
            'BTC'
        )
        self.assertEqual(res, '7c377eba-cb1e-45a2-8c13-9807b4139bec')

    @patch('requests.Session.post', Mock(return_value=fake_transaction_response))
    def test_execute_txn(self):
        res = self.api.execute_txn(
            '66cf2c86-8247-4094-bbec-ca29cea8220f',
            '7c377eba-cb1e-45a2-8c13-9807b4139bec',
        )
        self.assertEqual(res['id'], '7c377eba-cb1e-45a2-8c13-9807b4139bec')

        
class TestUser(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


if __name__ == '__main__':
    main()
