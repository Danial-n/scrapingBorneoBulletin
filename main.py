from typing import Final, List
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intent)')
        return

    elif is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    elif user_message[0] == '!':
        user_message = user_message[1:]

        if user_message == 'news':
            menu = 'menu'
            if is_private:
                    await message.author.send(menu)
            else:
                await message.channel.send(menu)

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