import re
import grequests
import one_beach_scrapping
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
    `url` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")

TABLES['Areas'] = (
    """CREATE TABLE `Areas` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `url` varchar(255) NOT NULL,
    `country_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (country_id) REFERENCES Countries(id)
    ) ENGINE=InnoDB""")

TABLES['Beaches'] = (
    """CREATE TABLE `Beaches` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `url` varchar(255) NOT NULL,
    `area_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (area_id) REFERENCES Areas(id)
    ) ENGINE=InnoDB""")

TABLES['Weathers'] = (
    """CREATE TABLE `Weathers` ( 
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")

TABLES['Conditions'] = (
    """CREATE TABLE `Conditions` ( 
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
    PRIMARY KEY (`id`),
    FOREIGN KEY (beach_id) REFERENCES Beaches(id)
    ) ENGINE=InnoDB""")

# FOREIGN KEY (weather_id) REFERENCES Weathers(id)


def create_database():
    """

    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995')
    cursor = connection.cursor()
    # Create database and tables
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as error:
        print(f"Failed creating database: {error}")
        exit(1)
    cursor.close()
    connection.close()


def create_table():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995')

    cursor = connection.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as error:
        print(f"Database {DB_NAME} does not exists.")
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
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


def insert_countries():
    """

    """
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995',
        database=DB_NAME)
    cursor = cnx.cursor()
    add_country = """INSERT INTO Countries (`name`, `url`) 
                    SELECT %s, %s
                    WHERE NOT EXISTS (
                        SELECT * FROM Countries WHERE Countries.name = %s AND Countries.url = %s);"""
    for name, url in CONFIG["SURF_FORECAST"].items():
        country = (name, url)
        cursor.execute(add_country, country + country)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_areas(areas_links, country):
    """

    """
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995',
        database=DB_NAME)
    cursor = cnx.cursor()
    add_area = """INSERT INTO Areas (`name`, `url`, `country_id`) 
                    SELECT %s, %s, (SELECT id FROM Countries where Countries.name = %s)
                    WHERE NOT EXISTS (
                        SELECT * FROM Areas 
                        WHERE `name` = %s AND `url` = %s 
                            AND country_id = (SELECT id FROM Countries where Countries.name = %s));"""
    for url in areas_links:
        #name = re.search(r'/([^/-]*)(-Surfing/)', url).group(1)
        name = url.split('/')[-3]
        area = (name, url, country)
        cursor.execute(add_area, area + area)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_beaches(area_dict):
    """

    """
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995',
        database=DB_NAME)
    cursor = cnx.cursor()
    add_beach = """INSERT INTO Beaches (`name`, `url`, `area_id`) 
                        SELECT %s, %s, (SELECT id FROM Areas where Areas.name = %s)
                        WHERE NOT EXISTS (
                        SELECT * FROM Beaches
                        WHERE name = %s AND url = %s
                            AND area_id = (SELECT id FROM Areas where Areas.name = %s));"""
    for area_name, beach_links in area_dict.items():
        for beach_url in beach_links:

            beach_name = re.search(r"/([^/]+?)-Surf", beach_url).group()[1:]
            print(beach_name)
            beach = (beach_name, beach_url, area_name)
            cursor.execute(add_beach, beach + beach)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_conditions(beach_info):
    """

    """
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1995',
        database=DB_NAME)
    cursor = cnx.cursor()
    add_condition = """INSERT INTO Conditions (`beach_id`, `timestamp`, `weather`, `wave_height_min(m)`, `wave_height_max(m)`, 
                    `temperature(C)`, `steady_wind_speed(kph)`, `gust_wind_speed(kph)`, `surfability`, `wind_direction`) 
                    SELECT (SELECT id FROM Beaches where Beaches.url = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                    SELECT * FROM Conditions 
                    WHERE beach_id = (SELECT id FROM Beaches where Beaches.url = %s) AND timestamp = %s AND weather = %s
                    AND `wave_height_min(m)` = %s AND `wave_height_max(m)` = %s AND `temperature(C)` = %s AND `steady_wind_speed(kph)` = %s
                    AND `gust_wind_speed(kph)` = %s AND surfability = %s AND wind_direction = %s
                    ); """

    for i, time in enumerate(beach_info['timestamp']):
        condition = (beach_info['url'], beach_info['timestamp'][i],
                     beach_info['weather'][i], beach_info['swell'][i][0], beach_info['swell'][i][1],
                     beach_info['temperature'][i], beach_info['steady_wind_speed'][i], beach_info['gust_wind_speed'][i],
                     beach_info['surfability'][i], beach_info['direction'][i])
        cursor.execute(add_condition, condition + condition)
    cnx.commit()
    cursor.close()
    cnx.close()


