import requests
import json
from bs4 import BeautifulSoup

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)

def extract_days(beach_soup):
    """Extract the dates of the past week."""
    days = [a.text for a in beach_soup.find_all("h6", class_="nomargin pull-left heavy table-header-title")]
    return days


def extract_hours(beach_soup):
    """Extract the time of the measurements."""
    hours = [a. text for a in beach_soup.find_all("td",
                                                  class_="nopadding-left row-title background-clear msw-js-tooltip")][:8]
    return hours


def extract_weather(beach_soup):
    """Extract the weather of the past week."""
    weather = [a['title'] for a in beach_soup.find_all("td", attrs={"data-filter": "weather"})]
    return weather


def extract_temperature(beach_soup):
    """Extract the temperature of the past week (8 times a day)."""
    temperature = [a.text for a in beach_soup.find_all("h5", class_="nomargin font-sans-serif heavy")]
    return temperature


def extract_swell(beach_soup):
    """Extract swell height of the past week."""
    swell = [a.text for a in beach_soup.select('span[class*="font-sans-serif"]')]
    return swell


def extract_swell_rating(beach_soup):
    """Extract the rates of the swell (how mush surfable is the spot at this time) of the past week."""
    rating = [len(stars.findChildren("li", class_="active"))
              for stars in beach_soup.find_all("ul", class_="rating clearfix")]
    return rating


def extract_wind_steady_speed(beach_soup):
    """Extract the speed of the steady wind of the past week."""
    steady_speed = [a.text.strip() for a in beach_soup.find_all("span", class_="stacked-text text-right")]
    #  extract unity
    return steady_speed


def extract_wind_gust_speed(beach_soup):
    """Extract the speed of the gusting wind in KpH of the past week."""
    gust_speed = [a.text.strip() for a in beach_soup.find_all("span", class_="stacked-text-item")][::2]
    return gust_speed


def extract_wind_direction(beach_soup):
    """Extract the wind direction of the past week."""
    direction = [a for a in beach_soup.find_all("td",
                                                class_="text-center last msw-js-tooltip td-square background-warning")]
    return direction


def extract_name(beach_soup):
    """Extract the name of the surf spot"""
    return beach_soup.find("h1").text


def print_beach_info(beach_soup):
    """Print all the info that was extracted in the surf spot."""
    name = extract_name(beach_soup)
    days = extract_days(beach_soup)
    hours = extract_hours(beach_soup)
    weathers = extract_weather(beach_soup)
    temperature = extract_temperature(beach_soup)
    swell = extract_swell(beach_soup)
    steady_wind = extract_wind_steady_speed(beach_soup)
    gust_wind = extract_wind_gust_speed(beach_soup)
    direction_wind = extract_wind_direction(beach_soup)
    surfability = extract_swell_rating(beach_soup)
    print(f"--------------- {name} ------------------")
    for i, day in enumerate(days):
        print(day)
        print("Time Weather  | Temperature | Swell | Steady Wind Speed (KpH) | Gust Wind Speed (KpH) |  Surfability [0-5]")
        for j, hour in enumerate(hours):
            print(hour, weathers[i * CONFIG['DAYS_IN_WEEK'] + j],
                  temperature[i*CONFIG['DAYS_IN_WEEK']+j],
                  swell[i * CONFIG['DAYS_IN_WEEK'] + j],
                  steady_wind[i * CONFIG['DAYS_IN_WEEK'] + j],
                  gust_wind[i * CONFIG['DAYS_IN_WEEK'] + j],
                  surfability[i * CONFIG['DAYS_IN_WEEK'] + j])


if __name__ == "__main__":
    get_page = requests.get("https://magicseaweed.com/Sokolov-Beach-Surf-Report/4640/Historic/",
                            headers={"User_agent": "Mozilla/5.0"})
    beach_soup = BeautifulSoup(get_page.text, "html.parser")
    print_beach_info(beach_soup)
