import grequests
from bs4 import BeautifulSoup
import json

RESPONSE_CODE_SUCCESS = 200

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def list_urls_to_list_responses(urls):
    """
    Given a list of URLs or a single URL, send GET requests to each URL using grequests and return the responses.

    :param urls: A single string or a list of strings representing the URLs to fetch
    :return: A single grequests.Response objects or a list of grequests.Response objects
            representing the responses for each URL
    """
    # When urls is a single string rather than a list
    if not isinstance(urls, list):
        urls = [urls]

    request_list = (grequests.get(url, headers=CONFIG['FAKE_USER_HEADER']) for url in urls)
    request_soup = []
    for response in grequests.imap(request_list, size=CONFIG['BATCH_SIZE']):
        if response.status_code != RESPONSE_CODE_SUCCESS:
            raise ConnectionError(f'Failed requesting url: {urls}')
        else:
            request_soup += [BeautifulSoup(response.content, "html.parser")]
    return request_soup
