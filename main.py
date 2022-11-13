from cgitb import text
import json
import re
import os
from random import randint
import sys
import datetime as dt
from datetime import datetime
import aiocron
from telethon import TelegramClient, events, sync
from telethon.events.newmessage import NewMessage
from telethon.sessions import StringSession
import asyncio

class TClient:
    client: TelegramClient
    regex_msg: None
    repository: None

    async def main(self):
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        print("Starting running...")
        sys.stdout.flush()

        with open('messages.json') as f:
            self.regex_msg = json.load(f)

        api_id = os.environ.get('API_ID')
        api_hash = os.environ.get('API_HASH')        
        session = os.environ.get('SESSION')
        self.cws_id = int(os.environ.get('CONF_CHAT_ID'))
        self.mobs_id = -1001408823679

        self.client: TelegramClient = await TelegramClient(StringSession(session), api_id, api_hash).start()       
        self.client.add_event_handler(self.cw_msg_handler, events.NewMessage(incoming=True, from_users='chtwrsbot'))
        self.client.add_event_handler(self.orders_msg_handler, events.NewMessage(incoming=True, from_users='botniatobot'))
        self.client.add_event_handler(self.foray_handler, events.NewMessage(incoming=True, from_users='chtwrsbot', pattern=self.regex_msg["foray"]))
        self.client.add_event_handler(self.trader_handler, events.NewMessage(from_users='chtwrsbot', pattern=self.regex_msg["trader"]))
        self.client.add_event_handler(self.config_trader_handler, events.NewMessage(from_users='me', chats=self.cws_id,pattern=self.regex_msg["traderConfig"]))
        self.client.add_event_handler(self.mobs_handler, events.NewMessage(from_users='chtwrsbot', pattern=self.regex_msg["mobs"]))
        print("Running...")
        sys.stdout.flush()        

        await self.client.send_message(self.cws_id, "Running...")        
        await self.client.run_until_disconnected()        

    @aiocron.crontab('*/1 * * * *')
    async def show_time(self):
        await self.client.send_message(self.cws_id, "Hello")

    async def send_order(self):
        await self.client.send_message(self.cws_id, "🛡Defend")
    
    async def cw_msg_handler(self, event: NewMessage.Event):        
        await self.client.forward_messages(self.cws_id, event.message)  
        
    async def orders_msg_handler(self, event: NewMessage.Event):  
        pattern1 = re.compile(self.regex_msg["order1"])
        pattern2 = re.compile(self.regex_msg["order2"])
        pattern3 = re.compile(self.regex_msg["order3"])
        if(pattern1.match(event.raw_text)):     
            await self.client.send_message('botniatobot', "/order")
        elif pattern2.match(event.raw_text):
            index = event.raw_text.find('/')
            delay = randint(2,5)  
            await asyncio.sleep(delay) 
            await self.client.send_message('botniatobot', event.raw_text[index:])
        elif pattern3.match(event.raw_text):
            order = re.search(r'.*(\(https:\/\/t.me\/share\/url\?url=(.*?)\))', event.raw_text).group(2)
            await self.client.send_message(self.cws_id, order)
            #await self.client.send_message(self.cws_id, schedule=)

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

    async def mobs_handler(self, event: NewMessage.Event):
        delay = randint(5, 20)  
        await self.client.send_message(self.cws_id, f"Sending mob to group: {delay} seconds.") 
        await asyncio.sleep(delay)
        await self.client.forward_messages(self.mobs_id, event.message)

    async def config_trader_handler(self, event: NewMessage.Event):
        sender = await event.get_sender()

if __name__ == '__main__':
    asyncio.run(TClient().main())
