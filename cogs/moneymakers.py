import discord
from discord.ext import commands
import time
import asyncio
import json
import os
import random
import itertools
import bisect



class skills(commands.Cog):

    def __init__(self, client):
        self.client = client


    def save_file(self):
        with open('jahcoins.json', 'w') as z:
            json.dump(self.client.jahcoins, z, indent = 4)

    @commands.command()
    async def upgradeprices(self, ctx):
        upgrade_prices = {"factory": 50000}
        embed = discord.Embed(title = "Upgrade Prices", color = 0xdaa520)
        embed.add_field(name = "=== PLEASE READ ===", value = "These prices are level 1 upgrades! Every upgrade after is the " +
                        "price of your current level * 2", inline = True)
        embed.add_field(name = "=== Upgrade : Upgrade Price ===", value = "**Factory** : 50,000", inline = True)
        embed.set_thumbnail(url=("https://northeastsecuritysolutions.com/wp-content/uploads/2018/12/update-1672350_960_720.png"))
        await ctx.send(embed=embed)

    @commands.command()
    async def upgrade(self, ctx, item_upgrade: str):
        id_ = str(ctx.message.author.id)
        factory_upgrades = {"factory": 85000}
        
        if item_upgrade in self.client.jahcoins[id_]:
            upgrade_price = 2**self.client.jahcoins[id_]['factory']['level'] * factory_upgrades.get(item_upgrade)
            if self.client.jahcoins[id_]['coins'] >= upgrade_price:
                self.client.jahcoins[id_]['factory']['level'] += 1
                self.client.jahcoins[id_]['coins'] -= upgrade_price
                self.save_file()
                await ctx.send(f"**UPGRADE SUCCESSFUL** You have upgraded your {item_upgrade} to " +
                               f"{(self.client.jahcoins[id_]['factory']['level'])} " +
                               f"for {upgrade_price:,}{self.client.jahcoin_emoji} {ctx.message.author.mention}")
            else:
                await ctx.send(f"You don't have enough {self.client.jahcoin_emoji} to afford this upgrade! " +
                               f"You need {upgrade_price:,}{self.client.jahcoin_emoji} and you have: " +
                               f"{(self.client.jahcoins[id_]['coins']):,}{self.client.jahcoin_emoji}" +
                               f"Your factory level is {self.client.jahcoins[id_]['factory']['level']} {ctx.message.author.mention}")

    @commands.command()
    async def mystats(self, ctx):
        id_ = str(ctx.message.author.id)
        if id_ in self.client.jahcoins:
            embed = discord.Embed(title = "=== Your Stats ===", color = 0xdaa520)
            embed.add_field(name = "=== Skill : Level : XP ===", value = f"**Fishing** : {self.client.jahcoins[id_]['fish']['level']} : {self.client.jahcoins[id_]['fish']['xp']:,}")
            embed.set_thumbnail(url=("https://cdn.discordapp.com/attachments/593203992541003807/602700218063912960/51GTualc6gL.png"))
            await ctx.send(embed=embed)
            

    @commands.command()
    async def digforworms(self, ctx, amount: int):
        id_ = str(ctx.message.author.id)
        worm_amount = list(range(1,3))
        with open('jahcoins.json','r') as x:
            json.load(x)
        if 'worms' not in self.client.jahcoins[id_]:
            self.client.jahcoins[id_]['worms'] = 0
            self.save_file()
        elif 'worms' in self.client.jahcoins[id_]:
            await ctx.send(f"You go digging for worms for {amount:,} seconds... {ctx.message.author.mention}")
            await asyncio.sleep(amount)
            worms_found = {'worms': 0}
            while amount > 0:
                amount -= 1
                if 'worms' not in self.client.jahcoins[id_]:
                    worm_timer = random.choices(worm_amount, k=1)[0]
                    worms_caught = int(worm_timer)
                    self.client.jahcoins[id_]['worms'] += worms_caught
                    worms_found['worms'] += worms_caught
                    self.save_file()
                elif 'worms' in self.client.jahcoins[id_]:
                    worm_timer = random.choices(worm_amount, k=1)[0]
                    worms_caught = int(worm_timer)
                    self.client.jahcoins[id_]['worms'] += worms_caught
                    worms_found['worms'] += worms_caught
                    self.client.jahcoins[id_]['cooldown'] = amount
                    self.save_file()
                    
            await ctx.send(f"It was hard but honest work, your hands are dirty,\n" +
                            f"and you manage to dig up **{(worms_found['worms']):,}** worms {ctx.message.author.mention}")

    @commands.command()
    async def gonetfishing(self, ctx, amount: int):
        id_ = str(ctx.message.author.id)
        BAIT_RARITIES = ['shrimp', 'minnows', 'squid', 'None']
        if 'fish' in self.client.jahcoins[id_]:
            if self.client.jahcoins[id_]['fish']['level'] < 8:
                return await ctx.send(f"You can not go net fishing, you need to be level 8 fishing {ctx.message.author.mention}")
            else:
                await ctx.send(f"You go net fishing for {amount:,} seconds... {ctx.message.author.mention}")
                await asyncio.sleep(amount)
                caught = {'shrimp': 0, 'minnows': 0, 'squid': 0}
                while amount > 0:
                    amount -= 1
                    bait_caught = random.choices(BAIT_RARITIES, weights=[40, 30, 20, 10])[0]
                    if bait_caught != 'None':
                        caught[bait_caught] += 1
                        self.client.jahcoins[id_]['fish'][bait_caught] += 1
                    self.save_file()
                await ctx.send(f"It was hard but honest work, your muscles are aching,\n" +
                               f"and you manage to catch:\n" +
                               f"{(caught['shrimp']):,} **Shrimp**" +
                               f"{(caught['minnows']):,} **Minnows**" +
                               f"{(caught['squid']):,} **Squid** {ctx.message.author.mention}")
                                
        
