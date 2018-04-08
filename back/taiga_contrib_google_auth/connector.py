# Copyright (C) 2018 Don Bowman <db@donbowman.ca>
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See 
# https://developers.google.com/oauthplayground/

import requests

import logging
#from http.client import HTTPConnection
#HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#req_log = logging.getLogger('requests.packages.urllib3')
#req_log.setLevel(logging.DEBUG)
#req_log.propagate = True

import json
import jwt

from collections import namedtuple
from urllib.parse import urljoin
from urllib.parse import quote_plus

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taiga.base.connectors.exceptions import ConnectorBaseException


class GoogleApiError(ConnectorBaseException):
    pass


######################################################
## Data
######################################################

CLIENT_ID = getattr(settings, "GOOGLE_API_CLIENT_ID", None)
CLIENT_SECRET = getattr(settings, "GOOGLE_API_CLIENT_SECRET", None)

REDIRECT_URI = getattr(settings, "GOOGLE_API_REDIRECT_URI", None)

URL = getattr(settings, "GOOGLE_API_URL",  "https://www.googleapis.com/")
API_RESOURCES_URLS = {
    "login": {
        "access-token": "oauth2/v4/token"
    },
}

HEADERS = {"Accept": "application/json",
           "user-agent": "taiga-google-auth",
          }

AuthInfo = namedtuple("AuthInfo", ["access_token"])
User = namedtuple("User", ["id", "username", "full_name", "email", "bio"])
Email = namedtuple("Email", ["email", "is_primary"])



######################################################
## utils
######################################################

def _build_url(*args, **kwargs) -> str:
    """
    Return a valid url.
    """
    resource_url = API_RESOURCES_URLS
    for key in args:
        resource_url = resource_url[key]

    if kwargs:
        resource_url = resource_url.format(**kwargs)

    return urljoin(URL, resource_url)


def _get(url:str, headers:dict) -> dict:
    """
    Make a GET call.
    """
    response = requests.get(url, headers=headers)

    data = response.json()
    if response.status_code != 200:
        raise GoogleApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


def _post(url:str, data:dict, headers:dict) -> dict:
    """
    Make a POST call.
    """
    response = requests.post(url, data=data, headers=headers)

    data = response.json()
    if response.status_code != 200 or "error" in data:
        raise GoogleApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


######################################################
## Simple calls
######################################################

def login(access_code:str, client_id:str=CLIENT_ID, client_secret:str=CLIENT_SECRET,
          headers:dict=HEADERS, redirect_uri:str=REDIRECT_URI):
    """
    Get access_token fron an user authorized code, the client id and the client secret key.
    (See https://developer.google.com/v4/oauth/#web-application-flow).
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise GoogleApiError({"error_message": _("Login with google account is disabled.")})

    url = _build_url("login", "access-token")
    # code=4%2FAACKrKggdEuKriXuoE8KjT7nVedo30lPEjThowNpS1Sff3jFOxnLOIeqVwb2xtLKjaHHsdmbBBfLu_YpJUVyAYo&redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&client_id=407408718192.apps.googleusercontent.com&client_secret=************&scope=&grant_type=authorization_code

    params={"code": access_code,
            "client_secret": client_secret,
            "scope": "openid email profile",
            "grant_type": "authorization_code",
            "redirect_uri": "https://kanban.donbowman.ca/login", #redirect_uri,
            "client_id": client_id,
            }
    data = _post(url, data=params, headers=headers)
    return data.get("id_token", None)

def get_user_profile(token):
    """
    Take a JWT token and get the user info
    """

    data = _get(url, headers=headers)
    return User(id=data.get("id", None),
                username=data.get("name", None).get("givenName", None) + data.get("name", None).get("familyName", None),
                full_name=(data.get("displayName", None) or ""),
                email=(data.get("emails", None)[0].get("value", None) or ""),
                bio=(data.get("bio", None) or ""))


def get_user_emails(headers:dict=HEADERS) -> list:
    """
    Get a list with all emails of the authenticated user.
    (See https://developer.google.com/v3/users/emails/#list-email-addresses-for-a-user).
    """
    url = _build_url("user", "emails")
    data = _get(url, headers=headers)
    return [Email(email=e.get("email", None), is_primary=e.get("primary", False))
                    for e in data]



######################################################
## Convined calls
######################################################

def me(access_code:str) -> tuple:
    """
    Connect to a google account and get all personal info (profile and the primary email).
    """
    idt = login(access_code)

    profile = jwt.decode(idt, verify=False)

    return User(id=profile['email'].split("@")[0],username=profile['email'].split("@")[0],full_name= "",email=profile['email'],bio= "")


