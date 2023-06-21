# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Command

# # Create a bot instance
# bot = Bot(token='5569548024:AAGoF56VhS--DysFkhBQZnrHyq7dFhezUNU')

# # Create a dispatcher instance
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

# @dp.message_handler(Command('start'))
# async def cmd_start(message: types.Message):
#     await message.answer("Welcome to the music bot! Send me the name of a song.")


# import requests

# def search_music(query):
#     # Make a request to the Deezer API to search for music
#     response = requests.get(f'https://api.deezer.com/search?q={query}&limit=5')
#     data = response.json()

#     # Extract the necessary information from the response
#     tracks = data['data']
#     results = []
#     for track in tracks:
#         title = track['title']
#         artist = track['artist']['name']
#         preview_url = track['preview']
#         results.append((title, artist, preview_url))
    
#     return results

# @dp.message_handler()
# async def search_and_send_music(message: types.Message):
#     query = message.text
    
#     # Search for music based on the user's query
#     results = search_music(query)
    
#     if not results:
#         await message.answer("No music found.")
#         return
    
#     # Send the found music to the user
#     for title, artist, preview_url in results:
#         text = f"{title} by {artist}\nListen: {preview_url}"
#         await message.answer(text)

# from aiogram import executor

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create a bot instance
bot = Bot(token='5569548024:AAGoF56VhS--DysFkhBQZnrHyq7dFhezUNU')

# Create a dispatcher instance
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Create a Spotify client instance
client_credentials_manager = SpotifyClientCredentials(
    client_id='9e80c910124542309a60266a0b7b52de',
    client_secret='842b20be74bd440a8d1ed9d4d28f7ec7'
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the music bot! Send me the name of a song.")
    
@dp.message_handler()
async def search_and_send_music(message: types.Message):
    query = message.text
    
    # Search for music using the Spotify API
    response = spotify.search(q=query, type='track', limit=5)
    tracks = response['tracks']['items']
    
    if not tracks:
        await message.answer("No music found.")
        return
    
    # Send the found music to the user
    for track in tracks:
        title = track['name']
        artist = track['artists'][0]['name']
        preview_url = track['preview_url']
        text = f"{title} by {artist}\nListen: {preview_url}"
        await message.answer(text)

from aiogram import executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
