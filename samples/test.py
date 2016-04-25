from __future__ import print_function, unicode_literals

import urllib3
import locale
try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser
import sys

sys.path.append('.')
from uphold import *

locale.setlocale(locale.LC_ALL, 'en_US')
Config = ConfigParser()
Config.read('samples/config.ini')

api = Uphold()
api.auth_pat( Config.get('Settings','pat') )

print("Getting user data...")
me = api.get_me()
print("First name: {}".format(me['firstName']))
print("Last name: {}".format(me['lastName']))

print("\nGetting cards...")
cards = api.get_cards()
for card in cards:
    print(card['label'] + ": " + card["available"] + " (" + card["id"] + ")")

card_id = cards[0]['id']

print("\nGetting card labeled '" + cards[0]['label'] + "'")
card = api.get_card( cards[0]['id'] )
print("Available balance: " + card['available'])

print("\nGetting contacts...")
contacts = api.get_contacts()
for contact in contacts:
    if contact and contact['firstName'] is not None and contact['lastName'] is not None: 
        print(contact['firstName'] + " " + contact['lastName'])

print("\nGetting phones...")
phones = api.get_phones()
for phone in phones:
    print(phone['internationalMasked'])

print("\nGetting personal access tokens...")
pats = api.get_pats()
print(pats)

print("\nGetting ledger (first 20 entries)...")
entries = api.get_reserve_ledger()
i = 0
for entry in entries:
    i += 1
    if i > 20:
        break
    if entry["in"]: 
        print(str(i) + ". " + entry['type'] + ": +" + entry["in"]["amount"] + " " + entry["in"]["currency"])
    if entry["out"]: 
        print(str(i) + ". " + entry['type'] + ": -" + entry["in"]["amount"] + " " + entry["in"]["currency"])

print("\nGetting transactions (first 20 entries)...")
entries = api.get_reserve_chain()
i = 0
for entry in entries:
    i += 1
    if i > 20:
        break
    print(str(i) + ". " + entry['origin']['amount'] + " " + entry["origin"]["currency"] + " => " + entry['destination']['amount'] + " " + entry["destination"]["currency"])

print("\nGetting all tickers...")
tic = api.get_ticker()
print("ok.")

exit(0)

