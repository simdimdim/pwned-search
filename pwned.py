#!/usr/bin/env python
import hashlib
import getpass
import sys

try:
    import requests
except ModuleNotFoundError:
    print("###  pip install requests  ###")
    raise

def lookup_pwned_api():
    """Returns hash and number of times password was seen in pwned database.

    Args:
        pwd: password to check

    Returns:
        A (sha1, count) tuple where sha1 is SHA-1 hash of pwd and count is number
        of times the password was seen in the pwned database.  count equal zero
        indicates that password has not been found.

    Raises:
        RuntimeError: if there was an error trying to fetch data from pwned
            database.
        UnicodeError: if there was an error UTF_encoding the password.
    """
    passhash = hashlib.sha1(getpass.getpass().encode("utf-8")).hexdigest().upper()
    head, tail = hash[:5], hash[5:]
    url = 'https://api.pwnedpasswords.com/range/'+head
    res = requests.get(url)
    if not res.ok:
            raise RuntimeError('Failed to fetch "{}": "{}"'.format(url. res.status_code))
    hashes=(line.split(':') for line in res.text.splitlines())
    count=next((int(count) for t,count in hs if t==tail),0)
    return passhass, count

def main():
    ec = 0
    while 1:
        print("""q (and Enter) to quit, otherwise, 
        press Enter and enter your password""")
        user_input = input().strip()
        if user_input != 'q':
            try:
                sha1, count = lookup_pwned_api()
            if count:
                foundmsg = "{0} was found with {1} occurrences (hash: {2})"
                print(foundmsg.format(count, sha1))
                ec = 1
            else:
                print("{} was not found".format(sha1))
         else:
            break
    return ec

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
