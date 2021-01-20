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

  if message.content.startswith("$hello"):
    await message.channel.send("@everyone \nMangaplus : {0} \nViz : {1}".format(settings["links"]["mangaplus"],settings["links"]["viz"]))


client.run(settings["settings"]["token"])