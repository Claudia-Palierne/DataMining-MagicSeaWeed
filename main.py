import argparse

import grequests
import requests
from bs4 import BeautifulSoup
import one_beach_scrapping
import selenium_scrapping
import json

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def extract_urls(country_forecast_urls):
    """
    Extract the urls of every beach spot in the country.
    :return: list of urls string
    """
    # Extract areas' urls
    surf_forecast_request = requests.get(country_forecast_urls, headers=CONFIG['FAKE_USER_HEADER'])
    surf_forecast_soup = BeautifulSoup(surf_forecast_request.content, "html.parser")
    area_urls = [CONFIG['HOST'] + area_link.attrs['href']
                 for area_link in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top")]
    # Extract beaches' urls from all areas
    all_beaches_urls = []
    for url in area_urls:
        all_beaches_urls += selenium_scrapping.get_spot_beaches_urls(url)
    print(all_beaches_urls)
    return all_beaches_urls


def get_soup(urls):
    """
    Given a list of URLs, send GET requests to each URL using grequests and return beautifulSoup objects.
    :param urls: list of strings representing the URLs.
    :return: a list of BeautifulSoup object for each url.
    """
    request_list = (grequests.get(url, headers=CONFIG['FAKE_USER_HEADER']) for url in urls)
    request_soup = []
    for response in grequests.imap(request_list, size=CONFIG['BATCH_SIZE']):
        if response.status_code != CONFIG['RESPONSE_CODE_SUCCESS']:
            raise ConnectionError(f'Failed requesting url: {urls}')
        else:
            request_soup += [BeautifulSoup(response.content, "html.parser")]
    return request_soup


def main():
    """
    Web scrapping of the site MagicSeaWeed.
    :return: None
    """

    parser = argparse.ArgumentParser()
    # Gets the country input by user
    parser.add_argument("-country", type=str, choices=['ALL', 'ISRAEL', 'FRANCE', 'HAWAII'],
                        default='ISRAEL',
                        help="choose a country from the list to scrap")

    # Get the execution mode
    parser.add_argument("-mode", type=str, choices=['print', 'database'],
                        default='print',
                        help="choose a mode of execution :"
                             "print will print the information in the std output"
                             "whereas database will store it in the db")

    # Using parser to further use the arguments
    args = parser.parse_args()
    country_to_scrap = args.country
    execution_mode = args.mode

    beaches_url = []
    if country_to_scrap == 'ALL':
        for country in ['ISRAEL', 'FRANCE', 'HAWAII']:
            country_forecast_urls = CONFIG["SURF_FORECAST"].get(country)
            beaches_url += extract_urls(country_forecast_urls)
    else:
        country_forecast_urls = CONFIG["SURF_FORECAST"].get(country_to_scrap)
        beaches_url = extract_urls(country_forecast_urls)

    if execution_mode == 'print':
        # Previous code :
        beaches_soup = get_soup(beaches_url)
        for bs in beaches_soup:
            one_beach_scrapping.print_beach_info(bs)
    else:
        print('Fill database')


if __name__ == "__main__":

    main()