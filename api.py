import requests
import json
import datetime

beach_info = {
    'url': 'https://magicseaweed.com/Bat-Yam-Surf-Report/3662/Historic/',
    'name': 'Bat-Yam-Surf',
    'timestamp': [datetime.datetime(2023, 4, 14, 0, 0),
                  datetime.datetime(2023, 4, 14, 3, 0),
                  datetime.datetime(2023, 4, 14, 6, 0),
                  datetime.datetime(2023, 4, 14, 9, 0),
                  datetime.datetime(2023, 4, 14, 12, 0),
                  datetime.datetime(2023, 4, 14, 15, 0),
                  datetime.datetime(2023, 4, 14, 18, 0),
                  datetime.datetime(2023, 4, 14, 21, 0), datetime.datetime(2023, 4, 15, 0, 0),
                  datetime.datetime(2023, 4, 15, 3, 0), datetime.datetime(2023, 4, 15, 6, 0),
                  datetime.datetime(2023, 4, 15, 9, 0), datetime.datetime(2023, 4, 15, 12, 0),
                  datetime.datetime(2023, 4, 15, 15, 0), datetime.datetime(2023, 4, 15, 18, 0),
                  datetime.datetime(2023, 4, 15, 21, 0), datetime.datetime(2023, 4, 16, 0, 0),
                  datetime.datetime(2023, 4, 16, 3, 0), datetime.datetime(2023, 4, 16, 6, 0),
                  datetime.datetime(2023, 4, 16, 9, 0), datetime.datetime(2023, 4, 16, 12, 0),
                  datetime.datetime(2023, 4, 16, 15, 0), datetime.datetime(2023, 4, 16, 18, 0),
                  datetime.datetime(2023, 4, 16, 21, 0), datetime.datetime(2023, 4, 17, 0, 0),
                  datetime.datetime(2023, 4, 17, 3, 0), datetime.datetime(2023, 4, 17, 6, 0),
                  datetime.datetime(2023, 4, 17, 9, 0), datetime.datetime(2023, 4, 17, 12, 0),
                  datetime.datetime(2023, 4, 17, 15, 0), datetime.datetime(2023, 4, 17, 18, 0),
                  datetime.datetime(2023, 4, 17, 21, 0), datetime.datetime(2023, 4, 18, 0, 0),
                  datetime.datetime(2023, 4, 18, 3, 0), datetime.datetime(2023, 4, 18, 6, 0),
                  datetime.datetime(2023, 4, 18, 9, 0), datetime.datetime(2023, 4, 18, 12, 0),
                  datetime.datetime(2023, 4, 18, 15, 0), datetime.datetime(2023, 4, 18, 18, 0),
                  datetime.datetime(2023, 4, 18, 21, 0), datetime.datetime(2023, 4, 19, 0, 0),
                  datetime.datetime(2023, 4, 19, 3, 0), datetime.datetime(2023, 4, 19, 6, 0),
                  datetime.datetime(2023, 4, 19, 9, 0), datetime.datetime(2023, 4, 19, 12, 0),
                  datetime.datetime(2023, 4, 19, 15, 0), datetime.datetime(2023, 4, 19, 18, 0),
                  datetime.datetime(2023, 4, 19, 21, 0), datetime.datetime(2023, 4, 20, 0, 0),
                  datetime.datetime(2023, 4, 20, 3, 0), datetime.datetime(2023, 4, 20, 6, 0),
                  datetime.datetime(2023, 4, 20, 9, 0), datetime.datetime(2023, 4, 20, 12, 0),
                  datetime.datetime(2023, 4, 20, 15, 0), datetime.datetime(2023, 4, 20, 18, 0),
                  datetime.datetime(2023, 4, 20, 21, 0)],
    'weather': ['Clear', 'Clear', 'Clear', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Clear', 'Clear', 'Clear', 'Clear',
                'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Clear', 'Clear', 'Clear', 'Clear', 'Sunny', 'Sunny', 'Sunny',
                'Sunny', 'Clear', 'Clear', 'Clear', 'Clear', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Clear', 'Clear',
                'Clear', 'Clear', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Clear', 'Clear', 'Clear', 'Clear', 'Sunny',
                'Sunny', 'Sunny', 'Sunny', 'Clear', 'Clear', 'Clear', 'Clear', 'Sunny', 'Sunny', 'Sunny', 'Sunny',
                'Clear'],
    'temperature': [16, 15, 14, 18, 20, 21, 20, 18, 17, 17, 17, 19, 22, 22, 21, 19, 18, 18, 17, 20, 22, 21, 21, 20, 19,
                    18, 18, 21, 23, 23, 22, 22, 21, 19, 19, 23, 24, 26, 25, 23, 24, 24, 22, 24, 29, 24, 24, 23, 23, 19,
                    18, 19, 20, 19, 19, 18],
    'swell': [[0.9, 1.4], [0.8, 1.3], [0.7, 1.2], [0.7, 1.1], [0.6, 1.0], [0.6, 0.9], [0.5, 0.8], [0.5, 0.7],
              [0.4, 0.7], [0.4, 0.6], [0.3, 0.5], [0.3, 0.5], [0.3, 0.5], [0.3, 0.4], [0.2, 0.4], [0.2, 0.4],
              [0.2, 0.3], [0.2, 0.3], [0.2, 0.3], [0.1, 0.2], [0.1, 0.2], [0.1, 0.2], [0.1, 0.2], [0.1, 0.2],
              [0.0, 0.0], [0.0, 0.0], [0.1, 0.2], [0.1, 0.2], [0.2, 0.2], [0.2, 0.3], [0.2, 0.3], [0.2, 0.3],
              [0.2, 0.3], [0.2, 0.3], [0.2, 0.3], [0.2, 0.3], [0.2, 0.3], [0.2, 0.2], [0.1, 0.2], [0.1, 0.2],
              [0.1, 0.2], [0.1, 0.2], [0.1, 0.2], [0.0, 0.0], [0.1, 0.2], [0.1, 0.2], [0.2, 0.2], [0.2, 0.3],
              [0.2, 0.3], [0.4, 0.6], [0.5, 0.7], [0.6, 0.9], [0.6, 0.9], [0.6, 0.9], [0.6, 0.9], [0.5, 0.8]],
    'steady_wind_speed': [5, 8, 7, 8, 8, 16, 20, 17, 10, 10, 9, 3, 6, 15, 14, 13, 7, 8, 4, 10, 12, 12, 12, 10, 11, 3, 5,
                          2, 9, 13, 12, 7, 11, 1, 8, 7, 12, 11, 11, 9, 6, 9, 10, 7, 3, 32, 22, 17, 25, 17, 15, 16, 21,
                          22, 16, 14],
    'gust_wind_speed': [5, 9, 8, 9, 8, 16, 21, 24, 12, 12, 11, 4, 6, 15, 17, 21, 10, 10, 5, 11, 12, 12, 14, 12, 14, 3,
                        5, 2, 9, 13, 13, 8, 12, 1, 8, 8, 12, 11, 12, 9, 6, 9, 10, 7, 4, 34, 35, 22, 31, 27, 19, 16, 21,
                        22, 17, 16],
    'direction': ['Cross/Offshore SSE - 168°', 'Cross/Offshore SSE - 160°', 'Offshore ESE - 121°', 'Offshore ENE - 67°',
                  'Onshore NW - 313°', 'Cross/Onshore NNW - 339°', 'Cross-shore N - 3°', 'Cross/Offshore NNE - 18°',
                  'Cross/Offshore NNE - 20°', 'Cross/Offshore NNE - 22°', 'Cross/Offshore NNE - 21°',
                  'Cross/Onshore SSW - 194°', 'Onshore W - 264°', 'Onshore WNW - 290°', 'Cross-shore N - 359°',
                  'Cross/Offshore NNE - 14°', 'Onshore NNW - 333°', 'Onshore WNW - 282°', 'Offshore SE - 140°',
                  'Cross/Onshore SSW - 201°', 'Onshore WSW - 258°', 'Onshore W - 275°', 'Cross/Onshore N - 350°',
                  'Offshore NNE - 25°', 'Onshore NNW - 334°', 'Cross/Onshore N - 354°', 'Cross-shore N - 2°',
                  'Onshore SW - 231°', 'Onshore W - 277°', 'Onshore WNW - 291°', 'Onshore NW - 324°',
                  'Offshore NE - 55°', 'Onshore WSW - 251°', 'Offshore NNE - 30°', 'Offshore SE - 129°',
                  'Onshore SSW - 206°', 'Onshore WNW - 284°', 'Onshore NNW - 329°', 'Cross/Onshore N - 355°',
                  'Offshore ENE - 57°', 'Offshore ENE - 77°', 'Offshore SSE - 152°', 'Cross/Onshore SSW - 195°',
                  'Offshore NNE - 26°', 'Cross/Onshore NNW - 347°', 'Onshore NNW - 328°', 'Offshore NNE - 25°',
                  'Offshore E - 80°', 'Onshore W - 260°', 'Cross/Onshore NNW - 343°', 'Onshore NW - 323°',
                  'Onshore NW - 313°', 'Onshore WNW - 295°', 'Onshore WNW - 301°', 'Onshore WNW - 302°',
                  'Onshore WNW - 298°'],
    'surfability': [2, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


def query_stormglass(beach_info):
    api_key_absolute_path = '/Users/mathias/Programming/myrepo/stormglass_api_key.txt'

    start_date_expected = datetime.datetime(2023, 4, 14, 0, 0)
    end_date_expected = datetime.datetime(2023, 4, 20, 21, 0)
    features = ['currentDirection', 'currentSpeed']

    start_date = beach_info['timestamp'][0]
    end_date = beach_info['timestamp'][-1]

    print(start_date, start_date_expected)
    print(end_date, end_date_expected)

    # with open(api_key_absolute_path, 'r') as api_key_file:
    #     api_key = api_key_file.read()
    #
    # response = requests.get('https://api.stormglass.io/v2/weather/point',
    #                         params={'lat': 32.9174347,
    #                                 'lng': 35.0797628,
    #                                 'params': ','.join(features),
    #                                 'start': start_date,  # Convert to UTC timestamp
    #                                 'end': end_date  # Convert to UTC timestamp
    #                                 },
    #                         headers={'Authorization': api_key})
    #
    # # Do something with response data.
    # json_data = response.json()
    # print(json_data)


if __name__ == '__main__':
    # For a given country we want a dictionary with areas and their longitude and latitude
    # israel_geo_coordinates = get_country_geo_coordinates('ISRAEL', area_dict_israel)
    # print(israel_geo_coordinates)

    query_stormglass(beach_info)
