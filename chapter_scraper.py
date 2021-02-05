import selenium
import selenium.webdriver as webdriver
import requests
import datetime
from selenium.webdriver.firefox.options import Options

months = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}

def create_webdriver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    return driver


def find_chapter_link_mp(driver,curren_chapter):
    driver.get("https://mangaplus.shueisha.co.jp/titles/100017")
    data = driver.find_elements_by_class_name("ChapterListItem-module_chapterListItem_ykICp")
    chapter = -1
    link = "https://mangaplus.shueisha.co.jp/viewer/"
    items = []

    if data == []: 
            return find_chapter_link_mp(driver,curren_chapter)
    else:
        for element in data: 
            
            for line in element.text.split("\n"):
                if not line[7:-6] == "-":
                    items.append(line)
                
            links = element.find_elements_by_class_name("ChapterListItem-module_thumbnail_1w6kS")    

            for i in links:
                items.append(i.get_attribute("data-src"))
    
        print (items)
        for i in range(0,len(items),4):
            print(items[i])
            if items[i] == "#{0}".format(curren_chapter):
                return ((items[i],items[i+1],items[i+2],link+(items[i+3][len("https://mangaplus.shueisha.co.jp/drm/title/100017/chapter/"):]).split("/")[0]))


def find_chapter_date(driver):
    driver.get("https://mangaplus.shueisha.co.jp/titles/100017")
    data = driver.find_elements_by_tag_name("p")
    date_of_chapter = ""  

    for i in data: 
        if "day" in i.text:
            date_of_chapter = i.text
    
    if date_of_chapter == "":
        return find_chapter_date(driver)
    
    split_date = date_of_chapter.split(", ")
    return datetime.datetime(2020,(int)(months[(split_date[1][:-3])]),(int)(split_date[1][4:]),(int)(split_date[2][:-3]))


    

