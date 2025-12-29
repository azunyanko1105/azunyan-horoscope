import calendar
import random
from datetime import date
from flask import Flask, request

app = Flask(__name__)

# --- 1. Google AdSense ---
ADS_CODE = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6112085882585441" crossorigin="anonymous"></script>
"""

# --- 2. CSS Style ---
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lora:ital,wght@0,400;1,400&family=Shippori+Mincho:wght@400;600&display=swap');
body { background-color: #050505; background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://www.transparenttextures.com/patterns/black-mamba.png'); color: #e2c08d; font-family: 'Shippori Mincho', serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 40px 0; }
.marble-panel { width: 90%; max-width: 650px; padding: 60px 40px; background: #0a0a0a; border: 1px solid #3d3326; box-shadow: 0 0 0 6px #0a0a0a, 0 0 0 10px #8c6d3e, 0 50px 100px rgba(0,0,0,1); text-align: center; margin-bottom: 50px; }
h1 { font-family: 'Shippori Mincho', serif; font-size: 42px; letter-spacing: 4px; margin: 0; color: #c9a063; line-height: 1.2; font-weight: 600; }
.sub-title { font-family: 'Cinzel', serif; font-size: 14px; color: #63543e; margin-bottom: 40px; letter-spacing: 5px; }
.latin-quote { font-family: 'Lora', serif; font-style: italic; font-size: 2.2em; line-height: 1.3; color: #f5e6b3; margin: 30px 0 10px 0; }
.jp-meaning { font-size: 1.6em; color: #8c6d3e; margin-bottom: 40px; font-weight: 600; line-height: 1.5; }
.fortune-text { font-size: 1.5em; line-height: 1.8; margin: 30px 0; color: #e2d1b9; text-align: left; border-left: 3px solid #8c6d3e; padding-left: 20px; white-space: pre-wrap; }
.divider { width: 100px; height: 1px; background: #8c6d3e; margin: 30px auto; }

/* ラッキーアイテム・カラーの文字サイズを小さく調整 */
.lucky-box { border-top: 1px solid #2a241b; padding-top: 30px; margin-top: 40px; text-align: center; }
.lucky-item-large { font-size: 1.6em; color: #f5e6b3; font-weight: 600; margin-bottom: 15px; display: block; }
.label-gold { font-family: 'Cinzel', serif; font-size: 13px; color: #8c6d3e; display: block; margin-bottom: 8px; letter-spacing: 2px; }

.color-circle { display: inline-block; width: 18px; height: 18px; border-radius: 50%; border: 1px solid #e2c08d; margin-right: 10px; vertical-align: middle; }
select, button.submit-btn { width: 100%; padding: 20px; background: #111; border: 1px solid #3d3326; color: #c9a063; font-family: 'Cinzel', serif; font-size: 20px; cursor: pointer; }
.chat-container { width: 90%; max-width: 650px; background: #0a0a0a; border: 1px solid #3d3326; padding: 20px; margin-top: 30px; }
.chat-messages { height: 150px; overflow-y: auto; text-align: left; border-bottom: 1px solid #3d3326; padding: 10px; font-size: 1.1em; color: #e2d1b9; margin-bottom: 10px; }
.chat-input-area { display: flex; flex-direction: column; gap: 10px; }
.chat-row { display: flex; gap: 10px; }
.chat-input { background: #111; border: 1px solid #3d3326; color: #e2c08d; padding: 10px; }
.name-input { width: 100px; }
.msg-input { flex: 1; }
.chat-send { background: #8c6d3e; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; color: #000; }
a { color: #63543e; text-decoration: none; font-size: 1.4em; border-bottom: 1px solid; }
.calendar-panel { width: 90%; max-width: 400px; padding: 20px; background: rgba(10,10,10,0.8); border: 1px solid #3d3326; text-align: center; margin-top: 30px; }
table.cal { width: 100%; border-collapse: collapse; font-family: 'Cinzel', serif; font-size: 16px; margin-top: 10px; }
.cal th { color: #8c6d3e; padding: 8px; }
.cal td { padding: 8px; color: #e2c08d; }
.cal .today { color: #f5e6b3; font-weight: bold; outline: 1px solid #8c6d3e; background: #1a1510; }
</style>
"""

# --- 3. Data ---
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
    "pisces": {"label": "PISCES", "jp": "魚座"}
}

