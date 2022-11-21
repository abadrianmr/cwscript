import asyncio
import json
import re
import os
from pytz import utc
from random import randint
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon.events.newmessage import NewMessage
from repository import repository, User

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
        self.client.add_event_handler(self.trader_handler, events.NewMessage(from_users='chtwrsbot', pattern=regex_msg["trader"]))
        self.client.add_event_handler(self.quest_handler, events.NewMessage(from_users='me', chats=cws_id, pattern=regex_msg["quest"]))

    async def start(self):
        await self.client.start()
        await self.client.send_message(self.cws_id, "Running...")        

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

    async def quest_handler(self, event: NewMessage.Event):         
        place = event.raw_text[0]
        amount = int(event.raw_text[1:])
        await self.client.send_message(self.cws_id, f"Place: {place}\nAmount: {amount}", )

async def setOrder():
    t: TClient
    for t in clients:
        await t.sendOrder()                

async def main():        
    users: list[User] = repository.GetUsers()
    scheduler.add_job(setOrder, trigger="cron", hour='6,14,22', minute=18)
    scheduler.start()

    u:User
    for u in users:
        clients.append(TClient(u.session, u.api_id, u.api_hash, u.cws_id))
    t: TClient
    for t in clients:
        await t.start()   

    await t.client.run_until_disconnected()


if __name__ == '__main__':  
    asyncio.run(main())