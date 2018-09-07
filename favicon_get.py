#!/usr/bin/env python3

import sys
import os
import requests
from pyquery import PyQuery as pq
import urllib.parse
import lxml.etree


favicon_dir = "favicons"

session = requests.Session()


def get_favicon(url, name=None):
    url = url if "://" in url else "http://" + url

    if name is None:
        name = urllib.parse.urlparse(url).netloc.split(".")[-2]

    print("url: " + url)
    print("name: " + name)

    r = session.get(url, timeout=10)
    d = pq(r.text)
    d.make_links_absolute(r.url)
    selection = d("link[rel~=icon]")

    if len(selection) == 1:
        el = selection[0]
        print("found 1 icon: " + element_to_string(el))

        icon_url = el.get("href")
        print("icon url: " + icon_url)

    elif len(selection) == 0:
        print("no icons found")
        u = urllib.parse.urlparse(url)

        icon_url = urllib.parse.urlunparse((u.scheme, u.netloc, "favicon.ico", "", "", ""))
        print("trying {}".format(icon_url))

    elif len(selection) > 1:
        print("found {} icons:".format(len(selection)))
        for i,el in enumerate(selection):
            print("\t{}. {}".format(i+1, element_to_string(el)))
        icon_num = int(input("icon number: "))

        icon_url = selection[icon_num - 1].get("href")
        name += "-{}".format(icon_num)

    ext = icon_url.split(".")[-1].split("?")[0]

    mkdir_if_not_exists(favicon_dir)

    r = session.get(icon_url, timeout=10)
    if r.ok:
        with open(os.path.join(favicon_dir, "{}.{}".format(name, ext)), "wb") as f:
            f.write(r.content)
    else:
        print(r.status_code, r.reason)


def element_to_string(el):
    return lxml.etree.tostring(el, encoding="unicode", with_tail=False)


def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def main():
    get_favicon(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)


if __name__ == "__main__":
    main()
