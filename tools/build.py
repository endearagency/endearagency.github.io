#!/usr/bin/env python3
"""Build the multi-page site from src/site.html.

Edit src/site.html, then run:  python3 tools/build.py [--artifact OUT_DIR]

Writes index.html (home) and talent/ art/ 3d/ merch/ about/ contact/ index.html,
each with its own title, description, canonical URL, structured data and page hero text.
With --artifact, also writes a preview copy (home as endear.html) into OUT_DIR,
using explicit index.html links so it works where folder URLs don't.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://endearagency.github.io/'

PAGES_EN = {
    'home': dict(title='endear | Thai VTubers, KOLs, anime art, 3D & merch agency',
        desc='endear is a Thai project management agency for anime, comics and games. Hire Thai and global VTubers, KOLs, MCs and cosplayers, and get illustration, Live2D, animation, 3D and merchandise done in one place.'),
    'talent': dict(title='Hire Thai VTubers, KOLs & streamers for promotion, reviews & voice | endear',
        desc='60+ Thai and global VTubers, streamers and KOLs for game and product promotion, reviews, voice dubbing, collabs and tie-ins. See each talent’s followers, channels and top videos.'),
    'art': dict(title='Anime illustration, character design, Live2D, animation & MV | endear',
        desc='Anime-style illustration, character design, emotes, LINE stickers, stream assets, Live2D models for VTubers, webtoons, motion graphics, animation and music videos.'),
    '3d': dict(title='3D modeling, 3D printing, custom merch & UV printing | endear',
        desc='3D models for games and brands, 3D-printed figures and custom merch, UV printing on special surfaces, and hands-on 3D printing classes in Thailand.'),
    'merch': dict(title='Custom merch: button badges, acrylic goods, pass cases & ema | endear',
        desc='Custom merchandise made to your design: button badges, aluminium badges, acrylic and glitter shakers, standees, pass cases, magnets, coasters, pocket mirrors, shikishi and ema.'),
    'about': dict(title='About endear | anime, comics & games project agency in Thailand',
        desc='endear is a Thai agency for anime, comics and games. We find the team, coordinate and see projects through, from VTubers and KOLs to art, 3D and merchandise.'),
    'contact': dict(title='Contact endear | LINE, phone, Facebook',
        desc='Tell us what you need and we will find the team and see it through. Contact endear via LINE plaiendear, phone +66 94 555 1424 or Facebook.'),
}

PAGES = {
    'home': dict(dir='', title='endear | หา VTuber ไทย KOL งานอาร์ต งาน 3D และสินค้าที่ระลึก',
        desc='เอเจนซี่ดูแลโปรเจกต์สายอนิเมะ การ์ตูน และเกม หา VTuber ไทย, KOL, MC, คอสเพลเยอร์ รับทำงานอาร์ต Live2D แอนิเมชัน งาน 3D และ merchandise ครบในที่เดียว | Thai VTuber, art, 3D & merch agency.'),
    'talent': dict(dir='talent/', title='VTuber ไทยและต่างประเทศ KOL สตรีมเมอร์ รับงานโปรโมต รีวิว พากย์เสียง | endear',
        desc='รวม VTuber ไทยและต่างประเทศ สตรีมเมอร์ (streamer) และ KOL กว่า 60 คน รับงานโปรโมตเกมและสินค้า รีวิว พากย์เสียง คอลแลป Tie-in ดูยอดผู้ติดตามและช่องทางของแต่ละคนได้ทันที | Thai VTubers, streamers & KOLs for hire.'),
    'art': dict(dir='art/', title='รับวาดภาพประกอบ ออกแบบตัวละคร Live2D แอนิเมชัน MV | endear',
        desc='ทีมนักวาดสายอนิเมะ รับวาดภาพประกอบ (illustration) ออกแบบตัวละคร (character design) อีโมต สติกเกอร์ LINE ฉากสตรีม โมเดล Live2D สำหรับ VTuber เว็บตูน โมชันกราฟิก แอนิเมชัน และ MV | Anime art, Live2D & animation.'),
    '3d': dict(dir='3d/', title='รับทำโมเดล 3D งานพิมพ์ 3D ของที่ระลึก พิมพ์ UV | endear',
        desc='ปั้นโมเดล 3D สำหรับเกมและงานทั่วไป ผลิตของที่ระลึกพิมพ์ 3D (3D printing) พิมพ์ UV บนพื้นผิวพิเศษ และคอร์สเรียน 3D Print ตั้งแต่แบบร่างจนเป็นชิ้นงานจริง | 3D modeling, 3D printing & custom merch.'),
    'merch': dict(dir='merch/', title='ผลิตสินค้าที่ระลึก เข็มกลัด อะคริลิค ที่ใส่บัตร merchandise | endear',
        desc='ผลิตสินค้าที่ระลึก (merchandise) ตามแบบของคุณ เข็มกลัด เข็มกลัดอะลูมิเนียม อะคริลิคเชคเกอร์ กลิตเตอร์เชคเกอร์ สแตนดี้ ที่ใส่บัตร แม่เหล็ก ที่รองแก้ว กระจกพกพา ชิกิชิ และอีมะ | Custom merch made to your design.'),
    'about': dict(dir='about/', title='เกี่ยวกับ endear เอเจนซี่สายอนิเมะ การ์ตูน และเกม',
        desc='endear เอเจนซี่ดูแลโปรเจกต์สายอนิเมะ การ์ตูน และเกมในประเทศไทย หาทีม ประสานงาน และดูแลงานให้จนจบ ทั้ง VTuber, KOL, งานอาร์ต, งาน 3D และสินค้าที่ระลึก'),
    'contact': dict(dir='contact/', title='ติดต่อ endear | LINE โทร Facebook',
        desc='คุยงานกับ endear บอกเราว่าอยากได้อะไร เราหาทีม ประสานงาน และดูแลให้จนจบงาน ติดต่อทาง LINE plaiendear โทร 094-555-1424 หรือ Facebook'),
}


def phero(src, page, lang='th'):
    """Page-hero text, read from the PH table in the page's own script."""
    key = "'3d'" if page == '3d' else page
    if lang == 'en':
        m = re.search(r"\n  %s:\{ e:\['[^']*','([^']*)'\].*?h:\['[^']*','([^']*)'\].*?s:\['[^']*','([^']*)'\]" % key, src)
    else:
        m = re.search(r"\n  %s:\{ e:\['([^']*)'.*?h:\['([^']*)'.*?s:\['([^']*)'" % key, src)
    return m.groups() if m else None


