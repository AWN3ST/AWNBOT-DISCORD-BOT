import io
import discord
from datetime import *
import asyncio
import sys
import random
import os
from bs4 import BeautifulSoup
import requests
from discord.ext import commands, tasks
import pyowm
import tweepy
import time
import json
from discord.utils import get
import ast



token = ('NTUzMzAyMTYyOTY5NDYwNzU0.XS5ifw.3hmXqbceWHyBirMH_XCySmMYyqQ')
client = commands.Bot('!')
jahcoin_emoji = '<:jahcoin2:600180930761588747>'
client.jahcoin_emoji = '<:jahcoin2:600180930761588747>'
jahcoins = {}

try:
    with open('jahcoins.json') as f:
        client.jahcoins = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
    print("Couldn't load jahcoins.json, likely because file is empty")
    with open('jahcoins.json', 'w') as f:
        f.write("{}")


@client.event
#This tells you that the bot is loaded and working
async def on_ready():
    game = discord.Game("Praying to Jah")
    await client.change_presence(activity = game)
    print("Bot is loaded.")



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    
@client.command()
async def details(ctx, other: discord.Member):
    other_id = str(other.id)
    id_ = str(ctx.message.author.id)
    avi = str(other.avatar_url)
    if other_id in client.jahcoins:
        embed = discord.Embed(title= f"Info on {other}", color = 0xdaa520)
        embed.add_field(name = "=== Account Balance ===", value = f"{(client.jahcoins[other_id]['coins']):,}{jahcoin_emoji}", inline = True)
        embed.add_field(name = "=== workers Owned ===", value = f"{(client.jahcoins[other_id]['workers']):,} workers", inline = True)
        if 'weed_seeds' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Weed Seeds ===", value = f"{(client.jahcoins[other_id]['weed_seeds']):,} Weed seeds", inline = True)
        else:
            embed.add_field(name = "=== Weed Seeds ===", value = "0 Weed seeds", inline = True)
        if 'marijuana' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Marijuana ===", value = f"{(client.jahcoins[other_id]['marijuana']):,} Marijuana", inline = True)
        else:
            embed.add_field(name = "=== Marijuana ===", value = "0 Marijuana", inline = True)
        if 'crack' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Crack ===", value = f"{(client.jahcoins[other_id]['crack']):,} Crack", inline = True)
        else:
            embed.add_field(name = "=== Crack ===", value = f"0 Crack", inline = True)
        if 'weapons' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Weapons ===", value = f"Glocks: {(client.jahcoins[other_id]['weapons']['glock'])}", inline = True)
        if 'worms' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Bait ===", value = f"{(client.jahcoins[other_id]['worms']):,} Worms", inline = True)
        if 'fish' in client.jahcoins[other_id]:
            embed.add_field(name = "=== Fish ===", value = f"**Salmon**: {(client.jahcoins[other_id]['fish']['salmon']):,} | \
                                                            **Bass**: {(client.jahcoins[other_id]['fish']['bass']):,}\
                                                            \n**Crappie**: {(client.jahcoins[other_id]['fish']['crappie']):,} | \
                                                            **Shark**: {(client.jahcoins[other_id]['fish']['shark']):,}", inline = True)
        else: 
            embed.add_field(name = "=== Weapons ===", value = "None", inline = True)

        embed.set_footer(text = "="*15 + f" User ID: {other_id} " + "="*15)
        embed.set_thumbnail(url=(avi))
        await ctx.send(embed=embed)
    elif other_id not in client.jahcoins:
        await ctx.send(f"{other.mention} does not have an account! Tell them to type !register")

