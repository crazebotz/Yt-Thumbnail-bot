# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)
# Author 2: Rahul Thakor (https://t.me/Rahul_thakor) (@Rahul_thakor)

import os
import ytthumb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.errors import FloodWait, UserNotParticipant


Bot = Client(
    "Yt-thum-bot",
    bot_token = os.environ.get("BOT_TOKEN"),
    api_id = int(os.environ.get("API_ID")),
    api_hash = os.environ.get("API_HASH")
)



START_TEXT = """Hello {},
I am a simple Youtube thumbnail downloader telegram bot.

- Send a youtube video link or video ID.
- I will send the thumbnail.
- You can also send youtube video link or video id with quality. ( like :- `rokGy0huYEA | sd`
  - sd - Standard Quality
  - mq - Medium Quality
  - hq - High Quality
  - maxres - Maximum Resolution

Made by @CrazeBots"""

BUTTON = [InlineKeyboardButton(
    '⚙ Join Channel ⚙', url='https://telegram.me/CrazeBots')]

photo_buttons = InlineKeyboardMarkup(
    [[InlineKeyboardButton('🎡 Other Qualities',
                           callback_data='qualities')], BUTTON]
)

join_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
        '⚙ Join Channel ⚙', url='https://telegram.me/CrazeBots')]]
)


@Bot.on_callback_query()
async def cb_data(_, message):
    data = message.data.lower()
    if data == "qualities":
        await message.answer('Select a quality')
        buttons = []
        for quality in ytthumb.qualities():
            buttons.append(
                InlineKeyboardButton(
                    text=ytthumb.qualities()[quality],
                    callback_data=quality
                )
            )
        await message.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [[buttons[0], buttons[1]], [buttons[2], buttons[3]], BUTTON]
            )
        )
    if data == "back":
        await message.edit_message_reply_markup(photo_buttons)
    if data in ytthumb.qualities():
        url=message.message.reply_to_message.text
        if "|" in message.message.reply_to_message.text:
            text = message.message.reply_to_message.text.split(" | ", -1)[0]
            url=f"https://youtu.be/{text}"
        thumbnail = ytthumb.thumbnail(
            video=url,
            quality=message.data
        )
        await message.answer('Updating')
        await message.edit_message_media(

            media=InputMediaPhoto(media=thumbnail),
            reply_markup=photo_buttons
        )

        await message.answer('Update Successfully')


async def forceSub(app, msg):
    try:
        await app.get_chat_member('crazebots', msg.from_user.id)
        return True
    except UserNotParticipant:
        await app.send_message(chat_id=msg.from_user.id, text="**Please Join My Update Channel To Use Me**", reply_markup=join_button, reply_to_message_id=msg.id)
        return False
    except:
        return True


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([BUTTON]),
        quote=True
    )


@Bot.on_message(filters.incoming & filters.private & filters.text)
async def send_thumbnail(_, update):
    message = await update.reply_text(
        text="`Analysing...`",
        disable_web_page_preview=True,
        quote=True
    )
    result = await forceSub(Bot,update)
    if result == False:
        await message.delete()
        return
    try:
        if " | " in update.text:
            video = update.text.split(" | ", -1)[0]
            quality = update.text.split(" | ", -1)[1]
        else:
            video = update.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await update.reply_photo(
            photo=thumbnail,
            reply_markup=photo_buttons,
            quote=True
        )
        await message.delete()
    except Exception as error:
        await message.edit_text(
            text=error,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([BUTTON])
        )
print("Bot Started Success")
Bot.run()
