import re
import json
import mysql.connector
from mysql.connector import errorcode

# These are actually used :
import grequests
import one_beach_scrapping
import requests
from bs4 import BeautifulSoup

with open("conf.json", "r") as jsonfile:
    CONFIG = json.load(jsonfile)

with open("conf_sql.json", "r") as jsonfile:
    SQL_CONFIG = json.load(jsonfile)



TABLES = {}
TABLES['Countries'] = (
    """CREATE TABLE IF NOT EXISTS `Countries` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(14) NOT NULL,
    `url` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")

TABLES['Areas'] = (
    """CREATE TABLE IF NOT EXISTS `Areas` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `url` varchar(255) NOT NULL,
    `country_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (country_id) REFERENCES Countries(id)
    ) ENGINE=InnoDB""")

TABLES['Beaches'] = (
    """CREATE TABLE IF NOT EXISTS `Beaches` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `url` varchar(255) NOT NULL,
    `area_id` int(11) NOT NULL,
    `latitude` float(24) NOT NULL,
    `longitude` float(24) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (area_id) REFERENCES Areas(id)
    ) ENGINE=InnoDB""")

TABLES['Conditions'] = (
    """CREATE TABLE IF NOT EXISTS `Conditions` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `beach_id` int(11) NOT NULL,
    `timestamp` datetime NOT NULL,
    `weather` varchar(255) NOT NULL,
    `wave_height_min(m)` float(24) NOT NULL,
    `wave_height_max(m)` float(24) NOT NULL,
    `temperature(C)` int(11) NOT NULL,
    `steady_wind_speed(kph)` int(11) NOT NULL,
    `gust_wind_speed(kph)` int(11) NOT NULL,
    `surfability` int(11) NOT NULL,
    `wind_direction` varchar(255) NOT NULL,
    `current_direction(°)` float(24) NOT NULL,
    `current_speed(mps)` float(24) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (beach_id) REFERENCES Beaches(id)
    ) ENGINE=InnoDB""")


def connect_to_db(database_selected=False):

    database = SQL_CONFIG["DB_NAME"] if database_selected else None

    connection = mysql.connector.connect(
        host=SQL_CONFIG["HOST"],
        user=SQL_CONFIG["USER"],
        password=SQL_CONFIG["PASSWORD"],
        database=database
    )

    return connection


def create_database():
    """
    This function will create a database in SQL.
    :return: None
    """

    connection = connect_to_db(database_selected=False)
    cursor = connection.cursor()
    # Create database and tables
    try:
        print("Creating database {}: ".format(SQL_CONFIG['DB_NAME']), end='')
        cursor.execute(f"CREATE DATABASE {SQL_CONFIG['DB_NAME']} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print("Database already exists.")
        else:
            print(err.msg)
            exit(1)
    else:
        print("OK")
    cursor.close()
    connection.close()


def create_table():
    """
    This function will create the table inside the database.
    :return: None
    """
    connection = connect_to_db(database_selected=False)
    cursor = connection.cursor()

    cursor.execute("USE {}".format(SQL_CONFIG['DB_NAME']))
    for table_name in TABLES.keys():
        table_description = TABLES.get(table_name)
        cursor.execute(table_description)

    cursor.close()
    connection.close()


def insert_countries():
    """
    This function will insert the data inside the table Countries in SQL.
    :return: None
    """
    connection = connect_to_db(database_selected=True)
    cursor = connection.cursor()

    add_country = """INSERT INTO Countries (`name`, `url`) 
                    SELECT %s, %s
                    WHERE NOT EXISTS (
                        SELECT * FROM Countries WHERE Countries.name = %s AND Countries.url = %s);"""
    for name, url in CONFIG["SURF_FORECAST"].items():
        country = (name, url)
        cursor.execute(add_country, country + country)
        print(f'{country} successfully inserted into db')

    connection.commit()
    cursor.close()
    connection.close()


def insert_areas(areas_dict, country):
    """
    This function will insert data inside the table Areas.
    :param areas_dict: a dictionary of all the areas' info.
    :param country: a string with the country name.
    :return: None
    """
    connection = connect_to_db(database_selected=True)
    cursor = connection.cursor()

    add_area = """INSERT INTO Areas (`name`, `url`, `country_id`) 
                    SELECT %s, %s, (SELECT id FROM Countries where Countries.name = %s)
                    WHERE NOT EXISTS (
                        SELECT * FROM Areas 
                        WHERE `name` = %s AND `url` = %s 
                            AND country_id = (SELECT id FROM Countries where Countries.name = %s)
                    );"""
    for area, beaches in areas_dict.items():
        area_name, area_url = area
        area = (area_name, area_url, country)
        cursor.execute(add_area, area + area)
        print(f'{area} successfully inserted into db')

    connection.commit()
    cursor.close()
    connection.close()


def insert_beaches(area_dict):
    """
    This function will insert the data inside the table Beaches in SQL.
    :param area_dict: a dictionary where the keys are the areas' name and the value are the beaches' urls.
    :return: None
    """
    connection = connect_to_db(database_selected=True)
    cursor = connection.cursor()

    add_beach = """INSERT INTO Beaches (`name`, `url`, `area_id`, `latitude`, `longitude`) 
                        SELECT %s, %s, (SELECT id FROM Areas where Areas.url = %s), %s, %s
                        WHERE NOT EXISTS (
                            SELECT * FROM Beaches
                            WHERE name = %s AND url = %s
                                AND area_id = (SELECT id FROM Areas where Areas.url = %s)
                        );"""
    for area, beaches in area_dict.items():
        area_name, area_url = area
        for beach in beaches:
            beach_tup = (beach["name"], beach["url"], area_url, beach["latitude"], beach["longitude"])
            cursor.execute(add_beach, beach_tup + (beach["name"], beach["url"], area_url))
            print(f'{beach} successfully inserted into db')

    connection.commit()
    cursor.close()
    connection.close()


def insert_conditions(beach_info):
    """
    This function will insert the data of one beach inside the table Conditions in SQL.
    :param beach_info: a dictionary of all the information for one beach.
    :return: None
    """
    connection = connect_to_db(database_selected=True)
    cursor = connection.cursor()

    add_condition = """INSERT INTO Conditions (`beach_id`, `timestamp`, `weather`, `wave_height_min(m)`, 
                    `wave_height_max(m)`, `temperature(C)`, `steady_wind_speed(kph)`, `gust_wind_speed(kph)`, 
                    `surfability`, `wind_direction`, `current_direction(°)`, `current_speed(mps)`) 
                    SELECT (SELECT id FROM Beaches where Beaches.url = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT * FROM Conditions 
                        WHERE beach_id = (SELECT id FROM Beaches where Beaches.url = %s) AND timestamp = %s
                    ); """

    for i, time in enumerate(beach_info['timestamp']):
        condition = (beach_info['url'], beach_info['timestamp'][i],
                     beach_info['weather'][i], beach_info['swell'][i][0], beach_info['swell'][i][1],
                     beach_info['temperature'][i], beach_info['steady_wind_speed'][i], beach_info['gust_wind_speed'][i],
                     beach_info['surfability'][i], beach_info['direction'][i],
                     beach_info["currentDirection"][i], beach_info["currentSpeed"][i])
        cursor.execute(add_condition, condition + (beach_info['url'], beach_info['timestamp'][i]))
        print(f'{time} successfully inserted into db')

    connection.commit()
    cursor.close()
    connection.close()


def initialize_db():
    """
    This function initialise the database, in order to insert the scrapping data.
    :return: None
    """
    create_database()
    create_table()
    insert_countries()
