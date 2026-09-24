import feedparser
import argparse
from datetime import datetime, timedelta

FEEDS = {
    'hankyung-it': 'https://www.hankyung.com/feed/it',
    'zdnet-kr': 'https://zdnet.co.kr/rss/news.xml',
}

def fetch(feed_url, since):
    d = feedparser.parse(feed_url)
    out = []
    for e in d.entries:
        pub = datetime(*e.published_parsed[:6])
        if pub >= since:
            out.append((pub, e.title, e.link))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=1)
    ap.add_argument('--out', default='digest.md')
    args = ap.parse_args()
    since = datetime.now() - timedelta(days=args.days)
    items = []
    for name, url in FEEDS.items():
        items += fetch(url, since)
    items.sort()
    with open(args.out, 'w', encoding='utf-8') as f:
        for pub, t, l in items:
            f.write(f'- [{t}]({l}) ({pub:%Y-%m-%d %H:%M})\n')

if __name__ == '__main__':
    main()
