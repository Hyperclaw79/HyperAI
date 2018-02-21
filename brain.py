import json
import aiohttp
import logging

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class Brain:
    def __init__(self, user, key, nick, loop):
        self.user = user
        self.key = key
        self.nick = nick
        body = {
            'user': user,
            'key': key,
            'nick': nick
        }
        self.loop = loop
        self.sess = aiohttp.ClientSession(loop=self.loop)
        self.sess.post('https://cleverbot.io/1.0/create', json=body)
        
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

