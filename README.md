# Uphold Python SDK

Welcome to the Uphold SDK for Python developers. Using this library, developers can more easily 
get started using the [Uphold API](https://developer.uphold.com/api/v0/). 

## Getting Started

To begin, visit the [Uphold website](http://uphold.com/) and create an account. With a 
username and password in hand, you can begin building apps against the Uphold API immediately. 

## Authentication

There are three ways to authenticate against the API:

* **OAuth** is the perfect solution for when your app needs to request permission to access a user's
Uphold account. 

* A **Personal Access Token ("PAT")** is ideal when you need to generate a token to access your own Uphold
account. 

* Basic authentication (username and password) can sometimes be the easiest way to get started, but is not always the best choice from a security perspective. 

You can find out more about these two methods in our [API documentation](https://developer.uphold.com/api/v0/#authentication). 

### Basic Auth Example

    from uphold import Uphold
    api = Uphold()
    api.auth( <username>, <password> )
    me = api.get_me()

### Personal Access Token Example

    from uphold import Uphold
    api = Uphold()
    api.auth_pat( <PAT> )
    me = api.get_me()

## Interacting with the Uphold Sandbox

The [Uphold Sandbox](https://developer.uphold.com/en/sandbox) is a test environment for developers to build and test their apps. The Sandbox environment uses fake money, but is otherwise an exact copy of our production system. 

    from uphold import Uphold
    api = Uphold(host='api-sandbox.uphold.com')

## Conducting a Transaction

Transactions are conducted in two steps. First you prepare a transaction. This retrieves a quote for the transaction which will be honored for 30 seconds. This is a perfect way of generating a transaction preview for your user if you need to. Second is to execute a prepared transaction. 

## Example: Sending a Transaction

Below is an example of how one would send 1 BTC to someone using Uphold:

    card_id = 'adc869d8-xxxx-xxxx-xxxx-72718f0a2be0'
    from uphold import Uphold
    api = Uphold()
    api.auth(<username>, <password>)
    txn_id = api.prepare_txn(card_id, 'luke@skywalker.net', 1, 'BTC')
    api.execute_txn(card_id, txn_id)

A couple of notes about the sample above:

* A card ID is required to identify from which store of value you will be sending value from.

* One may specify sending any amount in any denomination. If an exchange is implied, Uphold
  will handle the exchange for you automatically.

* When sending money via Uphold, you can specify a recipient in the form of a bitcoin address,
  an email address, or a Uphold member name.

* One may send money to a bitcoin address, an email address, a Uphold username, 
  or a phone number. 

*For a complete reference to the Uphold API, including examples in Python, please consult 
the [Uphold API documentation](http://developer.uphold.com/).*

## Resources

* [Uphold Home](http://uphold.com/)
* [Uphold Developer Site](http://developer.uphold.com/)
* [Uphold Help Center](http://support.uphold.com/)      

### Example Apps in Python

* [MoneyBot](https://github.com/jneves/moneybot) - a script that will distribute value across your cards based upon certain weightings. 

## License

This software is licensed under the MIT License. 
