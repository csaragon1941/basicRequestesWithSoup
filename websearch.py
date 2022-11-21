# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
"""
This scropt is to show the main dactors of reuqrsts and how to use it with an HTML Parser
HTML Parser to use is BeutifulSoup:
"""

import argparse
import sys

import requests

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urlparse

# version number
version = 3.03

site = ""
query = ""


# function to use with dispatch table
def search_google(searchterms):
    '''
    :param seachterms: the term to search for
    :return: the fully built query string
    '''

    searchterms = "+".join(searchterms.split())
    url = f'https://www.google.com/search?q={searchterms}'
    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.findAll("a", href=True):
        if link.h3:
            follow = urlparse(link['href'][7:]).hostname
            if follow:
                return f"https://{follow}"
    return ""


def search_amazon(searchterms):
    '''
    :param seachterms: the term to search for
    :return: the fully built query string
    '''
    searchterms = "+".join(searchterms.split())
    url = f'https://www.amazon.com/s?k={searchterms}'
    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.findAll("a", href=True):
        if link.h3:
            follow = urlparse(link['href'][7:]).hostname
            if follow:
                return f"https://{follow}"
    return ""


def search_wiki(searchterms):
    '''
    :param seachterms: the term to search for
    :return: the fully built query string
    '''
    searchterms = "_".join(searchterms.split())
    url = f'https://en.wikipedia.org/wiki/{searchterms}_(disambiguation)'
    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.findAll("a", href=True):
        if link.h3:
            follow = urlparse(link['href'][7:]).hostname
            if follow:
                return f"https://{follow}"
    return ""


def search_books(searchterms):
    '''
    :param seachterms: the term to search for
    :return: the fully built query string
    '''

    searchterms = "+".join(searchterms.split())
    url = f'http://www.gutenberg.org/ebooks/search/?submit_search=Go%21&query={searchterms}'
    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.findAll("a", href=True):
        if link.h3:
            follow = urlparse(link['href'][7:]).hostname
            if follow:
                return f"http://{follow}"
    return ""


def follow_links(searchterms):
    for i in range(5):
        searchterms = "+".join(searchterms.split())
        url = f'http://www.gutenberg.org/ebooks/search/?submit_search=Go%21&query={searchterms}'
        soup = BeautifulSoup(get_response(url), 'html.parser')
        tags = soup('a')
        count = 0
        for tag in tags:
            count = count + 1


# mian sites to search with query strings
sites = {
    "google": search_google,
    "amazon": search_amazon,
    "wikipedia": search_wiki,
    "wiki": search_wiki,
    "gutenberg": search_books,
    "books": search_books
}


def init() -> str:
    sysargs = argparse.ArgumentParser(description="Loads passed url to file after intial cleaning (munging).")
    sysargs.add_argument("-v", "--version", action="version", version=f"Current version is {version}")
    sysargs.add_argument("-s", "--site", help="The sire to search(google, wikipedia, gutenberg, amazon)")
    sysargs.add_argument("-q", "--query", help="The term(s) to seach for. ")
    sysargs.add_argument("-l", "--link_depth", help=("The link depth is limited to the 5th term. Please select 1 to "
                                                     "follow the first link, 2 for the second link, etc..."))
    args = sysargs.parse_args()

    global site
    global query

    site = str(args.site).lower()

    try:
        if args.query:
            query = args.query
            follow_links()
            return sites.get(site)(query)(follow_links())
        else:
            print("You must provide both the site (-s, --site), query string (-q, --q), "
                  "and link depth (-l, and link_depth) to use this program.")
            quit(1)
    except (KeyError, TypeError) as ex:
        print("Acceptable sites to search for are Google, Wikipedia, Gutenberg, and Amazon.")
        quit(1)


def get_response(uri):
    # search get and return a response from the url provided
    # Add https to urls without protocol with layer

    try:
        response = requests.get(uri)
        response.raise_for_status()

    except HTTPError as httperr:
        print(f'HTTP error: {httperr}')
        sys.exit(1)

    except Exception as err:
        print(f"Something went really wrong!: {err}")
        sys.exit(1)

    return response.text


if __name__ == '__main__':

    url = init()
    if get_response(url):
        with open(f"{site}_{query}.txt", "w", encoding="utf-8") as f:
            f.write(get_response(url))
    else:
        print("First link was unallowable or no links found.")
