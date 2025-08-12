import discord
import os
import asyncio
from discord.ext import commands, tasks
import openai

# الإعدادات
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
EVENT_CHANNEL = 123456789  # استبدل بمعرف قناتك

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# تنظيم البوتات
@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} يعمل الآن!')
    await organize_bots()
    daily_event.start()

# وظيفة تنظيم البوتات
async def organize_bots():
    guild = bot.guilds[0]
    
    # إنشاء كاتيجوري للبوتات
    category = await guild.create_category("🤖│البوتات")
    
    bots = [member for member in guild.members if member.bot and member != bot.user]
    
    for bot_member in bots:
        await guild.create_text_channel(
            name=f"{bot_member.name}-chat",
            category=category
        )
        await guild.create_voice_channel(
            name=f"{bot_member.name}-voice",
            category=category
        )

# فعالية يومية
@tasks.loop(hours=24)
async def daily_event():
    channel = bot.get_channel(EVENT_CHANNEL)
    await channel.send("@everyone 🎉 **الفعالية اليومية تبدأ الآن!** الساعة 6:00 مساءً")

# الدردشة مع الذكاء الاصطناعي
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if bot.user.mentioned_in(message):
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.content}]
        )
        await message.reply(response.choices[0].message.content)

    await bot.process_commands(message)

# تشغيل البوت
bot.run(TOKEN)
