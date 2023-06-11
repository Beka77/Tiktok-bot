import os
import requests
import urllib
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# https://t.me/rxc_official
from tiktok import getCookie, getDownloadUrl, getDownloadID, getStatus
import urllib.request
import config

TOKEN = config.token  # @rxc_official
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def download_video(video_url, name):
    r = requests.get(video_url, allow_redirects=True)
    content_type = r.headers.get('content-type')
    if content_type == 'video/mp4':
        open(f'./videos/video{name}.mp4', 'wb').write(r.content)
    else:
        pass

if not os.path.exists('videos'):
    os.makedirs('videos')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # https://t.me/rxc_official
    await bot.send_message(chat_id=message.chat.id, text=' Привет, я помогу тебе скачать видео с TikTok. \n/help - инструкция как скачать видео.')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    # @rxc_official
    await bot.send_message(chat_id=message.chat.id, text='Скопируй ссылку на видео TikTok и отправь её мне:')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.startswith('https://www.tiktok.com'):
        video_url = message.text
        cookie = getCookie()
        status = getStatus(video_url, cookie)
        if status == False:
            await bot.send_message(chat_id=message.chat.id, text='Неверная ссылка, видео было удалено или я его не нашел.')
        else:
            await bot.send_message(chat_id=message.chat.id, text='Скачиваю видео')
            url = getDownloadUrl(video_url, cookie)
            video_id = getDownloadID(video_url, cookie)
            download_video(url, video_id)
            path = f'./videos/video{video_id}.mp4'
            with open(f'./videos/video{video_id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Держи видео🚀 '
                )
            os.remove(path)
    elif message.text.startswith('https://vm.tiktok.com'):
        video_url = message.text
        req = urllib.request.Request(
            video_url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            }  # @rxc_official
        )
        url_v = urllib.request.urlopen(req).geturl()
        if url_v == 'https://www.tiktok.com/':
            await bot.send_message(chat_id=message.chat.id, text='Неверная ссылка, видео было удалено или я его не нашел.')
        else:
            cookie = getCookie()
            await bot.send_message(chat_id=message.chat.id, text='Скачиваю видео\nЖди⚡️')
            url = getDownloadUrl(url_v, cookie)
            video_id = getDownloadID(url_v, cookie)
            download_video(url, video_id)  # @rxc_official
            path = f'./videos/video{video_id}.mp4'
            with open(f'./videos/video{video_id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Держи видео🚀'
                )  # @rxc_official
            os.remove(path)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Я тебя не понял, отправь мне ссылку на видео TikTok.')
if __name__ == "__main__":
    # Запускаем бота и подписываемся на самый пиздатый канал @rxc_official
    executor.start_polling(dp, skip_updates=True)