def build(src, page, urls=None, lang='th', alt=None):
    cfg = dict(PAGES[page])
    if lang == 'en': cfg.update(PAGES_EN[page]); cfg['dir'] = 'en/' + PAGES[page]['dir']
    s = src.replace('<meta name="robots" content="noindex"><!--SRC-->\n', '')
    s = s.replace('<html lang="th">', '<html lang="%s" data-lang="%s" data-page="%s">' % (lang, lang, page), 1)
    depth = cfg['dir'].count('/')
    if depth:
        s = s.replace('<head>\n', '<head>\n<base href="%s">\n' % ('../' * depth), 1)
    th_url = SITE + PAGES[page]['dir']; en_url = SITE + 'en/' + PAGES[page]['dir']
    s = s.replace('<link rel="canonical"', '<link rel="alternate" hreflang="th" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s">\n<link rel="canonical"' % (th_url, en_url, th_url), 1)
    url = SITE + cfg['dir']
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % cfg['title'], s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % cfg['desc'], s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % cfg['title'], s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % cfg['desc'], s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, count=1)
    # structured data: talent list only on the talent page
    m = re.search(r'<script type="application/ld\+json" id="ld">(.*?)</script>', s, re.S)
    if m:
        ld = json.loads(m.group(1))
        if page != 'talent':
            ld['@graph'] = [g for g in ld['@graph'] if g.get('@type') != 'ItemList']
        if page == 'contact':
            fm = re.search(r'<script type="application/json" id="faqData">(.*?)</script>', s, re.S)
            if fm:
                k = 1 if lang == 'en' else 0
                ld['@graph'].append({'@type': 'FAQPage', 'mainEntity': [
                    {'@type': 'Question', 'name': q[k], 'acceptedAnswer': {'@type': 'Answer', 'text': q[2 + k]}}
                    for g in json.loads(fm.group(1)) for q in g[2]]})
        s = s[:m.start(1)] + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    # page hero text in the HTML itself so search engines read it without running scripts
    if page != 'home':
        ph = phero(src, page, lang)
        if ph:
            e, h, sub = ph
            s = re.sub(r'<!--PHERO-->.*?<!--/PHERO-->',
                       '<p class="eyebrow" id="phEyebrow">%s</p><h1 id="phH1">%s</h1><p class="hero-sub" id="phSub">%s</p><div class="chips ph-jump" id="phJump"></div>' % (e, h, sub),
                       s, count=1, flags=re.S)
            s = s.replace('<section id="phero" class="wrap hero phero" hidden>', '<section id="phero" class="wrap hero phero">', 1)
    else:
        s = s.replace('<!--PHERO-->', '').replace('<!--/PHERO-->', '')
    if urls or alt is not None:
        s = s.replace('<script>\n', '<script>%s%s</script>\n<script>\n' % ('window.PAGE_URLS=%s;' % json.dumps(urls) if urls else '', 'window.ALT_URL=%s;' % json.dumps(alt) if alt is not None else ''), 1)
    return s


