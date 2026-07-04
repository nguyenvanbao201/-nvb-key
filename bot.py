import telebot
from config import BOT_TOKEN
from database import check_user
from link4m import create_link

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "🔑 Nhấn /key để lấy key")


@bot.message_handler(commands=["key"])
def key(msg):
    user_id = msg.chat.id

    if not check_user(user_id):
        bot.send_message(user_id, "⛔ Bạn đã lấy key trong 24h")
        return

    # link trỏ về web trung gian của bạn
    link = create_link(f"https://telegra.ph/")

    bot.send_message(user_id, f"👉 Vượt link để lấy key:\n{link}")


bot.polling()