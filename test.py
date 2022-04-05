from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import csv
import re
import requests

for urlIdx in range(273, 1056) :
    #2.BeautifulSoup
    driver = webdriver.Chrome('/Users/heeyeon/Downloads/chromedriver')
    driver.get('https://recipe.bom.co.kr/recipe/'+str(urlIdx)+'/detail')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    error  = "/html/images/404.png"
    err = soup.find_all("img", attrs={"src":error})
    if (err != []) :
        print(err)
    else:
        print(urlIdx)