import requests
import json

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)

def add_api_data(area_dict):

    api_key = get_api_key()

    for area_key, area in area_dict.items():
        for beach in area:
            start_date, end_date = get_time_interval(beach)
            latitude, longitude = get_geo_coordinates(beach)
            parameters = {'lat': latitude, 'lng': longitude, 'params': ','.join(CONFIG["FEATURES"]),
                          'start': start_date, 'end': end_date}

            api_data = query_stormglass(parameters, api_key)

            # add data to dictionary
            for feature in CONFIG["FEATURES"]:
                beach['info'][feature] = extract_features_from_json(feature, api_data)

    return area_dict


def get_api_key():

    with open(CONFIG["API_KEY_ABSOLUTE_PATH"], 'r') as api_key_file:
        api_key = api_key_file.read()

    return api_key


def extract_features_from_json(feature, data_dict):
    feature_data = list()
    time_slots_lst = data_dict['hours']
    for slot, slot_dict in enumerate(time_slots_lst):
        slot_matches_time_frame = slot % 3 == 0
        if slot_matches_time_frame:
            feature_data.append(slot_dict.get(feature).get('meto'))

    return feature_data

def get_geo_coordinates(beach):
    latitude = beach['latitude']
    longitude = beach['longitude']

    return latitude, longitude


def get_time_interval(beach):
    start_date = beach['info']['timestamp'][0]
    end_date = beach['info']['timestamp'][-1]
    return start_date, end_date



def get_test_api_data(absolute_path):
    with open(absolute_path) as query_file:
        data = query_file.read()
    api_data_for_test = json.loads(data)

    return api_data_for_test


def query_stormglass(parameters, api_key):

    test_mode = True

    if test_mode :
        api_data = get_test_api_data(CONFIG["API_QUERY_RESULTS_FOR_TESTING_PATH"])
    else:
        response = requests.get(CONFIG["API"],
                                params=parameters,
                                headers={'Authorization': api_key})

        # read the response into json format response data.
        json_data = response.json()
        api_data = json_data

    return api_data


if __name__ == '__main__':
    pass