def sitemap(date):
    rows = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, pre + c['dir'], date) for pre in ('', 'en/') for c in PAGES.values())
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n'


def main():
    src = open(os.path.join(ROOT, 'src', 'site.html'), encoding='utf-8').read()
    assert '<script>\n' in src
    en_urls = {p: 'en/' + c['dir'] for p, c in PAGES.items()}
    for page, cfg in PAGES.items():
        for lang in ('th', 'en'):
            d = cfg['dir'] if lang == 'th' else 'en/' + cfg['dir']
            out = os.path.join(ROOT, d, 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            alt = ('en/' + cfg['dir']) if lang == 'th' else (cfg['dir'] or './')
            open(out, 'w', encoding='utf-8').write(build(src, page, en_urls if lang == 'en' else None, lang, alt))
    # old events URLs now point to the merch page
    for pre in ('', 'en/'):
        out = os.path.join(ROOT, pre + 'events', 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        to = SITE + pre + 'merch/'
        open(out, 'w', encoding='utf-8').write('<!doctype html><html><head><meta charset="utf-8"><title>endear</title><meta name="robots" content="noindex"><link rel="canonical" href="%s"><meta http-equiv="refresh" content="0; url=%s"></head><body><a href="%s">endear merch</a></body></html>\n' % (to, to, to))
    import datetime
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sitemap(datetime.date.today().isoformat()))
    if '--artifact' in sys.argv:
        dest = sys.argv[sys.argv.index('--artifact') + 1]
        urls = {p: (c['dir'] + 'index.html' if c['dir'] else 'endear.html') for p, c in PAGES.items()}
        eurls = {p: 'en/' + c['dir'] + 'index.html' for p, c in PAGES.items()}
        for page, cfg in PAGES.items():
            out = os.path.join(dest, cfg['dir'] + 'index.html' if cfg['dir'] else 'endear.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(build(src, page, urls, 'th', eurls[page]))
            out = os.path.join(dest, 'en', cfg['dir'], 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(build(src, page, eurls, 'en', urls[page]))
    print('built', ', '.join(PAGES))


if __name__ == '__main__':
    main()
