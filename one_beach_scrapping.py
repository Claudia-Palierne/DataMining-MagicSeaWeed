import json

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def extract_days(beach_soup):
    """
    Extract the dates for the surf spot.
    :param beach_soup: BeautifulSoup object
    :return: an array of dates.
    """
    days = [a.text for a in beach_soup.find_all("h6", class_="nomargin pull-left heavy table-header-title")]
    return days


def extract_hours(beach_soup):
    """
    Extract all the times that were made the measurements.
    :param beach_soup: BeautifulSoup Object
    :return: an array with hours
    """
    hours = [a.text for a in beach_soup.find_all("td",
                                                 class_="nopadding-left row-title background-clear msw-js-tooltip")][:8]
    return hours


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
    temperature = [a.text for a in beach_soup.find_all("h5", class_="nomargin font-sans-serif heavy")]
    return temperature


def extract_swell(beach_soup):
    """
    Extract swell height of the past week.
    :param beach_soup: BeautifulSoup object
    :return: an array of the swell height for each day and each hour.
    """
    swell = [a.text for a in beach_soup.select('span[class*="font-sans-serif"]')]
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
    steady_speed = [a.text.strip() for a in beach_soup.find_all("span", class_="stacked-text text-right")]
    return steady_speed


def extract_wind_gust_speed(beach_soup):
    """
    Extract the speed of the gusting wind in KpH of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the gust wind speed for each day and each hour.
    """
    gust_speed = [a.text.strip() for a in beach_soup.find_all("span", class_="stacked-text-item")][::2]
    return gust_speed


def extract_wind_direction(beach_soup):
    """
    Extract the wind direction of the past week.
    :param beach_soup: BeautifulSoup Object
    :return: an array with the wind direction for each day and each hour.
    """
    direction = [a for a in beach_soup.find_all("td",
                                                class_="text-center last msw-js-tooltip td-square background-warning")]
    return direction


def extract_name(beach_soup):
    """
    Extract the name of the surf spot
    :param beach_soup: BeautifulSoup Object
    :return: a string of the name of the surf spot.
    """
    return beach_soup.find("h1").text


def print_beach_info(beach_soup):
    """
    Print all the info that were extracted in the surf spot.
    :param beach_soup: BeautifulSoup Object
    :return: None
    """
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
        print("Time Weather  | Temperature | Swell | Steady Wind Speed (KpH) | Gust Wind Speed (KpH) |  Surfability ["
              "0-5]")
        for j, hour in enumerate(hours):
            print(hour, weathers[i * CONFIG['DAYS_IN_WEEK'] + j],
                  temperature[i * CONFIG['DAYS_IN_WEEK'] + j],
                  swell[i * CONFIG['DAYS_IN_WEEK'] + j],
                  steady_wind[i * CONFIG['DAYS_IN_WEEK'] + j],
                  gust_wind[i * CONFIG['DAYS_IN_WEEK'] + j],
                  surfability[i * CONFIG['DAYS_IN_WEEK'] + j])
