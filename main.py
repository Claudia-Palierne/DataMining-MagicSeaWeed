import grequests
import requests
from bs4 import BeautifulSoup
import one_beach_scrapping
import selenium_scrapping
import bs4_scrapping
import json

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def extract_urls():
    """
    Extract the urls of every beach spot in the country.
    :return: list of urls
    """
    # Extract areas' urls
    surf_forecast_request = requests.get(CONFIG['WEBSITE_SURF_FORECAST'], headers=CONFIG['FAKE_USER_HEADER'])
    surf_forecast_soup = BeautifulSoup(surf_forecast_request.content, "html.parser")
    area_urls = [CONFIG['HOST'] + area_link.attrs['href'] for area_link in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top")]
    # Extract beaches' urls from all areas
    all_beaches_urls = []
    for url in area_urls:
        all_beaches_urls += selenium_scrapping.get_spot_beaches_urls(url)
    print(all_beaches_urls)
    return all_beaches_urls


def main():
    """
    Web scrapping of the site MagicSeaWeed.
    """
    beaches_url = extract_urls()
    beaches_soup = bs4_scrapping.list_urls_to_list_responses(beaches_url)
    for bs in beaches_soup:
        one_beach_scrapping.print_beach_info(bs)


if __name__ == "__main__":
    main()

