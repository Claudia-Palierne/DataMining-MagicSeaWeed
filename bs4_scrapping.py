import grequests
from bs4 import BeautifulSoup

FAKE_USER_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

RESPONSE_CODE_SUCCESS = 200
BATCH_SIZE = 5


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

    request_list = [grequests.get(url, headers=FAKE_USER_HEADER) for url in urls]
    responses_list = grequests.map(request_list, size=BATCH_SIZE)
    for response in responses_list:
        if response.status_code != RESPONSE_CODE_SUCCESS:
            response_index = responses_list.index(response)
            url = urls[response_index]
            # : logfile shit
            raise ConnectionError(f'Failed requesting url: {url}')

    # : Send a list of soup instead of list responses ?
    #  Maybe No cause sometimes we went different arguments to be sent to beautiful soup
    # Maybe yes cause we would like not have bs4 and grequests in main() script

    return responses_list