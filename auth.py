#!/usr/bin/env python3

import requests
import re


def load_credentials():
    creds = []
    with open("auth", mode="r") as f:
        creds = f.readline().strip().split(",")

    form_data = {
        "username": creds[0],
        "password": creds[1],
        "_eventId": "submit",
        "submit": "Login",
    }

    return form_data


def manc_session():

    s = requests.Session()
    site = "https://my.manchester.ac.uk"

    login_url = "https://login.manchester.ac.uk/cas/login?service=https://my.manchester.ac.uk/uPortal/Login"

    r = s.get(login_url)

    form_data = load_credentials()

    form_data["lt"] = re.search('name="lt" value="(.+)"', r.text).group(1)
    form_data["execution"] = re.search('name="execution" value="(.+)"', r.text).group(1)

    r = s.post(r.url, data=form_data)

    return s


if __name__ == "__main__":
    manc_session()
