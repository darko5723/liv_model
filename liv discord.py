import discord
import os
import requests
import time
import asyncio
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"   # or 3B if slow

conversation_history = defaultdict(list)
COOLDOWN = {}
COOLDOWN_SECONDS = 4

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} is online and ready as Liv from PGR! 💙')
    print(f'Using model: {MODEL_NAME}')

@client.event
async def on_message(message):
    # ... (keep the same code as before for on_message)

    # At the very end of on_message, make sure to wrap the API call in try-except like this:
    try:
        # your existing requests.post code here
        ...
    except Exception as e:
        print(f"Error in message handler: {e}")
        await message.channel.send("Ah... something went wrong. I'm really sorry... 💦")

# Add this to prevent full crash on disconnects
@client.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}:", args, kwargs)

# Run with reconnect
while True:
    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"Bot crashed with error: {e}. Restarting in 10 seconds...")
        await asyncio.sleep(10)
