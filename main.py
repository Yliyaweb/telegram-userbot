import asyncio
from pyrogram import Client, filters, types

API_ID = 38371847
API_HASH = "7446032a115a1c4b90a3dea0ff81a6e8"
BOT_TOKEN = "7917245219:AAHwLeMHJdsfvPkpULcLUnqrIbnCdQrVNTQ"
MY_CHAT_ID = 1056886294
BOT_ID = 7917245219

# Список известных контактов (в памяти)
known_chats = set()

# Инициализация Userbot (для мониторинга)
user_app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# Инициализация Bot (для отправки уведомлений)
bot_app = Client("notification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@user_app.on_message(filters.private & filters.incoming & ~filters.me & ~filters.bot)
async def monitor_private_messages(client, message):
    # Игнорируем сообщения от конкретного бота
    if message.chat.id == BOT_ID:
        return

    chat_id = message.chat.id
    first_name = message.chat.first_name or "Неизвестный"
    username = message.chat.username or "нет username"
    text_content = (message.text or "[медиа/стикер]")[:200]

    # Проверка на новый контакт
    if chat_id not in known_chats:
        status_emoji = "🆕"
        status_text = "НОВЫЙ КОНТАКТ!"
        known_chats.add(chat_id)
    else:
        status_emoji = "💬"
        status_text = "Сообщение от известного контакта"

    # Формирование уведомления
    notification = (
        f"{status_emoji} {status_text}\n\n"
        f"👤 Отправитель: {first_name}\n"
        f"🆔 Username: @{username}\n"
        f"📱 User ID: {chat_id}\n"
        f"💬 Текст: {text_content}\n"
        f"🔗 Профиль: tg://user?id={chat_id}"
    )

    # Ограничение длины сообщения (600 символов)
    if len(notification) > 600:
        notification = notification[:597] + "..."

    try:
        await bot_app.send_message(MY_CHAT_ID, notification)
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")

async def main():
    print("Запуск мониторинга...")
    await asyncio.gather(
        user_app.start(),
        bot_app.start()
    )
    print("Userbot и Bot запущены!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    user_app.run(main())
