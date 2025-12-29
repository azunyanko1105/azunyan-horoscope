from flask import Flask, request

app = Flask(__name__)

FORTUNE = {
    "aries": "今日は勢いが鍵となります。迷いや不安を感じても、一歩踏み出す勇気を持つことが、新しい道を開くでしょう。直感を信じて前へ進むことが大切です。",
    "taurus": "丁寧な仕事ぶりや細やかな気配りが周囲から高く評価される一日です。焦らず、一つ一つのタスクに心を込めて取り組むことで、確かな成果と信頼を得られます。",
    "gemini": "会話運が非常に良い日です。短いやり取りやふとした言葉の中に、今後のチャンスに繋がるヒントが隠されています。積極的にコミュニケーションを取りましょう。",
    "cancer": "身近な人に優しく接することで、心の平穏が訪れ、全体的な運気が整うでしょう。",
    "leo": "あなたが主役の一日です。自信を持って堂々と行動することで、周りの人々を惹きつけるでしょう。",
    "virgo": "身の回りの片付けや整理整頓が開運アクションとなります。",
    "libra": "バランス感覚が冴えわたる日です。冷静な視点が重要です。",
    "scorpio": "集中力を発揮できる一日です。深く掘り下げると成果があります。",
    "sagittarius": "小さな冒険が吉。新しい場所へ。",
    "capricorn": "積み重ねが実を結ぶ日です。",
    "aquarius": "ひらめきを大切に。メモを。",
    "pisces": "感受性が高まる日。音楽や映画が吉。"
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
    options = ""
    for k, v in SIGN_LABEL.items():
        options += f'<option value="{k}">{v}</option>'

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Y2K 星座占い</title>
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
<h1>星座占い ✨</h1>
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
<a href="/" style="color:#ff2fb3">戻る</a>
</body>
</html>"""

if __name__ == "__main__":
    app.run()