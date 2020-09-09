#!/usr/bin/env python3

import requests

def main():
    url = "https://my.manchester.ac.uk/uPortal/f/mylearning/normal/render.uP"

    res = requests.get(url)

    with open("res.html", mode="w") as f:
        f.write(str(res.text))

if __name__ == '__main__':
    main()
