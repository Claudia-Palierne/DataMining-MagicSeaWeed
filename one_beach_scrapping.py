import requests
from bs4 import BeautifulSoup


def extract_days(beach_soup):
    days = [a.text for a in beach_soup.find_all("h6", class_="nomargin pull-left heavy table-header-title")]
    return days


def extract_hours(beach_soup):
    hours = [a. text for a in beach_soup.find_all("td", class_="nopadding-left row-title background-clear msw-js-tooltip")][:8]
    return hours


def extract_weather(beach_soup):
    weather = [a['title'] for a in beach_soup.find_all("td", attrs={"data-filter": "weather"})]
    return weather


def extract_temperature(beach_soup):
    temperature = [a.text for a in beach_soup.find_all("h5", class_="nomargin font-sans-serif heavy")]
    return temperature


def extract_swell(beach_soup):
    swell = [a.text for a in beach_soup.find_all("span", class_="h3 font-sans-serif heavy nomargin text-white")]
    return swell


def extract_swell_rating(beach_soup):
    rating = [len(stars.findChildren("li", class_="active")) for stars in beach_soup.find_all("ul", class_="rating clearfix")]
    return rating


def extract_wind_steady_speed(beach_soup):
    steady_speed = [a.text for a in beach_soup.find_all("span", class_="stacked-text text-right")]
    #  extract unity
    return steady_speed


def extract_wind_gust_speed(beach_soup):
    gust_speed = [a.text for a in beach_soup.find_all("span", class_="stacked-text-item")][::2]
    return gust_speed


def extract_wind_direction(beach_soup):
    direction = [a['title'] for a in beach_soup.find_all("td", class_="text-center last msw-js-tooltip td-square background-warning")]
    return direction


def print_beach_info(beach_soup):
    # get_page = requests.get("https://magicseaweed.com/Hilton-Surf-Report/3658/Historic/",
    #                         headers={"User-agent": "Mozilla/5.0"})
    # beach_soup = BeautifulSoup(get_page.text, "html.parser")
    days = extract_days(beach_soup)
    hours = extract_hours(beach_soup)
    weathers = extract_weather(beach_soup)
    temperature = extract_temperature(beach_soup)
    swell = extract_swell(beach_soup)
    steady_wind = extract_wind_steady_speed(beach_soup)
    gust_wind = extract_wind_gust_speed(beach_soup)
    direction_wind = extract_wind_direction(beach_soup)
    surfability = extract_swell_rating(beach_soup)
    for i, day in enumerate(days):
        print(day)
        print("| Time | Weather  | Temperature | Swell | Steady Wind Speed (KpH) | Gust Wind Speed (KpH) | Wind Direction | Surfability [0-5]")
        for j, hour in enumerate(hours):
            print(hour, weathers[i*7+j], temperature[i*7+j], swell[i*7+j], steady_wind[i*7+j], gust_wind[i*7+j])#, direction_wind[i*7+j], surfability[i*7+j])


