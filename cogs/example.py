import discord
from discord.ext import commands
import time
import asyncio
import json
import os
import random
import ast
import sports


class currency(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        

    def save_file(self):
        with open('jahcoins.json', 'w') as f:
            json.dump(self.client.jahcoins, f, indent = 4)

    @commands.command()
    async def nbatrivia(self, ctx):
        with open('questions.txt','r') as f:
            questions = ast.literal_eval(f.read())
        random_questions = random.choice(questions)
        correct_answer = random_questions[1].lower()
        id_ = ctx.message.author.id
        channel = ctx.message.channel
        LETTERS = ["\N{REGIONAL INDICATOR SYMBOL LETTER A}","\N{REGIONAL INDICATOR SYMBOL LETTER B}",
                   "\N{REGIONAL INDICATOR SYMBOL LETTER C}","\N{REGIONAL INDICATOR SYMBOL LETTER D}"]
        embed = discord.Embed(title = "Welcome to NBA trivia", color = 0xdaa520)
        embed.add_field(name = "Question:", value = f"{random_questions[0]}", inline = True)
        msg = await channel.send(embed = embed)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == correct_answer.upper()

        while True:
            await msg.add_reaction(LETTERS[0])
            await msg.add_reaction(LETTERS[1])
            await msg.add_reaction(LETTERS[2])
            await msg.add_reaction(LETTERS[3])
            reaction, user = await self.client.wait_for('reaction_add',  check = lambda reaction, user: user.id == ctx.message.author.id)
            try:
                await msg.remove_reaction(reaction.emoji, user)
            except:
                await ctx.send("I need to be able to remove reactions for this command")
                return
            if reaction.emoji == correct_answer:
                embed_2 = discord.Embed(title = "Welcome to NBA trivia", color = 0xdaa520)
                embed_2.add_field(name = "Question:", value = f"{random_questions[0]}", inline = False)
                embed_2.add_field(name = "YOUR ANSWER WAS CORRECT :white_check_mark:", value = "\u200b", inline = False)
                return await msg.edit(content = None, embed = embed_2)
            elif reaction.emoji != correct_answer:
                embed_3 = discord.Embed(title = "Welcome to NBA trivia", color = 0xdaa520)
                embed_3.add_field(name = "Question:", value = f"{random_questions[0]}", inline = False)
                embed_3.add_field(name = "YOUR ANSWER WAS WRONG :x:", value = f"The correct answer was {correct_answer.upper()}", inline = False)
                return await msg.edit(content = None, embed = embed_3)

    @commands.command()
    async def getscore(self, ctx, sport: str, team1: str, team2: str):
        id_ = ctx.message.author.id
        if sport == 'football' or 'fb' or 'nfl':
            match_score = sports.get_match(sports.FOOTBALL, team1, team2)
            await ctx.send(f'{match_score} {ctx.message.author.mention}')
            
    
    @commands.command()
    async def casino(self, ctx):
        id_ = ctx.message.author.id
        embed = discord.Embed(title = "$$$ Welcome to the Casino $$$", color = 0xdaa520)
        embed.add_field(name = "=== Roll Dice ===", value = "!rolldice [guess] [bet]", inline = False)
        embed.add_field(name = "=== Roulette ===", value = "!roulette [red=2x, blue=2x, green = 14x]")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/593203992541003807/601306587667103755/1512730.png")
        await ctx.send(content = None, embed=embed)

    @commands.command()
    async def rolldice(self, ctx, guess: int, amount: int):
        id_ = str(ctx.message.author.id)
        channel = ctx.message.channel
        dice_number = random.randint(1,6)
        guess_range = range(1, 7)
        with open('jahcoins.json','r') as x:
            json.load(x)
        if id_ in self.client.jahcoins:
            if guess in guess_range:
                if amount <= self.client.jahcoins[id_]['coins']:
                    await ctx.send(f"You bet {amount:,}{self.client.jahcoin_emoji} on **{guess}**")
                    await asyncio.sleep(2)
                    await ctx.send("You throw the dice onto the table . . .")
                    await asyncio.sleep(2)
                    await ctx.send("The dice tumble and roll a lot on the table . . .")
                    await asyncio.sleep(2)
                    if guess == dice_number:
                        win_amount = amount * 6
                        self.client.jahcoins[id_]['coins'] += win_amount
                        self.save_file()
                        await ctx.send(f"The dice finally lands and you rolled a **{dice_number}**!\n\n" +
                                       f" Congratulations! You won {win_amount:,}{self.client.jahcoin_emoji}{ctx.message.author.mention}")
                    elif guess != dice_number:
                        self.client.jahcoins[id_]['coins'] -= amount
                        self.save_file()
                        await ctx.send(f"The dice finally lands and you rolled a **{dice_number}**!\n\n" +
                                       f"Unfortunately, you lost {amount:,}{self.client.jahcoin_emoji}{ctx.message.author.mention}")
                else:
                    await ctx.send(f"You don't have enough to bet that much! {ctx.message.author.mention}")
            elif guess not in guess_range:
                await ctx.send(f"You tried guessing a number out of the range of 1-6! Guess a number between 1-6! {ctx.message.author.mention}")
        else:
            await ctx.send(f"You are not registered! Please type !register {ctx.message.author.mention}")

    @commands.command()
    async def roulette(self, ctx, guess: str, amount: int):
        id_ = str(ctx.message.author.id)
        colors = ['red', 'black', 'blue']
        result = random.choices(colors, weights=[18, 18, 2])[0]
        if amount > self.client.jahcoins[id_]['coins']:
            await ctx.send(f"You don't have enough to bet {amount:,}{self.client.jahcoin_emoji}! {ctx.message.author.mention}")
        else:
            embed = discord.Embed(title = "Roulette Wheel", color = 0xdaa520)
            embed.set_image(url = "https://cdn.discordapp.com/attachments/593203992541003807/601947156894711829/roulette_wheel.gif")
            msg = await ctx.send(content = None, embed = embed)
            await asyncio.sleep(5)
            if guess != result:
                self.client.jahcoins[id_]['coins'] -= amount
                self.save_file()
                if result == 'blue':
                    result_emoji = ":large_blue_circle:"
                else:
                    result_emoji = ':' + result +'_circle' + ':'
                    embed_2 = discord.Embed(title = "Roulette Wheel", color = 0xdaa520)
                    embed_2.add_field(name = "="*10, value =  f"Color landed on {result_emoji}, you LOST **{amount:,}**{self.client.jahcoin_emoji} {ctx.message.author.mention}")
                    await msg.edit(content = None, embed = embed_2)
            else:
                if result == 'red' or 'black':
                    if guess == result:
                        result_emoji = ':' + result +'_circle' + ':'
                        amount_won = amount * 1
                        self.client.jahcoins[id_]['coins'] += amount_won
                        embed_2 = discord.Embed(title = "Roulette Wheel", color = 0xdaa520)
                        embed_2.add_field(name = "="*10, value =  f"Color landed on {result_emoji},  you won **{amount_won:,}**{self.client.jahcoin_emoji} {ctx.message.author.mention}")
                        await msg.edit(content = None, embed = embed_2)
                if result == 'blue':
                    if guess == result:
                        result_emoji = ":large_blue_circle:"
                        amount_won = amount * 14
                        self.client.jahcoins[id_]['coins'] += amount_won
                        embed_2 = discord.Embed(title = "Roulette Wheel", color = 0xdaa520)
                        embed_2.add_field(name = "="*10, value =  f"Color landed on {result_emoji},  you won **{amount_won:,}**{self.client.jahcoin_emoji} {ctx.message.author.mention}")
                        await msg.edit(content = None, embed = embed_2)
            self.save_file()
        
    @commands.command()
    async def divide(self, ctx, first_num: int, second_num: int):
        id_ = str(ctx.message.author.id)
        total  = first_num / second_num
        await ctx.send(f"{first_num:,} / {second_num:,} = {total:,}")
    
    
    @commands.command()
    async def register(self, ctx):
        id_ = str(ctx.message.author.id)
        channel = ctx.message.channel
        if id_ not in self.client.jahcoins:
            self.client.jahcoins[id_] = {"coins": 100, "workers": 0, "worms": 0, "weed_seeds": 0, "marijuana": 0, "crack": 0, "feather": 0}
            self.client.jahcoins[id_]['weapons'] = {"glock": 0}
            self.client.jahcoins[id_]['fish'] = {"salmon": 0, "bass": 0, "crappie": 0, "shark": 0, "bluegill": 0, "trout": 0, "pike": 0, "sturgeon": 0,
                                                 "carp": 0, "catfish": 0, "walleye": 0, "red_snapper": 0, "flounder": 0, "tuna": 0, "swordfish": 0,
                                                 "barracuda": 0, "shrimp": 0, "minnows": 0, "squid": 0, "level": 0, "xp": 0}
            self.client.jahcoins[id_]['factory'] = {"level": 0}
            self.client.jahcoins[id_]['houses'] = {"2_bedroom": -1, "4_bedroom": -1, "gordon_hayward": -1, "kawhi_leonard": -1, "notch": -1, "bill_gates": -1}
            await channel.send(f"You are now registered and have been given 100{self.client.jahcoin_emoji} {ctx.message.author.mention}")
            self.save_file()
        elif id_ in self.client.jahcoins:
            await channel.send(f"You already have an account {ctx.message.author.mention}")
    
    
    @commands.command()
    async def set(self, ctx, item: str, amount: int, other: discord.Member):
        id_ = str(ctx.message.author.id)
        other_id = str(other.id)
        if id_ == '143583362508914688':
            if item == 'jahcoins':
                self.client.jahcoins[other_id]['coins'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} Jahcoin balance has been set to {amount:,}{self.client.jahcoin_emoji}")
            elif item == 'workers':
                self.client.jahcoins[other_id]['workers'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} worker count has been set to {amount:,}")
            elif item == 'weed_seeds':
                self.client.jahcoins[other_id]['weed_seeds'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} weed seeds count has been set to {amount:,}")
            elif item == 'marijuana':
                self.client.jahcoins[other_id]['marijuana'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} marijuana count has been set to {amount:,}")
            elif item == 'worms':
                self.client.jahcoins[other_id]['worms'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} worms count has been set to {amount:,}")
            elif item == 'shark':
                self.client.jahcoins[other_id]['fish']['shark'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} shark count has been set to {amount:,}")
            elif item == 'bass':
                self.client.jahcoins[other_id]['fish']['bass'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} bass count has been set to {amount:,}")
            elif item == 'salmon':
                self.client.jahcoins[other_id]['fish']['salmon'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} salmon count has been set to {amount:,}")
            elif item == 'crappie':
                self.client.jahcoins[other_id]['fish']['crappie'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} crappie count has been set to {amount:,}")
            else:
                self.client.jahcoins[other_id]['(item)'] = amount
                self.save_file()
                await ctx.send(f"{other.mention} {item} count has been set to {amount:,}")
        else:
            await ctx.send(f"YOU ARE NOT <@143583362508914688> !!! YOU CANT USE THIS COMMAND {ctx.message.author.mention}")
            
        
    
    @commands.command()
    async def sell(self, ctx, item: str, amount: int = None):
        id_ = str(ctx.message.author.id)
        channel = ctx.message.channel
        sell_prices = {"salmon": 50, "trout": 65, "pike": 75, "sturgeon": 100, "bass": 25, "crappie": 10, "bluegill": 25,
                       "carp": 185, "catfish": 150, "walleye": 130, "shark": 2250, "red_snapper": 500, "flounder": 300, "tuna": 1200,
                       "swordfish": 1500, "barracuda": 1850, "marijuana": 100}
        if id_ in self.client.jahcoins:                  
            if item in self.client.jahcoins[id_]['fish']: #checks if item is in dictionary fish
                if item == 'salmon':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'trout':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'pike':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'sturgeon':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'bluegill':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'carp':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'catfish':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'walleye':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'red_snapper':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'flounder':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'tuna':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'swordfish':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'barracuda':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'bass':
                    if amount != None:
                        sell_amount_total = amount * sell_prices.get(item)
                if item == 'crappie':
                    if amount != None:
                         sell_amount_total = amount * sell_prices.get(item)
                if item == 'shark':
                    if amount != None:
                         sell_amount_total = amount * sell_prices.get(item)
                if self.client.jahcoins[id_]['fish'][item] == 0:
                    sell_amount_total = 0
                    
                if amount != None:
                    if amount > self.client.jahcoins[id_]['fish'][item]:
                        return await ctx.send(f"If you want to sell all of your {item} then just type ``!sell {item}`` with no amount and it will sell all {ctx.message.author.mention}")
                    else:
                        if self.client.jahcoins[id_]['fish'][item] < amount:
                            sell_amount = self.client.jahcoins[id_]['fish'][item]
                            sell_amount_total = sell_amount * sell_prices.get(item)
                else:
                    sell_amount = self.client.jahcoins[id_]['fish'][item]
                    sell_amount_total = sell_amount * sell_prices.get(item)
                    
                if sell_amount_total == 0: # if they have 0 amount of the item they are trying to sell
                    await ctx.send(f"You have 0 {item}! {ctx.message.author.mention}")
                else:
                    self.client.jahcoins[id_]['coins'] += sell_amount_total
                    if amount != None:
                        self.client.jahcoins[id_]['fish'][item] -= amount
                        await channel.send(f"You successfully sold {amount:,} **{item}** for {sell_amount_total:,}{self.client.jahcoin_emoji}. {ctx.message.author.mention}")
                    else:
                        self.client.jahcoins[id_]['fish'][item] -= sell_amount
                        await channel.send(f"You successfully sold {sell_amount:,} **{item}** for {sell_amount_total:,}{self.client.jahcoin_emoji}. {ctx.message.author.mention}")
                    self.save_file()


            else:
                if item == 'marijuana':
                    sell_amount_total = amount * sell_prices.get(item)
                
                if self.client.jahcoins[id_][item] == 0:
                    sell_amount_total = 0
                
                elif self.client.jahcoins[id_][item] < amount:
                    amount = self.client.jahcoins[id_][item]
                    sell_amount_total = amount * sell_prices.get(item)

                if sell_amount_total == 0: # if they have 0 amount of the item they are trying to sell
                    await ctx.send(f"You have 0 {item}! {ctx.message.author.mention}")
                else:
                    self.client.jahcoins[id_]['coins'] += sell_amount_total
                    if amount != None:
                        self.client.jahcoins[id_][item] -= amount
                    else:
                        self.client.jahcoins[id_][item] -= sell_amount
                    self.save_file()
                    await channel.send(f"You successfully sold {amount:,} **{item}** for {sell_amount_total:,}{self.client.jahcoin_emoji}. {ctx.message.author.mention}")


    #lets user see items they can buy
    @commands.command()
    async def shop(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(title = "Item Shop", color = 0xdaa520)
        embed.add_field(name = "=== Item : Price ===", value = "**worker** : 500\n**Weed Seeds** : 125\n**Crack** : 200\n **Factory** : 50,000\n**Feathers** : 15", inline = False)
        embed.set_thumbnail(url=("https://cdn.discordapp.com/attachments/593203992541003807/600852947181502466/shop-front-icon-md.png"))
        await ctx.send(embed=embed)
                                

    #Tells user their balance
    @commands.command(aliases = ['balance'])
    async def bal(self, ctx):
        channel = ctx.message.channel
        id_ = str(ctx.message.author.id)
        if id_ in self.client.jahcoins:
            embed = discord.Embed(title = f"{ctx.message.author}", color = 0xdaa520)
            embed.add_field(name = "Account Balance", value = f"{(self.client.jahcoins[id_]['coins']):,}{self.client.jahcoin_emoji}", inline = False)
            embed.set_thumbnail(url=(ctx.message.author.avatar_url))
            await ctx.send(embed=embed)
        elif id_ not in self.client.jahcoins:
            await ctx.send(f"You do not have an account, please make one by typing !register {ctx.message.author.mention}")
    #house prices
    @commands.command()
    async def housecatalog(self, ctx):
        id_ = str(ctx.message.author.id)
        if id_ in self.client.jahcoins:
            embed = discord.Embed(title = "House Catalog", color = 0xdaa520)
            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/593203992541003807/604182650722451456/8-86626_house-hd-clipart-house-free-clipart-house-clipart.png")
            embed.add_field(name = "=== House : Price : Max Storage ===", value = "**2_Bedroom** : 500,000 : 50,000\n**4_bedroom** : 1,000,000 : 100,000\n\
                            **gordon_hayward** : 3,350,000 : 335,000\n**kawhi_leonard** : 13,300,000 : 1,330,000\n**notch** : 70,000,000 : 7,000,000\n\
                            **bill_gates** : 154,000,000 : 15,400,000")
            await ctx.send(content = f"{ctx.message.author.mention}", embed=embed)

    #House balance
    @commands.command()
    async def housebal(self, ctx):
        id_ = str(ctx.message.author.id)
        if id_ in self.client.jahcoins:
            embed = discord.Embed(title = f"House balance on {ctx.message.author}", color = 0xdaa520)
            embed.add_field(name = "House : Balance", value = f"**2 Bedroom** : {self.client.jahcoins[id_]['houses']['2_bedroom']:,}\n\
                            **4 bedroom** : {self.client.jahcoins[id_]['houses']['4_bedroom']:,}\n\
                            **Gordon Hayward** : {self.client.jahcoins[id_]['houses']['gordon_hayward']:,}\n\
                            **Kawhi Leonard** : {self.client.jahcoins[id_]['houses']['kawhi_leonard']:,}\n\
                            **Notch** : {self.client.jahcoins[id_]['houses']['notch']:,}\n\
                            **Bill Gates** : {self.client.jahcoins[id_]['houses']['bill_gates']:,}\n")
            await ctx.send(embed=embed)
            
                            
    #store money in houses
    @commands.command()
    async def depositjahcoins(self, ctx, amount: int, house_name: str):
        with open('jahcoins.json','r') as g:
            json.load(g)
        id_ = str(ctx.message.author.id)
        max_amount = {"2_bedroom": 50000, "4_bedroom": 100000, "kawhi_leonard": 1330000, "gordon_hayward": 335000, "bill_gates": 15400000, "notch": 7000000}
        if self.client.jahcoins[id_]['houses'][house_name] == -1:
            return await ctx.send(f"You don't own this house! {ctx.message.author.mention}")
        if house_name not in self.client.jahcoins[id_]['houses']:
            return await ctx.send(f"This house doesn't exist! {ctx.message.author.mention}")
        if self.client.jahcoins[id_]['houses'][house_name] >= max_amount.get(house_name):
            return await ctx.send(f"This house is full {ctx.message.author.mention}")
        else:
            if self.client.jahcoins[id_]['coins'] < amount:
                return await ctx.send(f"You don't have enough {self.client.jahcoin_emoji} to store {amount:,}{self.client.jahcoin_emoji} {ctx.message.author.mention}")
            if amount > (max_amount.get(house_name) - self.client.jahcoins[id_]['houses'][house_name]):
                amount = (max_amount.get(house_name) - self.client.jahcoins[id_]['houses'][house_name])
            self.client.jahcoins[id_]['houses'][house_name] += amount
            self.client.jahcoins[id_]['coins'] -= amount
            self.save_file()
            await ctx.send(f"Transfer successful.\n\n You successfuly deposited {amount:,}{self.client.jahcoin_emoji} into your {house_name} house. {ctx.message.author.mention}")

    #withdraw jahcoins from houses
    @commands.command()
    async def withdrawjahcoins(self, ctx, amount: int, house_name: str):
        with open('jahcoins.json','r') as g:
            json.load(g)
        id_ = str(ctx.message.author.id)
        if self.client.jahcoins[id_]['houses'][house_name] == -1:
            return await ctx.send(f"You don't own this house! {ctx.message.author.mention}")
        elif house_name not in self.client.jahcoins[id_]['houses']:
            return await ctx.send(f"This house doesn't exist! {ctx.message.author.mention}")
        else:
            if amount > self.client.jahcoins[id_]['houses'][house_name]:
                amount = self.client.jahcoins[id_]['houses'][house_name]
            self.client.jahcoins[id_]['houses'][house_name] -= amount
            self.client.jahcoins[id_]['coins'] += amount
            self.save_file()
            await ctx.send(f"Transfer successful.\n\n You successfuly withdrew {amount:,}{self.client.jahcoin_emoji} from your {house_name} house. {ctx.message.author.mention}")
             
    #buy houses
    @commands.command()
    async def buyhouse(self, ctx, house_name: str):
        with open('jahcoins.json','r') as g:
            json.load(g)
        id_ = str(ctx.message.author.id)
        house_prices = {"2_bedroom": 500000, "4_bedroom": 1000000, "kawhi_leonard": 13300000, "gordon_hayward": 3350000, "bill_gates": 154000000, "notch": 70000000}
        if id_ in self.client.jahcoins:
            if house_name not in house_prices:
                return await ctx.send(f"This house doesn't exist.")
            else:
                if house_name == '2_bedroom': #buy 2 bedroom house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604169055129042984/Perspective_1_ID1203_Maramani.png"
                    house_total = house_prices.get(house_name)
                if house_name == '4_bedroom': #buy 4 bedroom house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604169056190332928/1_109a789e-175b-4117-898a-11d4ba6cfe28.png"
                    house_total = house_prices.get(house_name)
                if house_name == 'kawhi_leonard': #buy kawhi leonard's house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604168502512844810/20190129-kawhihouse.png"
                    house_total = house_prices.get(house_name)
                if house_name == 'gordon_hayward': #buy gordon hawyard's house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604169976336613406/90.png"
                    house_total = house_prices.get(house_name)
                if house_name == 'bill_gates': #buy bill_gates house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604170702467366983/105841065-1554818009865gettyimages-626759612.png"
                    house_total = house_prices.get(house_name)
                if house_name == 'notch': #buy notch house
                    house_url = "https://cdn.discordapp.com/attachments/593203992541003807/604171122425987132/rmadgpsgoogjvecxd5nu.png"
                    house_total = house_prices.get(house_name)

            if self.client.jahcoins[id_]['houses'][house_name] == 0:
                return await ctx.send(f"You already own this house! {ctx.message.author.mention}")
            
            if house_total > self.client.jahcoins[id_]['coins']:
                return await ctx.send(f"You cannot afford this house! {ctx.message.author.mention}")
            
            else:
                self.client.jahcoins[id_]['coins'] -= house_total
                self.client.jahcoins[id_]['houses'][house_name] = 0
                self.save_file()
                embed_crack = discord.Embed(title = "Mortgage Receipt", color = 0xdaa520)
                embed_crack.set_image(url=(house_url))
                embed_crack.add_field(name = "=== House Purchased ===", value = f"You have purchased {house_name}", inline = False)
                embed_crack.add_field(name = "=== Total Price ===", value = f"{house_name} = {house_total:,}{self.client.jahcoin_emoji}", inline = False)
                embed_crack.add_field(name = "=== Account Balance ===", value = f"You now have: {(self.client.jahcoins[id_]['coins']):,}{self.client.jahcoin_emoji}\n\n", inline = False)
                embed_crack.add_field(name = "↓↓↓↓↓ HOUSE PURCHASED ↓↓↓↓↓", value = "\u200b", inline = False)
                await ctx.send(content=None, embed=embed_crack)
                    

    #User can buy an item from shop
    @commands.command()
    async def buy(self, ctx, item_name: str, amount: int):
        with open('jahcoins.json','r') as g:
            json.load(g)
        id_ = str(ctx.message.author.id)
        channel = ctx.message.channel
        buy_prices = {"workers": 500, "weed_seeds": 125, "crack": 200, "glock": 5000, "factory": 50000, "feather": 15}
        bad_item_list = ['glock', 'factory']
        if id_ in self.client.jahcoins:
            
            if item_name not in buy_prices:
                return await ctx.send("this item does not exist")

            else:
                buy_amount = amount
                
                if item_name == 'factory':
                    item_url = "https://cdn.discordapp.com/attachments/593203992541003807/602263683694854215/Wolfsburg_VW-Werk.png"
                    item_total = 1 * buy_prices.get(item_name)
                    if self.client.jahcoins[id_]['coins'] < 50000:
                        return await ctx.send(f"You can't afford a factory!")
                    if self.client.jahcoins[id_]['factory']['level'] != 0:
                        return await ctx.send(f"You already own a factory, you can upgrade it by typing !upgrade factory {ctx.message.author.mention}")
                    
                    elif self.client.jahcoins[id_]['factory']['level'] == 0:
                        self.client.jahcoins[id_]['factory']['level'] = 1
                        self.client.jahcoins[id_]['coins'] -= item_total
                           
                #buy glock
                elif item_name == 'glock':
                    item_url = "https://cdn.discordapp.com/attachments/593203992541003807/602267047795359744/glock-g19-pistol-1155366-1.png"
                    item_total = 1 * buy_prices.get(item_name)
                    if self.client.jahcoins[id_]['coins'] < 5000:
                        return await ctx.send(f"You can't afford a glock!")
                    if self.client.jahcoins[id_]['weapons']['glock'] != 0:
                        return await ctx.send("You already own a glock!")
                                              
                    elif self.client.jahcoins[id_]['weapons']['glock'] == 0:
                        self.client.jahcoins[id_]['weapons']['glock'] = 1
                        self.client.jahcoins[id_]['coins'] -= item_total
                
                elif item_name == 'workers': # buy workers
                    total_workers = self.client.jahcoins[id_]['workers'] + buy_amount
                    if self.client.jahcoins[id_]['workers'] >= 5000:
                        self.client.jahcoins[id_]['workers'] = 5000
                        self.save_file()
                        return await ctx.send(f"You can not have more than 5,000 workers! {ctx.message.author.mention}")
                    #if total_workers >= 5000:
                    buy_amount = 5000 - self.client.jahcoins[id_]['workers']
                    item_total = buy_amount * buy_prices.get(item_name)
                    item_url = "https://cdn.discordapp.com/attachments/593203992541003807/600921866567286784/sweatshop-bangladesh-child-labor-1-889x667.png"
                            
                #buy weed seeds
                elif item_name == 'weed_seeds':
                    item_total = buy_amount * buy_prices.get(item_name)
                    item_url = "https://cdn.discordapp.com/attachments/593203992541003807/600796732262973449/cannabis-seeds.jpg"
                
                        
                elif item_name == 'crack': #Buy crack
                    item_url = "https://cdn.discordapp.com/attachments/593203992541003807/601252817562370048/crack-cocaine-10.png"
                    item_total = buy_amount * buy_prices.get(item_name)

                elif item_name == 'feather':
                    if self.client.jahcoins[id_]['fish']['level'] < 2:
                        return await ctx.send(f"You are not a high enough fishing level to buy feathers! You need to be level 2. {ctx.message.author.mention}")
                    else:
                        item_url = "https://cdn.discordapp.com/attachments/593203992541003807/604688998354518025/latest.png"
                        item_total = buy_amount * buy_prices.get(item_name)

                if self.client.jahcoins[id_]['coins'] < item_total:
                    buy_amount = self.client.jahcoins[id_]['coins']//buy_prices.get(item_name)
                    item_total = buy_amount * buy_prices.get(item_name)
                    self.save_file()


                if buy_amount <= 0:
                    await ctx.send(f"You don't have enough to buy {amount:,} {item_name}! {ctx.message.author.mention}")

                else:
                    if item_name not in bad_item_list:
                        self.client.jahcoins[id_]['coins'] -= item_total
                        self.client.jahcoins[id_][item_name] += buy_amount
                        self.save_file()
                    else:
                        self.save_file()
                    embed_crack = discord.Embed(title = "Purchase Receipt", color = 0xdaa520)
                    embed_crack.set_image(url=(item_url))
                    embed_crack.add_field(name = "=== Item Purchased ===", value = f"You have purchased {buy_amount:,} {item_name}", inline = False)
                    embed_crack.add_field(name = "=== Total Price ===", value = f"{buy_amount:,} {item_name} = {item_total:,}{self.client.jahcoin_emoji}", inline = False)
                    embed_crack.add_field(name = "=== Account Balance ===", value = f"You now have: {(self.client.jahcoins[id_]['coins']):,}{self.client.jahcoin_emoji}\n\n", inline = False)
                    embed_crack.add_field(name = "↓↓↓↓↓ ITEM PURCHASED ↓↓↓↓↓", value = "\u200b", inline = False)
                    await channel.send(content=None, embed=embed_crack)

                      
def setup(client):
    client.add_cog(currency(client))
