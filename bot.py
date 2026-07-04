import telebot
from config import BOT_TOKEN, BASE_URL
from database import check_user
from link4m import create_link

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "👋 Chào bạn!\n\n"
        "🔑 Nhấn /key để nhận key sử dụng trong 24 giờ."
    )


@bot.message_handler(commands=["key"])
def key(msg):
    user_id = msg.chat.id

    # Nếu người dùng vẫn còn key hợp lệ thì không cho lấy mới
    if check_user(user_id):
        bot.send_message(
            user_id,
            "⛔ Bạn đã có key còn hiệu lực trong 24 giờ.\n"
            "Vui lòng đợi hết hạn rồi lấy key mới."
        )
        return

    # Tạo link Link4m dẫn tới trang sinh key
    long_url = f"{BASE_URL}/generate?id={user_id}"
    link = create_link(long_url)

    if not link:
        bot.send_message(
            user_id,
            "❌ Không thể tạo link rút gọn. Vui lòng thử lại sau."
        )
        return

    bot.send_message(
        user_id,
        f"👉 Vượt link để nhận key:\n\n{link}"
    )


print("🤖 Bot đang chạy...")
bot.infinity_polling(skip_pending=True)
