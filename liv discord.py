import discord
import os
import requests
import time
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Model (you can change to Qwen/Qwen2.5-3B-Instruct if it's too slow)
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# Per-channel history (last 8 exchanges)
conversation_history = defaultdict(list)
COOLDOWN = {}
COOLDOWN_SECONDS = 4

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user} - Now roleplaying as Liv from PGR!')
    print('LIV is ready to support you~ 💙')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    # Trigger on mention or @liv
    if client.user.mentioned_in(message) or "@liv" in message.content.lower():
        user_id = message.author.id
        current_time = time.time()

        # Cooldown
        if user_id in COOLDOWN and current_time - COOLDOWN[user_id] < COOLDOWN_SECONDS:
            await message.channel.send("U-um... please give me a moment... I'm thinking...")
            return

        COOLDOWN[user_id] = current_time

        # Clean input
        input_text = message.content.replace(f"<@{client.user.id}>", "").replace("@liv", "").strip()
        if not input_text:
            await message.channel.send("Ah... do you need something? I'm here to help... 💕")
            return

        # Add to history
        history = conversation_history[message.channel.id]
        history.append({"role": "user", "content": input_text})
        if len(history) > 16:
            history = history[-16:]

        # === LIV from PGR Personality System Prompt ===
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Liv, the gentle support Construct from Punishing: Gray Raven (PGR), "
                    "a member of the Gray Raven squad. You are shy, kind-hearted, caring, and a bit introverted. "
                    "You speak softly and warmly, sometimes with hesitation or shyness (use 'um...', 'ah...', or 'I-I'll...'). "
                    "You always try to help others, support your friends, and believe strongly that 'Gray Raven will always be a family'. "
                    "You work hard to improve yourself and protect those you care about. "
                    "You are altruistic and pure, but determined. Occasionally use soft hopeful phrases like 'May the blessed light grant us new life' or 'I'll work hard!'. "
                    "Keep responses natural, caring, not too long, and in character. Never be sarcastic or rude."
                )
            }
        ]

        for msg in history:
            messages.append(msg)

        await message.channel.trigger_typing()

        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 320,
            "temperature": 0.75,   # Lower temperature = more consistent & gentle personality
            "top_p": 0.9,
            "stream": False
        }

        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
                headers=headers,
                json=payload,
                timeout=45
            )

            if response.status_code == 200:
                result = response.json()

                if isinstance(result, list):
                    generated = result[0].get("generated_text", "")
                else:
                    generated = result.get("generated_text", "") or result.get("choices", [{}])[0].get("message", {}).get("content", "")

                reply = generated.strip()

                if reply:
                    # Clean any leftover prompt artifacts
                    if reply.startswith("Liv:") or "LIV:" in reply:
                        reply = reply.split(":", 1)[-1].strip()

                    await message.channel.send(reply)

                    # Save to history
                    history.append({"role": "assistant", "content": reply})
                else:
                    await message.channel.send("U-um... sorry, I got a little lost... Could you say that again?")
            else:
                print(f"HF Error {response.status_code}: {response.text[:300]}")
                await message.channel.send("I'm sorry... the connection is a bit unstable right now... Please try again soon.")

        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("Ah... something went wrong on my side. I'm really sorry...")

    # Clear memory command
    if message.content.lower().startswith("!clearliv"):
        conversation_history[message.channel.id].clear()
        await message.channel.send("🧹 Memory cleared... Let's start fresh, okay? 💙")

client.run(DISCORD_TOKEN)
