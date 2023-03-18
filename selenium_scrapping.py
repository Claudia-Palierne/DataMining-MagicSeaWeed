from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

TAG_NAME = 'a'
CLASS_NAME = r'clearfix spot-list-link spot-list-link-forecast padding-sm nopadding-left nopadding-right'


def get_spot_beaches_urls(url):
    """
    Extract the urls of every spot from the area's url.
    :param url: area url
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
        driver.implicitly_wait(5)

        # find elements by tag name 'a' and class =
        elements = driver.find_elements(By.CSS_SELECTOR, f"{TAG_NAME}[class='{CLASS_NAME}']")

        # fills the beaches_urls list to return
        for element in elements:
            beaches_urls.append(element.get_attribute('href'))

        return beaches_urls


if __name__ == "__main__":
    url = "https://magicseaweed.com/Central-Tel-Aviv-Surfing/113/"
    beaches = get_spot_beaches_urls(url)
    print(beaches)