@client.command()
async def myfish(ctx):
    id_ = str(ctx.message.author.id)
    avi = str(ctx.message.author.avatar_url)
    if id_ in client.jahcoins:
        embed = discord.Embed(title = "Fish Inventory", color = 0xdaa520)
        embed.add_field(name = "=== Freshwater Fish ===", value = f"**Salmon**: {(client.jahcoins[id_]['fish']['salmon']):,} | \
                                                            **Bass**: {(client.jahcoins[id_]['fish']['bass']):,}\
                                                            \n**Crappie**: {(client.jahcoins[id_]['fish']['crappie']):,} | \
                                                            **Bluegill**: {(client.jahcoins[id_]['fish']['bluegill']):,} \
                                                            \n**Trout**: {(client.jahcoins[id_]['fish']['trout']):,} | \
                                                            **Pike**: {(client.jahcoins[id_]['fish']['pike']):,} \
                                                            \n**Sturgeon**: {(client.jahcoins[id_]['fish']['sturgeon']):,} | \
                                                            **Carp**: {(client.jahcoins[id_]['fish']['carp']):,} \
                                                            \n**Catfish**: {(client.jahcoins[id_]['fish']['catfish']):,} | \
                                                            **Walleye**: {(client.jahcoins[id_]['fish']['walleye']):,}", inline = True)
        embed.add_field(name = "=== Saltwater Fish ===", value = f"**Red Snapper**: {(client.jahcoins[id_]['fish']['red_snapper']):,} | \
                                                                **Flounder**: {(client.jahcoins[id_]['fish']['flounder']):,}  \
                                                                \n**Tuna**: {(client.jahcoins[id_]['fish']['tuna']):,} | \
                                                                **Swordfish**: {(client.jahcoins[id_]['fish']['swordfish']):,} \
                                                                \n**Barracuda**: {(client.jahcoins[id_]['fish']['barracuda']):,} | \
                                                                **Shark**: {(client.jahcoins[id_]['fish']['shark']):,}", inline = True)
        embed.add_field(name = "=== Bait ===", value = f"**Worms**: {(client.jahcoins[id_]['worms']):,} | **Feathers**: {(client.jahcoins[id_]['feather']):,} \
                                                            \n**Shrimp**: {(client.jahcoins[id_]['fish']['shrimp']):,} | \
                                                            **Minnows**: {(client.jahcoins[id_]['fish']['minnows']):,} \
                                                            \n**Squid**: {(client.jahcoins[id_]['fish']['squid']):,}", inline = True)
        embed.set_footer(text = "="*15 + f" User ID: {id_}" + "="*15)
        embed.set_thumbnail(url=(avi))
        await ctx.send(embed=embed)
    elif id_ not in client.jahcoins:
        await ctx.send(f"You do not have an account! Please type !register {ctx.message.author.mention}")


@client.command()
async def myinfo(ctx):
    id_ = str(ctx.message.author.id)
    avi = str(ctx.message.author.avatar_url)
    if id_ in client.jahcoins:
        embed = discord.Embed(title= f"Info on {ctx.message.author}", color = 0xdaa520)
        embed.add_field(name = "=== Account Balance ===", value = f"{(client.jahcoins[id_]['coins']):,}{jahcoin_emoji}", inline = True)
        embed.add_field(name = "=== workers Owned ===", value = f"{(client.jahcoins[id_]['workers']):,} workers", inline = True)
        if 'weed_seeds' in client.jahcoins[id_]:
            embed.add_field(name = "=== Weed Seeds ===", value = f"{(client.jahcoins[id_]['weed_seeds']):,} Weed seeds", inline = True)
        else:
            embed.add_field(name = "=== Weed Seeds ===", value = "0 Weed seeds", inline = True)
        if 'marijuana' in client.jahcoins[id_]:
            embed.add_field(name = "=== Marijuana ===", value = f"{(client.jahcoins[id_]['marijuana']):,} Marijuana", inline = True)
        else:
            embed.add_field(name = "=== Marijuana ===", value = "0 Marijuana", inline = True)
        if 'crack' in client.jahcoins[id_]:
            embed.add_field(name = "=== Crack ===", value = f"{(client.jahcoins[id_]['crack']):,} Crack", inline = True)
        else:
            embed.add_field(name = "=== Crack ===", value = f"0 Crack", inline = True)
        if 'weapons' in client.jahcoins[id_]:
            embed.add_field(name = "=== Weapons ===", value = f"Glocks: {(client.jahcoins[id_]['weapons']['glock'])}", inline = True)
        else: 
            embed.add_field(name = "=== Weapons ===", value = "None", inline = True)

        embed.set_footer(text = "="*15 + f" User ID: {id_} " + "="*15)
        embed.set_thumbnail(url=(avi))
        await ctx.send(embed=embed)
    elif id_ not in client.jahcoins:
        await ctx.send(f"You do not have an account! Please type !register {ctx.message.author.mention}")

