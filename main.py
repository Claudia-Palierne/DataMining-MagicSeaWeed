# : ne pas enlever grequests, tout plante sinon car on utilise response.content
import grequests
from bs4 import BeautifulSoup
import selenium_scrapping

import bs4_scrapping

WEBSITE_URL = "https://magicseaweed.com"
WEBSITE_SURF_FORECAST = "https://magicseaweed.com/Israel-Surf-Forecast/90/"

SINGLE_RESPONSE = 0

# MEs noms de modules sont très bien

def main():

    surf_forecast_page_response = bs4_scrapping.list_urls_to_list_responses(WEBSITE_SURF_FORECAST)
    surf_forecast_soup = BeautifulSoup(surf_forecast_page_response[SINGLE_RESPONSE].content, "html.parser")

    surf_spots_url_list = []
    for tag in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top"):
        surf_spots_url_list.append(WEBSITE_URL + tag.attrs['href'])

    all_beaches_urls = []
    for url in surf_spots_url_list:
        all_beaches_urls += selenium_scrapping.get_spot_beaches_urls(url)

    print(all_beaches_urls)


if __name__ == "__main__":
    main()

