from flask import Flask, request
from datetime import date

app = Flask(__name__)

# 今日の訪問者カウンター（簡易）
today = date.today()
visitor_count = 0

FORTUNE = {
    "aries": "今日は勢いが鍵となります。迷いや不安を感じても、一歩踏み出す勇気を持つことが、新しい道を開くでしょう。",
    "taurus": "丁寧な仕事ぶりや細やかな気配りが評価される一日です。",
    "gemini": "会話運が良好。言葉の中にチャンスあり。",
    "cancer": "優しさが運気を整えます。",
    "leo": "あなたが主役の日。堂々と。",
    "virgo": "整理整頓が開運アクション。",
    "libra": "冷静な判断が光ります。",
    "scorpio": "集中力が成果を生みます。",
    "sagittarius": "小さな冒険が吉。",
    "capricorn": "積み重ねが実を結ぶ日。",
    "aquarius": "ひらめきを大切に。",
    "pisces": "感受性が高まる日。"
}

SIGN_LABEL = {
    "aries": "牡羊座",
    "taurus": "牡牛座",
    "gemini": "双子座",
    "cancer": "蟹座",
    "leo": "獅子座",
    "virgo": "乙女座",
    "libra": "天秤座",
    "scorpio": "蠍座",
    "sagittarius": "射手座",
    "capricorn": "山羊座",
    "aquarius": "水瓶座",
    "pisces": "魚座",
}

@app.get("/")
def home():
    global visitor_count, today

    if date.today() != today:
        today = date.today()
        visitor_count = 0

    visitor_count += 1

    options = ""
    for k, v in SIGN_LABEL.items():
        options += f'<option value="{k}">{v}</option>'

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>あずにゃんこ星座占い</title>
<style>
body {{
  background: linear-gradient(135deg, #000, #1a0033);
  color: #fff;
  font-family: Arial, sans-serif;
}}
.card {{
  margin: 80px auto;
  width: 320px;
  padding: 20px;
  border-radius: 20px;
  background: rgba(255,255,255,0.1);
  box-shadow: 0 0 20px #ff2fb3;
}}
button {{
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  border-radius: 12px;
  border: none;
  font-weight: bold;
  background: linear-gradient(90deg, #ff2fb3, #18f2ff);
}}
</style>
</head>
<body>
<div class="card">
<h1>🐱 あずにゃんこ星座占い ✨</h1>
<p style="text-align:center;font-size:12px;color:#18f2ff;">
TODAY'S VISITORS ✦ {visitor_count}
</p>
<form action="/fortune">
<select name="sign">{options}</select>
<button type="submit">占う</button>
</form>
</div>
</body>
</html>"""

@app.get("/fortune")
def fortune():
    sign = request.args.get("sign", "aries")
    label = SIGN_LABEL.get(sign, "不明")
    text = FORTUNE.get(sign, "")

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>結果</title>
</head>
<body style="background:black;color:white;font-family:Arial">
<h1>{label}</h1>
<p>{text}</p>
<p><a href="/" style="color:#ff2fb3">戻る</a></p>
</body>
</html>"""
