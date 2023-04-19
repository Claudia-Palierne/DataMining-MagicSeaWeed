import argparse

import database
import one_beach_scrapping
import url_extraction
import json

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def main():
    """
    Web scrapping of the site MagicSeaWeed.
    :return: None
    """

    args = create_parser()

    country_to_scrap = args.country
    execution_mode = args.mode

    if country_to_scrap == 'ALL':
        country_to_scrap = CONFIG["SURF_FORECAST"].keys()
    else:
        country_to_scrap = [country_to_scrap]

    for idx, country in enumerate(country_to_scrap):
        # Extracting urls
        country_forecast_urls = CONFIG["SURF_FORECAST"].get(country)
        print(f'{country}: url extraction successful')
        areas_urls = url_extraction.extract_areas_urls(country_forecast_urls)
        print(f'{country}: areas url extraction successful')

        area_dict, beaches_url = build_area_dict(areas_urls, country)

        # we should only use area dict and no more beaches url, but that's not for today mamen
        beaches_soup = url_extraction.get_soup(beaches_url)

        if execution_mode == 'database':
            database.initialize_db() if idx == 0 else None
            database.insert_areas(areas_urls, country)
            database.insert_beaches(area_dict)

        execute(execution_mode, beaches_soup)


def build_area_dict(areas_urls, country):
    area_dict = {}
    beaches_url = []
    for url in areas_urls:
        area_name = url.split('/')[CONFIG['IDX_AREA_NAME']]
        beach_per_area_url = url_extraction.extract_beaches_urls([url])

        print(f'{country}: {area_name}: beaches urls extraction successful')
        area_dict[area_name] = beach_per_area_url
        beaches_url += beach_per_area_url

    return area_dict, beaches_url


def execute(mode, beaches_soup):

    # Execution mode
    for bs in beaches_soup:
        beach_data = one_beach_scrapping.beach_historic(bs)
        if mode == 'print':
            one_beach_scrapping.print_beach_info(beach_data)
        else:
            database.insert_conditions(beach_data)


def create_parser():

    parser = argparse.ArgumentParser()
    # Gets the country input by user
    parser.add_argument("-country", type=str, choices=['ALL', 'ISRAEL', 'FRANCE', 'HAWAII'],
                        default='ISRAEL',
                        help="choose a country from the list to scrap")

    # Get the execution mode
    parser.add_argument("-mode", type=str, choices=['print', 'database'],
                        default='print',
                        help="choose a mode of execution :"
                             "print will print the information in the std output"
                             "whereas database will store it in the db")

    # Using parser to further use the arguments
    return parser.parse_args()



if __name__ == "__main__":
    main()
