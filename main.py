
from cgitb import text
import json
import re
import os
from random import randint
from telethon import TelegramClient, events, sync
from telethon.events.newmessage import NewMessage
import  asyncio

with open('messages.json') as f:
    regex_msg = json.load(f)

api_id = 1594535
api_hash = '720d893966b2d956fc855b99696dee38'
cws_id = -727169472
client = TelegramClient('anon', api_id, api_hash).start()
print("Hello")
client.send_message(cws_id, "Running...") 

@client.on(events.NewMessage(incoming=True, from_users='chtwrsbot'))
async def cw_msg_handler(event: NewMessage.Event):        
    await client.forward_messages(cws_id, event.message)  

@client.on(events.NewMessage(incoming=True, from_users='chtwrsbot', pattern=regex_msg["foray"]))
async def foray_handler(event: NewMessage.Event): 
    delay = randint(30, 60)  
    await client.send_message(cws_id, f"Sending in: {delay} seconds.") 
    await asyncio.sleep(delay)    
    event.message.click(0)

@client.on(events.NewMessage(from_users='chtwrsbot', pattern=regex_msg["trader"]))
async def trader_handler(event: NewMessage.Event): 
    delay = randint(10,20)  
    await client.send_message(cws_id, f"Sending in: {delay} seconds.") 
    await asyncio.sleep(delay)    
    ammount = re.findall(r'\b\d+\b', event.raw_text)
    await client.send_message(cws_id, f"/sc 41 {ammount[1]}") 

client.run_until_disconnected()