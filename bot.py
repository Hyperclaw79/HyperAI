import discord
import aiohttp
import os
import asyncio
import inspect
from textwrap import dedent
from brain import Brain
from secrets import *
import re
import requests

class HyperAI(discord.Client):
    def __init__(self):
        self.prefix = '*'
        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' HyperAI/1.0'
        self.brain = Brain(cb_username, cb_key, cb_nick, loop=self.loop)        
        self.delay = 0
        self.triggerable = True
        self.redundancy_count = 0
        self.session = requests.Session()
        

    async def on_ready(self):
        print('HyperAI is now live!')
        game = discord.Game(name="that Chatgame with @CharlesTheAI")
        await self.change_presence(game=game)
        created_brain = await self.brain.create()
        print(created_brain)

    async def cmd_set_delay(self,message):
        if message.author.id == 132500768317112320 or "admin" in [role.name.lower() for role in message.author.roles]:
            self.delay = int(message.content.replace("{}set_delay ".format(self.prefix),'').strip())
        print("Successfully set the delay to {} seconds.".format(self.delay))

    async def cmd_bot_replies(self,message):
        if message.author.id == 132500768317112320 or "admin" in [role.name.lower() for role in message.author.roles]:
            switch = message.content.replace("{}bot_replies ".format(self.prefix),'').strip()
            if switch.lower() == "on":
                self.triggerable = True
                mess =  "Okay {}, HyperAI will respond to bots."
            elif switch.lower() == "off":
                self.triggerable = False
                mess = "Okay {}, HyperAI won't respond to bots."
            await message.channel.send(mess.format(message.author.mention))    
                
    async def cmd_ping(self, message):
        """
        Usage:
            {command_prefix}ping
                        
        Is it alive??
        """
        await message.channel.send("Pong!")

    async def cmd_say(self, message):
        """
        Usage:
            {command_prefix}say [your message]
                        
        Echoes your message after deleting it.
        """
        msg = message.content.replace("{}say".format(self.prefix),'').strip() 
        await message.channel.send(msg)
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))

    async def cmd_shrug(self, message):
        """
        Usage:
            {command_prefix}shrug
                        
        ASCII Shrugimation.
        """
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))
        shrugList = ["`¯\__(ツ)/¯`", "`¯\_(ツ)_/¯`", "`¯\(ツ)__/¯`", "`¯\_(ツ)_/¯`"]
        lulz = await message.channel.send(shrugList[1])
        i = 2
        while i < 400:
            await lulz.edit(content=shrugList[i%4])
            i = i + 1    

    async def cmd_wow(self, message):
        """
        Usage:
            {command_prefix}wow [your message]
                        
        Stylize your message using emoji letters.
        """
        message_content = message.content.strip()
        chan = message.channel
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))
        mesg = message_content.replace('{}wow'.format(self.prefix), '')

        t = ""
        nums = ['zero','one','two','three','four','five','six','seven','eight','nine']
        for c in mesg:
           if ord(c)<90 and ord(c)>=65:
              c = chr(ord(c)+32)
              c = ":regional_indicator_{}: ".format(c)
           elif c == " ":
              c = "  "
           elif ord(c)>=97 and ord(c)<=122:
              c = ":regional_indicator_{}: ".format(c)
           elif int(c)>=0 and int(c)<=9: 
              c = ":{}:".format(nums[int(c)])
           t = t + c
        await chan.send('\n{}'.format(t))            

    async def cmd_ppap(self, message):
       """
       Usage: 
       {command_prefix}ppap

       PPAP cancer, bot version.
       """
       mes = await message.channel.send("`¯\_(ツ)_/¯`")
       await mes.edit(content=":pen_ballpoint:         \n¯\_(ツ)_/¯")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pen_ballpoint:         :apple:\n¯\_(ツ)_/¯")
       await asyncio.sleep(1) 	   
       await mes.edit(content=":apple::pen_ballpoint:")
       await asyncio.sleep(2.5)
       await mes.edit(content=":pen_ballpoint:         \n¯\_(ツ)_/¯")
       await asyncio.sleep(1) 	   
       await mes.edit(content=":pen_ballpoint:         :pineapple:\n¯\_(ツ)_/¯")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pineapple::pen_ballpoint:")
       await asyncio.sleep(2.5)	   
       await mes.edit(content=":apple::pen_ballpoint:")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pineapple::pen_ballpoint:")
       await asyncio.sleep(2.5) 	   
       await mes.edit(content=":pen_ballpoint:")		
       await mes.edit(content=":pen_ballpoint::pineapple:")		
       await mes.edit(content=":pen_ballpoint::pineapple::apple:")	   
       await mes.edit(content=":pen_ballpoint::pineapple::apple::pen_ballpoint:")    

    async def cmd_moonwalk(self, message):
       """
       Usage:
           {command_prefix}moonwalk
                
       Use to see an emoji perform moonwalk.
       """
       m1 = await message.channel.send(".:walking:")	
       l = [":runner:",":walking:"]
       t = "."
       for i in range(25):
          t = t + "."
          s = t+l[i%2]
          await m1.edit(content=s)

    async def cmd_react(self, message):
        """
        Usage:
            {command_prefix}react [reaction1 reaction2 ....]
                        
        Add a list of reactions to the previous message. Separate the emojis with spaces.
        """
        target = await message.channel.history(limit=1, before=message).next()
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))
        reactions = message.content.replace('{}react ','').split(' ')
        for reaction in reactions:
            try:
                await target.add_reaction(reaction)
            except:
                pass    
    

    async def cmd_prune(self, message):
        """
        Usage:
            {command_prefix}prune
                        
        Deletes last X messages. Mods only.
        """
        role = str(message.author.top_role)
        mods = ["admin","mods"]
        if role in mods:
            try:
                count = int(message.content.split('{}prune '.format(self.prefix))[1].split(' ')[0].strip()) + 1
                try:
                    await message.channel.purge(limit=count)
                    notif = await message.channel.send("Successfully deleted the last {} messages. :thumbsup:".format(count))
                    await asyncio.sleep(30)
                    await notif.delete()
                except PermissionError:
                    await message.channel.send("Looks like I don't have permission to delete messages here. :eyes:")        
                except Exception as e:
                    print(str(e))        
            except IndexError:
                notif = await message.channel.send("You didn't provide the count.")
                await asyncio.sleep(30)
                await notif.delete()
        else:
            await message.author.send("Sorry but only the mods can prune messages. :sweat_smile:")

    async def cmd_help(self, message):
        """
        Usage:
            {command_prefix}help [command]
        
        Prints a help message.
        If a command is specified, it prints a help message for that command.
        Otherwise, it lists the available commands.
        """
        try:
            command = message.content.split("{}help ".format(self.prefix))[1].strip()
            cmdc = getattr(self, 'cmd_' + command, None)
            if cmdc:
                content = dedent(cmdc.__doc__).replace('{command_prefix}', '@   ' + self.prefix)
                content = content.replace('Usage','Usage (exclude the @)').replace('\n\n','\n')
                await message.author.send('```py\n{}```'.format(content))
            else:
                await message.author.send('No such command')
        except:
            msg1 = await message.author.send('**HyperAI Commands List:**\n')
            commands = []
            cmdc = {}
            #txt2 = ''
            #txt3 = ''
            for att in dir(self):
                if att.startswith('cmd_') and att != 'cmd_help':
                    try:
                        atc = getattr(self, att)
                        print(atc.__doc__ + '\n')
                        cmdc[att] = dedent(atc.__doc__.split('\n')[4])
                    except:
                        print('No docstring written for: ' + att)
            ''' 
            msg5 = await self.send_message(message.channel, '__Total number of commands__: **%d**' % comlen)
            count = 0
            for att in cmdc:
                count += 1
                if count < 15:
                    txt1 += dedent('```md\n<%s>```' % att.replace('cmd_', self.config.command_prefix) + '```diff\n-%s```\n' % cmdc[att])
                elif count > 15 and count < 30:
                    txt2 += dedent('```md\n<%s>```' % att.replace('cmd_', self.config.command_prefix) + '```diff\n-%s```\n' % cmdc[att])
                else:
                    txt3 += dedent('```md\n<%s>```' % att.replace('cmd_', self.config.command_prefix) + '```diff\n-%s```\n' % cmdc[att])

            msg2 = await (self.send_message(message.channel, txt1))
            msg3 = await (self.send_message(message.channel, txt2))
            msg4 = await (self.send_message(message.channel, txt3))
            await asyncio.sleep(300)
            await self.delete_message(msg1)
            await self.delete_message(msg5)
            await self.delete_message(msg2)
            await self.delete_message(msg3)
            await self.delete_message(msg4) '''
            comlen = len(cmdc)
            delme = await message.author.send('__Total number of commands__: **{}**\n'.format(comlen))
            txt1 = "```md\n"
            for att in cmdc:
                txt1 += dedent('[{}]( {})\n' .format(att.replace('cmd_', self.prefix),cmdc[att]))
            txt1 += "```"    
            await delme.edit(content=delme.content+txt1)
            await asyncio.sleep(300)
            await msg1.delete()
            await delme.delete()

    async def on_message(self, message):
        
        if self.prefix not in message.content and message.content != "(╯°□°）╯︵ ┻━┻" and not self.user.mentioned_in(message):
            return

        # we do not want the bot to reply to itself or other bots
        if message.author.id == self.user.id:
            return

        #Chatbot
        if self.user.mentioned_in(message) and not message.mention_everyone:
            if (message.author.bot and self.triggerable) or not message.author.bot:
                async with message.channel.typing():
                    if message.author.bot:
                        with open('logs.txt','r') as f:
                            logs = [message.split('-> ')[1] for message in f.read().splitlines() if '->' in message]
                        reply = re.sub(r"<@\d+>", "" ,message.content.strip())
                        if reply in logs:
                            self.redundancy_count += 1
                            quote = self.session.get("https://random-quote-generator.herokuapp.com/api/quotes/random").json()
                            while "quote" not in quote.keys():
                                quote = self.session.get("https://random-quote-generator.herokuapp.com/api/quotes/random").json()
                            quote = quote["quote"]
                            await message.channel.send("{} {}".format(message.author.mention,quote))
                            with open('logs.txt','a') as f:
                                f.write("\n{} -> {}".format(message.guild.me.name, quote.replace('\n',' ')))
                        else:    
                            await asyncio.sleep(self.delay)
                            with open('logs.txt','a') as f:
                                reply = re.sub(r"<@\d+>", "" ,message.content.strip())
                                f.write("\n{} -> {}".format(message.author.name, reply.replace('\n',' ')))
                                response, status = await self.brain.query(message.content)
                                if status == 500:
                                    while "quote" not in quote.keys():
                                        quote = self.session.get("https://random-quote-generator.herokuapp.com/api/quotes/random").json()
                                    quote = quote["quote"]
                                    response = response.strip()
                                reply = re.sub(r"<@\d+>", "" , response)
                                while reply in logs:
                                    self.redundancy_count += 1
                                    while "quote" not in quote.keys():
                                        quote = self.session.get("https://random-quote-generator.herokuapp.com/api/quotes/random").json()
                                    quote = quote["quote"]
                                    reply = re.sub(r"<@\d+>", "" , response)
                                await message.channel.send("{} {}".format(message.author.mention,response))
                                f.write("\n{} -> {}".format(message.guild.me.name, reply.replace('\n',' ')))
                    else:
                        response, status = await self.brain.query(message.content)
                        if status == 500:
                            while "quote" not in quote.keys():
                                quote = self.session.get("https://random-quote-generator.herokuapp.com/api/quotes/random").json()
                            quote = quote["quote"]
                            response = response.strip()
                        await message.channel.send("{} {}".format(message.author.mention,response))
                        
            elif message.author.bot and not self.triggerable:
                return
            else:
                pass


        if message.content == "(╯°□°）╯︵ ┻━┻":
            await message.channel.send("┬─┬ ノ( ゜-゜ノ)")    

        #----------------------------------------------------------------------------#
        # Don't worry about this part. We are just defining **kwargs for later use.
        cmd, *args = message.content.split(' ') # The first word is cmd, everything else is args. 
        cmd = cmd[len(self.prefix):].lower().strip() # For '$', cmd = cmd[1:0]. Eg. $help -> cmd = help
        handler = getattr(self,'cmd_{}'.format(cmd),None) # Checks if MyBot has an attribute called cmd_command (cmd_help).
        if not handler: # The command given doesn't exist in our code, so ignore it.
            return
        prms = inspect.signature(handler) # If attr is defined as async def help(a,b='test',c), prms = (a,b='test',c)
        params = prms.parameters.copy() # Copy since parameters are immutable.
        h_kwargs = {}                   # Dict for group testing all the attrs.
        if params.pop('message',None):
            h_kwargs['message'] = message
        if params.pop('channel',None):
            h_kwargs['channel'] = message.channel
        if params.pop('guild',None):
            h_kwargs['guild'] = message.guild
        if params.pop('mentions',None):
            h_kwargs['mentions'] = list(map(message.server.get_member, message.raw_mentions)) # Gets the user for the raw mention and repeats for every user in the guild.            
        if params.pop('args',None):
            h_kwargs['args'] = args

        # For remaining undefined keywords:
        for key, param in list(params.items()):
            if not args and param.default is not inspect.Parameter.empty: # Junk parameter present for attribute 
                params.pop(key) 
                continue        # We don't want that in our tester.

            if args:
                h_kwargs[key] = args.pop(0) # Binding keys to respective args.
                params.pop(key)

        # Time to call the test.
        res = await handler(**h_kwargs)
        if res and isinstance(res, Response): # Valid Response object
                content = res.content
                if res.reply:
                    content = '{},{}'.format(message.author.mention, content)

                sentmsg = await message.channel.send(content)

bot = HyperAI()    
bot.run(bot_token)
