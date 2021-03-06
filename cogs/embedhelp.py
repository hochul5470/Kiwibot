import discord
import os
import collections
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/help/toggle.json"
        self.riceCog = dataIO.load_json(self.profile)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def sethelp(self, ctx):
        self.profile = "data/help/toggle.json"
        self.riceCog = dataIO.load_json(self.profile)
        dm_msg = "The help message will now be send in DM."
        no_dm_msg = "The help message will now be send into the channel."
        if 'toggle' not in self.riceCog:
            self.riceCog['toggle'] = "no_dm"
            dataIO.save_json(self.profile,
                             self.riceCog)
            msg = no_dm_msg
        elif self.riceCog['toggle'] == "dm":
            self.riceCog['toggle'] = "no_dm"
            dataIO.save_json(self.profile,
                             self.riceCog)
            msg = no_dm_msg
        elif self.riceCog['toggle'] == "no_dm":
            self.riceCog['toggle'] = "dm"
            dataIO.save_json(self.profile,
                             self.riceCog)
            msg = dm_msg
        if msg:
            await self.bot.say(msg)



    @commands.command(name='help', pass_context=True)
    async def _help(self, ctx, command = None):
        """Embedded help command"""
        author = ctx.message.author
        if 'toggle' not in self.riceCog:
            self.riceCog['toggle'] = "dm"
            dataIO.save_json(self.profile,
                             self.riceCog)
            await self.bot.say("Help message is set to DM by default. use "
                               "**{}sethelp** to change it!".format(ctx.prefix))
            toggle = self.riceCog['toggle']
        else:
            toggle = self.riceCog['toggle']
        if not command:
            msg = "**명령어 목록:**"
            color = 0xffa500


            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if self.bot.commands[com].module.__name__ not in com_groups:
                        com_groups.append(self.bot.commands[com].module.__name__)
                    else:
                        continue
                except Exception as e:
                        print(e)
                        continue
            com_groups.sort()
            alias = []
            #print(com_groups)
            for com_group in com_groups:
                commands = []
                for com in self.bot.commands:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if com in self.bot.commands[com].aliases:
                        continue
                    if com_group == self.bot.commands[com].module.__name__:
                        commands.append(com)
                final_coms[com_group] = commands

            to_send = []

            final_coms = collections.OrderedDict(sorted(final_coms.items()))
            field_count = 0
            page = 0
            counter = 0

            for group in final_coms:
                counter += 1
                if field_count == 0:
                    page += 1
                    title = "**명령어 목록,** {}페이지".format(page)
                    em=discord.Embed(description=title,
                                     color=color)

                field_count += 1
                is_last = counter == len(final_coms)
                msg = ""
                final_coms[group].sort()
                count = 0
                for com in final_coms[group]:
                    if count == 0:
                        msg += ' `{}`'.format(com)
                    else:
                        msg += ' `{}`'.format(com)
                    count += 1

                cog_name = group.replace("cogs.", "").title()
                cog =  "```\n"
                cog += cog_name
                cog += "\n```"
                em.add_field(name=cog,
                             value=msg,
                             inline=False)

                if field_count == 15 or is_last:
                    to_send.append(em)
                    field_count = 0


            if toggle == "dm":
                await self.bot.say("{}님! 제가 당신 DM에게 "
                                   "도움말을 보냈어요!".format(author.mention))
                for em in to_send:
                    await self.bot.send_message(ctx.message.author,
                                                embed=em)
                await self.bot.send_message(ctx.message.author, "레드 디스코드 봇 \n제작 Twentysix26(cog_creator) 한글화 및 embed화 : 채뭉")
            elif toggle == 'no_dm':
                for em in to_send:
                    await self.bot.say(embed=em)
                await self.bot.say("레드 디스코드 봇 \n제작 Twentysix26(cog_creator) 한글화 및 embed화 : 채뭉")

        else:
            msg = "**명령어 도움:**"
            color = 0xffa500

            em=discord.Embed(description=msg,
                             color=color)
            try:
                if not self.bot.commands[command].can_run(ctx):
                    await self.bot.say("Might be lacking perms for this "
                                       "command.")
                    return
                commie =  "```\n"
                commie += command + " " + " ".join(["[" + com + "]" for com in \
                                                    self.bot.commands[command].\
                                                    clean_params])
                commie += "\n```"
                info = self.bot.commands[command].help
                em.add_field(name=commie,
                             value=info,
                             inline=False)
                await self.bot.say(embed=em)
            except Exception as e:
                print(e)
                em=discord.Embed(color=discord.Colour.red())
                em.add_field(name='잠시만요!',
                             value='명령어가 존재 하지 않아요! 오타가 있으신지 확인 해보세요!',
                             inline=False)
                await self.bot.say(embed=em)

def check_folder():
    if not os.path.exists("data/help"):
        print("Creating data/help folder")
        os.makedirs("data/help")

def check_file():
    data = {}
    f = "data/help/toggle.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/help/toggle.json")
        dataIO.save_json(f,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.remove_command('help')
    bot.add_cog(Help(bot))
