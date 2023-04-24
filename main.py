import argparse
import database
import one_beach_scrapping
import url_extraction
import json
import api
import logging

logging.basicConfig(filename='magicLogger.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
        logging.info(f'{country}: url extraction successful')
        areas_urls = url_extraction.extract_areas_urls(country_forecast_urls)
        logging.info(f'{country}: areas url extraction successful')

        area_dict = build_area_dict(areas_urls, country)

        if execution_mode == 'database':
            database.initialize_db(area_dict, country) if idx == 0 else None

        execute(execution_mode, area_dict)


def build_area_dict(areas_urls, country):
    area_dict = create_area_dict(areas_urls, country)
    area_dict = one_beach_scrapping.get_beach_info(area_dict)
    area_dict = api.add_api_data(area_dict)

    return area_dict


def create_area_dict(areas_urls, country):
    area_dict = {}
    beaches_url = []
    for url in areas_urls:
        area_name = url.split('/')[CONFIG['IDX_AREA_NAME']]
        area_dict[(area_name, url)] = one_beach_scrapping.area_data(url)
        beaches_url += [beach["url"] for beach in area_dict[(area_name, url)]]
        logging.info(f'{country}: {area_name}: beaches urls extraction successful')

    return area_dict


def execute(mode, area_dict):

    for area, beaches in area_dict.items():
        for beach in beaches:
            if mode == 'print':
                one_beach_scrapping.print_beach_info(beach['info'])
            else:
                database.insert_conditions(beach['info'])


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
