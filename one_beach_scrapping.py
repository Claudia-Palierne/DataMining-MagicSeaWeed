from datetime import datetime
import json
import re

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def extract_timestamp(beach_soup):
    """
    Extract the dates for the surf spot.
    :param beach_soup: BeautifulSoup object
    :return: an array of datetime.
    """
    days = [a.text for a in beach_soup.find_all("h6", class_="nomargin pull-left heavy table-header-title")]
    hours = [a.text if a.text.strip() != 'Noon' else ' 12PM ' for a in beach_soup.find_all("td", class_="nopadding-left row-title background-clear msw-js-tooltip")][:8]
    timestamp = [datetime.strptime('2023 ' + day + hour, '%Y %A %d/%m %I%p ') for day in days for hour in hours]
    return timestamp


def extract_weather(beach_soup):
    """
    Extract the weather of the past week.
    :param beach_soup: BeautifulSoup object
    :return: an array that extract the weather for each day and each hour.
    """
    weather = [a['title'] for a in beach_soup.find_all("td", attrs={"data-filter": "weather"})]
    return weather


def extract_temperature(beach_soup):
    """
    Extract the temperature of the past week (8 times a day).
    :param beach_soup: BeautifulSoup object
    :return: an array that extract the temperature for each day and each hour.
    """
    temperature = [int(re.search(r'\d+', a.text).group()) for a in beach_soup.find_all("h5", class_="nomargin font-sans-serif heavy")]
    return temperature


def extract_swell(beach_soup):
    """
    Extract swell height of the past week.
    :param beach_soup: BeautifulSoup object
    :return: an array of the swell height for each day and each hour.
    """
    swell = []
    for a in beach_soup.select('span[class*="font-sans-serif"]'):
        if a.text.strip() == "Flat":
            swell.append([0.0, 0.0])
        else:
            pattern = r"[\d.]+"
            matches = re.findall(pattern, a.text)
            tmp = [float(match) for match in matches]
            if len(tmp) < 2:
                swell.append(tmp + tmp)
            else:
                swell.append(tmp)
    return swell


def extract_swell_rating(beach_soup):
    """
    Extract the rates of the swell (how much surfable is the spot at this time) of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the rate swell for each day and each hour.
    """
    rating = [len(stars.findChildren("li", class_="active"))
              for stars in beach_soup.find_all("ul", class_="rating clearfix")]
    return rating


def extract_wind_steady_speed(beach_soup):
    """
    Extract the speed of the steady wind of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the steady wind speed for each day and each hour.
    """
    steady_speed = [int(a.text.strip()) for a in beach_soup.find_all("span", class_="stacked-text text-right")]
    return steady_speed


def extract_wind_gust_speed(beach_soup):
    """
    Extract the speed of the gusting wind in KpH of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the gust wind speed for each day and each hour.
    """
    gust_speed = [a.text.strip() for a in beach_soup.find_all("span", class_="stacked-text-item")][::2]
    gust_speed = list(map(int, gust_speed))
    return gust_speed


def extract_wind_direction(beach_soup):
    """
    Extract the wind direction of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the wind direction for each day and each hour.
    """
    direction = [a['title'].split(", ")[1] for a in beach_soup.select('td[class*="text-center last msw-js-tooltip td-square background"]')]
    return direction


def extract_name(beach_soup):
    """
    Extract the name of the surf spot
    :param beach_soup: BeautifulSoup Object
    :return: a string of the name of the surf spot.
    """
    name = re.search(r"/([^/]+?)-Surf", beach_soup.find("link")['href']).group()[1:]
    print('extract name : ', name)
    return name


def beach_historic(beach_soup):
    """
    Put all the extracted information of beach into a dictionary.
    :param beach_soup: BeautifulSoup Object
    :return: a dictionary
    """
    infos = {}
    infos['name'] = extract_name(beach_soup)
    infos['timestamp'] = extract_timestamp(beach_soup)
    infos['weather'] = extract_weather(beach_soup)
    infos['temperature'] = extract_temperature(beach_soup)
    infos['swell'] = extract_swell(beach_soup)
    infos['steady_wind_speed'] = extract_wind_steady_speed(beach_soup)
    infos['gust_wind_speed'] = extract_wind_gust_speed(beach_soup)
    infos['direction'] = extract_wind_direction(beach_soup)
    infos['surfability'] = extract_swell_rating(beach_soup)
    return infos


def print_beach_info(beach_info):
    """
    Print all the info that were extracted in the surf spot.
    :param beach_soup: BeautifulSoup Object
    :return: None
    """
    # beach_info = beach_historic(beach_soup)
    print(f"--------------- {beach_info['name']} ------------------")
    for i, time in enumerate(beach_info['timestamp']):
        if i % 8 == 0:
            print(beach_info['timestamp'][i].date())
            print("Time | Weather  | Temperature | Swell (m) [min-max]| Steady Wind Speed (KpH) | Gust Wind Speed (KpH) |  Surfability [0-5]")
        print(beach_info['timestamp'][i].time(),
              beach_info['weather'][i],
              beach_info['temperature'][i],
              beach_info['swell'][i],
              beach_info['steady_wind_speed'][i],
              beach_info['gust_wind_speed'][i],
              beach_info['surfability'][i],
              beach_info['direction'][i])
