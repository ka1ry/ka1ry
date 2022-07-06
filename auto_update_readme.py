"""
METRIC FIELDS

1 => Joined GitHub X year ago
2 => Followed by X users
3 => . (bugged)
4 => Contributed to X repository
5 => X commits
6 => X PRs Reviewed
7 => X PRs Opened
8 => X Issues Opened
9 => X Issues comments
10 => Member of X organizations
11 => Following X users
12 => Sponsoring X repositories
13 => Starred X repositories
14 => Watching X repository
15 => Preferred license
16 => X Releases
17 => X Packages
18 => X byte used (code)
19 => X Sponsors
20 => X Stargazers
21 => X Forkers
22 => X Watchers
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = (
    "https://metrics.lecoq.io/ed1ndev"
    "?template=classic&isocalendar=1&isocalendar.duration=half-year"
    "&config.timezone=Europe%2FLjubljana"
)

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

fields = [div.text.strip() for div in soup.find_all('div', class_='field')]


def extract_number(string):
    n = ''.join(ch for ch in string if ch.isdigit() or ch == '.')
    return int(n) if n.isdigit() else float(n)


data = {
    k: extract_number(fields[i])
    for (k, i) in {
        'contributed': 4,
        'pr_opened': 7,
        'issues': 8,
    }.items()
}

today = datetime.now()
DATE_OF_BIRTH = datetime(year=2005, month=7, day=20)

current_age = int((today - DATE_OF_BIRTH).days / 365)
data['age'] = current_age

with open('BASE.md', 'r') as f:
    base = f.read()

with open('README.md', 'w') as f:
    f.write(base.format(**data))
