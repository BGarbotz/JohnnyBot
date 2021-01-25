import discord
import os
import json
import tweepy

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

  elif settings["settings"]["channel"] == "":
    await message.channel.send("Please specify a designated channel first!")

  elif message.content.startswith("$hello"):
    await client.get_channel((int)((settings["settings"]["channel"])[2:-1])).send("@everyone \nMangaplus : {0} \nViz : {1}".format(settings["links"]["mangaplus"],settings["links"]["viz"]))

  elif message.content.startswith("$set_channel"): 
    if (message.content == "$set_channel"):
      await message.channel.send("Please select a channel!")

    set_channel(message.content.replace("$set_channel ",""))
    print((settings["settings"]["channel"])[2:-1])
    await message.channel.send("From now on I'll send messages into {0}".format(client.get_channel((int)((settings["settings"]["channel"])[2:-1])).name))


def set_channel(new_channel):
  settings["settings"]["channel"] = new_channel

  with open("settings.json","w") as json_data:
    json.dump(settings, json_data, indent=2)


client.run(settings["settings"]["token"])