import one_beach_scrapping
import json
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
    `beach_id` int(11) NOT NULL,
    `timestamp` date NOT NULL,
    `weather_id` int(11) NOT NULL,
    `wave_height_min(m)` int(11) NOT NULL,
    `wave_height_max(m)` int(11) NOT NULL,
    `temperature(C)` int(11) NOT NULL,
    `steady_wind_speed(kph)` int(11) NOT NULL,
    `gust_wind_speed(kph)` int(11) NOT NULL,
    `wind_direction(degree)` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (beach_id) REFERENCES Beaches(id),
    FOREIGN KEY (weather_id) REFERENCES Weathers(id)
    ) ENGINE=InnoDB""")

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
    cnx = mysql.connector.connect(user='scott', database='employees')
    cursor = cnx.cursor()
    beach_info = one_beach_scrapping.beach_historic(beach_soup)
    for i in range():
        for j in range():
            cursor.execute(f"""INSERT INTO Conditions 
            VALUES (DEFAULT, {len(beach_info['name'])}, {beach_info['timestamp'][i * CONFIG['DAYS_IN_WEEK'] + j]}, {beach_info['weather'][i * CONFIG['DAYS_IN_WEEK'] + j]},
            {beach_info['swell'][i * CONFIG['DAYS_IN_WEEK'] + j][0]}, {beach_info['swell'][i * CONFIG['DAYS_IN_WEEK'] + j][1]}, {beach_info['temperature'][i * CONFIG['DAYS_IN_WEEK'] + j]}, 
            {beach_info['steady_wind_speed'][i * CONFIG['DAYS_IN_WEEK'] + j]}, {beach_info['gust_wind_speed'][i * CONFIG['DAYS_IN_WEEK'] + j]}, {beach_info['direction'][i * CONFIG['DAYS_IN_WEEK'] + j]})
            """)
    cnx.commit()
    cursor.close()
    cnx.close()
