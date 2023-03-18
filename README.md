# Magicseeweed.com

## Description
This is a web scraping project that extracts historic beach data in Israel from Magicseeweed.com.
The project aims to collect as much detail as possible for each data point, including wave height, wind speed, and temperature.

## Data Source
The data source used in this project is Magicseeweed.com.

Magicseaweed.com is a website that provides surf forecasting and related information for beaches around the world.
It offers up-to-date data on wave height, swell direction, wind speed, tide times, and other relevant metrics to help surfers, windsurfers, and kitesurfers plan their sessions.

The data is not publicly available via an API.

## Requirements
[List all the requirements and dependencies needed to run the code. Include a requirements.txt file with all the necessary packages and versions.]

`pip install requirements.txt`

`pip install selenium`

`pip install webdriver-manager`

## How to Run
Install the required packages using pip install -r requirements.txt.
Run the main Python script using python main.py.
The script will collect data from Magicseeweed.com and print the results in the **standard output/logfile**

## Project Structure
main.py: The main script that initiates the web scraping process.
bs4_scrapping.py: Contains the functions for web scraping using requests and BeautifulSoup.
selenium_scrapping.py: Contains the functions for web scraping using Selenium.

## Contributors
Claudia Palierne
Mathias Kammoun

## Usage
[Include instructions on how to run the code, including any command-line arguments or configuration settings that need to be set.]
The code can be run from command line or from any IDE like PyCharm.

## Results
[Include a summary of the data that was scraped, including any interesting patterns or insights that were discovered.]
Milestone 1 : For every beach on the coast of Israel and for every 3 hours every day of the week past the execution, the code prints the following information:
* weather ()
* temperature (in Celsius)
* swell (wave quality indicator)
* rating (wave quality indicator)
* steady_speed (one of two wind speed)
* direction (indicators for wind direction)

## Future Work
The next steps of this project will aim to store the printed values into a relevant data structure and perfom an analysis :
Given the past and current weather data, outputs the best spot in the country to go surf.

## References
* Selenium :
[medium.com](https://medium.com/pythoneers/web-scraping-using-selenium-python-6c511258ab50#:~:text=It%20is%20the%20process%20of,can%20scrape%20dynamic%20web%20easily)

* BeautifulSoup and HTML:
[realpython.com](https://realpython.com/beautiful-soup-web-scraper-python/)