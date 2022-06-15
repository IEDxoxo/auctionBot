#time to port to discord.py :)
#this is an older version of discord that is compatible with the code.
#pip install py-cord==2.0.0b1 = fix
import discord, os, time,json
from discord.ext.commands import has_permissions
from colored import fg
Token = input("Enter Token > ")
success = fg('green')
violet = fg("violet")
failure = fg('red')
client = discord.Bot()
allowedusers = [] # put in your discord ids that are allowed to use specific commands.
@client.event
async def on_ready():
    print(violet)
    mainmenu = rf"""  ______                         __      __                      _______              __     
 /      \                       |  \    |  \                    |       \            |  \    
|  $$$$$$\ __    __   _______  _| $$_    \$$  ______   _______  | $$$$$$$\  ______  _| $$_   
| $$__| $$|  \  |  \ /       \|   $$ \  |  \ /      \ |       \ | $$__/ $$ /      \|   $$ \  
| $$    $$| $$  | $$|  $$$$$$$ \$$$$$$  | $$|  $$$$$$\| $$$$$$$\| $$    $$|  $$$$$$\\$$$$$$  
| $$$$$$$$| $$  | $$| $$        | $$ __ | $$| $$  | $$| $$  | $$| $$$$$$$\| $$  | $$ | $$ __ 
| $$  | $$| $$__/ $$| $$_____   | $$|  \| $$| $$__/ $$| $$  | $$| $$__/ $$| $$__/ $$ | $$|  \
| $$  | $$ \$$    $$ \$$     \   \$$  $$| $$ \$$    $$| $$  | $$| $$    $$ \$$    $$  \$$  $$
 \$$   \$$  \$$$$$$   \$$$$$$$    \$$$$  \$$  \$$$$$$  \$$   \$$ \$$$$$$$   \$$$$$$    \$$$$ 
                                                                                             
                                                                                             
                                                                                             """
    print(mainmenu)
    print(f"{violet}[{success}\{violet}]{violet} started discord client")
@client.slash_command()
async def createauction(ctx, name, bininput, bid, tid, oge, information):
    try:
        obj = json.load(open("auctions.json"))
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON data fixing now.")
        obj = {'auctions': {}}
    if ctx.author.id in allowedusers:
        if name in obj["auctions"]:
            await ctx.respond(f"ERROR auction already running")
            pass
        else:
            obj["auctions"][name] = {"bin": 0, "bid": 0, "information": None, "status": None}
            obj["auctions"][name]["bin"] = int(bininput)
            obj["auctions"][name]["bid"] = int(bid)
            obj["auctions"][name]["information"] = information
            obj["auctions"][name]["status"] = "running"
            obj["auctions"][name]["lastbid"] = None
            embed = discord.Embed(title="New Auction!", color=0xFF0000)
            embed.add_field(name="Name", value=name)
            embed.add_field(name="TID", value=tid)
            embed.add_field(name="OGE", value=oge)
            embed.add_field(name="BID", value=bid)
            embed.add_field(name="BIN", value=bininput)
            embed.add_field(name="Information", value=information)
            embed.set_footer(text="created by deviant#0001")
            c = open("auctions.json", "r+")
            c.truncate()
            c.write(json.dumps(obj))
            c.close()
            await ctx.respond(embed=embed)
    else:
        await ctx.respond(f"Your discord ID is not in the database.")
@client.slash_command()
async def endauction(ctx, auctionname):
    try:
        obj = json.load(open("auctions.json"))
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON data fixing now.")
        obj = {'auctions': {}}
    if ctx.author.id in allowedusers:
        if auctionname in obj["auctions"]:
            obj["auctions"][auctionname]["status"] = "finished"
            await ctx.respond(f"Auction is finished. Winner is: {obj['auctions'][auctionname]['lastbid']} make a ticket!")
            newdict = {}
            newdict["auctions"] = {}
            c = open("auctions.json", "r+")
            c.truncate()
            for item in obj["auctions"]:
                if item == auctionname:
                    pass
                else:
                    print(item)
                    newdict["auctions"] = item
            c.write(json.dumps(newdict))
            c.close()
        else:
            await ctx.respond(f"Auction hasn't been made or there is an error inside the auctions.json")
    else:
        await ctx.respond(f"Your discord ID is not in the database.")
@client.slash_command()
async def bid(ctx, name, bidamt):
    try:
        obj = json.load(open("auctions.json"))
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON data fixing now.")
        obj = {'auctions': {}}
    if name in obj["auctions"]:
        bidamt = int(bidamt)
        if int(obj["auctions"][name]["bid"] + 5) <= bidamt and not bidamt > 2000:
            if bidamt >= int(obj["auctions"][name]["bin"]):
                await ctx.respond(f"Contact the owner to purchase this item. | Bid is equal to or over the set BIN price.")
            else:
                if obj["auctions"][name]["status"] != "finished":
                    obj["auctions"][name]["bid"] = bidamt
                    obj["auctions"][name]["lastbid"] = str(ctx.author)
                    await ctx.respond(f"Successfully updated the bid! Current BID Now: {bidamt}")
                    c = open("auctions.json", "r+")
                    c.truncate()
                    c.write(json.dumps(obj))
                    c.close()
                else:
                    await ctx.respond(f"Auction is not running currently.")
        else:
            await ctx.respond(f"Bid is invalid. Input: {bidamt}")
try:
    client.run(Token)
except Exception as e:
    print(f"{violet}[{failure}\{violet}] {failure}failed to start client Reason: {e}")
