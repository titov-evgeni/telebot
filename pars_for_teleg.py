import requests
from bs4 import BeautifulSoup
import random
import time
import json


def get_data(search):
    all_categories_dict = {}
    search_list = search.split()
    next_link = ""
    x = 0
    while True:
        if not x:
            url = "https://rabota.by/search/vacancy?st=searchVacancy" \
                  "&L_profession_id=29.8&area=1002&no_magic=true&text=%D0%9F%D1" \
                  "%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82" \
                  "+Python&page=0 "
        else:
            url = "https://rabota.by" + next_link

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.159 Safari/537.36 "
        }
        req = requests.get(url, headers=headers)
        src = req.text
        #
        # with open("index.html", "w", encoding="utf-8-sig") as file:
        #     file.write(src)
        #
        # with open("index.html", encoding="utf-8-sig") as file:
        #     src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_products_hrefs = soup.find_all("span", class_="g-user-content")

        for item in all_products_hrefs:
            item = item.find("a", {"class": "bloko-link"})
            item_text = item.text.lower()
            item_href = item.get("href")
            for word in search_list:
                if word in item_text:
                    all_categories_dict[item_text] = item_href
        try:
            next_page = soup.find_all("span", class_="bloko-form-spacer")
            for link in next_page:
                link = link.find("a", {"class": "bloko-button"})
            next_link = link.get("href")
            x += 1
            print(f"Итерация #{x} завершена")
            time.sleep(random.randrange(2, 4))
        except Exception as end:
            print("Page end")
            print(end)

            with open("all_categories_dict.json", "w",
                      encoding="utf-8-sig") as file:
                json.dump(all_categories_dict, file, indent=4,
                          ensure_ascii=False)
            # return True
            json_data = json.dumps(all_categories_dict, indent=4,
                                   ensure_ascii=False)
            return json_data
