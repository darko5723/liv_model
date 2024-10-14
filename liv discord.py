import discord
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord bot token and Hugging Face API token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Model name from Hugging Face repository
model_name = "darko5723/liv_model"

# Define intents
intents = discord.Intents.default()
intents.messages = True

# Initialize Discord client with intents
client = discord.Client(intents=intents)

# Function to handle user messages
@client.event
async def on_ready():
    print(f'Logged in as {client.user} and ready to receive messages.')

@client.event
async def on_message(message):
    # Log received message and author
    print(f"Received message: '{message.content}' (author: {message.author})")

    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # Check if the message contains "@liv" or any command matching "liv"
    if client.user.mentioned_in(message) or "@liv" in message.content.lower():
        # Clean up the message content by removing mentions and extra spaces
        input_text = message.content.replace("@liv", "").replace(f"<@{client.user.id}>", "").strip()

        # Skip empty messages after cleaning
        if not input_text:
            print("Empty message received after cleaning, skipping...")
            return

        # Log the input being sent to the model
        print(f"Sending input to model: '{input_text}'")

        # Set up headers for Hugging Face Inference API request
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}"
        }

        # Send request to Hugging Face Inference API
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model_name}",
            headers=headers,
            json={"inputs": input_text}
        )

        if response.status_code == 200:
            generated_text = response.json().get('generated_text', '').strip()
            if generated_text:
                # Send the response back to Discord
                await message.channel.send(generated_text)
            else:
                print("No valid response from model.")
        else:
            print(f"Failed to get a response from the model: {response.status_code} - {response.text}")
            await message.channel.send("I'm having trouble processing that right now. Please try again later.")

    else:
        print(f"No matching command detected for message: '{message.content}'")

# Run the bot
client.run(DISCORD_TOKEN)



































