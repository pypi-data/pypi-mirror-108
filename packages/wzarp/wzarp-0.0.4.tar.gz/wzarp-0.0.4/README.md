# Wzarp 

Wzarp is a Python library for outputting of weather of Russian cities to the console.

## Installation
Use the package manager [pip](https://pypi.org/project/wzarp/0.0.1/) to install wzarp.

```bash
pip install wzarp
```
## Usage

```python
from wzarp.CityWeather import WeatherOfCity

city = input("Enter the name of the city: ")

city_weather = WeatherOfCity(city) # creating object of class WeatherOfCity
# During the initialization of an object you need 
# to put proper name of the city in English

city_weather.print_weather() # returns weather in chosen city

city_weather.print_temp() # returns temperature in chosen city
```