def initialize_db():
    create_table()
    insert_countries()


if __name__ == "__main__":

    initialize_db()

    areas_links_ISRAEL = ['https://magicseaweed.com/Central-Tel-Aviv-Surfing/113/', 'https://magicseaweed.com/Southern-Surfing/1019/', 'https://magicseaweed.com/Haifa-Surfing/1020/', 'https://magicseaweed.com/Red-Sea-Surfing/1074/']
    areas_links_ALL = ['https://magicseaweed.com/Central-Tel-Aviv-Surfing/113/', 'https://magicseaweed.com/Southern-Surfing/1019/', 'https://magicseaweed.com/Haifa-Surfing/1020/', 'https://magicseaweed.com/Red-Sea-Surfing/1074/',
                       'https://magicseaweed.com/The-Channel-Surfing/26/', 'https://magicseaweed.com/Brittany-North-Surfing/27/', 'https://magicseaweed.com/Finistere-South-Surfing/28/', 'https://magicseaweed.com/Morbihan-Loire-Atlantique-Surfing/29/', 'https://magicseaweed.com/Vendee-Surfing/30/', 'https://magicseaweed.com/Charente-Maritime-Surfing/31/', 'https://magicseaweed.com/Gironde-Surfing/32/', 'https://magicseaweed.com/Landes-Surfing/33/', 'https://magicseaweed.com/Hossegor-Surfing/34/', 'https://magicseaweed.com/Biarritz-Anglet-Surfing/35/', 'https://magicseaweed.com/La-Cote-Basque-Surfing/36/', 'https://magicseaweed.com/Mediterranean-France-West-Surfing/39/', 'https://magicseaweed.com/Southern-France-East-Surfing/40/',
                       'https://magicseaweed.com/Big-Island-Surfing/179/', 'https://magicseaweed.com/Kauai-Surfing/177/', 'https://magicseaweed.com/North-West-Maui-Surfing/178/', 'https://magicseaweed.com/Oahu-North-Shore-Surfing/176/', 'https://magicseaweed.com/Oahu-South-Shore-Surfing/366/']
    country = "ISRAEL"

    insert_areas(areas_links_ISRAEL, country)



    area_dict = {'Central-Tel-Aviv-Surfing': ['https://magicseaweed.com/Argamans-Beach-Surf-Report/4932/Historic/', 'https://magicseaweed.com/Bat-Yam-Surf-Report/3662/Historic/', 'https://magicseaweed.com/Beit-Yanai-Surf-Report/3783/Historic/', 'https://magicseaweed.com/Dolphinarium-Surf-Report/3660/Historic/', 'https://magicseaweed.com/Dromi-Herzlyia-Marina-Surf-Report/4744/Historic/', 'https://magicseaweed.com/Gazebbo-Beach-Club-Surf-Report/3980/Historic/', 'https://magicseaweed.com/Gordon-Beach-Surf-Report/8019/Historic/', 'https://magicseaweed.com/Ha-Rama-Beach-Surf-Report/5538/Historic/', 'https://magicseaweed.com/Hazuk-Beach-Surf-Report/3659/Historic/', 'https://magicseaweed.com/Hilton-Surf-Report/3658/Historic/', 'https://magicseaweed.com/Hof-Maravi-Surf-Report/3663/Historic/', 'https://magicseaweed.com/Marina-Herzelia-Surf-Report/3979/Historic/', 'https://magicseaweed.com/Netanya-Surf-Report/4558/Historic/', 'https://magicseaweed.com/Palmahim-Surf-Report/3975/Historic/', 'https://magicseaweed.com/Poleg-Beach-Surf-Report/5539/Historic/', 'https://magicseaweed.com/Rishon-Lezion-Surf-Report/3976/Historic/', 'https://magicseaweed.com/Sidna-Ali-Surf-Report/3986/Historic/', 'https://magicseaweed.com/Sironit-Beach-Surf-Report/4933/Historic/', 'https://magicseaweed.com/Tel-Baruch-North-Surf-Report/3978/Historic/', 'https://magicseaweed.com/Topsea-Surf-Report/3661/Historic/', 'https://magicseaweed.com/Zvulun-Herzelia-Surf-Report/3981/Historic/'], 'Southern-Surfing': ['https://magicseaweed.com/Ashdod-Surf-Report/4219/Historic/', 'https://magicseaweed.com/Ashqelon-Surf-Report/3811/Historic/', 'https://magicseaweed.com/Foxes-Point-Surf-Report/7992/Historic/', 'https://magicseaweed.com/Gute-Beach-Surf-Report/4732/Historic/', 'https://magicseaweed.com/Nachal-Yarkon-St-Surf-Report/5540/Historic/', 'https://magicseaweed.com/Zikim-Surf-Report/3977/Historic/'], 'Haifa-Surfing': ['https://magicseaweed.com/Achziv-Beach-Surf-Report/8990/Historic/', 'https://magicseaweed.com/Argaman-Beach-Surf-Report/6794/Historic/', 'https://magicseaweed.com/Atlit-Beach-Surf-Report/6795/Historic/', 'https://magicseaweed.com/Backdoor-Haifa-Surf-Report/3987/Historic/', 'https://magicseaweed.com/Betset-Surf-Report/4738/Historic/', 'https://magicseaweed.com/Caesarea-Surf-Report/3983/Historic/', 'https://magicseaweed.com/Haifa-The-Peak-Surf-Report/3671/Historic/', 'https://magicseaweed.com/Jisr-az-zarqa-Surf-Report/4934/Historic/', 'https://magicseaweed.com/Kadarim-Surf-Report/4866/Historic/', 'https://magicseaweed.com/Kiriat-Yam-Surf-Report/4753/Historic/', 'https://magicseaweed.com/Maagan-Michael-Surf-Report/3984/Historic/', 'https://magicseaweed.com/Nahsholim-Surf-Report/4880/Historic/', 'https://magicseaweed.com/Neve-Yam-Beach-Surf-Report/4935/Historic/', 'https://magicseaweed.com/Nirvana-Beach-Surf-Report/8282/Historic/', 'https://magicseaweed.com/Olga-Beach-Surf-Report/7913/Historic/', 'https://magicseaweed.com/Sdot-Yam-Surf-Report/3982/Historic/', 'https://magicseaweed.com/Shavei-Tzion-Surf-Report/8991/Historic/', 'https://magicseaweed.com/Sokolov-Beach-Surf-Report/4640/Historic/'], 'Red-Sea-Surfing': ['https://magicseaweed.com/Eilat-Surf-Report/8268/Historic/', 'https://magicseaweed.com/Sharm-El-Sheikh-Surf-Report/8274/Historic/']}

    insert_beaches(area_dict)

    beach_response = (grequests.get(url, headers=CONFIG['FAKE_USER_HEADER']) for url in area_dict['Central-Tel-Aviv-Surfing'])
    cond = [BeautifulSoup(response.text, "html.parser") for response in grequests.imap(beach_response, size=CONFIG['BATCH_SIZE'])]
    insert_conditions(cond)

# TODO : nettoyer le code.