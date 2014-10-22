# Bitreserve Python SDK

Welcome to the Bitreserve SDK for Python developers. Using this library, developers can more easily 
get started using the [Bitreserve API](http://developers.bitreserve.org/api/v1/). 

## Getting Started

To begin, visit the [Bitreserve website](http://bitreserve.org/) and create an account. With a 
username and password in hand, you can begin building apps against the Bitreserve API immediately. 

## Authentication

Bitreserve utilizes OAuth2 for authentication. Right now, Bitreserve requires passing a username 
and password via the API to obtain a User Authentication Token (UAT). The python SDK eliminates much
of the need to worry about such details though. Here is an example of how to authenticate using 
the Python SDK:

    from bitreserve import Bitreserve
    api = Bitreserve()
    api.auth( <username>, <password> )
    me = api.get_me()

*In the future, Bitreserve will support additional means of authentication that do not require the 
direct use of a username and password hard coded in software or config files.*

## Example: Sending a Transaction

Below is an example of how one would send 1 BTC to someone using Bitreserve:

    card_id = 'adc869d8-xxxx-xxxx-xxxx-72718f0a2be0'
    from bitreserve import Bitreserve
    api = Bitreserve()
    api.auth( <username>, <password> )
    promise = api.prepare_txn( card_id, 'luke@skywalker.net', 1, 'BTC' )
    api.execute_txn( card_id, 'luke@skywalker.net', 1, 'BTC', promise )

A couple of notes about the sample above:

* A card ID is required to identify from which store of value you will be sending value from.

* One may specify sending any amount in any denomination. If an exchange is implied, Bitreserve
  will handle the exchange for you automatically.

* When sending money via Bitreserve, you can specify a recipient in the form of a bitcoin address,
  an email address, or a Bitreserve member name.

* Obtaining a "promise" is helpful when a transaction involves an exchange of value from one form
  or another. This promise secures a quote for the transaction which Bitreserve will honor for 30
  seconds. Obtaining a promise is *not* required.

*For a complete reference to the Bitreserve API, including examples in Python, please consult 
the [Bitreserve API documentation](http://developers.bitreserve.org/).*

## Resources

* [Bitreserve Home](http://bitreserve.org/)
* [Bitreserve API Documentation](http://developers.bitreserve.org/)
* [Bitreserve Help Center](http://support.bitreserve.org/)      

## About Bitreserve

Bitreserve makes using digital money fast, easy and free.

Bitreserve shields its members from bitcoin volatility by enabling them to hold bitcoin as stable, 
real-world currency. Bitreserve keeps your value safe while letting you spend it as bitcoin and send 
it to anyone in the world instantly and for free.

Transfer your bitcoin to U.S. dollars, euros, pounds, yen and yuan with no delays — we offer instant, 
low-cost currency conversions. And we maintain a full reserve of real-world currencies and publish a 
real-time, verifiable proof of solvency, so you always know your value is safe.

## License

This software is licensed under the MIT License. 
