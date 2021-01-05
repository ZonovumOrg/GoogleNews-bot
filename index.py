# Important import
from GoogleNews import GoogleNews
import time

# Default params
LANG = "en"
PERIOD = "1Y"
KEY_WORD = "bitcoin"
open('news.txt', 'a')
# Important fonction
news_csv_list = []
# while True:
googlenews = GoogleNews()
googlenews.set_lang(LANG)
googlenews.set_period(PERIOD)
googlenews.get_news(KEY_WORD)
news = googlenews.results()
print(len(news))
    # for x in news:
    #     news = x
    #     news_csv_list.append(news['title']+";"+news['desc']+";"+news['link']+";"+news['img']+";"+news['date'])
    # csv_convert = "\n".join(news_csv_list)
    # open('news.txt', 'w').write('title;desc;link;img;datetime\n%s'% csv_convert)
    # time.sleep(60)
    
