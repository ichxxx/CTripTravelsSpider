import re
import json
import random
import time
import requests
import string
from bs4 import BeautifulSoup
from headers_config import headers, USERAGENT_CONFIG

articles_titile = []
articles_url = []
articles_date = []

def get_resp(url, trys):
	if random.randint(0, 5) == 1:
		refresh_cookies()

	try:
		if trys < 0:
			return
		resp = session.get(url)
		return resp

	except:
		return get_resp(session, url, trys - 1)

def set_checkpoint(article_url):
	with open('checkpoint', 'w') as f:
		f.write(json.dumps({
		    "article_url": article_url
		}))
		f.close()

def get_checkpoint():
	try:
		with open('checkpoint', 'r') as f:
			content = f.read()
			if not content:
				return 0
			data = json.loads(content)
			if data:
				return data['article_url']
			else:
				return 0
	except IOError as e:
		return 0

def get_articles_info():
    global articles_url, articles_titile, articles_date

    try:
        with open('articles_info', 'r') as f:
            content = f.read()
            if not content:
                return 0
            articles_info = json.loads(content)
            if articles_info:
                for article_id in list(articles_info.keys()):
                    articles_titile.append(articles_info[article_id]['title'])
                    articles_url.append(articles_info[article_id]['url'])
                    articles_date.append(articles_info[article_id]['date'])
            else:
                return 0
    except IOError as e:
        return 0

def get_articles(articles_titile, article_url, articles_date):
	data = get_resp(article_url, 3)

	if data is None:
		print("ip被封!")
		return

	soup = BeautifulSoup(data.text, 'html.parser')

	content = soup.find_all("div", class_=re.compile("^ctd_content[\sa-z_]*"))

    for each in content:
        save_articles(article_title, each, article_date)

	set_checkpoint(article_url)

	time.sleep(1)

def save_articles(article_titile, article_content, article_date):
	f = open(article_titile + "_" + article_date + ".txt", "a")

    for p in article_content.find_all("p"):
        valid_content = p.get_text().replace(" ", "").replace("\n", "")
        if valid_content:
            try:
                f.write(valid_content + "\r\n\r\n")
            except IndexError as e:
                pass
            except ValueError as e:
                pass

    f.close()

def refresh_cookies():
	session.headers.clear()
	session.cookies.clear()
	random_useragent = random.choice(USERAGENT_CONFIG)
	session.headers = {
		"User-Agent": random_useragent,
		"Host": "article.douban.com",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, sdch, br",
		"Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
		"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
	}

def main():
	global articles_url, articles_title, articles_date

	get_articles_info()
	checkpoint = get_checkpoint()

	if checkpoint == 0:
		last_pos = 0
	else:
		last_pos = articles_url.index(checkpoint)

	for i in range(last_pos,len(articles_url)):
		print("正在获取第 %d 篇文章...进度 %.2f %" % (str(i), i*100/(len(articles_url)-1)))
		get_articles(articles_url[i])

	print('完成')

if __name__ == '__main__':
	with requests.Session() as session:
		main()
