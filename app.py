from flask import Flask, request
from datetime import date
import calendar

app = Flask(__name__)

# ===== Google AdSense コード (ここに定義) =====
ADS_CODE = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6112085882585441"
     crossorigin="anonymous"></script>
"""

# ===== 共通デザイン設定 (CSS) =====
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Shippori+Mincho:wght@400;600&display=swap');

body {
    background-color: #050505;
    background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://www.transparenttextures.com/patterns/black-mamba.png');
    color: #e2c08d;
    font-family: 'Shippori Mincho', serif;
    display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 40px 0;
}

.marble-panel {
    width: 90%; max-width: 650px; padding: 70px 50px;
    background: #0a0a0a; border: 1px solid #3d3326;
    box-shadow: 0 0 0 6px #0a0a0a, 0 0 0 10px #8c6d3e, 0 50px 100px rgba(0,0,0,1);
    text-align: center; margin-bottom: 50px;
}

h1 { font-family: 'Cinzel', serif; font-size: 52px; letter-spacing: 12px; margin: 0; color: #c9a063; }
.sub-title { font-family: 'Cinzel', serif; font-size: 16px; color: #63543e; margin-bottom: 50px; letter-spacing: 6px; }

.latin-quote { font-family: 'Cinzel', serif; font-size: 2.6em; line-height: 1.25; color: #f5e6b3; margin: 40px 0 20px 0; font-weight: 700; }
.jp-meaning { font-size: 2.0em; color: #8c6d3e; margin-bottom: 50px; font-weight: 600; line-height: 1.5; }
.fortune-text { font-size: 2.0em; line-height: 1.8; margin: 40px 0; color: #e2d1b9; text-align: left; border-left: 3px solid #8c6d3e; padding-left: 25px; }

.divider { width: 120px; height: 1px; background: #8c6d3e; margin: 40px auto; }

select, button {
    width: 100%; padding: 22px; background: #111; border: 1px solid #3d3326; color: #c9a063;
    font-family: 'Cinzel', serif; font-size: 22px; cursor: pointer;
}
button { background: #1a1510; border-color: #8c6d3e; font-weight: bold; margin-top: 30px; }

.lucky-box { border-top: 1px solid #2a241b; padding-top: 40px; margin-top: 50px; font-size: 2.2em; color: #f5e6b3; }
.label-gold { font-family: 'Cinzel', serif; font-size: 16px; color: #8c6d3e; display: block; margin-bottom: 15px; letter-spacing: 3px; }

.calendar-panel {
    width: 90%; max-width: 450px; padding: 30px;
    background: rgba(10, 10, 10, 0.9); border: 1px solid #3d3326; text-align: center;
}
table.cal { width: 100%; border-collapse: collapse; font-family: 'Cinzel', serif; font-size: 18px; }
.cal th { color: #8c6d3e; padding: 12px; }
.cal td { padding: 12px; color: #444; }
.cal .today { color: #c9a063; font-weight: bold; outline: 1px solid #c9a063; }

a { color: #63543e; text-decoration: none; font-size: 1.5em; letter-spacing: 4px; border-bottom: 1px solid; }
</style>
"""

# ===== データ定義 =====
SIGN_DATA = {
    "aries": {"label": "ARIES", "jp": "牡羊座"},
    "taurus": {"label": "TAURUS", "jp": "牡牛座"},
    "gemini": {"label": "GEMINI", "jp": "双子座"},
    "cancer": {"label": "CANCER", "jp": "蟹座"},
    "leo": {"label": "LEO", "jp": "獅子座"},
    "virgo": {"label": "VIRGO", "jp": "乙女座"},
    "libra": {"label": "LIBRA", "jp": "天秤座"},
    "scorpio": {"label": "SCORPIO", "jp": "蠍座"},
    "sagittarius": {"label": "SAGITTARIUS", "jp": "射手座"},
    "capricorn": {"label": "CAPRICORN", "jp": "山羊座"},
    "aquarius": {"label": "AQUARIUS", "jp": "水瓶座"},
    "pisces": {"label": "PISCES", "jp": "魚座"},
}

