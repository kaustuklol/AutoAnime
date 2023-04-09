import asyncio
from config import PUBLIC_CHANNEL_ID
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def handle_force_subscribe(bot, message):
    try:
        invite_link = await bot.create_chat_invite_link(int(PUBLIC_CHANNEL_ID))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await bot.get_chat_member(int(PUBLIC_CHANNEL_ID), message.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry Sir, You are Banned..",
                disable_web_page_preview=True,
                reply_to_message_id=message.id,
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You need to join this channel to use me, click on the button and join the channel and then press the watch button again",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Channel 🤖", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
                    ]
                ]
            ),
            reply_to_message_id=message.id,
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Something Went Wrong.",
            disable_web_page_preview=True,
            reply_to_message_id=message.id,
        )
        return 400

