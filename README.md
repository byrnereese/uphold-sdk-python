# Bitreserve Python SDK

Welcome to the Bitreserve SDK for Python developers. Using this library, developers can more easily 
get started using the [Bitreserve API](https://developer.bitreserve.org/api/v0/). 

## Getting Started

To begin, visit the [Bitreserve website](http://bitreserve.org/) and create an account. With a 
username and password in hand, you can begin building apps against the Bitreserve API immediately. 

## Authentication

There are three ways to authenticate against the API:

* **OAuth** is the perfect solution for when your app needs to request permission to access a user's
Bitreserve account. 

* A **Personal Access Token ("PAT")** is ideal when you need to generate a token to access your own Bitreserve
account. 

* Basic authentication (username and password) can sometimes be the easiest way to get started, but is not always the best choice from a security perspective. 

You can find out more about these two methods in our [API documentation](https://developer.bitreserve.org/api/v0/#authentication). 

### Basic Auth Example

    from bitreserve import Bitreserve
    api = Bitreserve()
    api.auth( <username>, <password> )
    me = api.get_me()

### Personal Access Token Example

    from bitreserve import Bitreserve
    api = Bitreserve()
    api.auth_pat( <PAT> )
    me = api.get_me()

## Interacting with the Bitreserve Sandbox

The [Bitreserve Sandbox](https://developer.bitreserve.org/en/sandbox) is a test environment for developers to build and test their apps. The Sandbox environment uses fake money, but is otherwise an exact copy of our production system. 

    from bitreserve import Bitreserve
    api = Bitreserve(host='api-sandbox.bitreserve.org')

## Conducting a Transaction

Transactions are conducted in two steps. First you prepare a transaction. This retrieves a quote for the transaction which will be honored for 30 seconds. This is a perfect way of generating a transaction preview for your user if you need to. Second is to execute a prepared transaction. 

## Example: Sending a Transaction

Below is an example of how one would send 1 BTC to someone using Bitreserve:

    card_id = 'adc869d8-xxxx-xxxx-xxxx-72718f0a2be0'
    from bitreserve import Bitreserve
    api = Bitreserve()
    api.auth(<username>, <password>)
    txn_id = api.prepare_txn(card_id, 'luke@skywalker.net', 1, 'BTC')
    api.execute_txn(card_id, txn_id)

A couple of notes about the sample above:

* A card ID is required to identify from which store of value you will be sending value from.

* One may specify sending any amount in any denomination. If an exchange is implied, Bitreserve
  will handle the exchange for you automatically.

* When sending money via Bitreserve, you can specify a recipient in the form of a bitcoin address,
  an email address, or a Bitreserve member name.

* One may send money to a bitcoin address, an email address, a Bitreserve username, 
  or a phone number. 

*For a complete reference to the Bitreserve API, including examples in Python, please consult 
the [Bitreserve API documentation](http://developers.bitreserve.org/).*

## Resources

* [Bitreserve Home](http://bitreserve.org/)
* [Bitreserve Developer Site](http://developer.bitreserve.org/)
* [Bitreserve Help Center](http://support.bitreserve.org/)      

### Example Apps in Python

* [MoneyBot](https://github.com/jneves/moneybot) - a script that will distribute value across your cards based upon certain weightings. 

## License

This software is licensed under the MIT License. 
