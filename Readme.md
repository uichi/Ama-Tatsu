# About Ama-Tatsu
Ama-Tatsu is the weather forecaster bot which work in the slack. This bot scrape the information in the weather news site.

# How to use
Configure the Outgoing WebHooks in your slack.

Set the subject channel, Trigger Word(s) and URL(s).

Trigger Word(s) is ```Ama-Tatsu,amatatsu,ama-tatsu,amat,あまたつ```.

After the git clone, you type as follws.

```
python3  stationed.py
```

Type ```ama-tatsu、千代田区の天気を教えて```.

Ama-Tatsu reply as follows.

```
天気予報
千代田区の今日の天気は晴
最高気温は24度
最低気温は15度です。千代田区の明日の天気は晴
最高気温は26度
最低気温は15度です。
```

# Weater news area
If you see the municipality.csv, you can know the compatible area. In case you would like to add the other area, help yourself.

