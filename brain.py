import json
import aiohttp
import logging

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class Brain:
    def __init__(self, user, key, nick, loop):
        self.user = user
        self.key = key
        self.nick = nick
        self.loop = loop
        self.sess = aiohttp.ClientSession(loop=self.loop)

    async def create(self):
        body = {
                    'user': self.user,
                    'key': self.key,
                    'nick': self.nick
                }
        with aiohttp.Timeout(10):
            async with self.sess.post('https://cleverbot.io/1.0/create', json=body) as resp:
                r = await resp.json()
        if resp.status > 304:
            return "API is down. Using qoutes mode."
        else:
            return "API is online. Using clever mode."
        
    async def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }
        try:
            with aiohttp.Timeout(10):
                async with self.sess.post('https://cleverbot.io/1.0/ask', json=body) as resp:
                    r = await resp.json()

            if r['status'] == 'success':
                return r['response'], 200
        except:
            return "Looks like the CleverBot.IO api is down. Please try later.", 500

