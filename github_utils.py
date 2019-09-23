import os
import sys

import requests

from parse_link import parse_link_value


GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", None)
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", None)


def get(url):
    if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
        if (
            "client_id" not in url
        ):  # some of the URLs that github gives us already have it.
            url = f"{url}?client_id={GITHUB_CLIENT_ID}&client_secret={GITHUB_CLIENT_SECRET}"
    res = requests.get(url)
    if res.status_code >= 400:
        sys.stderr.write(f"Fetch error: {res.status_code} for {url}\n")
        raise IOError
        return
    remaining = res.headers.get("x-ratelimit-remaining", None)
    if remaining is not None:
        remaining = int(remaining)
        if remaining < 100:
            sys.stderr.write(f"WARNING: {remaining} requests left.\n")
    return res


def collapse_list(url, output=[]):
    try:
        res = get(url)
    except IOError:
        return output
    output += res.json()

    if "link" in res.headers:
        links = parse_link_value(res.headers["link"])
        rel_next = rel_last = None
        for link, params in links.items():
            rel = params.get("rel", None)
            if rel == "next":
                rel_next = link
            elif rel == "last":
                rel_last = link
        if rel_next:
            collapse_list(rel_next, output)
        elif rel_last:
            collapse_list(rel_last, output)
    return output
