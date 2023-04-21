import requests
import json
import datetime


def add_api_data(area_dict):

    api_key_absolute_path = '/Users/mathias/Programming/myrepo/stormglass_api_key.txt'
    with open(api_key_absolute_path, 'r') as api_key_file:
        api_key = api_key_file.read()
    features = ['currentDirection', 'currentSpeed']

    for area_key, area in area_dict.items():
        for beach in area:
            # print(f'{area_key = },{beach = }')
            start_date, end_date = get_time_interval(beach)
            latitude, longitude = get_geo_coordinates(beach)
            parameters = {'lat': latitude,
                          'lng': longitude,
                          'params': ','.join(features),
                          'start': start_date,
                          'end': end_date}
            json_api_data = query_stormglass(parameters, api_key)

            # need to add data to dictionnary

    return area_dict


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
    return json_data


if __name__ == '__main__':
    pass