class FishingGame(commands.Cog):
    def __init__(self, client):
        self.client = client


    def save_file(self):
        with open('jahcoins.json', 'w') as z:
            json.dump(self.client.jahcoins, z, indent = 4)
    
    
    @commands.command()
    async def gofishing(self, ctx, water_type: str, amount: int, bait: str):
        with open('types_of_fish.json','r') as g:
            fish_type = json.load(g)  
        with open('jahcoins.json','r') as e:
            json.load(e)
        id_ = str(ctx.message.author.id)
        FISH_RARITIES_POND = ['bass', 'crappie', 'None', 'bluegill']
        FISH_RARITIES_RIVER = ['salmon', 'trout', 'pike', 'sturgeon', 'None']
        FISH_RARITIES_LAKE = ['carp', 'bass', 'catfish', 'walleye', 'None']
        FISH_RARITIES_OCEAN = ['shark', 'red_snapper', 'flounder', 'tuna', 'swordfish', 'barracuda', 'None']
        FISH_XP = {'salmon': 8, 'bass': 5, 'crappie': 2, 'shark': 32, 'bluegill': 7, 'trout': 9, 'pike': 10, 'sturgeon': 12, 'carp': 18, 'catfish': 16, 'walleye': 14,
                   'barracuda': 28, 'swordfish': 26, 'tuna': 23, 'red_snapper': 21, 'flounder': 18}
        if 'fish' not in self.client.jahcoins[id_]:
            self.client.jahcoins[id_]['fish'] = {"crappie": 0, "bass": 0, "salmon": 0, "shark": 0, "bluegill": 0, "carp": 0, "catfish": 0, "walleye": 0,
                                                 "red_snapper": 0, "flounder": 0, "tuna": 0, "swordfish": 0, "barracuda": 0, "level": 0, "xp": 0}
            self.save_file()
        elif 'fish' in self.client.jahcoins[id_]:
            if water_type == 'pond':
                if self.client.jahcoins[id_][bait] == 0:
                    return await ctx.send(f"You can't go fishing, you have no {bait}! {ctx.message.author.mention}")
                elif self.client.jahcoins[id_][bait] < amount:
                    amount = self.client.jahcoins[id_][bait]
                if bait == 'worms':
                    await ctx.send(f"You go to the pond and take your {amount:,} {bait} with you. " +
                                        f" You'll be gone for {amount/2:,} seconds {ctx.message.author.mention}")
                    await asyncio.sleep(amount/2)
                    caught = {'bass': 0, 'crappie': 0, 'bluegill': 0}
                    total_xp = {'xp': 0} 
                    while amount > 0:
                        amount -= 1
                        fish_caught = random.choices(FISH_RARITIES_POND, weights=[20, 60, 20, 30])[0]
                        if fish_caught != 'None':
                            caught[fish_caught] += 1
                            total_xp['xp'] += FISH_XP.get(fish_caught)
                            self.client.jahcoins[id_]['fish'][fish_caught] += 1
                            self.client.jahcoins[id_]['fish']['xp'] += FISH_XP.get(fish_caught)                              
        
                        self.client.jahcoins[id_]['worms'] -= 1
                        self.save_file()

                    await ctx.send(f"You are back from fishing and have caught:\n\n" +
                                    f"{(caught['bass']):,} **Bass**\n"+
                                    f"{(caught['crappie']):,} **Crappie**\n" +
                                    f"{(caught['bluegill']):,} **Bluegill**\n" +
                                    f"You also received {total_xp['xp']:,} **XP** {ctx.message.author.mention}")

            if water_type == 'river':
                if self.client.jahcoins[id_][bait] == 0:
                    return await ctx.send(f"You can't go fishing, you have no {bait}! {ctx.message.author.mention}")
                elif self.client.jahcoins[id_][bait] < amount:
                    amount = self.client.jahcoins[id_][bait]
                river_valid_bait_types = ['worms', 'feather']
                if self.client.jahcoins[id_]['fish']['level'] < 2:
                    return await ctx.send(f"You are not a high enough fishing level to fish in a river! You need to be level 2 \
                                        {ctx.message.author.mention}")
                if bait not in river_valid_bait_types:
                    return await ctx.send(f"Invalid bait type {ctx.message.author.mention}")
                else:
                    await ctx.send(f"You go to the river and take your {amount:,} {bait} with you. " +
                                   f"You'll be gone for {amount/2:,} seconds {ctx.message.author.mention}")
                    await asyncio.sleep(amount/2)
                    caught = {'salmon': 0, 'trout': 0, 'pike': 0, 'sturgeon': 0}
                    total_xp = {'xp': 0}
                    while amount > 0:
                        if bait == 'worms': 
                            fish_caught = random.choices(FISH_RARITIES_RIVER, weights=[22, 18, 15, 8, 42])[0]
                        if bait == 'feather':
                            fish_caught = random.choices(FISH_RARITIES_RIVER, weights=[28, 24, 20, 12, 16])[0]
                        amount -= 1
                        if fish_caught != 'None':
                            caught[fish_caught] += 1
                            total_xp['xp'] += FISH_XP.get(fish_caught)
                            self.client.jahcoins[id_]['fish'][fish_caught] += 1
                            self.client.jahcoins[id_]['fish']['xp'] += FISH_XP.get(fish_caught)

                        self.client.jahcoins[id_][bait] -= 1
                        self.save_file()
                    await ctx.send(f"You are back from fishing and have caught:\n\n" +
                                f"{(caught['salmon']):,} **Salmon**\n"+
                                f"{(caught['trout']):,} **Trout**\n" +
                                f"{(caught['pike']):,} **Pike**\n" +
                                f"{(caught['sturgeon']):,} **Sturgeon**\n" +
                                f"You also received {total_xp['xp']:,} **XP** {ctx.message.author.mention}")

            if water_type == 'lake':
                lake_valid_bait_types = ['worms', 'feather']
                if self.client.jahcoins[id_][bait] == 0:
                    return await ctx.send(f"You can't go fishing, you have no {bait}! {ctx.message.author.mention}")
                elif self.client.jahcoins[id_][bait] < amount:
                    amount = self.client.jahcoins[id_][bait]
                if self.client.jahcoins[id_]['fish']['level'] < 5:
                    return await ctx.send(f"You are not a high enough fishing level to fish in a lake! You need to be level 5 {ctx.message.author.mention}")
                if bait not in lake_valid_bait_types:
                    return await ctx.send(f"Invalid bait type {ctx.message.author.mention}")
                else:
                    await ctx.send(f"You go to the lake and take your {amount:,} {bait} with you. " +
                                   f"You'll be gone for {amount/2:,} seconds {ctx.message.author.mention}")
                    await asyncio.sleep(amount/2)
                    caught = {'bass': 0, 'carp': 0, 'catfish': 0, 'walleye': 0}
                    total_xp = {'xp': 0}
                    while amount > 0:
                        if bait == 'worms':
                            fish_caught = random.choices(FISH_RARITIES_LAKE, weights=[5, 18, 8, 11, 58])[0]
                        if bait == 'feather':
                            fish_caught = random.choices(FISH_RARITIES_LAKE, weights=[12, 40, 16, 19, 13])[0]
                        amount -= 1
                        if fish_caught != 'None':
                            caught[fish_caught] += 1
                            total_xp['xp'] += FISH_XP.get(fish_caught)
                            self.client.jahcoins[id_]['fish'][fish_caught] += 1
                            self.client.jahcoins[id_]['fish']['xp'] += FISH_XP.get(fish_caught)

                        self.client.jahcoins[id_][bait] -= 1
                        self.save_file()
                    await ctx.send(f"You are back from fishing and have caught:\n\n" +
                                   f"{(caught['bass']):,} **Bass**\n" +
                                   f"{(caught['carp']):,} **Carp**\n" +
                                   f"{(caught['catfish']):,} **Catfish**\n" +
                                   f"{(caught['walleye']):,} **Walleye**\n" +
                                   f"You also received {total_xp['xp']:,} **XP** {ctx.message.author.mention}")
            if water_type == 'ocean':
                ocean_valid_bait_types = ['shrimp', 'minnows', 'squid']
                if self.client.jahcoins[id_]['fish'][bait] == 0:
                    return await ctx.send(f"You can't go fishing, you have no {bait}! {ctx.message.author.mention}")
                elif self.client.jahcoins[id_]['fish'][bait] < amount:
                    amount = self.client.jahcoins[id_]['fish'][bait]
                if self.client.jahcoins[id_]['fish']['level'] < 8:
                    return await ctx.send(f"You are not a high enough fishing level to fish in the ocean! You need to be level 8 \
                                        {ctx.message.author.mention}")
                if bait not in ocean_valid_bait_types:
                    return await ctx.send(f"Invalid bait type {ctx.message.author.mention}")
                else:
                    await ctx.send(f"You go to the ocean and take your {amount:,} {bait} with you. " +
                                   f"You'll be gone for {amount/2:,} seconds {ctx.message.author.mention}")
                    await asyncio.sleep(amount/2)
                    caught = {'shark': 0, 'red_snapper': 0, 'flounder': 0, 'tuna': 0, 'swordfish': 0, 'barracuda': 0}
                    total_xp = {'xp': 0}
                    while amount > 0:
                        if bait == 'shrimp':
                            fish_caught = random.choices(FISH_RARITIES_OCEAN, weights=[1, 10, 15, 6, 4, 2, 62])[0]
                        if bait == 'minnows':
                            fish_caught = random.choices(FISH_RARITIES_OCEAN, weights=[1.5, 13, 18, 8, 6, 3, 50.5])[0]
                        if bait == 'squid':
                            fish_caught = random.choices(FISH_RARITIES_OCEAN, weights=[3.5, 18, 25, 10, 8, 6, 29.5])[0]
                        amount -= 1
                        if fish_caught != 'None':
                            caught[fish_caught] += 1
                            total_xp['xp'] += FISH_XP.get(fish_caught)
                            self.client.jahcoins[id_]['fish'][fish_caught] += 1
                            self.client.jahcoins[id_]['fish']['xp'] += FISH_XP.get(fish_caught)

                        self.client.jahcoins[id_]['fish'][bait] -= 1
                        self.save_file()
                    await ctx.send(f"You are back from fishing and have caught:\n\n" +
                                   f"{(caught['shark']):,} **Shark**\n" +
                                   f"{(caught['red_snapper']):,} **Red Snapper**\n" +
                                   f"{(caught['flounder']):,} **Flounder**\n" +
                                   f"{(caught['tuna']):,} **Tuna**\n" +
                                   f"{(caught['swordfish']):,} **Swordfish**\n" +
                                   f"{(caught['barracuda']):,} **Barracuda**\n" +
                                   f"You also received {total_xp['xp']:,} **XP** {ctx.message.author.mention}")
                    
                                                                
            if self.client.jahcoins[id_]['fish']['xp'] >= 9123085:
                self.client.jahcoins[id_]['fish']['level'] = 10
            elif self.client.jahcoins[id_]['fish']['xp'] >= 6028390:
                self.client.jahcoins[id_]['fish']['level'] = 9
            elif self.client.jahcoins[id_]['fish']['xp'] >= 3965260:
                self.client.jahcoins[id_]['fish']['level'] = 8
            elif self.client.jahcoins[id_]['fish']['xp'] >= 2589840:
                self.client.jahcoins[id_]['fish']['level'] = 7
            elif self.client.jahcoins[id_]['fish']['xp'] >= 1672893:
                self.client.jahcoins[id_]['fish']['level'] = 6
            elif self.client.jahcoins[id_]['fish']['xp'] >= 1061595:
                self.client.jahcoins[id_]['fish']['level'] = 5
            elif self.client.jahcoins[id_]['fish']['xp'] >= 654063:
                self.client.jahcoins[id_]['fish']['level'] = 4
            elif self.client.jahcoins[id_]['fish']['xp'] >= 382375:
                self.client.jahcoins[id_]['fish']['level'] = 3
            elif self.client.jahcoins[id_]['fish']['xp'] >= 201250:
                self.client.jahcoins[id_]['fish']['level'] = 2
            elif self.client.jahcoins[id_]['fish']['xp'] >= 80500:
                self.client.jahcoins[id_]['fish']['level'] = 1
            await ctx.send(f"You have leveled up to level {(self.client.jahcoins[id_]['fish']['level'])} fishing! {ctx.message.author.mention}")
            self.save_file()
                    

                                            
def setup(client):
    client.add_cog(skills(client))
    client.add_cog(FishingGame(client))
