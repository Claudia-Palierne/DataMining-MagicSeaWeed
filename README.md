# Magicseeweed.com

## Description

This is a web scraping project that extracts Surf Forecast data from the website [MagicSeaWeed.com](https://magicseaweed.com/).
The project aims to collect as much detail as possible for each data point, including wave height, wind speed (gust and steady speed), and temperature.

## Data Source

The data source used in this project is Magicseeweed.com.

Magicseaweed.com is a website that provides surf forecasting and related information for beaches around the world.
It offers up-to-date data on wave height, swell direction, wind speed, tide times, and other relevant metrics to help surfers, windsurfers, and kitesurfers plan their sessions.

The data is not publicly available via an API.

## Requirements

Please run the following in order to install all the required modules that the code to run :

```pip install requirements.txt```

## How to Run

* Install the required packages running the commands above (Requirements). 
* Run the main Python script using python main.py withthe following options passed as arguments :
  - `-mode` : whether should the data be print in the stdout or store in a SQL database (more information about this option below)
  - `-country` : the country from which you want to extract the data : Hawaii, France or Israel. You can also extract all of them with choosing the "ALL" option.

EXAMPLE : main.py -mode database -country Hawaii will print to the stdout all the data from every beach in Hawaii.


## Project Structure

* main.py: The main script that initiates the web scraping process. 
* one_beach_scrapping.py: Contains the functions for retrieving the data of interest (detailed below) for one url page. 
* url_extraction.py: Contains the functions for getting all beaches urls using Selenium.
* database.py : containes the function related to SQL, i.e. create database and table and inserting the values.
* conf.json : the configuration file read by all the .py
* conf_sql.json : the configuration file read for the sql queries.

## Database Structure

If you choose the `-mode database` option while running the script then, it will create a database named MagicSeaWeed.
The tables are constructed in the following manner:
![SQL_diagram](ERD.png)

## Contributors

<a href="https://www.linkedin.com/in/claudia-palierne/">
  <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn logo" style="width:15px;height:15px;">
</a>
Claudia Palierne 


<a href="https://www.linkedin.com/in/mathias-kammoun/">
  <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn logo" style="width:15px;height:15px;">
</a>
Mathias Kammoun 

## Usage

The code can be run from command line or from any IDE like PyCharm.

## Results

Milestone 2 : For every beach in a given country coast and for every 3 hours every day of the week past the execution, the code prints/store the following information:
* weather
* temperature (in Celsius)
* swell : min and maximum of the wave height
* surfability (wave quality indicator)
* steady speed wind (in KpH)
* gust speed wind  (in KpH)
* direction : indicators for wind direction and rotation

## Future Work

The next steps of this project will aim to create an API and perform an analysis :
Given the past and current weather data, outputs the best spot in the country to go surf.

## References

* Selenium :
[medium.com](https://medium.com/pythoneers/web-scraping-using-selenium-python-6c511258ab50#:~:text=It%20is%20the%20process%20of,can%20scrape%20dynamic%20web%20easily)
[zenrows](https://www.zenrows.com/blog/scraping-javascript-rendered-web-pages#the-disadvantage-of-using-selenium)

* BeautifulSoup and HTML:
[realpython.com](https://realpython.com/beautiful-soup-web-scraper-python/)