# 40個のラッキーアイテム（日常的・実用的なもの）
LUCKY_ITEMS = [
    "折りたたみ傘", "ハンカチ", "ボールペン", "ミントタブレット", "エコバッグ",
    "ワイヤレスイヤホン", "文庫本", "ハンドクリーム", "腕時計", "コインケース",
    "リップバーム", "スマートフォンの充電器", "眼鏡拭き", "マイボトル", "付箋",
    "のど飴", "キーホルダー", "名刺入れ", "手帳", "ブックマーク",
    "除菌スプレー", "モバイルバッテリー", "トートバッグ", "お守り", "修正テープ",
    "ヘアゴム", "目薬", "マスクケース", "ミニタオル", "パスケース",
    "USBメモリ", "ペンケース", "スケジュール帳", "懐中電灯", "印鑑ケース",
    "ソーイングセット", "ばんそうこう", "鏡", "カードケース", "靴べら"
]

LATIN_QUOTES = [
    {"lt": "Abeunt studia in mōrēs.", "jp": "熱意は習慣に変わる。"},
    {"lt": "Age quod agis.", "jp": "一意専心。"},
    {"lt": "Ālea jacta est.", "jp": "賽は投げられた。"},
    {"lt": "Amīcitia sāl vītae.", "jp": "友情は人生の塩。"},
    {"lt": "Amor caecus.", "jp": "恋は盲目。"},
    {"lt": "Amor magister optimus.", "jp": "愛は最良の教師。"},
    {"lt": "Amor omnibus īdem.", "jp": "愛はすべてに等しい。"},
    {"lt": "Amor tussisque nōn cēlantur.", "jp": "愛と咳は隠せない。"},
    {"lt": "Aquila nōn captat muscam.", "jp": "わしははえをつかまえない。"},
    {"lt": "Ars longa, vīta brevis.", "jp": "技は長く人生は短い。"},
    {"lt": "Carpe diem.", "jp": "今日という日を摘め。"},
    {"lt": "Cōgitō ergo sum.", "jp": "われ思うゆえにわれあり。"},
    {"lt": "Disce gaudēre.", "jp": "楽しむことを学べ。"},
    {"lt": "Docēre est discere.", "jp": "教えることは学ぶことである。"},
    {"lt": "Dum spīrō spērō.", "jp": "息をするあいだ希望をもつ。"},
    {"lt": "Errāre hūmānum est.", "jp": "間違うことは人間的である。"},
    {"lt": "Expende Hannibalem.", "jp": "ハンニバルを量ってみよ。"},
    {"lt": "Experientia docet.", "jp": "経験は教える。"},
    {"lt": "Festīnā lentē.", "jp": "ゆっくり急げ。"},
    {"lt": "Fīat lux.", "jp": "光あれ。"},
    {"lt": "Flōs ūnus nōn facit hortum.", "jp": "一輪の花は庭を造らない。"},
    {"lt": "Fluctuat nec mergitur.", "jp": "たゆたえども沈まず。"},
    {"lt": "Fortūna caeca.", "jp": "運命は盲目。"},
    {"lt": "Gutta cavat lapidem.", "jp": "滴は石に穴をあける。"},
    {"lt": "Homō sum.", "jp": "私は人間である。"},
    {"lt": "In varietāte concordia.", "jp": "多様性の中の調和。"},
    {"lt": "Justitiam cole et pietātem.", "jp": "正義と敬虔を重んじよ。"},
    {"lt": "Labor omnia vīcit.", "jp": "労働がすべてに打ち勝った。"},
    {"lt": "Manus manum lavat.", "jp": "手は手を洗う。"},
    {"lt": "Mementō morī.", "jp": "死を想え。"},
    {"lt": "Mens sāna in corpore sānō.", "jp": "健全な精神は健全な肉体に宿る。"},
    {"lt": "Mors certa, hōra incerta.", "jp": "死は確実、時は不確実。"},
    {"lt": "Nē sīs miser ante tempus.", "jp": "時が来るより先に惨めになるな。"},
    {"lt": "Ōdī et amō.", "jp": "われ憎みかつ愛す。"},
    {"lt": "Omnia tempus habent.", "jp": "万事ときを持つ。"},
    {"lt": "Omnia vānitās.", "jp": "一切虚無。"},
    {"lt": "Omnia vincit Amor.", "jp": "愛はすべてに勝つ。"},
    {"lt": "Per aspera ad astra.", "jp": "困難を超えて栄光へ。"},
    {"lt": "Post nūbila Phoebus.", "jp": "雨のち晴れ。"},
    {"lt": "Quō vādis?", "jp": "あなたはどこに行くのか。"},
    {"lt": "Sequere nātūram.", "jp": "自然に従え。"},
    {"lt": "Serit arbōrēs.", "jp": "木を植える。"},
    {"lt": "Tacēre quī nescit, nescit loquī.", "jp": "沈黙を知らぬ者は語ることを知らぬ。"},
    {"lt": "Tempus fugit.", "jp": "時は逃げる。"},
    {"lt": "Varietās dēlectat.", "jp": "多様性は喜ばせる。"},
    {"lt": "Vēnī vīdī vīcī.", "jp": "来た、見た、勝った。"},
    {"lt": "Vēritās vincit.", "jp": "真理は勝利する。"},
    {"lt": "Vīve hodiē.", "jp": "今日生きよ。"},
    {"lt": "Vīvere est cōgitāre.", "jp": "生きることは考えることである。"},
    {"lt": "Vox populī vox deī.", "jp": "人民の声は神の声。"},
    {"lt": "Ad astra per aspera.", "jp": "苦難を通じ栄光へ。"},
    {"lt": "Aequat omnes cinis.", "jp": "灰になれば人に違いなし。"},
    {"lt": "Amor mūsicam docet.", "jp": "愛は音楽を教える。"},
    {"lt": "Animum rege.", "jp": "心を抑えよ。"},
    {"lt": "Audentēs Fortūna juvat.", "jp": "運命は勇気ある者を助ける。"},
    {"lt": "Aurea mediocritās.", "jp": "黄金の中庸。"},
    {"lt": "Aut disce, aut discēde.", "jp": "学べ、さもなくば去れ。"},
    {"lt": "Calamus gladiō fortior.", "jp": "ペンは剣よりも強し。"},
    {"lt": "Cor ad cor loquitur.", "jp": "心が心に語りかける。"},
    {"lt": "Dabit deus hīs quoque fīnem.", "jp": "神はこの不幸にも終わりを与えよう。"},
    {"lt": "Disce libens.", "jp": "楽しく学べ。"},
    {"lt": "Dīvidē et imperā.", "jp": "分割して統治せよ。"},
    {"lt": "Et arma et verba vulnerant.", "jp": "武器も言葉も傷つける。"},
    {"lt": "Etiam senī est discendum.", "jp": "老人もまた学ばねばならない。"},
    {"lt": "Ex concordiā fēlīcitās.", "jp": "調和から幸福が生まれる。"},
    {"lt": "Ex nihilō nihil fit.", "jp": "無から有は生じない。"},
    {"lt": "Ex ore parvulorum veritas.", "jp": "子どもの口から真理。"},
    {"lt": "Exempla docent, nōn jubent.", "jp": "模範は教える。"},
    {"lt": "Experientia docet.", "jp": "経験は教える。"},
    {"lt": "Fidēs facit fidem.", "jp": "信頼は信頼を作る。"},
    {"lt": "Fīnis corōnat opus.", "jp": "終わりは作品を飾る。"},
    {"lt": "Fit via vī.", "jp": "力で道が開ける。"},
    {"lt": "Forsan et haec ōlim meminisse juvābit.", "jp": "今の苦しみを思い出して喜べるときがくる。"},
    {"lt": "Honōs alit artēs.", "jp": "名誉は学問・芸術を養う。"},
    {"lt": "Ignis aurum probat.", "jp": "火は黄金を証明する。"},
    {"lt": "In vīnō vēritās.", "jp": "酒の中に真理あり。"},
    {"lt": "Incipe. Dimidium est facti coepisse.", "jp": "始めれば仕事の半分は片付いている。"},
    {"lt": "Inter arma silent Mūsae.", "jp": "戦争の間ミューズは沈黙する。"},
    {"lt": "Īra furor brevis.", "jp": "怒りは短い狂気。"},
    {"lt": "Justitia saepe causa gloriae est.", "jp": "正義はしばしば栄光の原因である。"},
    {"lt": "Librī mūtī magistrī.", "jp": "本は寡黙な教師。"},
    {"lt": "Merentem laudāre justitia est.", "jp": "ほめるに値する者をほめるのが正しい。"},
    {"lt": "Multa petentibus dēsunt multa.", "jp": "多くを望む者には多くが欠乏する。"},
    {"lt": "Nātūra nōn facit saltum.", "jp": "自然は跳躍しない。"},
    {"lt": "Nēmō fortūnam jūre accūsat.", "jp": "誰も運命を正当に非難できない。"},
    {"lt": "Nescit vox missa reverti.", "jp": "放たれた言葉は戻ることを知らない。"},
    {"lt": "Nihil sub sōle novum.", "jp": "太陽の下に新しいものはない。"},
    {"lt": "Nulla diēs sine lineā.", "jp": "一本の線も引かない日は一日もない。"},
    {"lt": "Nunc aut numquam.", "jp": "今やるか、一生やらないか。"},
    {"lt": "Nunc omnia rīdent.", "jp": "今万物が微笑んでいる。"},
    {"lt": "Omnēs ūna nox manet.", "jp": "万人を一夜が待ち受ける。"},
    {"lt": "Omnis habet sua dōna diēs.", "jp": "毎日その日の贈り物がある。"},
    {"lt": "Per angusta ad augusta.", "jp": "苦境を通じ神聖へ。"},
    {"lt": "Prōtinus vīve.", "jp": "直ちに生きよ。"},
    {"lt": "Sōl omnibus lūcet.", "jp": "太陽は万物を照らす。"},
    {"lt": "Spem successus alit.", "jp": "成功は希望を養う。"},
    {"lt": "Ūnus prō omnibus, omnēs prō ūnō.", "jp": "一人はみんなのために、みんなは一人のために。"},
    {"lt": "Ūsus est altera nātūra.", "jp": "習慣は第二の天性。"},
    {"lt": "Vēritātis simplex ōrātiō est.", "jp": "真理の言葉は単純である。"},
    {"lt": "Virtūs mille scūta.", "jp": "勇気は千の盾。"}
]

