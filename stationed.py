#coding: utf-8
import logging, MeCab, time
from flask import Flask, request, jsonify
from scrape_news import WeatherData
from arrange_news import ArrangeWeatherData

app = Flask(__name__)

# message class of the Slack.
class PostedSlackApi(object):

    def __init__(self, params):
        self.token = params["token"]
        self.team_id = params["team_id"]
        self.channel_id = params["channel_id"]
        self.channel_name = params["channel_name"]
        self.timestamp = params["timestamp"]
        self.user_id = params["user_id"]
        self.user_name = params["user_name"]
        self.text = params["text"]
        self.trigger_word = params["trigger_word"]

    def __str__(self):
        posted_data = self.__class__.__name__
        posted_data += "@{0.token}[channel={0.channel_name}, user={0.user_name}, text={0.text}]".format(self)
        return posted_data
        
class Reporter:
    
    @app.route('/', methods=['POST'])
    def ama_tatsu():
        
        global municipality
        def say_weather_news(weather_news):
            """Slackの形式でJSONを返す"""
            notify_weather = {"title": '天気予報', "text": weather_news[0] + "\n\n" + weather_news[1]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify_weather]
            })
            
        def say_today_weather(weather_news):
            """Slackの形式でJSONを返す"""
            notify_today_weather = {"title": '天気予報', "text": weather_news[0]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify_today_weather]
            })
                
        def say_tomorrow_weather(weather_news):
            notify_tomorrow_weather = {"title": '天気予報', "text": weather_news[0]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify_tomorrow_weather]
            })
            
        def say_today_hourly_weather(weather_news):
            notify_tomorrow_weather = {"title": '天気予報', "text": "今日1時間ごとの天気です。\n\n" + "\n".join(weather_news)}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify_tomorrow_weather]
            })
            
        def say_tomorrow_hourly_weather(weather_news):
            notify_tomorrow_weather = {"title": '天気予報', "text": "明日1時間ごとの天気です。\n\n" + "\n".join(weather_news)}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify_tomorrow_weather]
            })
            
        posted_data = PostedSlackApi(request.form)
        logging.debug(posted_data)

        # ignore the slackbot.
        if posted_data.user_name == "slackbot":
            return ''
            
        # language analysis.
        municipality = ''
        municipality_dict = ArrangeWeatherData().get_municipality_data()
        tagger_neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tagger_neologd.parse('')
        node = tagger_neologd.parseToNode(posted_data.text)
        word_list = []
        while node:
            word_feature = node.feature.split(',')
            word = node.surface
            if word in municipality_dict:
                municipality = word
            elif bool(word) and word_feature[0] in ['名詞', '形容詞'] and word not in ['Ama-Tatsu', 'amat', 'amatatsu', 'あまたつ', 'amatatsu', '\n', 'です', 'ます', '。', '', '']:
                word_list.append(word)
            node = node.next
            
        if '天気' in ''.join(word_list):
            if bool([i for i in ['1時間ごと', '1時間', '一時間', '一時間ごと', '1時間毎', '一時間毎'] if i in word_list]):
                if bool([i for i in ['今日', '今日の天気'] if i in word_list]):
                    weather_news = ArrangeWeatherData().today_hourly_weather_news_format(municipality=municipality)
                    return say_today_hourly_weather(weather_news)
                elif bool([i for i in ['明日', '明日の天気'] if i in word_list]):
                    weather_news = ArrangeWeatherData().tomorrow_hourly_weather_news_format(municipality=municipality)
                    return say_tomorrow_hourly_weather(weather_news)
            elif bool([i for i in ['今日', '今日の天気'] if i in word_list]):
                weather_news = ArrangeWeatherData().today_weather_news_format(municipality=municipality)
                return say_today_weather(weather_news)
            elif bool([i for i in ['明日', '明日の天気'] if i in word_list]):
                weather_news = ArrangeWeatherData().tomorrow_weather_news_format(municipality=municipality)
                return say_tomorrow_weather(weather_news)
            else:
                weather_news = ArrangeWeatherData().weather_news_format(municipality=municipality)
                return say_weather_news(weather_news)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
