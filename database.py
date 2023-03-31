import one_beach_scrapping
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)

DB_NAME = "MagicSeaWeed"
TABLES = {}
TABLES['Countries'] = (
    """CREATE TABLE `Countries` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(14) NOT NULL,
    `url` varchar(14) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")

TABLES['Areas'] = (
    """CREATE TABLE `Areas` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(14) NOT NULL,
    `url` varchar(14) NOT NULL,
    `country_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (country_id) REFERENCES Countries(id)
    ) ENGINE=InnoDB""")

TABLES['Beaches'] = (
    """CREATE TABLE `Beaches` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(14) NOT NULL,
    `url` varchar(14) NOT NULL,
    `area_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (area_id) REFERENCES Areas(id)
    ) ENGINE=InnoDB""")

TABLES['Weathers'] = (
    """CREATE TABLE `Weathers` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(14) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")

TABLES['Conditions'] = (
    """CREATE TABLE `Conditions` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `beach_id` varchar(255) NOT NULL,
    `timestamp` datetime NOT NULL,
    `weather_id` varchar(255) NOT NULL,
    `wave_height_min(m)` float(24) NOT NULL,
    `wave_height_max(m)` float(24) NOT NULL,
    `temperature(C)` int(11) NOT NULL,
    `steady_wind_speed(kph)` int(11) NOT NULL,
    `gust_wind_speed(kph)` int(11) NOT NULL,
    `surfability` int(11) NOT NULL,
    `wind_direction` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")
# FOREIGN KEY (beach_id) REFERENCES Beaches(id),
# FOREIGN KEY (weather_id) REFERENCES Weathers(id)

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234')

cursor = connection.cursor()


def create_database(cursor):
    """

    """
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as error:
        print(f"Failed creating database: {error}")
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as error:
    print(f"Database {DB_NAME} does not exists.")
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print(f"Database {DB_NAME} created successfully.")
        connection.database = DB_NAME
    else:
        print(error)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
connection.close()


def insert_conditions(beach_soup):
    """

    """
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database=DB_NAME)
    cursor = cnx.cursor()
    beach_info = one_beach_scrapping.beach_historic(beach_soup)
    add_condition = """INSERT INTO Conditions (`beach_id`, `timestamp`, `weather_id`, `wave_height_min(m)`, `wave_height_max(m)`, 
                    `temperature(C)`, `steady_wind_speed(kph)`, `gust_wind_speed(kph)`, `surfability`, `wind_direction`) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, time in enumerate(beach_info['timestamp']):
        condition = (beach_info['name'], beach_info['timestamp'][i],
                     beach_info['weather'][i], beach_info['swell'][i][0], beach_info['swell'][i][1],
                     beach_info['temperature'][i], beach_info['steady_wind_speed'][i], beach_info['gust_wind_speed'][i],
                     beach_info['surfability'][i], beach_info['direction'][i])
        print(condition)
        cursor.execute(add_condition, condition)
    cnx.commit()
    cursor.close()
    cnx.close()


#TEST
get_url = requests.get("https://magicseaweed.com/Beit-Yanai-Surf-Report/3783/Historic/", headers=CONFIG['FAKE_USER_HEADER'])
get_soup = BeautifulSoup(get_url.content, "html.parser")
insert_conditions(get_soup)

#('Beit Yanai', datetime.datetime(2023, 3, 30, 12, 0), 'Light Showers', 1.4, 2.2, 15, 31, 31, 0, 'Onshore WNW - 292°')