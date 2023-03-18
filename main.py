# : ne pas enlever grequests, tout plante sinon car on utilise response.content
import grequests
import requests
from bs4 import BeautifulSoup

import one_beach_scrapping
import selenium_scrapping

import bs4_scrapping

HOST = "https://magicseaweed.com"
WEBSITE_SURF_FORECAST = "https://magicseaweed.com/Israel-Surf-Forecast/90/"
SINGLE_RESPONSE = 0

FAKE_USER_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def extract_urls():
    #Point de depart
    # surf_forecast_page_response = bs4_scrapping.list_urls_to_list_responses(WEBSITE_SURF_FORECAST)
    # surf_forecast_soup = BeautifulSoup(surf_forecast_page_response[SINGLE_RESPONSE].content, "html.parser")
    #Prend les regions
    surf_spots_url_list = []
    # for tag in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top"):
    #     surf_spots_url_list.append(HOST + tag.attrs['href'])


    surf_forecast_request = requests.get(WEBSITE_SURF_FORECAST, headers=FAKE_USER_HEADER)
    surf_forecast_soup = BeautifulSoup(surf_forecast_request.content, "html.parser")
    for tag in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top"):
        surf_spots_url_list.append(HOST + tag.attrs['href'])  #ajouter historic


    # #Prend les plages
    all_beaches_urls = []
    for url in surf_spots_url_list:
        all_beaches_urls += selenium_scrapping.get_spot_beaches_urls(url)
    return all_beaches_urls


def main():
    beaches_url = extract_urls()
    beaches_soup = bs4_scrapping.list_urls_to_list_responses(beaches_url)
    for bs in beaches_soup:
        # Ajouter le nom des plages
        # List index out of range
        one_beach_scrapping.print_beach_info(bs)


if __name__ == "__main__":
    main()