COLORS = [
    {"n": "ルビーレッド", "c": "#C41E3A"},
    {"n": "ミッドナイトブルー", "c": "#191970"},
    {"n": "フォレストグリーン", "c": "#228B22"},
    {"n": "サフランイエロー", "c": "#F4C430"},
    {"n": "ロイヤルパープル", "c": "#7851A9"},
    {"n": "ローズピンク", "c": "#FF66CC"},
    {"n": "ピュアホワイト", "c": "#FFFFFF"},
    {"n": "ジェットブラック", "c": "#000000"},
    {"n": "アンバー", "c": "#FFBF00"},
    {"n": "スカイブルー", "c": "#87CEEB"}
]

LUCKY_ITEMS = [
    "折りたたみ傘", "ハンカチ", "ボールペン", "ミントタブレット", "エコバッグ",
    "ワイヤレスイヤホン", "文庫本", "ハンドクリーム", "腕時計", "コインケース",
    "リップバーム", "スマートフォンの充電器", "眼鏡拭き", "マイボトル", "付箋",
    "のど飴", "キーホルダー", "名刺入れ", "手帳", "ブックマーク",
    "除菌スプレー", "モバイルバッテリー", "トートバッグ", "お守り", "修正テープ",
    "ヘアゴム", "目薬", "マスクケース", "ミニタオル", "パスケース",
    "USBメモリ", "ペンケース", "スケジュール帳", "懐中電灯", "印鑑ケース",
    "ソーイングセット", "ばんそうこう", "鏡", "カードケース", "靴べら",
    "香水", "サングラス", "レザー小物", "シルバーアクセサリー", "スカーフ",
    "ニット帽", "キャップ", "腕時計用替えベルト", "スマホストラップ", "レザーポーチ",
    "キーリング", "フレグランスシート", "リップグロス", "ハンドミラー", "ネイルオイル",
    "ミニ財布", "長財布", "キャンバストート", "レザー手帳カバー", "ブレスレット",
    "イヤーカフ", "ピアス", "ネックレス", "アロマロールオン", "カードホルダー",
    "ブックカバー", "ノートPCケース", "タブレットケース", "ポーチ", "ミニ巾着",
    "コットンハンカチ", "カシミヤストール", "レザーキーケース", "ミニ香水アトマイザー",
    "腕時計クロス", "メガネケース", "レザーコインケース", "シンプルリング"
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
    "aries": [
        "【Impetus】内なる情熱に従え。停滞していた運命の歯車は、あなたの勇気によってのみ動き出す。今日は迷い続けるよりも、たとえ小さくとも一歩踏み出しましょう。自分を信じて行動するのが吉です。ただし、勢いだけで突き進むことは避け、怒りや焦りに任せた決断はしない方がよいでしょう。",
        "【Prudentia】今日は盾を掲げよ。無謀なる進軍よりも、静かなる守護が明日の勝利を約束する日です。今は積極的に動くより、状況を見極める時間を持ちましょう。待つことも立派な選択です。衝動的な判断や強引な行動は、後悔を生みやすいので控えるのが吉。",
        "【Inceptum】小さな火種を絶やすな。今この瞬間の挑戦が、後に消えぬ自信の灯火となります。大きな成果を求める必要はありません。今日始める小さな行動が未来につながります。完璧を求めすぎて何も始めないことは、最も避けたい選択です。"
    ],
    "taurus": [
        "【Silentium】喧騒を離れ、己の深淵を覗け。真実の答えは常に、静かなる時間の中に隠されています。今日は一人で考える時間を意識的に持ちましょう。落ち着いた環境で自分の本音と向き合うのが吉。周囲の雑音に流されることは避けた方がよいでしょう。",
        "【Moderatio】無理を強いるな。自然の理に身を任せる選択こそが、最善の果実をもたらします。今日は頑張りすぎないことが運気安定の鍵です。できる範囲で丁寧に進めましょう。自分に厳しすぎる態度や、限界を超えた努力はよくありません。",
        "【Affinitas】身近な者の言葉に耳を傾けよ。何気ない会話の中に、運命を切り拓く鍵が眠っています。今日は信頼できる人との対話を大切にしましょう。一人で抱え込むことは避け、素直に頼るのが吉です。"
    ],
    "gemini": [
        "【Verbum】放たれた言葉は戻らぬ矢。その一言が運命を左右します。今日は発言に慎重になりましょう。言葉を選ぶことで、誤解や衝突を避けられます。思いつきで話すことや、感情的な言動は控えた方がよいでしょう。",
        "【Fortuitus】予期せぬ出会いを尊べ。偶然という名の神の悪戯が、あなたに新たな視界を授けます。計画通りにいかない出来事こそ、運命の導きです。予定外を拒まず受け入れるのが吉。柔軟さを失うことは避けましょう。",
        "【Ratio】情報の海を整理せよ。知性を羅針盤とすれば、立ち込めていた迷いの霧は晴れるでしょう。今日は頭の中を整理する日です。不要な情報を減らし、優先順位を見直すのが吉。考えすぎて混乱するのはよくありません。"
    ],
    "cancer": [
        "【Animus】己の感情に偽りを持つな。心の震えをそのまま受け入れることで、真の安らぎが訪れます。今日は自分の気持ちを否定せず、受け止めましょう。感情を抑え込みすぎることは避けた方がよいでしょう。",
        "【Caritas】他者を想う慈しみの心を持て。その献身は巡り巡って、あなた自身の魂を救う光となります。今日は優しさを行動に移すのが吉。ただし、自己犠牲になりすぎないよう注意しましょう。",
        "【Stabilitas】今は城壁を固める時。守りに徹することで、揺るぎない精神の基盤が築かれます。今日は新しい挑戦より、足元を整えることを優先しましょう。無理な変化は避けるのが吉です。"
    ],
    "leo": [
        "【Magnificentia】王者の如く堂々と振る舞え。己を信じて歩む道こそが、黄金の未来へと通じています。今日は自信を持って前に出ましょう。遠慮しすぎない姿勢が吉です。",
        "【Dignitas】主役はあなたである。しかし、他者を照らさぬ輝きは、やがて孤独という影を生みます。周囲への配慮を忘れずに。自己中心的な行動は控えた方がよいでしょう。",
        "【Gloria】焦る必要はありません。真の評価は常に後からついてきます。今日は結果を急がず、信念を貫くのが吉。途中で諦めることは避けましょう。"
    ],
    "virgo": [
        "【Subtilitas】細部に神は宿ります。徹底した気配りと秩序への献身が、凡庸なる結果を卓越へと変えます。今日は丁寧さを意識しましょう。雑な対応は運気を下げやすいので注意。",
        "【Perfectio】完璧の檻から抜け出せ。不完全さを受け入れる度量が、真の成功を引き寄せます。今日は妥協も必要です。自分を責めすぎることは避けましょう。",
        "【Ordo】まずは身辺を整えよ。環境の調和を取り戻すことで、心にも余裕が生まれます。片付けや整理が吉。乱れた状態を放置するのはよくありません。"
    ],
    "libra": [
        "【Aequitas】調和こそが最大の美徳。極端を避け、中道を選ぶことで運命の天秤は正しく保たれます。今日はバランスを意識しましょう。",
        "【Dubium】惑うときは中庸を選べ。すぐに結論を出さず、時間を置くのが吉。感情で判断することは避けましょう。",
        "【Pax】人との距離感を大切に。適切な均衡を保つことで、穏やかな一日になります。踏み込みすぎはよくありません。"
    ],
    "scorpio": [
        "【Profunditas】物事の核心を突き詰めよ。今日は表面ではなく本質を見る日です。深く考えることで答えが見えてきます。",
        "【Arcanum】秘密は重んじられるべきもの。今日は話さない方がよいことがあります。軽率な共有は避けましょう。",
        "【Intentio】全神経を一点に注げ。集中することで大きな成果を得られます。気を散らす行動は控えましょう。"
    ],
    "sagittarius": [
        "【Peregrinatio】境界を越えてゆけ。今日は新しいことに挑戦するのが吉。小さな冒険が流れを変えます。",
        "【Spatium】視野を広げよ。可能性を限定しないことで未来は開けます。思い込みは避けましょう。",
        "【Intuitio】魂の叫びに従え。直感を信じることで正しい選択ができます。理屈に縛られすぎないのが吉です。"
    ],
    "capricorn": [
        "【Labor】積み重ねた努力は裏切りません。今日もコツコツ続けるのが吉。近道を探すのは避けましょう。",
        "【Constantia】不変の意志を持て。今日の我慢が未来の安定につながります。途中で諦めることは大切です。",
        "【Auctoritas】責任ある決断を。誠実な姿勢が信頼を高めます。曖昧な態度はよくありません。"
    ],
    "aquarius": [
        "【Inventio】常識という枷を外せ。自由な発想が状況を打破します。独自性を恐れないのが吉。",
        "【Libertas】縛られることを拒め。自分らしい選択が幸運を呼びます。他人の目を気にしすぎないように。",
        "【Visionarium】ひらめきを記録せよ。今日の思いつきは未来の種です。流してしまうのは避けましょう。"
    ],
    "pisces": [
        "【Misericordia】感受性を研ぎ澄ませ。美しいものに触れることで心が整います。雑音から距離を置くのが吉。",
        "【Fluentia】抗うな、流れに身を任せよ。自然な選択が心を軽くします。無理に進めるのはよくありません。",
        "【Requies】今は戦う時ではありません。しっかり休むことが再生につながります。休息を後回しにしないのが吉。"
    ]
}

