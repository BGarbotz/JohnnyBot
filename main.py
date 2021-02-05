import discord
import json
#import tweepy
import requests
import datetime
import pytz
import chapter_scraper


months = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
driver = chapter_scraper.create_webdriver()

client = discord.Client()
with open("settings.json") as json_data:
  settings = json.load(json_data)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  elif message.content.startswith("$mha_when"):

    chapter_date = chapter_scraper.find_chapter_date(driver)
    chapter_date.replace(tzinfo=pytz.timezone("Europe/Berlin"))
    now = datetime.datetime.now()
    difference = chapter_date - now 
    if message.content[len("$mha_when "):]=="":
      if difference.days == 0:
        await message.channel.send("The new My Hero Academia chapter releases today in {0} hours and {1} minutes".format((int)(difference.seconds/3600),(int)(difference.seconds/60) % 60))
      else:
        await message.channel.send("The new My Hero Academia chapter releases in {0} hours and {1} minutes".format((int)(difference.seconds/3600),(int)(difference.seconds/60) % 60)) 
    else:
      if message.content[len("$mha_when "):] not in pytz.all_timezones:
        if difference.days == 0:
          await message.channel.send("Invalid timezone! The new My Hero Academia chapter releases today in {0} hours and {1} minutes".format((int)(difference.seconds/3600),(int)(difference.seconds/60) % 60))  
        else:
          await message.channel.send("Invalid timezone! The new My Hero Academia chapter releases in {0} hours and {1} minutes".format((int)(difference.seconds/3600),(int)(difference.seconds/60) % 60)) 
      else:
        chapter_date = chapter_date.astimezone(pytz.timezone(message.content[len("$mha_when "):]))
        if difference.days == 0:
          await message.channel.send("The new My Hero Academia chapter releases today at {0}".format(chapter_date.strftime("%X")))  
        else:
          await message.channel.send("The new My Hero Academia chapter releases on {0} {1} at {2}".format(chapter_date.strftime("%A"),chapter_date.strftime("%x"),chapter_date.strftime("%X")))


  elif message.content.startswith("$mha_where"):
    await message.channel.send("\nMangaplus : {0} \nViz : {1}".format(settings["links"]["mangaplus"],settings["links"]["viz"]))  
  

  elif message.content.startswith("$mha_chapter"):
    chapter = chapter_scraper.find_chapter_link_mp(driver,settings["latest"]["manga_chapter_next"])
    await message.channel.send("You can read the newest My Hero Academia Chapter **{0}**, released {1}, on\nMangaplus : <{2}>\nViz : <{3}>".format(chapter[1],chapter[2],chapter[3],chapter_scraper.find_chapter_link_viz(driver,settings["latest"]["manga_chapter_next"])))


  elif message.content.startswith("$help"):
    await message.channel.send("Hi! Here are the available commands:\n**$mha_when**: Find out when the next My Hero Academia Chapter releases!\n**$mha_where**: Find out where to read My Hero Academia!\n**$mha_chapter**: Get the link to the latest My Hero Academia Chapter!") 

  elif message.content.startswith("$stop"):
    driver.quit()


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
