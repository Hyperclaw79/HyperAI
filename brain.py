import json
import requests
import aiohttp
import logging

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class Brain:
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick
        body = {
            'user': user,
            'key': key,
            'nick': nick
        }
        requests.post('https://cleverbot.io/1.0/create', json=body)


    async def query(self, text):
        sess = aiohttp.ClientSession()
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        async with sess.post('https://cleverbot.io/1.0/ask', json=body) as resp:
            r = await resp.json()

        if r['status'] == 'success':
            return r['response']
        else:
            return False

