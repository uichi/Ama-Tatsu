import requests, lxml, cchardet
from bs4 import BeautifulSoup

class WeatherData:

    def __init__(self, url):
        response = requests.get(url)
        # character code measures.
        response_encoding = cchardet.detect(response.content)["encoding"]
        self.soup = BeautifulSoup(response.content, 'lxml', from_encoding=response_encoding)

    def scrape_today_weather(self):
        today_weather = self.soup.find('section', class_='today-weather').find('p', class_='weather-telop').get_text()
        today_high_temp = self.soup.find('section', class_='today-weather').find('dd', class_='high-temp').find('span', class_='value').get_text()
        today_low_temp = self.soup.find('section', class_='today-weather').find('dd', class_='low-temp').find('span', class_='value').get_text()
        return today_weather, today_high_temp, today_low_temp

    def scrape_tomorrow_weather(self):
        tomorrow_weather = self.soup.find('section', class_='tomorrow-weather').find('p', class_='weather-telop').get_text()
        tomorrow_high_temp = self.soup.find('section', class_='tomorrow-weather').find('dd', class_='high-temp').find('span', class_='value').get_text()
        tomorrow_low_temp = self.soup.find('section', class_='tomorrow-weather').find('dd', class_='low-temp').find('span', class_='value').get_text()
        return tomorrow_weather, tomorrow_high_temp, tomorrow_low_temp

    def scrape_today_hourly_weather(self):
        today_hourly_time = [time.get_text() for time in self.soup.find_all('tr', class_='hour')[0].find_all('td')]
        today_hourly_weather = [weather.get_text() for weather in self.soup.find_all('tr', class_='weather')[0].find_all('p')]
        today_hourly_temp = [temp.get_text() for temp in self.soup.find_all('tr', class_='temperature')[0].find_all('span')]
        today_hourly_precipitation = [precipitation.get_text() for precipitation in self.soup.find_all('tr', class_='prob-precip')[0].find_all('td')]
        return today_hourly_time, today_hourly_weather, today_hourly_temp, today_hourly_precipitation

    def scrape_tomorrow_hourly_weather(self):
        tomorrow_hourly_time = [time.get_text() for time in self.soup.find_all('tr', class_='hour')[1].find_all('td')]
        tomorrow_hourly_weather = [weather.get_text() for weather in self.soup.find_all('tr', class_='weather')[1].find_all('p')]
        tomorrow_hourly_temp = [temp.get_text() for temp in self.soup.find_all('tr', class_='temperature')[1].find_all('span')]
        tomorrow_hourly_precipitation = [precipitation.get_text() for precipitation in self.soup.find_all('tr', class_='prob-precip')[1].find_all('td')]
        return tomorrow_hourly_time, tomorrow_hourly_weather, tomorrow_hourly_temp, tomorrow_hourly_precipitation