FORTUNE = {
    "aries": ["【Impetus】内なる情熱に従え。停滞していた運命の歯車は、あなたの勇気によってのみ動き出す。", "【Prudentia】今日は盾を掲げよ。無謀なる進軍よりも、静かなる守護が明日の勝利を約束する。", "【Inceptum】小さな火種を絶やすな。今この瞬間の挑戦が、後に消えぬ自信の灯火となる。"],
    "taurus": ["【Silentium】喧騒を離れ、己の深淵を覗け。真実の答えは常に、静かなる時間の中に隠されている。", "【Moderatio】無理を強いるな。自然の理に身を任せる選択こそが、最善の果実をもたらすだろう。", "【Affinitas】身近な者の言葉に耳を傾けよ。何気ない会話の中に、運命を切り拓く鍵が眠っている。"],
    "gemini": ["【Verbum】放たれた言葉は戻らぬ矢。その一言が運命を左右する。今日は語る前に思索せよ。", "【Fortuitus】予期せぬ出会いを尊べ。偶然という名の神の悪戯が、あなたに新たな視界を授ける。", "【Ratio】情報の海を整理せよ。知性を羅針盤とすれば、立ち込めていた迷いの霧は晴れるだろう。"],
    "cancer": ["【Animus】己の感情に偽りを持つな。心の震えをそのまま受け入れることで、真の安らぎが訪れる。", "【Caritas】他者を想う慈しみの心を持て。その献身は巡り巡って、あなた自身の魂を救う光となる。", "【Stabilitas】今は城壁を固める時。守りに徹することで、揺るぎない精神の基盤が築かれるだろう。"],
    "leo": ["【Magnificentia】王者の如く堂々と振る舞え。己を信じて歩む道こそが、黄金の未来へと通じている。", "【Dignitas】主役はあなたである。しかし、他者を照らさぬ輝きは、やがて孤独という影を生む。", "【Gloria】焦る必要はない。真の評価は常に後からついてくる。今はただ、高潔なる意志を貫け。"],
    "virgo": ["【Subtilitas】細部に神は宿る。徹底した気配りと秩序への献身が、凡庸なる結果を卓越へと変える。", "【Perfectio】完璧の檻から抜け出せ。不完全さを受け入れる度量が、真の成功を引き寄せる鍵となる。", "【Ordo】まずは身辺を整えよ。環境の調和を取り戻すことで、濁っていた心にも余裕が生まれる。"],
    "libra": ["【Aequitas】調和こそが最大の美徳である。極端を避け、中道を選ぶことで、運命の天秤は正しく保たれる。", "【Dubium】惑うときは中庸を選べ。どちらにも寄らぬ平穏な心が、最も賢明な判断を下すだろう。", "【Pax】人との距離感を大切にせよ。適切な均衡を保つ振る舞いが、周囲に安寧と幸運をもたらす。"],
    "scorpio": ["【Profunditas】物事の核心を突き詰めよ。深く鋭い洞察こそが、隠された真実を白日の下に晒すだろう。", "【Arcanum】秘密は重んじられるべきもの。大切な真理は口外せず、己の胸の内で静かに育てよ。", "【Intentio】全神経を一点に注げ。余計な雑音を排した揺るぎない集中力が、最大の武器となる。"],
    "sagittarius": ["【Peregrinatio】境界を越えてゆけ。未知なる世界への小さな一歩が、滞っていた運気に新しい風を吹き込む。", "【Spatium】視野を地平線の先まで広げよ。可能性を限定しない自由な発想が、未来を無限に変える。", "【Intuitio】緻密な計画よりも、魂の叫びに従え。野生の直感が、理屈を超えた正解を指し示す。"],
    "capricorn": ["【Labor】積み重ねた努力は裏切らない。地道な一歩こそが、標高高き成功の頂へとあなたを導く。", "【Constantia】不変の意志を持て。今日の堅実な歩みが、未来における揺るぎない地位の礎となる。", "【Auctoritas】責任ある決断を下せ。あなたの誠実な判断が、周囲からの深い信頼と敬意を勝ち取る。"],
    "aquarius": ["【Inventio】常識という枷を外せ。独創的な閃きこそが、袋小路に陥った現状を打破する革命となる。", "【Libertas】縛られることを拒め。誰にも似ていない選択をすることが、あなたに真の幸運を運んでくる。", "【Visionarium】脳裏に浮かぶイメージを記録せよ。その断片は、未来を創るための重要な設計図である。"],
    "pisces": ["【Misericordia】感受性を研ぎ澄ませ。芸術や美しきものに触れることで、魂は癒やされ、運気は開かれる。", "【Fluentia】抗うな、流れに身を任せよ。大いなる運命の奔流に漂うことで、心は真の解放を得る。", "【Requies】今は戦う時ではない。心と身体を深く休めることを最優先せよ。休息こそが再生の源である。"],
}

