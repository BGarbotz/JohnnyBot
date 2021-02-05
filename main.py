import discord
import os
import json
import tweepy
import selenium
import selenium.webdriver as webdriver
import requests
import datetime
from selenium.webdriver.firefox.options import Options


months = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}


client = discord.Client()
with open("settings.json") as json_data:
  settings = json.load(json_data)

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)


def find_chapter_link_mp(driver):
    driver.get("https://mangaplus.shueisha.co.jp/titles/100017")
    data = driver.find_elements_by_class_name("ChapterListItem-module_chapterListItem_ykICp")
    chapter = -1
    link = "https://mangaplus.shueisha.co.jp/viewer/"
    items = []

    if data == []: 
            return find_chapter_link_mp(driver)
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
            if items[i] == "#298":
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


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  elif message.content.startswith("$mha_when"):
    await message.channel.send(find_chapter_date(driver))

  elif message.content.startswith("$mha_where"):
    await message.channel.send("\nMangaplus : {0} \nViz : {1}".format(settings["links"]["mangaplus"],settings["links"]["viz"]))  
  
  elif message.content.startswith("$mha_chapter"):
    chapter = find_chapter_link_mp(driver)
    await message.channel.send("You can read the newest My Hero Academia Chapter **{0}**, released {1}, on\nMangaplus : {2}".format(chapter[1],chapter[2],chapter[3]))

  elif message.content.startswith("$help"):
    await message.channel.send("Hi! Here are the available commands:\n**$mha_when**: Find out when the next My Hero Academia Chapter releases!\n**$mha_where**: Find out where to read My Hero Academia!\n**$mha_chapter**: Get the link to the latest My Hero Academia Chapter!") 

  elif message.content.startswith("$set_channel"): 
    if (message.content == "$set_channel"):
      await message.channel.send("Please select a channel!")

    set_channel(message.content.replace("$set_channel ",""))
    print((settings["settings"]["channel"])[2:-1])
    await message.channel.send("From now on I'll send messages into {0}".format(client.get_channel((int)((settings["settings"]["channel"])[2:-1])).name))

  elif settings["settings"]["channel"] == "" and message.content.startswith("$"):
    await message.channel.send("Please specify a designated channel first!")

def set_channel(new_channel):
  settings["settings"]["channel"] = new_channel

  with open("settings.json","w") as json_data:
    json.dump(settings, json_data, indent=2)






client.run(settings["settings"]["token"])