@client.command()
async def gamble(ctx, gamble_amount: int):
    id_ = str(ctx.message.author.id)
    if id_ in client.jahcoins:
        random_number = random.randint(0,100)
        if gamble_amount > client.jahcoins[id_]["coins"]:
            await ctx.send(f"You don't have enough! You have {(client.jahcoins[id_]['coins']):,}{jahcoin_emoji} when you tried betting {gamble_amount:,}{jahcoin_emoji} {ctx.message.author.mention}")
        elif gamble_amount <= client.jahcoins[id_]["coins"]:
            if random_number < 50:
                client.jahcoins[id_]["coins"] += gamble_amount
                _save()
                await ctx.send(f'You won! Congratulations, you now have {(client.jahcoins[id_]["coins"]):,}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number > 50:
                client.jahcoins[id_]["coins"] -= gamble_amount
                _save()

                await ctx.send(f'Unfortunately you lost, you now have {(client.jahcoins[id_]["coins"]):,}{jahcoin_emoji} {ctx.message.author.mention}')


@commands.cooldown(1, 60*60*24, commands.BucketType.user)
@client.command()
async def dailyspin(ctx):
    from collections import namedtuple
    results_template = namedtuple("result", ["percent", "amount", "message"])
    id_ = str(ctx.message.author.id)
    if id_ in client.jahcoins:
        random_number = random.uniform(0.0, 290.0)
        await ctx.send('You spin the wheel really fast. . .')
        await asyncio.sleep(0.75)
        await ctx.send('The wheel continues to spin fast. . .')
        await asyncio.sleep(0.75)
        await ctx.send('The wheel begins to slow down. . .')
        await asyncio.sleep(0.75)
        await ctx.send('The wheel is just about to stop. . .')
        await asyncio.sleep(0.75)
        if random_number <= 14.5: # 14% chance
            result = results_template(5, 50000, "INCREDILBE LUCK!")
        elif random_number <= 90.0: # 10% chance
            result = results_template(10, 35000, "INSANE!")
        elif random_number <= 58.0: # 20% chance
            result = results_template(20, 15000, "Good job!")
        elif random_number <= 87.0: # 30% chance
            result = results_template(30, 10000, "Not too shabby!")
        elif random_number <= 145.0: # 50% chance
            result = results_template(50, 5000, "could have been better...")
        elif random_number <= 203.0: # 75% chance
            result = results_template(75, 25000, "Not the worst...")
        elif random_number <= 290.0: # 100% chance
            result = results_template(100, 1000, "the worst, better luck tomorrow!")
        elif random_number <= 2.9: # 1% chance
            result = result_template(1, 1000000, "THE ASBOLUTE BEST LUCK!")
        client.jahcoins[id_]["coins"] += (result.amount)
        await ctx.send(f"The wheel finally stops and with a {result.percent}% chance, you won {result.amount:,}{jahcoin_emoji} for your daily spin,\n {result.message}!\n\nYour new balance is:" +
                    f" {(client.jahcoins[id_]['coins']):,}{jahcoin_emoji}{ctx.message.author.mention}")
        _save()
        
    if id_ not in client.jahcoins:
            await ctx.send(f"You don't have an account! Please type !register to make an account {ctx.message.author.mention}")
            return


@dailyspin.error
async def dailyspin_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You already had your daily, your next spin will be in {round(error.retry_after / 60)} minutes")

@client.command()
async def leaderboard(ctx):
    with open('jahcoins.json', 'r') as g:
        users = json.load(g)
        high_score_list = sorted(users, key=lambda x : users[x].get('coins', 0), reverse = True)
        message = ''
        for number, user in enumerate(high_score_list):
            message += f'{number+1}. {"<" + "@" + user + ">"} = {users[user].get("coins",0):,} {jahcoin_emoji}\n'
    embed = discord.Embed(title = f"{jahcoin_emoji} Leaderboard", color = 0xdaa520)
    embed.add_field(name = "=== User : Balance ===", value = (message))
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/593203992541003807/601119498992615444/leaderboard.png")
    await ctx.send(embed=embed)
    

@commands.cooldown(1, 25, commands.BucketType.user)    
@client.command()
async def plantseeds(ctx, plant_amount: int):
    id_ = str(ctx.message.author.id)
    cop_chance = random.uniform(0.0,100.0)
    if plant_amount > 2000:
        plant_amount = 2000
    if plant_amount > client.jahcoins[id_]['weed_seeds']:
        plant_amount = client.jahcoins[id_]['weed_seeds']
    random_plant_amount = random.randint(1,5) * plant_amount
    cop_fine = 100 * random_plant_amount
    if id_ in client.jahcoins:
        t_end = time.time() + 20
        if client.jahcoins[id_]['weed_seeds'] == 0:
            return await ctx.send(f"You don't have enough weed seeds to plant that many! You have: 0 seeds. {ctx.message.author.mention}")
        while time.time() < t_end:
            if 'marijuana' in client.jahcoins[id_]:
                if cop_chance > 25:
                    await ctx.send(f"You plant {plant_amount:,} marijuana seeds into the ground. {ctx.message.author.mention}")
                    await asyncio.sleep(10)
                    await ctx.send(f"Your {plant_amount:,} marijuana seeds are done growing. You begin your harvest. {ctx.message.author.mention}")
                    await asyncio.sleep(10)
                    client.jahcoins[id_]['weed_seeds'] -= plant_amount
                    client.jahcoins[id_]['marijuana'] += random_plant_amount
                    _save()
                    await ctx.send(f"You are done harvesting your {plant_amount:,} marijuana plants. You now have: {(client.jahcoins[id_]['marijuana']):,} marijuana. {ctx.message.author.mention}")
                elif cop_chance < 25:
                    await ctx.send(f"You plant {plant_amount:,} marijuana seeds into the ground. {ctx.message.author.mention}")
                    await asyncio.sleep(10)
                    await ctx.send(f"Your {plant_amount:,} marijuana seeds are done growing. You begin your harvest. {ctx.message.author.mention}")
                    await asyncio.sleep(10)
                    client.jahcoins[id_]['weed_seeds'] -= plant_amount
                    client.jahcoins[id_]['coins'] -= cop_fine
                    _save()
                    await ctx.send(f"The cops catch you and confiscate {random_plant_amount:,} **marijuana** and they fine you **{cop_fine:,}**{jahcoin_emoji}! {ctx.message.author.mention}")
                if client.jahcoins[id_]['marijuana'] < 0:
                    client.jahcoins[id_]['marijuana'] = 0
                    _save()
                    break
                        

@plantseeds.error
async def dailyspin_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You already have weed plants growing, you can grow more in {round(error.retry_after)} seconds. {ctx.message.author.mention}")
                
                
@client.command()
async def workers(ctx):
    id_ = str(ctx.message.author.id)
    if id_ in client.jahcoins:
        await ctx.send(f"You have {(client.jahcoins[id_]['workers']):,} workers. {ctx.message.author.mention}")


@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def workworkers(ctx, drug = None, amount: int = None):
    id_ = str(ctx.message.author.id)
    random_number = random.uniform(0,100)
    random_slave_deaths = random.randint(1, client.jahcoins[id_]['workers'])
    print('Workers are working')
    if client.jahcoins[id_]['factory']['level'] == 0:
        return await ctx.send(f"You must own a factory to work your workers! Buy one from the shop {ctx.message.author.mention}")

    else:
        first_num = client.jahcoins[id_]['factory']['level'] * 5
        second_num = client.jahcoins[id_]['factory']['level'] * 10
        random_coin = random.randint(first_num, second_num) * client.jahcoins[id_]['workers'] 
        t_end = time.time() + 30
        crack_time = time.time() + 5
        if drug == None:
            while time.time() < t_end:
                await ctx.send(f"You put your {(client.jahcoins[id_]['workers']):,} worker(s) to work for 30 seconds {ctx.message.author.mention}",file = discord.File(r"C:\Users\Matt\Desktop\AwnBot Discord\workers.gif"))
                await asyncio.sleep(30)
                client.jahcoins[id_]['coins'] += random_coin
                _save()
                await ctx.send(f"Your {(client.jahcoins[id_]['workers']):,} worker(s) is back from the factory and has earned you {random_coin:,}{jahcoin_emoji}! {ctx.message.author.mention}")
                if random_number < 6:
                    client.jahcoins[id_]['workers'] -= random_slave_deaths
                    _save()
                    await ctx.send(f"Although your workers worked hard and made you some {jahcoin_emoji}, {random_slave_deaths:,} died in the process. {ctx.message.author.mention}")
                    break
        elif drug == 'with_crack' and amount != None:
                crack_num1 = client.jahcoins[id_]['factory']['level'] * 25
                crack_num2 = client.jahcoins[id_]['factory']['level'] * 50
                crack_coin = random.randint(crack_num1, crack_num2) * amount 
                while time.time() < crack_time:
                    random_crack_death = random.randint(1,amount)
                    if amount <= client.jahcoins[id_]['crack']:
                        if amount <= client.jahcoins[id_]['workers']:
                            random_crack_death = random.randint(1,amount)
                            await ctx.send(f"You put {amount} worker(s) to work for 5 seconds AND THEY ARE CRACKED OUT OF THEIR MIND", file = discord.File(r"C:\Users\Matt\Desktop\AwnBot Discord\slavejumps.gif"))
                            await asyncio.sleep(5)
                            client.jahcoins[id_]['crack'] -= amount
                            client.jahcoins[id_]['coins'] += crack_coin
                            await ctx.send(f"Your {amount} cracked out worker(s) are back from the factory and they have earned you {crack_coin:,}{jahcoin_emoji}! {ctx.message.author.mention}")
                            _save()
                            if random_number < 15:
                                client.jahcoins[id_]['workers'] -= random_crack_death
                                _save()
                                await ctx.send(f"Although your cracked out workers worked hard and made you {crack_coin:,}{jahcoin_emoji}, {random_crack_death:,} died in the process. {ctx.message.author.mention}")
                        else:
                            await ctx.send("You don't have that many workers to give crack to!")
                            break
                    else:
                        await ctx.send("You don't have enough crack to give!")
                        break
                    

@workworkers.error
async def workworkers_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You must wait {round(error.retry_after)} seconds before putting your workers to work again! {ctx.message.author.mention}")

    
@commands.cooldown(1, 600, commands.BucketType.user)            
@client.command()
async def stealjahcoins(ctx, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    random_number = random.randint(1,2)
    
    if client.jahcoins[other_id]['coins'] <= 0:
        await ctx.send(f"{other.mention} Does not have enough {jahcoin_emoji} to steal! They must have at least 1 {jahcoin_emoji}")
                                                                 
    else:
        jahcoin_amount = random.randint(0, client.jahcoins[other_id]['coins'])
        if random_number == 1:
            client.jahcoins[primary_id]['coins'] += jahcoin_amount
            client.jahcoins[other_id]['coins'] -= jahcoin_amount
            _save()
            await ctx.send(f"You successfully stole {jahcoin_amount:,}{jahcoin_emoji} from {other.mention}!\nYou now have a balance of: {(client.jahcoins[primary_id]['coins']):,}{ctx.message.author.mention}")
        else:
            client.jahcoins[primary_id]['coins'] -= jahcoin_amount
            client.jahcoins[other_id]['coins'] += jahcoin_amount
            _save()
            await ctx.send(f"You were unsucessful at stealing a potential {jahcoin_amount:,}{jahcoin_emoji} from {other.mention}. Instead, they took from you what you were going to steal.\nYour new balance is: {(client.jahcoins[primary_id]['coins']):,}{ctx.message.author.mention}")


@stealjahcoins.error
async def stealjahcoins_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown for another {round(error.retry_after)} seconds because it was used recently! {ctx.message.author.mention}")


@commands.cooldown(1, 600, commands.BucketType.guild)         
@client.command()
async def stealworkers(ctx, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    random_number = random.randint(1,2)
    
    if client.jahcoins[other_id]['workers'] <= 0:
        await ctx.send(f"{other.mention} Does not have enough workers to steal! They must have at least 1 slave")
                                                                 
    else:
        slave_amount = random.randint(1, client.jahcoins[other_id]['workers'])
        if random_number == 1:
            client.jahcoins[primary_id]['workers'] += slave_amount
            client.jahcoins[other_id]['workers'] -= slave_amount
            _save()
            await ctx.send(f"You successfully stole {slave_amount:,} slave(s) from {other.mention}!\nYou now have: {(client.jahcoins[primary_id]['workers']):,}{ctx.message.author.mention}")
        else:
            if client.jahcoins[primary_id]['workers'] - slave_amount < 0:
                client.jahcoins.update[primary_id] = {"workers": 0}
                client.jahcoins[other_id]['workers'] += slave_amount
                _save()
                await ctx.send(f"You were unsucessful at stealing a potential {slave_amount:,} slave(s) from {other.mention}. Instead, they took from you what you were going to steal.\nYou now have: {(client.jahcoins[primary_id]['workers']):,} workers {ctx.message.author.mention}")
            elif client.jahcoins[primary_id]['workers'] >= slave_amount:
                client.jahcoins[primary_id]['workers'] -= slave_amount
                client.jahcoins[other_id]['workers'] += slave_amount
                _save()
                await ctx.send(f"You were unsucessful at stealing a potential {slave_amount:,} slave(s) from {other.mention}. Instead, they took from you what you were going to steal.\nYou now have: {(client.jahcoins[primary_id]['workers']):,} workers {ctx.message.author.mention}")            

        
@stealworkers.error        
async def stealworkers_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown for another {round(error.retry_after)} seconds because it was used recently! {ctx.message.author.mention}")    


@client.command()
async def give(ctx, other: discord.Member, jahcoin: int):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in client.jahcoins:
        await ctx.send(f"You do not have an account, create one by typing !register {ctx.message.author.mention}")
    elif other_id not in client.jahcoins:
        await ctx.send(f"The other party {other.mention} does not have an account, he/or she needs to type !register {ctx.message.author.mention}")
    elif client.jahcoins[primary_id]['coins'] < jahcoin:
        await ctx.send(f"You cannot afford to give {other.mention} {jahcoin:,}{jahcoin_emoji} because you only have {(client.jahcoins[primary_id]['coins']):,}{jahcoin_emoji} {ctx.message.author.mention}")
    else:
        client.jahcoins[primary_id]['coins'] -= jahcoin
        client.jahcoins[other_id]['coins'] += jahcoin
        await ctx.send(f"Transaction complete.\n\n{other.mention} new balance is: {(client.jahcoins[other_id]['coins']):,}{jahcoin_emoji}\n\n{ctx.message.author.mention} new balance is: " +
                                  f"{(client.jahcoins[primary_id]['coins']):,}{jahcoin_emoji}")
    _save()


@client.command()
async def giveitem(ctx, other: discord.Member, item_name: str, amount: int):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in client.jahcoins:
        await ctx.send(f"You do not have an account, create one by typing !register {ctx.message.author.mention}")
    elif other_id not in client.jahcoins:
        await ctx.send(f"The other party {other.mention} does not have an account, he/or she needs to type !register {ctx.message.author.mention}")
    else:
        if item_name == 'weed_seeds':
            if client.jahcoins[primary_id]['weed_seeds'] < amount:
                await ctx.send(f"You don't have {amount:,} weed seeds to give to {other.mention} because you only have {(client.jahcoins[primary_id]['weed_seeds']):,} weed seeds! {ctx.message.author.mention}")
            else:
                client.jahcoins[primary_id]['weed_seeds'] -= amount
                client.jahcoins[other_id]['weed_seeds'] += amount
                _save()
                await ctx.send(f"Transaction complete.\n\n{other.mention} now has: {(client.jahcoins[other_id]['weed_seeds']):,} weed seeds.\n\n{ctx.message.author.mention} now has: " +
                                  f"{(client.jahcoins[primary_id]['weed_seeds']):,} weed seeds!")
        if item_name == 'workers':
            if client.jahcoins[primary_id]['workers'] < amount:
                await ctx.send(f"You don't have {amount:,} workers to give to {other.mention} because you only have {(client.jahcoins[primary_id]['workers']):,} workers! {ctx.message.author.mention}")
            else:
                client.jahcoins[primary_id]['workers'] -= amount
                client.jahcoins[other_id]['workers'] += amount
                _save()
                await ctx.send(f"Transaction complete.\n\n{other.mention} now has: {(client.jahcoins[other_id]['workers']):,} workers.\n\n{ctx.message.author.mention} now has: " +
                                  f"{(client.jahcoins[primary_id]['workers']):,} workers!")
        if item_name == 'glock':
            if 'glock' not in client.jahcoins[primary_id]['weapons']:
                await ctx.send(f"You don't have a glock to give to {other.mention}! {ctx.message.author.mention}")
            elif 'glock' in client.jahcoins[primary_id]['weapons']:
                client.jahcoins[primary_id]['weapons']['glock'] = 0
                if 'weapons' not in client.jahcoins[other_id]:
                    client.jahcoins[other_id]['weapons']
                    _save()
                else:
                    if 'glock' not in client.jahcoins[other_id]['weapons']:
                        client.jahcoins[other_id]['weapons'] = {"glock": 1}
                        _save()
                    elif 'glock' in client.jahcoins[other_id]['weapons']:
                        client.jahcoins[other_id]['weapons']['glock'] = 1
                        _save()
                await ctx.send(f"Transaction complete.\n\n{other.mention} now has a glock.\n\n{ctx.message.author.mention} now has no glock")
                

@give.error
async def give_error(ctx, error):
    id_ = str(ctx.message.author.id)
    if isinstance(error, commands.BadArgument):
        await ctx.send("**\nBAD INPUT**\n\nRemember !give @USER_NAME (amount)")


@client.command()
async def jahcoin(ctx):
    embed = discord.Embed(title = "How to use Jahcoin Currency", color = 0xdaa520)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/593203992541003807/600183870520033281/exclamation.png")
    embed.add_field(name = "=== Registering ===", value = "First thing first is to register an account by typing **!register**.\nThis will register you into the database and start you out with 100 Jahcoin(s).", inline = True)
    embed.add_field(name = "=== Gambling ===", value = " You can gamble your jahcoin by typing **!gamble (amount to gamble)**. If you win, the amount you gambled will be added to your balance, if you lose the amount, you gambled will be taken away.", inline = True)
    embed.add_field(name = "=== Daily Spin ===", value = "You can have a daily spin by typing **!dailyspin**.", inline = True)
    embed.add_field(name = "=== Checking your Balance ===", value = "To check your balance simply type **!bal**.", inline = True)
    embed.add_field(name = "=== Giving ===", value = "Feeling generous? Give some of your {jahcoin_emoji} to another user by\ntyping **!give @user (amount)**.", inline = True)
    embed.add_field(name = "=== Balance ===", value = "Checking your balance is simple, type either **!bal** or **!balance**.", inline = True)
    
    await ctx.send(content=None, embed=embed)


def _save():
    with open('jahcoins.json', 'w') as f:
        json.dump(client.jahcoins, f, indent = 4)


@client.command()
async def cmds(ctx):
        id_ = str(ctx.message.author.id)
        embed = discord.Embed(title = "AwnBot Commands - Pg. 1/2", color = 0x008000)
        embed.add_field(name = "!gm", value = "Says good morning & tells word of the day + Bible verse of the day + today's date\n" + "-"*95, inline = False)
        embed.add_field(name = "!8ball", value = "Let's you play 8-ball\n" + "-"*95, inline = False)
        embed.add_field(name = "!coinflip", value = "Flips a coin for heads or tails\n" + "-"*95, inline = False)
        embed.add_field(name = "!say", value = "Repeats whatever your \nmessage is in Text-to-speech\n" + "-"*95, inline = False)
        msg = await ctx.send(content=None, embed=embed)
        right = "\N{BLACK RIGHT-POINTING TRIANGLE}"
        left = "\N{BLACK LEFT-POINTING TRIANGLE}"

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '\N{BLACK RIGHT-POINTING TRIANGLE}'
   
        while True:
            await msg.add_reaction(left)
            await msg.add_reaction(right)
            reaction, user = await client.wait_for('reaction_add',  check = lambda reaction, user: user.id == ctx.message.author.id)
            try:
                await msg.remove_reaction(reaction.emoji, user)
            except:
                await ctx.send("I need to be able to remove reactions for this command")
                return
            if reaction.emoji == right:
                embed_2 = discord.Embed(title = "AwnBot Commands - Pg. 2/2", color = 0x008000)
                embed_2.add_field(name = "!weather", value = "Shows current temperature of a city by the following format: !weather (CITY NAME, COUNTRY CODE) with no parantheses.\n" + "-"*95, inline = False)
                embed_2.add_field(name = "!chance", value = "Gives you a random percentage between 0-100% of something happening.\n Example: !chance The Pats win the super bowl this year?\n" + "-"*95, inline = False)
                embed_2.add_field(name = "!kawhi", value = "WHAT IT DO BABY, check for yourself what it does ;)" + "-"*95 , inline = False)
                embed_2.add_field(name = "!randomvid", value = "Sends a random video, usually a funny meme", inline = False)
                embed_2.add_field(name = "!jahcoin", value = "Tells you the list of commands for our discord currency, Jahcoin.", inline = False) 
                await msg.edit(content = None, embed = embed_2)
            elif reaction.emoji == left:
                await msg.edit(content = None, embed = embed)
                                                 
                                                
@client.command()
async def pfp(ctx, other: discord.Member):
    other_id = str(other.id)
    id_ = str(ctx.message.author.id)
    avi = str(other.avatar_url)
    channel = ctx.message.channel
    embed = discord.Embed(title=" ", description = f"{ctx.message.author.mention}", color = 0xecce8b)
    embed.set_image(url=(avi))
    await ctx.send(embed=embed)


@client.command(aliases = ["8ball"])
async def _8ball(ctx):
        responses = ['It is certain.','It is decidedly so.','Without a doubt','Yes - definitely',
                        'You may rely on it.','As I see it, yes.','Most likely.','Outlook good.','Yes.',
                        'Signs point to yes.','Reply hazy, try again','Ask again later','Better not tell you now',
                        'Cannot predict now.','Concentrate and ask again','Do not count on it','My reply is no.',
                        'My sources say no.','Outlook not so good.','Very doubtful.']
        
        await ctx.send(random.choice(responses) + f" {ctx.message.author.mention}")


@client.command()
async def coinflip(ctx):
        await ctx.send('Coin is tossed in the air . . .')
        time.sleep(1.5)
        await ctx.send('Coin flips numerous times before landing . . .')
        time.sleep(1.5)
        await ctx.send('The coin finally lands. . . and it is ' + random.choice(['Heads','Tails']) + f" {ctx.message.author.mention}")


@client.command()
async def say(ctx):
        args = ctx.message.content.split(" ")
        while True:
            await ctx.send("%s" % (" ".join(args[1:])), tts=True)


@client.command()
async def gm(ctx):
        date = datetime.today().strftime('%Y-%m-%d')
        bibledate = datetime.today().strftime('%Y/%m/%d')
        await ctx.send(f"Good morning! {ctx.message.author.mention}\n" + "\nToday's date is " + date + " \n\n**Below is the word of the day**\n" + "https://www.merriam-webster.com/word-of-the-day\n")
        await ctx.send("\n**Bible verse of the day is below**" + "\nhttps://www.dailyverses.net/" + bibledate)


@client.command()
async def weather(ctx):
        degree_sign = u'\N{DEGREE SIGN}'
        owm = pyowm.OWM('e8ad7c8e66dd46d2fdb5492d0789abaf')
        location = ctx.message.content[9:]
        zipcode = ctx.message.content[9:]
        observation = owm.weather_at_place(location or zipcode)
        weather = observation.get_weather()
        temperature = weather.get_temperature('fahrenheit')['temp']
        wind = weather.get_wind('miles_hour')['speed']
        windspeed = (round(wind, 2))
        humidity = weather.get_humidity()
        status = weather.get_detailed_status()

        embed = discord.Embed(title = f'Weather for {location}', color = 0x00ffff)
        embed.add_field(name = "-"*99, value = f':thermometer: The temperature in {location} is {temperature}{degree_sign}F', inline = False)
        embed.add_field(name = "-"*99, value = f':dash: {location} has a wind speed of {windspeed} mph.', inline = False)
        embed.add_field(name = "-"*99, value = f':sweat_drops: {location} humidity is {humidity}% with {status}', inline = False)

        await ctx.send(content=None, embed=embed)


@client.command()
async def chance(ctx):
        percentage = (random.uniform(0.00, 100.00))
        percent = (round(percentage, 2))
        
        await ctx.send(f'There is a {percent}% chance of it happening. {ctx.message.author.mention}')

        
@client.command()
async def kawhi(ctx):
    await ctx.send("WHAT IT DO BABY", file = discord.File(r"C:\Users\Matt\Desktop\AwnBot Discord\kawhi.mp4"))


@client.command()
async def randomvid(ctx):
    path ='C:/Users/Matt/Desktop/AwnBot Discord/meme vids'
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    vidName = (files[index])

    await ctx.send(file = discord.File(r'C:/Users/Matt/Desktop/AwnBot Discord/meme vids/' + vidName))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename} loaded')

                                               
client.run(token)


