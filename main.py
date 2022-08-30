
from cgitb import text
import json
import re
import os
from random import randint
import sys
from telethon import TelegramClient, events, sync
from telethon.events.newmessage import NewMessage
from telethon.sessions import StringSession
import  asyncio

class TClient:
    client: TelegramClient
    regex_msg = None

    @client.on(events.NewMessage(incoming=True, from_users='chtwrsbot'))
    async def cw_msg_handler(self, event: NewMessage.Event):        
        await self.client.forward_messages(self.cws_id, event.message)  

    @client.on(events.NewMessage(incoming=True, from_users='botniatobot'))
    async def orders_msg_handler(self, event: NewMessage.Event):  
        pattern1 = re.compile(self.regex_msg["order1"])
        pattern2 = re.compile(self.regex_msg["order2"])
        if(pattern1.match(event.raw_text)):     
            await self.client.send_message('botniatobot', "/order")
        elif pattern2.match(event.raw_text):
            index = event.raw_text.find('/')
            await self.client.send_message('botniatobot', event.raw_text[index:])

    @client.on(events.NewMessage(incoming=True, from_users='chtwrsbot', pattern=regex_msg["foray"]))
    async def foray_handler(self, event: NewMessage.Event): 
        delay = randint(30, 60)  
        await self.client.send_message(self.cws_id, f"Sending in: {delay} seconds.") 
        await asyncio.sleep(delay)    
        await event.message.click(0)

    @client.on(events.NewMessage(from_users='chtwrsbot', pattern=regex_msg["trader"]))
    async def trader_handler(self, event: NewMessage.Event): 
        delay = randint(10,20)  
        await self.client.send_message(self.cws_id, f"Sending in: {delay} seconds.") 
        await asyncio.sleep(delay)    
        ammount = re.findall(r'\b\d+\b', event.raw_text)
        await self.client.send_message('chtwrsbot', f"/sc 11 {ammount[1]}", ) 

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

        self.client: TelegramClient = TelegramClient(StringSession(session), api_id, api_hash).start()        

        print("Running...")
        sys.stdout.flush()
        self.client.send_message(self.cws_id, "Running...") 
        self.client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(TClient().main())