def generate_calendar():
    today = date.today()
    cal = calendar.monthcalendar(today.year, today.month)
    html = f'<div class="calendar-panel"><div class="label-gold">{today.year}.{today.month}</div><table class="cal"><tr>'
    for d in ["SU","MO","TU","WE","TH","FR","SA"]: html += f'<th>{d}</th>'
    html += "</tr>"
    for wk in cal:
        html += "<tr>"
        for d in wk:
            if d == 0: html += "<td></td>"
            elif d == today.day: html += f'<td class="today">{d}</td>'
            else: html += f'<td>{d}</td>'
        html += "</tr>"
    return html + "</table></div>"

@app.get("/")
def home():
    opts = "".join([f'<option value="{k}">{v["label"]} / {v["jp"]}</option>' for k,v in SIGN_DATA.items()])
    return f"""<!doctype html><html lang='ja'><head><meta charset='utf-8'><title>今日の星座占い</title>{ADS_CODE}{STYLE}</head>
    <body>
        <div class='marble-panel'>
            <h1>今日の星座占い</h1>
            <div class='sub-title'>HODIERNA MEA SIDERA</div>
            <div class='divider'></div>
            <form action='/fortune'>
                <select name='sign'>{opts}</select>
                <button type='submit' class='submit-btn'>DIVINE YOUR FATUM</button>
            </form>
        </div>
        
        <div class="chat-container">
            <span class="label-gold">DELPHIC ORACLE CHAT / 聖なる交流</span>
            <div class="chat-messages" id="chat-box">
                <div>[ピュティア]：汝の運命は、いかなる星影に照らされたか？</div>
            </div>
            <div class="chat-input-area">
                <div class="chat-row">
                    <input type="text" id="chat-name" class="chat-input name-input" placeholder="あだ名">
                    <input type="text" id="chat-input" class="chat-input msg-input" placeholder="メッセージを入力...">
                </div>
                <button class="chat-send" onclick="sendMessage()">SEND / 送信</button>
            </div>
        </div>
        
        {generate_calendar()}

        <script>
            function sendMessage() {{
                const nameInput = document.getElementById('chat-name');
                const msgInput = document.getElementById('chat-input');
                const box = document.getElementById('chat-box');
                
                let name = nameInput.value.trim();
                if (name === '') name = '匿名';
                
                const msg = msgInput.value.trim();
                
                if(msg !== '') {{
                    const div = document.createElement('div');
                    div.innerHTML = `<span style="color:#8c6d3e">[</span><span>${{name}}]：</span>` + msg;
                    box.appendChild(div);
                    msgInput.value = '';
                    box.scrollTop = box.scrollHeight;
                }}
            }}
        </script>
    </body></html>"""

