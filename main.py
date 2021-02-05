import discord
import json
#import tweepy
import requests
import datetime
import chapter_scraper


months = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}


client = discord.Client()
with open("settings.json") as json_data:
  settings = json.load(json_data)
client.run(settings["settings"]["token"])
driver = chapter_scraper.create_webdriver()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  elif message.content.startswith("$mha_when"):
    await message.channel.send(chapter_scraper.find_chapter_date(driver))

  elif message.content.startswith("$mha_where"):
    await message.channel.send("\nMangaplus : {0} \nViz : {1}".format(settings["links"]["mangaplus"],settings["links"]["viz"]))  
  
  elif message.content.startswith("$mha_chapter"):
    chapter = chapter_scraper.find_chapter_link_mp(settings["latest"]["manga_chapter"])
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


