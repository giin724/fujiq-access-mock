# -*- coding: utf-8 -*-
"""出発地別「高速バスで行く」ページ（bus/*.html）を生成するスクリプト。
python build_bus.py  で fujiq-access-mock/bus/ 配下に7ページを書き出す。
"""
import html, os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "bus")
TICKET = "https://membersclub.fujiq.jp/ticket/"
TOUR = "https://www.fujikyu-travel.co.jp/free/03_3.html"
HOTEL = "https://www.fujikyu-travel.co.jp/hotel/TOP3.html"

# ---------------------------------------------------------------- data
PREFS = [
  dict(slug="tokyo", name="東京都", short="東京", src="https://www.fujiq.jp/access/tokyo2025.html",
    lead="バスタ新宿・東京駅・渋谷・池袋など都内各地から直行。往復バスとワンデイパスのセットがおトクです。",
    facts=[("8", "路線", "都内各地から直行"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="special", title="超・得Qパック", badge="限定",
           desc="往復高速バス＋優先入園ワンデイパス＋絶叫優先券1枚のセット。",
           routes=[dict(stops=["新宿駅"], info="http://www.fujiq.jp/event/tokuQpack_2025.html", buy=None, infoLabel="プラン詳細")]),
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[
             dict(stops=["バスタ新宿","中央道三鷹","中央道深大寺","中央道府中","中央道日野","中央道八王子"], info="https://bus.fujikyu.co.jp/highway/detail/id/1"),
             dict(stops=["渋谷マークシティ","二子玉川駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/32"),
             dict(stops=["東京駅（八重洲南口・鉄鋼ビル）","東京ドームホテル"], info="https://bus.fujikyu.co.jp/highway/detail/id/37"),
             dict(stops=["秋葉原駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/40"),
             dict(stops=["町田バスセンター","南町田駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/34"),
             dict(stops=["サンシャインプリンスホテル","池袋駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/8"),
             dict(stops=["お台場"], info="https://bus.fujikyu.co.jp/highway/detail/id/46"),
             dict(stops=["羽田空港"], info="https://bus.fujikyu.co.jp/highway/detail/id/4"),
           ]),
      dict(kind="tour", title="バスツアー（富士急トラベル）", badge="ツアー",
           desc="新宿・上野・八王子発。乗り換えの不安がなく、優先入園付きワンデイパスやトーマスランドパスも選べます。",
           routes=[dict(stops=["新宿","上野","八王子"], info=TOUR, infoLabel="ツアー詳細", buy=None)]),
      dict(kind="only", title="高速バスのみ", badge="セット券なし",
           desc="ワンデイパスとのセット券はありません。バス単体でのご利用になります。",
           routes=[dict(stops=["品川駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/4")]),
      dict(kind="hotel", title="宿泊セット", badge="泊まる",
           desc="高速バス＋ワンデイパス付きのオフィシャルホテル宿泊プラン。",
           routes=[dict(stops=["オフィシャルホテル宿泊プラン"], info=HOTEL, infoLabel="宿泊プランを見る", buy=None)]),
    ]),
  dict(slug="kanagawa", name="神奈川県", short="神奈川", src="https://www.fujiq.jp/access/kanagawa2025.html",
    lead="横浜・藤沢・本厚木・橋本など県内各地から直行。往復バスとワンデイパスのセットがおトクです。",
    facts=[("4", "路線", "県内各地から直行"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[
             dict(stops=["横浜駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/6"),
             dict(stops=["日吉駅","センター北駅","たまプラーザ駅","市ヶ尾駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/7"),
             dict(stops=["藤沢駅","辻堂駅","本厚木駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/35"),
             dict(stops=["橋本駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/34"),
           ]),
      dict(kind="tour", title="バスツアー（富士急トラベル）", badge="ツアー",
           desc="新横浜発。富士急へ最短で行けて、乗り換えが不安な方でも安心。優先入園付きワンデイパス付き。",
           routes=[dict(stops=["新横浜駅"], info=TOUR, infoLabel="ツアー詳細", buy=None)]),
      dict(kind="hotel", title="宿泊セット", badge="泊まる",
           desc="高速バス＋ワンデイパス付きのオフィシャルホテル宿泊プラン。",
           routes=[dict(stops=["オフィシャルホテル宿泊プラン"], info=HOTEL, infoLabel="宿泊プランを見る", buy=None)]),
    ]),
  dict(slug="yamanashi", name="山梨県", short="山梨", src="https://www.fujiq.jp/access/yamanashi2025.html",
    lead="甲府駅から路線バスで。往復路線バスとワンデイパスのセットがおトクです。",
    facts=[("路線バス", "", "甲府駅から"), ("往復", "", "バス＋ワンデイパス"), ("予約不要", "", "路線バスで気軽に")],
    sections=[
      dict(kind="local", title="往復路線バス＆ワンデイパスセット", badge="路線バス",
           desc="往復の路線バスとワンデイパスがセットになったきっぷ。",
           routes=[dict(stops=["甲府駅"], info="https://www.fujikyubus.co.jp/regular/#section-6")]),
    ]),
  dict(slug="shizuoka", name="静岡県", short="静岡", src="https://www.fujiq.jp/access/shizuoka2025.html",
    lead="三島・静岡からの高速バス、御殿場・新富士・富士宮からの路線バス。ワンデイパスとのセットもあります。",
    facts=[("高速・路線", "", "2種類のバス"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[
             dict(stops=["三島駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/29"),
             dict(stops=["静岡駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/12"),
           ]),
      dict(kind="tour", title="バスツアー（富士急トラベル）", badge="ツアー",
           desc="静岡発。富士急へ最短で行けて、乗り換えの心配なし。優先入園付きワンデイパス付き。",
           routes=[dict(stops=["静岡"], info=TOUR, infoLabel="ツアー詳細", buy=None)]),
      dict(kind="only", title="高速バスのみ", badge="セット券なし",
           desc="ワンデイパスとのセット券はありません。バス単体でのご利用になります。",
           routes=[dict(stops=["御殿場駅","御殿場プレミアム・アウトレット"], info="https://bus.fujikyu.co.jp/highway/detail/id/41")]),
      dict(kind="local", title="往復路線バス＆ワンデイパスセット", badge="路線バス",
           desc="往復の路線バスとワンデイパスがセットになったきっぷ。",
           routes=[
             dict(stops=["御殿場駅"], info="https://www.fujikyubus.co.jp/regular/"),
             dict(stops=["新富士駅","富士宮駅"], info="https://www.fujikyubus.co.jp/regular/"),
           ]),
    ]),
  dict(slug="chiba", name="千葉県", short="千葉", src="https://www.fujiq.jp/access/chiba2025.html",
    lead="海浜幕張・津田沼・西船橋から直行。成田空港からの高速バスもあります。",
    facts=[("2", "路線", "県内・成田空港から"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[dict(stops=["海浜幕張駅","京成津田沼駅","西船橋駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/15")]),
      dict(kind="only", title="高速バスのみ（成田空港発）", badge="セット券なし",
           desc="ワンデイパスとのセット券はありません。バス単体でのご利用になります。",
           routes=[dict(stops=["成田空港"], info="https://bus.fujikyu.co.jp/highway/detail/id/39")]),
      dict(kind="hotel", title="宿泊セット", badge="泊まる",
           desc="高速バス＋ワンデイパス付きのオフィシャルホテル宿泊プラン。",
           routes=[dict(stops=["オフィシャルホテル宿泊プラン"], info=HOTEL, infoLabel="宿泊プランを見る", buy=None)]),
    ]),
  dict(slug="saitama", name="埼玉県", short="埼玉", src="https://www.fujiq.jp/access/other2025.html",
    lead="大宮・川越・狭山から直行。往復バスとワンデイパスのセットがおトクです。",
    facts=[("1", "路線", "大宮〜川越〜狭山"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[dict(stops=["大宮駅","川越駅","狭山駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/8#d_h01")]),
      dict(kind="tour", title="バスツアー（富士急トラベル）", badge="ツアー",
           desc="大宮発。富士急へ最短で行けて、乗り換えが不安な方でも安心。",
           routes=[dict(stops=["大宮"], info=TOUR, infoLabel="ツアー詳細", buy=None)]),
      dict(kind="hotel", title="宿泊セット", badge="泊まる",
           desc="高速バス＋ワンデイパス付きのオフィシャルホテル宿泊プラン。",
           routes=[dict(stops=["オフィシャルホテル宿泊プラン"], info="https://www.fujikyu-travel.co.jp/hotel/TOP1.html", infoLabel="宿泊プランを見る", buy=None)]),
    ]),
  dict(slug="kansai", name="京都府・大阪府", short="京都・大阪", src="https://www.fujiq.jp/access/kansai2025.html",
    lead="京都駅・大阪駅・あべのハルカス・近鉄難波駅から直行。往復バスとワンデイパスのセットがおトクです。",
    facts=[("関西発", "", "京都・大阪から直行"), ("乗換なし", "", "園前バスターミナル着"), ("優先入園", "", "ワンデイパス付き")],
    sections=[
      dict(kind="set", title="往復高速バス＆ワンデイパスセット", badge="得Qパック",
           desc="往復の高速バスとワンデイパスがセットになったおトクなきっぷ。",
           routes=[
             dict(stops=["京都駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/9"),
             dict(stops=["大阪駅","あべのハルカス","近鉄難波駅"], info="https://bus.fujikyu.co.jp/highway/detail/id/9"),
           ]),
      dict(kind="hotel", title="宿泊セット", badge="泊まる",
           desc="高速バス＋ワンデイパス付きのオフィシャルホテル宿泊プラン。",
           routes=[dict(stops=["オフィシャルホテル宿泊プラン"], info=HOTEL, infoLabel="宿泊プランを見る", buy=None)]),
    ]),
]

KIND_ICON = {
  "set": "🎟", "special": "⭐", "tour": "🚌", "only": "🚌", "local": "🚏", "hotel": "🏨",
}

def e(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- template parts
def route_card(r, kind):
    stops = r["stops"]
    info_label = r.get("infoLabel", "路線・料金表")
    buy = r.get("buy", TICKET)
    chips = "".join(f'<span class="stop">{e(s)}</span>' for s in stops) if len(stops) > 1 else ""
    first = e(stops[0]) + ("　ほか" if len(stops) > 1 else "")
    buy_html = f'<a class="b buy" href="{e(buy)}" target="_blank" rel="noopener">購入する</a>' if buy else ""
    return f'''
      <article class="route">
        <div class="route-head">
          <div class="from"><span class="lbl">出発地</span><b>{first}</b></div>
          <span class="to">→ 富士急ハイランド</span>
        </div>
        {f'<div class="stops">{chips}</div>' if chips else ''}
        <div class="route-actions">
          <a class="b info" href="{e(r["info"])}" target="_blank" rel="noopener">{e(info_label)}</a>
          {buy_html}
        </div>
      </article>'''

def section(sec):
    routes = "".join(route_card(r, sec["kind"]) for r in sec["routes"])
    return f'''
    <section class="sec kind-{sec["kind"]}" id="s-{sec["kind"]}">
      <div class="sec-head">
        <span class="ico">{KIND_ICON.get(sec["kind"], "🚌")}</span>
        <div><span class="badge">{e(sec["badge"])}</span><h2>{e(sec["title"])}</h2></div>
      </div>
      <p class="sec-desc">{e(sec["desc"])}</p>
      {routes}
    </section>'''

def pref_switch(current):
    items = []
    for p in PREFS:
        cls = ' class="is-active"' if p["slug"] == current else ""
        items.append(f'<a href="{p["slug"]}.html"{cls}>{e(p["short"])}</a>')
    return "".join(items)

def jump_tabs(p):
    labels = {"special":"超・得Q","set":"往復セット","tour":"ツアー","only":"バスのみ","local":"路線バス","hotel":"宿泊"}
    return "".join(f'<a href="#s-{s["kind"]}">{labels.get(s["kind"], s["title"])}</a>' for s in p["sections"])

def facts(p):
    out = []
    for v, unit, k in p["facts"]:
        u = f'<small>{e(unit)}</small>' if unit else ""
        out.append(f'<div><div class="v">{e(v)}{u}</div><div class="k">{e(k)}</div></div>')
    return "".join(out)

def page(p):
    secs = "".join(section(s) for s in p["sections"])
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["name"])}から高速バスで | 交通アクセス | 富士急ハイランド（モック）</title>
<link rel="stylesheet" href="bus.css">
</head>
<body>
<header class="header">
  <div class="wrap">
    <a class="logo" href="../index-b.html"><span class="q">Q</span>富士急ハイランド</a>
    <div class="hdr-r">
      <a class="btn-ticket" href="{TICKET}">チケット購入</a>
      <button class="btn-menu" aria-label="メニュー"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<section class="hero">
  <div class="wrap">
    <nav class="crumb"><a href="../index-b.html">交通アクセス</a><span>›</span><a href="../index-b.html#bus">バス</a><span>›</span>{e(p["name"])}から</nav>
    <div class="en">BUS ACCESS</div>
    <h1><span class="pref">{e(p["name"])}</span>から<br>高速バスで富士急ハイランドへ</h1>
    <p>{e(p["lead"])}</p>
  </div>
  <div class="wrap">
    <div class="pref-switch" aria-label="出発地を切り替える">{pref_switch(p["slug"])}</div>
  </div>
</section>

<div class="wrap">
  <div class="facts">{facts(p)}</div>

  <nav class="jump"><div class="jump-in">{jump_tabs(p)}</div></nav>

  {secs}

  <section class="card notes">
    <h2>ご利用にあたって</h2>
    <ul>
      <li>所要時間・運賃・時刻は各路線の「路線・料金表」でご確認ください。道路状況により遅れる場合があります。</li>
      <li>セット券のワンデイパスには開園前に入園できる優先入園が付きます（一部対象外あり）。</li>
      <li>高速バスは「ハイランドリゾート ホテル＆スパ」駐車場内のバスターミナルに到着します。<a href="https://maps.app.goo.gl/nqQ9NiLLDiu8B9Hv5" target="_blank" rel="noopener">地図を見る ›</a></li>
      <li>料金・運行内容は予告なく変更になる場合があります。</li>
    </ul>
  </section>

  <div class="other">
    <h2>ほかの出発地から</h2>
    <div class="pref-grid">{pref_switch(p["slug"])}</div>
    <a class="back" href="../index-b.html">交通アクセス トップへ戻る</a>
  </div>
</div>

<footer>© FUJIKYU HIGHLAND — モック（出発地別ページ）<br><small>元ページ: <a href="{e(p["src"])}">{e(p["src"])}</a></small></footer>

<div class="bar">
  <a class="r" href="#top" data-pref-open>出発地を変更</a>
  <a class="t" href="{TICKET}">チケット購入</a>
</div>

<div class="sheet" id="sheet" aria-hidden="true">
  <div class="sheet-bg" data-pref-close></div>
  <div class="sheet-body" role="dialog" aria-label="出発地を選ぶ">
    <div class="sheet-handle"></div>
    <h3>出発地を選ぶ</h3>
    <div class="pref-grid">{pref_switch(p["slug"])}</div>
    <button class="sheet-close" type="button" data-pref-close>閉じる</button>
  </div>
</div>

<script>
  const sheet=document.getElementById('sheet');
  document.querySelectorAll('[data-pref-open]').forEach(b=>b.addEventListener('click',ev=>{{ev.preventDefault();sheet.classList.add('is-open');sheet.setAttribute('aria-hidden','false');}}));
  document.querySelectorAll('[data-pref-close]').forEach(b=>b.addEventListener('click',()=>{{sheet.classList.remove('is-open');sheet.setAttribute('aria-hidden','true');}}));
  // ジャンプタブのアクティブ表示
  const jl=[...document.querySelectorAll('.jump a')];
  const io=new IntersectionObserver(es=>{{es.forEach(x=>{{if(x.isIntersecting)jl.forEach(a=>a.classList.toggle('is-active',a.getAttribute('href')==='#'+x.target.id));}});}},{{rootMargin:'-120px 0px -60% 0px'}});
  jl.forEach(a=>{{const t=document.querySelector(a.getAttribute('href'));if(t)io.observe(t);}});
</script>
</body>
</html>
'''

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in PREFS:
        path = os.path.join(OUT, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(p))
        print("wrote", path)
