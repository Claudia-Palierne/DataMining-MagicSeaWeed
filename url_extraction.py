from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json


import grequests
import requests
from bs4 import BeautifulSoup

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def get_spot_beaches_urls(url):
    """
    Extract the urls of every spot from the area's url.
    :param url: a string of the area's url
    :return: list of every beach spot in the area.
    """
    beaches_urls = []

    # this returns the path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)

    # start by defining the options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # it's more scalable to work in headless mode
    options.page_load_strategy = 'none'

    # initialize web driver
    with webdriver.Chrome(options=options, service=chrome_service) as driver:
        # navigate to the url
        driver.get(url)
        driver.implicitly_wait(CONFIG['WAIT_TIME_SECOND'])

        # find elements by tag name 'a' and class =
        elements = driver.find_elements(By.CSS_SELECTOR, f"a[class='clearfix spot-list-link spot-list-link-forecast "
                                                         f"padding-sm nopadding-left nopadding-right']")

        # fills the beaches_urls list to return
        for element in elements:
            beaches_urls.append(element.get_attribute('href') + CONFIG['ARCHIVE'])

        return beaches_urls


def extract_areas_urls(country_forecast_urls):
    """
    Extract the urls of every beach spot in the country.
    :return: list of urls string
    """
    # Extract areas' urls
    surf_forecast_request = requests.get(country_forecast_urls, headers=CONFIG['FAKE_USER_HEADER'])
    surf_forecast_soup = BeautifulSoup(surf_forecast_request.content, "html.parser")
    area_urls = [CONFIG['HOST'] + area_link.attrs['href']
                 for area_link in surf_forecast_soup.find_all('a', class_="list-group-item h6 nomargin-top")]
    return area_urls


def extract_beaches_urls(area_urls):
    """
    # Extract beaches' urls from all areas
    :param area_urls: a list with the areas urls
    :return: a list with the urls of that beach's area
    """
    all_beaches_urls = []
    for url in area_urls:
        all_beaches_urls += get_spot_beaches_urls(url)
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
