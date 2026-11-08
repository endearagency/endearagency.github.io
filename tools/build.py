#!/usr/bin/env python3
"""Build the multi-page site from src/site.html.

Edit src/site.html, then run:  python3 tools/build.py [--artifact OUT_DIR]

Writes index.html (home) and talent/ art/ 3d/ events/ about/ contact/ index.html,
each with its own title, description, canonical URL, structured data and page hero text.
With --artifact, also writes a preview copy (home as endear.html) into OUT_DIR,
using explicit index.html links so it works where folder URLs don't.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://endearagency.github.io/'

PAGES = {
    'home': dict(dir='', title='endear | หา VTuber ไทย KOL งานอาร์ต งาน 3D และสินค้าที่ระลึก',
        desc='เอเจนซี่ดูแลโปรเจกต์สายอนิเมะ การ์ตูน และเกม หา VTuber ไทย, KOL, MC, คอสเพลเยอร์ รับทำงานอาร์ต Live2D แอนิเมชัน งาน 3D และ merchandise ครบในที่เดียว | Thai VTuber, art, 3D & merch agency.'),
    'talent': dict(dir='talent/', title='VTuber ไทยและต่างประเทศ KOL สตรีมเมอร์ รับงานโปรโมต รีวิว พากย์เสียง | endear',
        desc='รวม VTuber ไทยและต่างประเทศ สตรีมเมอร์ (streamer) และ KOL กว่า 60 คน รับงานโปรโมตเกมและสินค้า รีวิว พากย์เสียง คอลแลป Tie-in ดูยอดผู้ติดตามและช่องทางของแต่ละคนได้ทันที | Thai VTubers, streamers & KOLs for hire.'),
    'art': dict(dir='art/', title='รับวาดภาพประกอบ ออกแบบตัวละคร Live2D แอนิเมชัน MV | endear',
        desc='ทีมนักวาดสายอนิเมะ รับวาดภาพประกอบ (illustration) ออกแบบตัวละคร (character design) อีโมต สติกเกอร์ LINE ฉากสตรีม โมเดล Live2D สำหรับ VTuber เว็บตูน โมชันกราฟิก แอนิเมชัน และ MV | Anime art, Live2D & animation.'),
    '3d': dict(dir='3d/', title='รับทำโมเดล 3D งานพิมพ์ 3D ของที่ระลึก พิมพ์ UV | endear',
        desc='ปั้นโมเดล 3D สำหรับเกมและงานทั่วไป ผลิตของที่ระลึกพิมพ์ 3D (3D printing) พิมพ์ UV บนพื้นผิวพิเศษ และคอร์สเรียน 3D Print ตั้งแต่แบบร่างจนเป็นชิ้นงานจริง | 3D modeling, 3D printing & custom merch.'),
    'events': dict(dir='events/', title='อีเวนต์ สตาฟบูธ ผลิตสินค้าที่ระลึก merchandise | endear',
        desc='ดูแลอีเวนต์สายอนิเมะ การ์ตูน และเกม จัดหาสตาฟประจำบูธ (booth staff) และผลิตสินค้าที่ระลึก (merchandise) ตามแบบของคุณ | Events, booth staff & merchandise.'),
    'about': dict(dir='about/', title='เกี่ยวกับ endear เอเจนซี่สายอนิเมะ การ์ตูน และเกม',
        desc='endear เอเจนซี่ดูแลโปรเจกต์สายอนิเมะ การ์ตูน และเกมในประเทศไทย หาทีม ประสานงาน และดูแลงานให้จนจบ ทั้ง VTuber, KOL, งานอาร์ต, งาน 3D และสินค้าที่ระลึก'),
    'contact': dict(dir='contact/', title='ติดต่อ endear | LINE โทร Facebook',
        desc='คุยงานกับ endear บอกเราว่าอยากได้อะไร เราหาทีม ประสานงาน และดูแลให้จนจบงาน ติดต่อทาง LINE plaiendear โทร 094-555-1424 หรือ Facebook'),
}


def phero_th(src, page):
    """Thai page-hero text, read from the PH table in the page's own script."""
    m = re.search(r"\n  %s:\{ e:\['([^']*)'.*?h:\['([^']*)'.*?s:\['([^']*)'" % (("'3d'" if page == '3d' else page)), src)
    return m.groups() if m else None


def build(src, page, urls=None):
    cfg = PAGES[page]
    s = src.replace('<meta name="robots" content="noindex"><!--SRC-->\n', '')
    s = s.replace('<html lang="th">', '<html lang="th" data-page="%s">' % page, 1)
    if cfg['dir']:
        s = s.replace('<head>\n', '<head>\n<base href="../">\n', 1)
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
        s = s[:m.start(1)] + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    # page hero text in the HTML itself so search engines read it without running scripts
    if page != 'home':
        ph = phero_th(src, page)
        if ph:
            e, h, sub = ph
            s = re.sub(r'<!--PHERO-->.*?<!--/PHERO-->',
                       '<p class="eyebrow" id="phEyebrow">%s</p><h1 id="phH1">%s</h1><p class="hero-sub" id="phSub">%s</p><div class="chips ph-jump" id="phJump"></div>' % (e, h, sub),
                       s, count=1, flags=re.S)
            s = s.replace('<section id="phero" class="wrap hero phero" hidden>', '<section id="phero" class="wrap hero phero">', 1)
    else:
        s = s.replace('<!--PHERO-->', '').replace('<!--/PHERO-->', '')
    if urls:
        s = s.replace('<script>\n', '<script>window.PAGE_URLS=%s;</script>\n<script>\n' % json.dumps(urls), 1)
    return s


def sitemap(date):
    rows = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, c['dir'], date) for c in PAGES.values())
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n'


def main():
    src = open(os.path.join(ROOT, 'src', 'site.html'), encoding='utf-8').read()
    assert '<script>\n' in src
    for page, cfg in PAGES.items():
        out = os.path.join(ROOT, cfg['dir'], 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(build(src, page))
    import datetime
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sitemap(datetime.date.today().isoformat()))
    if '--artifact' in sys.argv:
        dest = sys.argv[sys.argv.index('--artifact') + 1]
        urls = {p: (c['dir'] + 'index.html' if c['dir'] else 'endear.html') for p, c in PAGES.items()}
        for page, cfg in PAGES.items():
            out = os.path.join(dest, cfg['dir'] + 'index.html' if cfg['dir'] else 'endear.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(build(src, page, urls))
    print('built', ', '.join(PAGES))


if __name__ == '__main__':
    main()
