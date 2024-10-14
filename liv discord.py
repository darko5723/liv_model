import discord
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Model name from Hugging Face repository
model_name = "darko5723/liv_model"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set up the device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

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

        # Get the message content and pass it to the model
        inputs = tokenizer(input_text, return_tensors="pt").to(device)

        # Adjust generation parameters for better conversational output
        outputs = model.generate(
            **inputs,
             max_new_tokens=15,
             min_length=7,
             num_beams=1,
             do_sample=True,
             top_k=20,
             temperature=0.2,
             repetition_penalty=4.0,
             pad_token_id=tokenizer.eos_token_id,
             eos_token_id=tokenizer.eos_token_id
            )

        # Decode and send the response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        await message.channel.send(generated_text)

    else:
        print(f"No matching command detected for message: '{message.content}'")

# Run the bot
client.run(DISCORD_TOKEN)


































