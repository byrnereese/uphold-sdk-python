from __future__ import print_function, unicode_literals

import urllib3
import getpass
import sys

sys.path.append('.')
from uphold import *

#input('You are about to generate a persistent Personal Access Token on Uphold. Press ENTER to continue. ')

un   = input("Uphold username: ").rstrip()
pw   = getpass.getpass("Uphold password: ").rstrip()
desc = input("Label/description for PAT (optional): ").rstrip()

api  = Uphold(True)
api.auth_basic( un, pw )

pat = None

try:
    print("Creating PAT...")
    pat = api.create_pat(desc)
except uphold.VerificationRequired as e:
    otp = input("Enter the verification code you got from Uphold: ")
    api.verification_code(otp)
    try:
        pat = api.create_pat(desc)
    except Exception as e2:
        print("Error again: " + repr(e2))
except Exception as e:
    print("An unexpected error occurred: " + repr(e))
    exit(0);

if pat is not None:
    print("Your PAT is: " + pat)
else:
    print("Failed to generate PAT")

exit(0)

