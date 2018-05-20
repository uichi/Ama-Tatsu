#coding: utf-8
import csv
from scrape_news import WeatherData
    
class ArrangeWeatherData:

    # 市区町村ごとのURLを取得
    def get_municipality_data(self):
        municipality_dict = {}
        with open('municipality.csv', 'r') as municipality_file:
            reader = csv.reader(municipality_file)
            for municipality_data in reader:
                municipality_dict[municipality_data[0]] = municipality_data[1]
        return municipality_dict

    def weather_news_format(self, municipality):
        municipality_dict = self.get_municipality_data()
        weather_data = WeatherData(municipality_dict[municipality])
        today_weather_data = weather_data.scrape_today_weather()
        weather_news = []
        weather_news.append(municipality + "の今日の天気は" + today_weather_data[0] + "\n"\
                            "最高気温は" + today_weather_data[1] + "度\n"\
                            "最低気温は" + today_weather_data[2] + "度です。")

        tomorrow_weather_data = weather_data.scrape_tomorrow_weather()
        weather_news.append(municipality + "の明日の天気は" + tomorrow_weather_data[0] + "\n"\
                            "最高気温は" + tomorrow_weather_data[1] + "度\n"\
                            "最低気温は" + tomorrow_weather_data[2] + "度です。")
        return weather_news
    
    def today_weather_news_format(self, municipality):
        municipality_dict = self.get_municipality_data()
        weather_data = WeatherData(municipality_dict[municipality])
        today_weather_data = weather_data.scrape_today_weather()
        weather_news = []
        weather_news.append(municipality + "の今日の天気は" + today_weather_data[0] + "\n"\
                            "最高気温は" + today_weather_data[1] + "度\n"\
                            "最低気温は" + today_weather_data[2] + "度です。")
        return weather_news
        
    def tomorrow_weather_news_format(self, municipality):
        municipality_dict = self.get_municipality_data()
        weather_data = WeatherData(municipality_dict[municipality])
        tomorrow_weather_data = weather_data.scrape_tomorrow_weather()
        weather_news = []
        weather_news.append(municipality + "の明日の天気は" + tomorrow_weather_data[0] + "\n"\
                            "最高気温は" + tomorrow_weather_data[1] + "度\n"\
                            "最低気温は" + tomorrow_weather_data[2] + "度です。")
        return weather_news
        
    def today_hourly_weather_news_format(self, municipality):
        municipality_dict = self.get_municipality_data()
        weather_data = WeatherData(municipality_dict[municipality]+'1hour.html')
        hourly_weather_data = weather_data.scrape_today_hourly_weather()
        weather_news = []
        for i, hourly_time in enumerate(hourly_weather_data[0]):
            hourly_weather = str(int(hourly_time)-1) + "時 : "+\
                                hourly_weather_data[1][i]+\
                                ', 気温は' + hourly_weather_data[2][i]+'℃'\
                                ', 降水確率は' + hourly_weather_data[3][i] + '％です。'
            weather_news.append(hourly_weather)
        return weather_news
        
    def tomorrow_hourly_weather_news_format(self, municipality):
        municipality_dict = self.get_municipality_data()
        weather_data = WeatherData(municipality_dict[municipality]+'1hour.html')
        hourly_weather_data = weather_data.scrape_tomorrow_hourly_weather()
        weather_news = []
        for i, hourly_time in enumerate(hourly_weather_data[0]):
            hourly_weather = str(int(hourly_time)-1) + "時 : "+\
                                hourly_weather_data[1][i]+\
                                ', 気温は' + hourly_weather_data[2][i]+'℃'\
                                ', 降水確率は' + hourly_weather_data[3][i] + '％です。'
            weather_news.append(hourly_weather)
        return weather_news