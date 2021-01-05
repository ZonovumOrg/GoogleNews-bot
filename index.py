# Important import
from GoogleNews import GoogleNews
import time
import pandas as pd
# Default params
LANG = "en"
PERIOD = "1Y"
KEY_WORD = "bitcoin"
open('news.txt', 'a')
# Important fonction
news_csv_list = []
dates = []
titles = []
descs = []
links = []
# while True:
print('Loading... ', end=" ")
googlenews = GoogleNews()
googlenews.set_lang(LANG)
googlenews.set_period(PERIOD)
googlenews.get_news(KEY_WORD)
news = googlenews.results()
print('Done.')
for x in news:
    dates.append(x['datetime'])
    titles.append(x['title'])
    descs.append(x['desc'])
    links.append(x['link'])
df = pd.DataFrame({'dates': dates, 'titles': titles, 'descs': descs, 'links': links})
csv_file = df.to_csv(index=False)
open('news.txt', 'w').write(csv_file)
print('New news file added.')
