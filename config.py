import json
import re

import requests

from _compatibility import input
import BaseHTTPServer
PORT_NUMBER = 80 # Maybe set this to 9000.

DESC_CLIENT_ID = "What's your OAuth 2.0 client ID (read README.rst)?"
DESC_SECRET_ID = "What's your OAUTH 2.0 secrect?"
DESC_URL =       "Copy and Paste the URL below into browser address bar"\
                 "and hit enter:\n%s\nNow enter the OpenID code (in the " \
                 "address bar of your browser [code=?]:"
DESC_CONFIG = {
    'client_id':        DESC_CLIENT_ID,
    'client_secret':    DESC_SECRET_ID,
    'openid_code':      DESC_URL
}

REDIRECT_URI = 'http://localhost'
GOOGLE_ACCOUNT_URL = "https://accounts.google.com/o/oauth2/"

CONFIG_FILE = 'config.json'


def analyze(config):
    def check(key, arguments=()):
        if not key in config:
            print(DESC_CONFIG[key] % arguments)
            config[key] = input(key + ': ')

    check('client_id')
    check('client_secret')
    url =  GOOGLE_ACCOUNT_URL + "auth?%s&%s&%s&%s" % (
                  "client_id=%s" % config['client_id'],
                  "redirect_uri=%s:%s" % (REDIRECT_URI, PORT_NUMBER), 
                  "scope=https://www.googleapis.com/auth/fusiontables",
                  "response_type=code")

    check('openid_code', url)

    if not 'contacts' in config:
        config['contacts'] = []

    save_config(config)
    return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def get_config():
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except IOError:
        config = {}

    return analyze(config)


def get_token():
    """Retrieving access_token and refresh_token from Token API."""
    config = get_config()
    access_token_req = {
        "code":             config['openid_code'],
        "client_id":        config['client_id'],
        "client_secret":    config['client_secret'],
        "redirect_uri":     "%s:%s" % (REDIRECT_URI, PORT_NUMBER),
        "grant_type":       "authorization_code",
    }
    from urllib import urlencode
    content_length=len(urlencode(access_token_req))
    access_token_req['content-length'] = str(content_length)

    r = requests.post(GOOGLE_ACCOUNT_URL + "token", data=access_token_req)
    data = r.json()
    if r.status_code != 200:
        print data
        exit("Couldn't get token from google")
    print data
    return data["access_token"]


def add_contact(name, number):
    """Retrieving access_token and refresh_token from Token API."""
    if not name:
        exit('Need a valid name!')

    valid_number = r'^(\d{10}|\d{13}|\+\d{11})$'
    if not re.match(valid_number, number):
        exit('Need a valid phone number!')

    config = get_config()
    config['numbers'].append((name, number))
    save_config(config)
