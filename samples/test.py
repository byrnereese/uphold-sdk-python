from __future__ import print_function, unicode_literals

import urllib3
import locale
try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser
import sys

sys.path.append('.')
from uphold import Uphold

locale.setlocale(locale.LC_ALL, 'en_US')
Config = ConfigParser()
Config.read('samples/config.ini')

api = Uphold()
api.auth( Config.get('Settings','username'), Config.get('Settings','password') )
print("Getting user data...")
me = api.get_me()
print("First name: {}".format(me['firstName']))
print("Last name: {}".format(me['lastName']))

print("\nGetting cards...")
cards = api.get_cards()
for card in cards:
    print(card['label'] + ": " + card["available"] + " (" + card["id"] + ")")

print("\nGetting USD Card...")
usd_card = api.get_card("20c0ccf3-e316-40c1-8a2a-982dd92a96ca")
print(usd_card['label'])

print("\nGetting contacts...")
contacts = api.get_contacts()
for contact in contacts:
    print(contact['firstName'] + " " + contact["lastName"])

'''
print "\nGetting addresses..."
addresses = api.get_addresses()
for addr in addresses:
    print addr
'''

print("\nGetting phones...")
phones = api.get_phones()
for phone in phones:
    print(phone['internationalMasked'])

print("\nGetting reserve status...")
stats = api.get_reserve_status()
for stat in stats:
    cur = stat["currency"]
    for norm in stat["normalized"]:
        if norm["currency"] == "USD":
            break
    if cur == "USD":
        print(cur + ": liabilities=" + locale.currency( float(stat["liabilities"]), grouping=True ) + ", assets=" + locale.currency( float(stat["assets"]), grouping=True ))
    else:
        print(cur + ": liabilities=" + stat["liabilities"] + " (" + locale.currency( float(norm["liabilities"]), grouping=True ) + "), assets=" + stat["assets"] + " (" + locale.currency( float(norm["assets"]), grouping=True ) + ")")

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

tic = api.get_ticker('USD')
print("EUR => USD: " + tic['EURUSD']['bid'])

exit(0)

