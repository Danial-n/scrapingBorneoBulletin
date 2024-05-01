from typing import Final, List
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from discord.ui import Button, View
from responses import get_response
from wsBorneoBulletin import scraper
from responses import sort_news, news_file

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

class NewsButton(discord.ui.Button):
    def __init__(self, category):
        super().__init__(label=category.capitalize(), style=discord.ButtonStyle.primary)
        self.category = category

    async def callback(self, interaction: discord.Interaction): 
        news_items = sort_news(self.category)
        if [f'No {self.category} news today'] != news_items:
            await interaction.response.send_message(f"Today news in {self.category}:", ephemeral=True)
            for news_item in news_items:
                await interaction.followup.send(news_item, ephemeral=True)
            await interaction.followup.send("Choose a category:", view=NewsView(), ephemeral=True) 
        else:
            await interaction.response.send_message(f'No news in {self.category} today')
            await interaction.followup.send("Choose a category:", view=NewsView()) 

class NewsView(View):
    def __init__(self):
        super().__init__()
        categories = ['national', 'southeast', 'world', 'business', 'tech', 'lifestyle', 'entertainment', 'features', 'sports', 'opinion']
        for category in categories:
            self.add_item(NewsButton(category))

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intent)')
        return

    elif is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    elif user_message[0] == '!':
        user_message = user_message[1:]

        if user_message == 'news':
            if is_private:
                await message.author.send("Choose a category:", view=NewsView())
            else:
                await message.channel.send("Choose a category:", view=NewsView())

        elif user_message == 'update':
            get_news = 'Retrieving news...'
            if is_private:
                await message.author.send(get_news)
                scraper()
                await message.author.send('News updated')
            else:
                await message.channel.send(get_news)
                scraper()
                await message.channel.send('News updated')

        else:
            try:
                response_list: List[str] = get_response(user_message)

                for response in response_list:
                    if is_private:
                        await message.author.send(response)
                    else:
                        await message.channel.send(response)
                        
            except Exception as e:
                print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main() -> None: 
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()