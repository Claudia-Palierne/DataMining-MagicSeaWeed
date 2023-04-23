import requests
import json
import datetime

FEATURES = ['currentDirection', 'currentSpeed']
API_KEY_ABSOLUTE_PATH = '/Users/mathias/Programming/myrepo/stormglass_api_key.txt'


query_result_for_test_path = '/Users/mathias/Programming/myrepo/Geocoordinates.txt'
with open(query_result_for_test_path) as query_file:
    data = query_file.read()

query_result_for_test = json.loads(data)



def add_api_data(area_dict):

    api_key = get_api_key()

    for area_key, area in area_dict.items():
        for beach in area:
            start_date, end_date = get_time_interval(beach)
            latitude, longitude = get_geo_coordinates(beach)
            parameters = {'lat': latitude, 'lng': longitude, 'params': ','.join(FEATURES),
                          'start': start_date, 'end': end_date}

            # api_data = query_stormglass(parameters, api_key)
            api_data = query_result_for_test

            # add data to dictionary
            for feature in FEATURES:
                beach['info'][feature] = extract_features_from_json(feature, api_data)

    return area_dict


def get_api_key():

    with open(API_KEY_ABSOLUTE_PATH, 'r') as api_key_file:
        api_key = api_key_file.read()

    return api_key

def extract_features_from_json(feature, data_dict):
    feature_data = list()
    time_slots_lst = data_dict['hours']
    for slot, slot_dict in enumerate(time_slots_lst):
        slot_matches_time_frame = slot % 3 == 0
        if slot_matches_time_frame:
            print(f'{slot = } , {slot_dict.get("time") = }')
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


def query_stormglass(parameters, api_key):

    response = requests.get('https://api.stormglass.io/v2/weather/point',
                            params=parameters,
                            headers={'Authorization': api_key})

    # Do something with response data.
    json_data = response.json()

    return type(json_data), json_data


if __name__ == '__main__':
    pass
