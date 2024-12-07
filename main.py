import requests
import random
import telegram
from dotenv import load_dotenv
import os


def get_image(image_num):
    url = f"https://xkcd.com/{image_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    image = response.json()["img"]
    comment = response.json()["alt"]
    return image, comment

  
def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def number_comics():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    total_num = response.json()["num"]
    image_num = random.randint(1, total_num)
    return image_num


def tg_bot(filename, comment, tg_key, chat_id):
    bot = telegram.Bot(token=tg_key)
    with open(filename, 'rb') as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=comment)
    


def main():
    load_dotenv()
    try:
        tg_key = os.environ["TG_BOT_TOKEN"]
        chat_id = os.environ["TG_CHAT_ID"]
        filename = "image.png" 
        image_num = number_comics()
        image, comment = get_image(image_num)
        download_image(image, filename)
        tg_bot(filename, comment, tg_key, chat_id)
    finally:
        os.remove(filename)


if __name__ == "__main__":
    main()