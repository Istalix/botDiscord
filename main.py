import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import random
import os
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
load_dotenv()
#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#Variables e intents

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='/',intents=intents)


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#Eventos del bot de discord
@bot.event
async def on_ready():
    print(f"We are are ready to go {bot.user.name}")
@bot.event
async def on_message(message):
    #variables del mensaje
    #============================
    
    if message.author == bot.user:
        return
    if message.mentions:
        print(f"El contenido del mensaje es : {message.content.lower()}")
        mencionado = message.mentions[0]
        print(f"Id del mencionado {mencionado}")
        status_mencionado = message.mentions[0].status
        msg_content = message.content

        if message.mentions and "kick" in message.content.lower() and mencionado.voice:
                await message.delete()
                array_msg = ["Un coñeta menos del que preocuparse", "chupala un rato", " a ido a buscar a su padre al estanco", "damn is 🎉😂!","a ido en busca de silksong(no existe)"]
                random_msg = random.choice(array_msg)
                await mencionado.move_to(None)
                await message.channel.send(f"{mencionado.mention} {random_msg}")

        if message.mentions and "spamear" in message.content.lower() and status_mencionado == discord.Status.online:
            await message.delete()
            await message.channel.send(f"{mencionado.mention} esta conectado, estas mas ciego que cletus conduciendo")
        elif message.mentions and "spamear" in message.content.lower() and status_mencionado != discord.Status.online:
            pattern = r"(\d+)\s*$"
            match = re.findall(pattern, msg_content)
            num_reps = int(match[0])
            await message.delete()
            if num_reps > 25:
                await message.channel.send(f"{mencionado.mention} el blud se cree que le voy a dejar spamear {num_reps} veces")
                return
            elif num_reps < 25:
                for i in range(num_reps):
                    await message.channel.send(f"{mencionado.mention} metete bujarra")

        if bot.user.mentioned_in(message) and "dime un secreto" in message.content.lower():
            if message.author.voice:
                #Variables Canal de Voz
                voice_channel_actual =  message.author.voice.channel
                channel_voice_members = voice_channel_actual.members
                member_random = random.choice(channel_voice_members)
                array_secrets = [f"{member_random.mention} es un coñeta",f"{member_random.mention} le debe 5 euros a {member_random.mention}",f"{member_random.mention} llama todas las noches a los teletubbies.exe",f"Damn is🎉😂",f"{member_random.mention} conduce como cletus",f"{member_random.mention} se parece a miguelroy",f"Valen es to malo en el blasphemous",f"No va a salir Siksong nunca" ]
                random_secret = random.choice(array_secrets)
                await message.channel.send(f"{random_secret} 🤫")  
    await bot.process_commands(message)

#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#


#Comandos del bot de discord
@bot.command()
async def ruleta(ctx):
    if ctx.author == bot.user:
        return
    if ctx.author.voice:
        #Variables Canal de Voz
        voice_channel_actual =  ctx.author.voice.channel
        channel_voice_members = voice_channel_actual.members
        mencion_author_message = ctx.author.mention
        await ctx.channel.send(f"{mencion_author_message} quiere hacer una ruleta de coñetas‍🌈:speaking_head: !")
        await ctx.channel.send("3")
        await ctx.channel.send("2")
        await ctx.channel.send("1")
        array_ruleta_ctx = ["tu no te escapas bujarra", "a sido deportado por Pedro Sanchez por ser español", "no se aceptan wiggas en este server", "se le ha petado el pc como al coñeta que todos sabemos","se ha ido a merendar(mentira, solo pocos saben)"]
        random_ctx_ruleta = random.choice(array_ruleta_ctx)
        kicked_member = random.choice(channel_voice_members)
        await ctx.channel.send(f"{kicked_member.mention} {random_ctx_ruleta}")
        await kicked_member.move_to(None)


#TODO: WEBSCRAPPER
@bot.command()
async def busca(ctx,*,query):
    if ctx.author == bot.user:
        return
    print(query)
    search_name = query.replace(' ', '_')
    url = 'https://wikipedia.org/wiki/'
    url_final = urljoin(url,search_name)
    print (url_final)
    headers = {'User-Agent':"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/131.0.0.0 Safari/537.36"}
    response = requests.get(url_final, headers=headers)

    if response.status_code == 200:
        print("La peticion a sido existosa")

        soup = BeautifulSoup(response.text, 'html.parser')
        
        svg = soup.find(class_='mw-file-description')
        img_svg = svg.find('img')
        img_svg_url = img_svg.get('src')
        if img_svg_url:
            await ctx.channel.send(urljoin(url, img_svg_url))
        else:
            await ctx.channel.send(url)


#TODO: Revisar api infojobs y hacer un comando que busque ofertas de trabajo





#NO BORRAR
bot.run(token, log_handler=handler,log_level=logging.DEBUG)