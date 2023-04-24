import requests
import json
import logging

# Create a logger with the same name as the one in main.py
logger = logging.getLogger('magicLogger.log')

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)


def add_api_data(area_dict):
    """
    Add the api data for all the beaches to the area dictionary
    :param area_dict: the dictionary containing all the areas data
    :return: area_dict: the dictionary completed with the api data
    """
    query_api = True

    api_key = CONFIG["API_KEY"]

    for area_key, area in area_dict.items():
        for beach in area:
            start_date, end_date = get_time_interval(beach)
            latitude, longitude = get_geo_coordinates(beach)
            parameters = {'lat': latitude, 'lng': longitude, 'params': ','.join(CONFIG["FEATURES"]),
                          'start': start_date, 'end': end_date}

            api_data = query_stormglass(parameters, api_key, query_api)
            query_api = False

            # add data to dictionary
            for feature in CONFIG["FEATURES"]:
                beach['info'][feature] = extract_features_from_json(feature, api_data)
                logging.info(f'{beach["name"]}: {feature} was added ')

    return area_dict


def extract_features_from_json(feature, data_dict):
    """
    API query returned the features data for all the hours in the time interval.
    The code needs the features data of every three hour interval
    extract all the relevant feature data (every three hour slots) from the dictionary returned by the query
    :param feature: the feature of interest
    :param data_dict: data returned by the query containing the feature data for all the hours within time interval
    :return: relevant feature data to add to the beach
    """
    feature_data = list()
    time_slots_lst = data_dict['hours']
    for slot, slot_dict in enumerate(time_slots_lst):
        # retrieving the feature data only for every three hour intervals
        slot_matches_time_frame = slot % 3 == 0
        if slot_matches_time_frame:
            feature_data.append(slot_dict.get(feature).get('meto'))

    return feature_data


def get_geo_coordinates(beach):
    """
    Get the geo coordinates of a given beach to send as parameter for the query
    :param beach: a dictionary containing all the data of a given beach
    :return: latitude, longitude: geo coordinates of the beach
    """
    latitude = beach['latitude']
    longitude = beach['longitude']

    return latitude, longitude


def get_time_interval(beach):
    """
    Get the time interval of the data for a given beach to send as parameter for the query
    :param beach: a dictionary containing all the data from one beach
    :return: start_date, end_date: the boundaries of the time interval
    """
    start_date = beach['info']['timestamp'][0]
    end_date = beach['info']['timestamp'][-1]
    return start_date, end_date


def get_test_api_data(absolute_path):
    """
    The query from the API is limited.
    This function returns the data of a previous query saved in a test file
    :param absolute_path: the absolute path to txt file
    :return: api_data_for_test: a dictionnary containing all the data from a previous query
    """
    with open(absolute_path) as query_file:
        data = query_file.read()
    api_data_for_test = json.loads(data)

    return api_data_for_test


def query_stormglass(parameters, api_key, query_api):
    """
    send a query to the stormglass API and returns the features data
    :param query_api: API query is limited: query_api = True only for the first area
    :param parameters: a dictionary sent as a parameter to the API query containing information needed for the query
    and the features we want to retrieve data from
    :param api_key: the stormglass api key
    :return: api_data: a dictionary with the new features retrieved from API to complete area_dict
    """

    if query_api:
        response = requests.get(CONFIG["API"],
                                params=parameters,
                                headers={'Authorization': api_key})
        if response.status_code != CONFIG['RESPONSE_CODE_SUCCESS']:
            logging.error(f'Failed requesting parameters: latitude = {parameters.get("lat")} and '
                          f'longitude = {parameters.get("lat")}')
            raise ConnectionError(f'Failed requesting parameters: {parameters}')
        else:
            # read the response into json format response data.
            logging.info(f'API was queried and data will be added to dictionary ')
            json_data = response.json()
            api_data = json_data
    else:
        api_data = get_test_api_data(CONFIG["API_QUERY_RESULTS_PATH"])
        logging.info(f'API was not queried. Data from the txt file was returned latitude = {parameters.get("lat")} and '
                     f'longitude = {parameters.get("lat")}')

    return api_data