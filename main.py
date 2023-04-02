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
    args = parser.parse_args()
    country_to_scrap = args.country
    execution_mode = args.mode

    if country_to_scrap == 'ALL':
        country_to_scrap = CONFIG["SURF_FORECAST"].keys()
    else:
        country_to_scrap = [country_to_scrap]

    for idx, country in enumerate(country_to_scrap):
        # Extracting urls
        country_forecast_urls = CONFIG["SURF_FORECAST"].get(country)
        areas_urls = url_extraction.extract_areas_urls(country_forecast_urls)
        area_dict = {}
        beaches_url = []
        for url in areas_urls:
            beach_per_area_url = url_extraction.extract_beaches_urls([url])
            area_name = url.split('/')[-3]
            area_dict[area_name] = beach_per_area_url
            beaches_url += beach_per_area_url

        # Execution mode
        if execution_mode == 'print':
            beaches_soup = url_extraction.get_soup(beaches_url)
            for bs in beaches_soup:
                beach_data = one_beach_scrapping.beach_historic(bs)
                one_beach_scrapping.print_beach_info(beach_data)

        else:
            database.initialize_db() if idx == 0 else None
            database.insert_areas(areas_urls, country)
            database.insert_beaches(area_dict)

            beaches_soup = url_extraction.get_soup(beaches_url)
            for bs in beaches_soup:
                beach_data = one_beach_scrapping.beach_historic(bs)
                database.insert_conditions(beach_data)


if __name__ == "__main__":
    main()
