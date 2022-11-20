import asyncio
import json
import re
import os
from pytz import utc
from random import randint
from telethon import TelegramClient, events, sync, functions, types
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.sessions import StringSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from telethon.events.newmessage import NewMessage

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')        
session = os.environ.get('SESSION')
cws_id = int(os.environ.get('CONF_CHAT_ID'))

clients = []
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=utc)
with open('messages.json') as f:
    regex_msg = json.load(f)

class TClient:
    client: TelegramClient
    cws_id: int

    async def ping(self, event: events.NewMessage):
        await self.client.send_message(self.cws_id, "pong")

    def __init__( self, session, api_id, api_hash, cws_id ):
        self.client = TelegramClient(StringSession(session), api_id, api_hash)
        self.cws_id = cws_id
        self.mobs_id = -1001408823679
        self.client.add_event_handler(self.ping, events.NewMessage(from_users='me', chats=cws_id, pattern="ping"))
        self.client.add_event_handler(self.cw_msg_handler, events.NewMessage(incoming=True, from_users='chtwrsbot'))
        self.client.add_event_handler(self.foray_handler, events.NewMessage(incoming=True, from_users='chtwrsbot', pattern=regex_msg["foray"]))
        self.client.add_event_handler(self.trader_handler, events.NewMessage(from_users='chtwrsbot', pattern=regex_msg["trader"]))
        self.client.add_event_handler(self.mobs_handler, events.NewMessage(from_users='chtwrsbot', pattern=regex_msg["mobs"]))

    async def start(self):
        await self.client.start()
    
    async def run(self):
        await self.client.send_message(self.cws_id, "Running...")
        await self.client.run_until_disconnected()

    async def sendOrder(self):
        await self.client.send_message('chtwrsbot', "🛡Defend")
    
    async def mobs_handler(self, event: NewMessage.Event):
        delay = randint(5, 20)  
        await self.client.send_message(self.cws_id, f"Sending mob to group: {delay} seconds.") 
        await asyncio.sleep(delay)
        await self.client.forward_messages(self.mobs_id, event.message)

    async def cw_msg_handler(self, event: NewMessage.Event):        
        await self.client.forward_messages(self.cws_id, event.message)

    async def foray_handler(self, event: NewMessage.Event): 
        delay = randint(30, 60)  
        await self.client.send_message(self.cws_id, f"Sending in: {delay} seconds.") 
        await asyncio.sleep(delay)    
        await event.message.click(0)

    async def trader_handler(self, event: NewMessage.Event): 
        delay = randint(10,20)  
        await self.client.send_message(self.cws_id, f"Sending in: {delay} seconds.") 
        await asyncio.sleep(delay)    
        ammount = re.findall(r'\b\d+\b', event.raw_text)
        await self.client.send_message('chtwrsbot', f"/sc 02 {ammount[1]}", )

async def setOrder():
    t: TClient
    for t in clients:
        await t.sendOrder()                

async def main():    
    scheduler.add_job(setOrder, trigger="cron", hour='6,14,22', minute=18)
    scheduler.start()
    clients.append(TClient(session, api_id, api_hash, cws_id))
    t: TClient
    for t in clients:
        await t.start()        
        await t.run()

if __name__ == '__main__':  
    asyncio.run(main())