@app.get("/fortune")
def fortune():
    sign = request.args.get("sign", "aries")
    today = date.today()
    seed = today.toordinal() + sum(ord(c) for c in sign)
    random.seed(seed)
    q = random.choice(LATIN_QUOTES)
    msgs = FORTUNE.get(sign, ["神託は沈黙している。"])
    msg = random.choice(msgs)
    item = random.choice(LUCKY_ITEMS)
    color = random.choice(COLORS)
    return f"""<!doctype html><html lang='ja'><head><meta charset='utf-8'><title>結果</title>{ADS_CODE}{STYLE}</head><body>
    <div class='marble-panel'>
        <span class='label-gold'>SENTENTIA / 今日の格言</span><div class='latin-quote'>{q['lt']}</div><div class='jp-meaning'>{q['jp']}</div><div class='divider'></div>
        <span class='label-gold'>ORACULUM / {SIGN_DATA.get(sign, {}).get('jp', '星')}の運勢</span><div class='fortune-text'>{msg}</div>
        <div class='lucky-box'>
            <span class='label-gold'>LUCKY ITEM</span><span class='lucky-item-large'>{item}</span>
            <span class='label-gold'>LUCKY COLOR</span>
            <span class='lucky-item-large'><span class="color-circle" style="background:{color['c']}"></span>{color['n']}</span>
        </div>
        <div style='margin-top:50px;'><a href='/'>RETURN</a></div>
    </div></body></html>"""

if __name__ == "__main__":
    app.run()
