import requests
from bs4 import BeautifulSoup


class WeatherOfCity:
    def __init__(self, name_of_city: str):
        self.__name_of_city = name_of_city
        self.__get_weather_info()

    def __get_weather_info(self):
        link = "https://www.wunderground.com/weather/ru/{}/".format(self.__name_of_city)
        r = requests.get(link)

        page = r.text

        soup = BeautifulSoup(page, "html.parser")
        wclass = "wu-value wu-value-to"
        temp_span = soup.find("span", {"class": wclass})

        temp_in_fahrenheit = int(temp_span.text)
        self.__temp_in_celsius = int(5 / 9 * (temp_in_fahrenheit - 32))

        weather_span = soup.find("div", {"class": "condition-icon small-6 medium-12 columns"})
        self.__weather = weather_span.text

    def print_temp(self):
        print("Temperature in {} is: ".format(self.__name_of_city), self.__temp_in_celsius)

    def print_weather(self):
        print("The weather in is:", self.__weather)
