import MeCab, csv
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
            notify = {"title": '天気予報', "text": weather_news[0] + "\n\n" + weather_news[1]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify]
            })
            
        def say_today_weather(weather_news):
            """Slackの形式でJSONを返す"""
            notify = {"title": '天気予報', "text": weather_news[0]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify]
            })
                
        def say_tomorrow_weather(weather_news):
            notify = {"title": '天気予報', "text": weather_news[0]}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify]
            })
            
        def say_today_hourly_weather(weather_news):
            notify = {"title": '天気予報', "text": "今日1時間ごとの天気です。\n\n" + "\n".join(weather_news)}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify]
            })
            
        def say_tomorrow_hourly_weather(weather_news):
            notify = {"title": '天気予報', "text": "明日1時間ごとの天気です。\n\n" + "\n".join(weather_news)}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":slightly_smiling_face:",
            "attachments": [notify]
            })
            
        def say_error_message():
            notify = {"title": 'エラー', "text": "対応していない地域が含まれるか、メッセージが正しく入力されていません。"}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":confounded:",
            "attachments": [notify]
            })
            
        def say_hi():
            notify = {"title": '', "text": "はーい!"}
            return jsonify({
            "username": "Ama-Tatsu",
            "icon_emoji": ":grinning:",
            "attachments": [notify]
            })
            
        posted_data = PostedSlackApi(request.form)

        # ignore the slackbot if it post the message.
        if posted_data.user_name == "slackbot":
            return ''
            
        # language analysis.
        municipality = ''
        tagger_neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tagger_neologd.parse('')
        node = tagger_neologd.parseToNode(posted_data.text)
        word_list = []
        # extract the noun and adjective.
        while node:
            word_feature = node.feature.split(',')
            word = node.surface
            if word in municipality_dict:
                municipality = word
            elif bool(word) and word_feature[0] in ['名詞', '形容詞'] and word not in ['Ama-Tatsu', 'amat', 'amatatsu', 'あまたつ', 'amatatsu', '\n', 'です', 'ます', '。', 'あまたつ!', '!', '！']:
                word_list.append(word)
            node = node.next
            
        try:
            if bool([i for i in ['天気', 'てんき', '今日の天気', '明日の天気'] if i in word_list]):
                if bool([i for i in ['1時間ごと', '1時間', '一時間', '一時間ごと', '1時間毎', '一時間毎', '1', '１'] if i in word_list]):
                    if bool([i for i in ['明日', '明日の天気', 'あした'] if i in word_list]):
                        weather_news = ArrangeWeatherData().tomorrow_hourly_weather_news_format(municipality=municipality)
                        return say_tomorrow_hourly_weather(weather_news)
                    else:
                        weather_news = ArrangeWeatherData().today_hourly_weather_news_format(municipality=municipality)
                        return say_today_hourly_weather(weather_news)
                elif bool([i for i in ['今日', '今日の天気', 'きょう'] if i in word_list]):
                    weather_news = ArrangeWeatherData().today_weather_news_format(municipality=municipality)
                    return say_today_weather(weather_news)
                elif bool([i for i in ['明日', '明日の天気', 'あした'] if i in word_list]):
                    weather_news = ArrangeWeatherData().tomorrow_weather_news_format(municipality=municipality)
                    return say_tomorrow_weather(weather_news)
                else:
                    weather_news = ArrangeWeatherData().weather_news_format(municipality=municipality)
                    return say_weather_news(weather_news)
            elif bool(word_list) is False:
                return say_hi()
            else:
                return say_error_message()
        except:
            return say_error_message()
            
if __name__ == '__main__':
    # get the each municipality.
    municipality_dict = {}
    with open('municipality.csv', 'r') as municipality_file:
        reader = csv.reader(municipality_file)
        for municipality_data in reader:
            municipality_dict[municipality_data[0]] = municipality_data[1]
    app.debug = False
    app.run(host='0.0.0.0', port=5000)