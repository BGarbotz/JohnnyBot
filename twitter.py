import selenium
import selenium.webdriver as webdriver
import requests
import datetime
from selenium.webdriver.firefox.options import Options


def find_chapter_link(driver):
    driver.get("https://mangaplus.shueisha.co.jp/titles/100017")
    data = driver.find_elements_by_css_selector("div.ChapterListItem-module_chapterListItem_ykICp")



    if data == []: 
        print("fail")
        find_chapter_link(driver)
    else: 
        for i in data:
            print(i.text)
            print(i.get_attribute("data-src"))


def find_chapter_date(driver):
    driver.get("https://mangaplus.shueisha.co.jp/titles/100017")
    data = driver.find_elements_by_tag_name("p")
    date_of_chapter = ""  

    for i in data: 
        print (i.text)
        if "day" in i.text:
            date_of_chapter = i.text
    
    if date_of_chapter == "":
        return find_chapter_date(driver)
    
    split_date = date_of_chapter.split(", ")
    return datetime.datetime(2020,(int)(months[(split_date[1][:-3])]),(int)(split_date[1][4:]),(int)(split_date[2][:-3]))

months = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)
#print(find_chapter_date(driver))
find_chapter_link(driver) 

