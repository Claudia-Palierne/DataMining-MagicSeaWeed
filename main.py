import grequests
import requests
from bs4 import BeautifulSoup
import one_beach_scrapping
import selenium_scrapping
import bs4_scrapping

HOST = "https://magicseaweed.com"
WEBSITE_SURF_FORECAST = "https://magicseaweed.com/Israel-Surf-Forecast/90/"
FAKE_USER_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def extract_urls():
    """
    Extract the urls of every beach spot in the country.
    :return: list of urls
    """
    # Extract areas' urls
    surf_forecast_request = requests.get(WEBSITE_SURF_FORECAST, headers=FAKE_USER_HEADER)
    surf_forecast_soup = BeautifulSoup(surf_forecast_request.content, "html.parser")
    area_urls = [HOST + area_link.attrs['href'] for area_link in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top")]
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

