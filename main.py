import asyncio
import datetime
import logging
import os

import pytz
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaPhoto

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)

TIME_ZONE = os.environ["TIME_ZONE"]
BOT_LIST = [i.strip() for i in os.environ.get("BOT_LIST").split(" ")]
CHANNEL_OR_GROUP_ID = int(os.environ["CHANNEL_OR_GROUP_ID"])
MESSAGE_ID = int(os.environ["MESSAGE_ID"])
try:
    BOT_ADMIN_IDS = [int(i.strip()) for i in os.environ.get("BOT_ADMIN_IDS").split(" ")]
except BaseException:
    BOT_ADMIN_IDS = [int(os.environ.get("BOT_ADMIN_IDS", 0)).split()]

API_HASH = os.environ.get("API_HASH", None)
API_ID = int(os.environ.get("API_ID", 0))
SESSION_NAME = os.environ.get("SESSION_NAME", None)


app = Client(SESSION_NAME, API_ID, API_HASH)

logging.warning("Starting ➿➿➿....")


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def main():
    async with app:
        logging.warning("Starting Bot Check Loop ➿....")
        while True:
            logging.warning("Checking...")
            GET_CHANNEL_OR_GROUP = await app.get_chat(int(CHANNEL_OR_GROUP_ID))
            CHANNEL_OR_GROUP_NAME = GET_CHANNEL_OR_GROUP.title
            CHANNEL_OR_GROUP_TYPE = GET_CHANNEL_OR_GROUP.type
            yax = 600
            bg = Image.open("images/bg.jpg")
            bg = changeImageSize(1300, 2000, bg)
            # font = ImageFont.load_default()
            font = ImageFont.truetype("stuff/fonts/arial.ttf", 60)
            xxx_tg = f"📊 **<u>LIVE BOT STATUS @NACBOTS</u>**\n\n**💬 {CHANNEL_OR_GROUP_TYPE}**: {CHANNEL_OR_GROUP_NAME}"
            for bot in BOT_LIST:
                try:
                    yyy_tg = await app.send_message(bot, "/start")
                    aaa = yyy_tg.message_id
                    await asyncio.sleep(10)
                    zzz_tg = await app.get_history(bot, limit=1)
                    for ccc in zzz_tg:
                        bbb = ccc.message_id
                    if aaa == bbb:
                        logo = Image.open("images/down.jpg")
                        # imgffff = Image.open("temp.png")
                        bg = bg.copy()
                        yax = yax + 175
                        bg.paste(logo, (1000, yax))
                        draw = ImageDraw.Draw(bg)
                        draw.text((200, yax), f"{bot}", (26, 84, 174), font=font)
                        for bot_admin_id in BOT_ADMIN_IDS:
                            try:
                                await app.send_message(
                                    int(bot_admin_id),
                                    f"🚨 **Beep! Beep!! {bot} is down** ❌",
                                )
                            except Exception:
                                pass
                        await app.read_history(bot)
                    else:
                        logo = Image.open("images/up.jpg")
                        # imgffff = Image.open("temp.png")
                        bg = bg.copy()
                        yax = yax + 190
                        bg.paste(logo, (1000, yax))
                        draw = ImageDraw.Draw(bg)
                        # font = ImageFont.truetype("font.ttf", 80)
                        draw.text((200, yax), f"{bot}", (26, 84, 174), font=font)
                        await app.read_history(bot)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))

            last_update = time.strftime(f"%d %b %Y at %I:%M %p")
            xxx_tg += f"\n\n✔️ Last updated on: {last_update} ({TIME_ZONE})\n\n<i>⇋ Updates every 45min - Powered by @NACBots</i>"
            bg.save("md.jpg")
            await app.edit_message_media(
                CHANNEL_OR_GROUP_ID,
                MESSAGE_ID,
                InputMediaPhoto(media="md.jpg", caption=xxx_tg),
            )
            logging.warning(f"Last checked on: {last_update}")
            await asyncio.sleep(2700)
            # await asyncio.sleep(60)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