# ===== CSS スタイル (日本語訳の巨大化) =====
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Shippori+Mincho:wght@400;600&display=swap');

body {
    background-color: #050505;
    background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://www.transparenttextures.com/patterns/black-mamba.png');
    color: #e2c08d;
    font-family: 'Shippori Mincho', serif;
    display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 40px 0;
}

.marble-panel {
    width: 90%; max-width: 650px; padding: 70px 50px;
    background: #0a0a0a; border: 1px solid #3d3326;
    box-shadow: 0 0 0 6px #0a0a0a, 0 0 0 10px #8c6d3e, 0 50px 100px rgba(0,0,0,1);
    text-align: center; margin-bottom: 50px;
}

h1 { font-family: 'Cinzel', serif; font-size: 52px; letter-spacing: 12px; margin: 0; color: #c9a063; }
.sub-title { font-family: 'Cinzel', serif; font-size: 16px; color: #63543e; margin-bottom: 50px; letter-spacing: 6px; }

/* テキスト強調 */
.latin-quote { font-family: 'Cinzel', serif; font-size: 2.6em; line-height: 1.25; color: #f5e6b3; margin: 40px 0 20px 0; font-weight: 700; }

/* 日本語訳を大きく設定 */
.jp-meaning { font-size: 2.0em; color: #8c6d3e; margin-bottom: 50px; font-weight: 600; line-height: 1.5; }
.fortune-text { font-size: 2.0em; line-height: 1.8; margin: 40px 0; color: #e2d1b9; text-align: left; border-left: 3px solid #8c6d3e; padding-left: 25px; }

.divider { width: 120px; height: 1px; background: #8c6d3e; margin: 40px auto; }

select, button {
    width: 100%; padding: 22px; background: #111; border: 1px solid #3d3326; color: #c9a063;
    font-family: 'Cinzel', serif; font-size: 22px; cursor: pointer;
}
button { background: #1a1510; border-color: #8c6d3e; font-weight: bold; margin-top: 30px; }

.lucky-box { border-top: 1px solid #2a241b; padding-top: 40px; margin-top: 50px; font-size: 2.2em; color: #f5e6b3; }
.label-gold { font-family: 'Cinzel', serif; font-size: 16px; color: #8c6d3e; display: block; margin-bottom: 15px; letter-spacing: 3px; }

/* カレンダー */
.calendar-panel {
    width: 90%; max-width: 450px; padding: 30px;
    background: rgba(10, 10, 10, 0.9); border: 1px solid #3d3326; text-align: center;
}
table.cal { width: 100%; border-collapse: collapse; font-family: 'Cinzel', serif; font-size: 18px; }
.cal th { color: #8c6d3e; padding: 12px; }
.cal td { padding: 12px; color: #444; }
.cal .today { color: #c9a063; font-weight: bold; outline: 1px solid #c9a063; }

a { color: #63543e; text-decoration: none; font-size: 1.5em; letter-spacing: 4px; border-bottom: 1px solid; }
</style>
"""

def generate_calendar():
    today = date.today()
    yy, mm = today.year, today.month
    cal = calendar.monthcalendar(yy, mm)
    html = f'<div class="calendar-panel"><div class="label-gold" style="font-size:18px;">{yy} . {mm}</div><table class="cal"><tr>'
    for day in ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]:
        html += f'<th>{day}</th>'
    html += "</tr>"
    for week in cal:
        html += "<tr>"
        for day in week:
            if day == 0: html += "<td></td>"
            elif day == today.day: html += f'<td class="today">{day}</td>'
            else: html += f'<td>{day}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html

@app.get("/")
def home():
    options = "".join([f'<option value="{k}">{v["label"]} / {v["jp"]}</option>' for k, v in SIGN_DATA.items()])
    return f"""<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>ORACLE</title>{STYLE}</head>
<body>
    <div class="marble-panel">
        <h1>ORACLE</h1>
        <div class="sub-title">STATUE OF DESTINY</div>
        <div class="divider"></div>
        <form action="/fortune">
            <select name="sign">{options}</select>
            <button type="submit">DIVINE YOUR FATUM</button>
        </form>
    </div>
    {generate_calendar()}
</body>
</html>"""

@app.get("/")
def home():
    options = "".join([f'<option value="{k}">{v["label"]} / {v["jp"]}</option>' for k, v in SIGN_DATA.items()])
    return f"""<!doctype html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>ORACLE</title>
    {ADS_CODE}
    {STYLE}
</head>
<body>
    <div class="marble-panel">
        <h1>ORACLE</h1>
        <div class="sub-title">STATUE OF DESTINY</div>
        <div class="divider"></div>
        <form action="/fortune">
            <select name="sign">{options}</select>
            <button type="submit">DIVINE YOUR FATUM</button>
        </form>
    </div>
    {generate_calendar()}
</body>
</html>"""

@app.get("/fortune")
def fortune():
    # ... (前回の占い計算ロジック) ...
    return f"""<!doctype html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>FATUM</title>
    {ADS_CODE}
    {STYLE}
</head>
<body>
    <div class="marble-panel">
        <span class="label-gold">SENTENTIA HODIERNA</span>
        <div class="latin-quote">{quote['lt']}</div>
        <div class="jp-meaning">{quote['jp']}</div>
        <div class="divider"></div>
        <span class="label-gold">ORACULUM : {data['label']}</span>
        <div class="fortune-text">{fortune_msg}</div>
        <div class="lucky-box">
            <span class="label-gold">LUCKY ITEM</span>
            {lucky_item}
        </div>
        <div style="margin-top:70px;">
            <a href="/">RETURN</a>
        </div>
    </div>
</body>
</html>"""

if __name__ == "__main__":
    app.run(debug=True)
</body>
</html>"""
