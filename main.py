#system bot
import sys
import settings
from discord.ext import commands

#from .env
client = commands.Bot(command_prefix=settings.PREFIX)
DBG = int(settings.DBG)
TOKEN=settings.TOKEN

#dbg feature
def isDBG(reqlv:int):
  if(DBG >= reqlv):
    return True
  else:
    return False

#custom index function
def indexordefault(list, x, default=False):
  return list.index(x) if x in list else default

#get voice-channel ctx.author is talking in
async def gettalkingvc(ctx):
  talkingvc = None
  vclist = ctx.guild.voice_channels
  if(isDBG(2)):
    await ctx.send("ctx.author.id:"+str(ctx.author.id))
    await ctx.send("len(vclist):"+str(len(vclist)))
  for vc in vclist:
    memberlist = list(vc.voice_states)
    if(isDBG(2)):
      await ctx.send("len(member of "+str(vc.name)+"):"+str(len(memberlist)))
    for memberid in memberlist:
      if(isDBG(2)):
        await ctx.send("memberid:" + str(memberid))
      if(str(memberid) == str(ctx.author.id)):
        if(isDBG(2)):
          await ctx.send("Found in " + str(vc.name))
        talkingvc = vc
        continue
  return talkingvc

#command
#Changes vc-region 
#notation: .rc auto || japan || hongkong ...
#systemreply: yes
@client.command(description="changes channnel region.", brief="change region", aliases=['rc', 'change'])
async def regionchange(ctx, *args):
  if(len(args) == 0):
    await ctx.send(":writing_hand: region list:\n auto amsterdam brazil dubai eu-central eu-west europe frankfurt hongkong india japan london russia singapore southafrica south-korea sydney us-central us-east us-south us-west vip-amsterdam vip-us-east vip-us-west")
    return

  talkingvc = await gettalkingvc(ctx)
  if(talkingvc == None):
    await ctx.send("You are not in voice-channel.")
    return

  await ctx.send(":thinking: regionchange("+talkingvc.name+" to "+args[0]+")...")

  try:
    if(args[0] == "auto"):
       await talkingvc.edit(rtc_region=None, reason= ctx.author.name + " sent request")
    else:
       await talkingvc.edit(rtc_region=args[0], reason= ctx.author.name + "sent request")
    await ctx.send(":ok: complete.")
  except:
    await ctx.send(":anger: could not change region.")

#command
#Rolls vc-region
#notation: .rr
#system reply: yes
@client.command(description="changes channel region to unusing region.", brief="roll region", aliases=['rr', 'roll'])
async def regionroll(ctx, *args):
  talkingvc = await gettalkingvc(ctx)
  if(talkingvc == None):
    await ctx.send("You are not in voice channel")

  candidate = ['japan', 'hongkong', 'singapore', 'india', 'sydney', 'us-west']
  currentregion = talkingvc.rtc_region
  if(isDBG(1)):
    await ctx.send("currentregion:" + str(currentregion))
  index = indexordefault(candidate, str(currentregion))
  if(index == False):
    await regionchange(ctx, candidate[1])
    return
  else:
    if(index  == len(candidate) - 1):
      index = -1
    await regionchange(ctx, candidate[index + 1])
    return


#do nothing right now
@client.event
async def on_message(message):
  await client.process_commands(message)

  if(client.user==message.author):
    return

#prints starting message on console
@client.event
async def on_ready():
  print("system bot is running as user name[" + str(client.user.name) + "] id[" + str(client.user.id) + "]" )

#GO
client.run(TOKEN)
