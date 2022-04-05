from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import csv
import re
import requests


 #1. csv file open
csv_name = "recipe10.csv"
csv_open = open(csv_name, "w+", encoding="utf-8")
csv_writer = csv.writer(csv_open)
csv_writer.writerow(("cat/dog","health issue", "cooking time", "name", "save", "ingredient", "cook"))

for urlIdx in range(429, 1056) :
    #2.BeautifulSoup
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    d = webdriver.Chrome('/Users/heeyeon/Downloads/chromedriver', chrome_options=chrome_options)
    try:
        d.get('https://recipe.bom.co.kr/recipe/'+str(urlIdx)+'/detail')
        html = d.page_source
    except WDE:
        continue
    #driver = webdriver.Chrome('/Users/heeyeon/Downloads/chromedriver')
    #driver.get('https://recipe.bom.co.kr/recipe/'+str(urlIdx)+'/detail')


    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)

    error = "/html/images/404.png"
    error2 = "Whoops, looks like something went wrong."
    err = soup.find_all("img", attrs={"src": error})
    err2 = soup.find_all("h1", text=error2)

    if (err != []):
        continue
    elif (err2 != []):
        continue
    else:


            #headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            #ro_url = f"https://recipe.bom.co.kr/recipe/1037/detail"
            #result = requests.get(ro_url, headers=headers)
            #soup = BeautifulSoup(result.text, 'html.parser')

            #print(soup)


            #4. Get element selector

        total=[]
        #print(tmp)
        des = []
        health_issue = "/searchs?function="
        cooking_time = "/searchs?cooking_time="
        recipe_des = soup.select("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div.items-talk-detail.block-view-detail.clearfix > div > div.item-description > div.link ")
        for div in recipe_des:
            for a in div.findAll('a'):
                if(a['href'] == "/dogs"): #강아지/고양이
                    total.append("강아지")
                elif(a['href']=="/cats"):
                    total.append("고양이")
                elif(health_issue in a['href']): #건강 고민
                    total.append(a.text)
                elif(cooking_time in a['href']): #조리 시간
                    total.append(a.text)


        #레시피 이름
        recipe_name = soup.select_one("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div.items-talk-detail.block-view-detail.clearfix > div > div.item-description > strong").text
        total.append(recipe_name)

        #보관 정보
        processed_text = ""
        recipe_save = soup.select_one("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div.items-talk-detail.block-view-detail.clearfix > div > div.item-description > div.des").text
        for word in recipe_save:
            processed_text += word.replace(',', '').replace('\'', '').replace('!', '')
        total.append(processed_text)

        #재료 정보
        ingredients=""
        recipe_ingredient = soup.select("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div:nth-child(5) > div.items.row")

        for div in recipe_ingredient:
            details = div.findAll("div", "detail")

        for h3, span in details:
            name = h3.select_one('a').text
            ingredients+=name
            amount = span.text
            ingredients+=amount
        total.append(ingredients)
        #조리 순서
        orders=""
        cooking = soup.select("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div.block-view-order > div.block-content ")
        for div in cooking:
            description = div.findAll("div", "des")
        for div in description:
            orders+=div.text
        total.append(orders)
        csv_writer.writerow(total)

csv_open.close()

#item = []
#item = soup.select("#app > div:nth-child(2) > div.wrapper > main > div.container > div > div.items-talk-detail.block-view-detail.clearfix > div > div.item-description > div.link ").text
#print(item)


#lists = bs.select("#container > div.content > div.product_result_wrap.product_result_wrap01 > div > dl > dd:nth-child(2) > div.product_list > dl > dd:nth-child(2) > ul > li:nth-child(1) > dl > dd")
#imgs = bs.select("#container > div.content > div.product_result_wrap.product_result_wrap01 > div > dl > dd:nth-child(2) > div.product_list > dl > dd:nth-child(2) > ul > li:nth-child(1) > dl > dt > a > img")
#5. Save drink, img
#with open(csv_name, "w+", encoding = "utf-8") as file:
#    for i in range(len(lists)):
#        #drink
#        drink = lists[i]['dd']

#        #image_url
#        img_url = crawling_url + '/' + imgs[i]['src']

#        writer = csv.writer(file)
#        writer.writerow((drink, img_url))
