import re
import json
import time
import urllib.request
import requests
from bs4 import BeautifulSoup
from headers_config import headers

def get_articles():
    total_page = 400
    index = 1
    data = {}

    for i in range(index, total_page+1):
        counter = 1

        json_url = "https://you.ctrip.com/searchsite/travels/?query=古城&isRecommended=1&PageNo=" + str(i)

        res = session.get(json_url, headers=headers)

        res_soup = BeautifulSoup(res.text, "html.parser")
        main_contain = res_soup.find_all("li", class_="cf")

        for each in main_contain:
            articles_info = each.find_all("a")
            tag = str(index) + "-" + str(counter)
            data[tag] = {}
            data[tag]["url"] = "https://you.ctrip.com" + articles_info[1]["href"]
            data[tag]["title"] = articles_info[1].text
            data[tag]["date"] = re.findall(r"[0-9]+-[0-9]+-[0-9]+", str(articles_info[2].next_sibling))

            print("Progress: %d # %d" % (int(index), int(counter)))

            counter += 1

        index += 1
        time.sleep(1)

    f = open("articles_info", "a")
    try:
        f.write(json.dumps(data))
    except IndexError as e:
        pass
    except ValueError as e:
        pass
    finally:
        f.close()

if __name__ == '__main__':
    with requests.Session() as session:
        get_articles()