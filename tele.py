import telebot
import threading
import time
import re
import os

# Lớp để quản lý trạng thái của từng bot
class BotState:
    def __init__(self, admin_id):
        self.ADMIN_ID = admin_id
        self.allowed_users = set()
        self.treo_list = {}
        self.treo_threads = {}
        self.treo_anh_list = {}

# Danh sách các trạng thái bot
bot_states = {}

# Nhập token ban đầu
TOKENS = input("Nhập Token Bot:").strip().split(',')
bots = [telebot.TeleBot(token.strip()) for token in TOKENS]

while True:
    try:
        initial_admin_id = int(input("ID Admin: ").strip())
        break
    except ValueError:
        print("❌ ID Admin phải là số. Vui lòng nhập lại!")

# Gán trạng thái ban đầu cho các bot
for bot in bots:
    bot_states[bot.token] = BotState(initial_admin_id)

def is_authorized(bot, user_id):
    return user_id == bot_states[bot.token].ADMIN_ID or user_id in bot_states[bot.token].allowed_users

def read_txt_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def send_spam_image(bot, chat_id, file_name, delay, image_name, user_id):
    content = read_txt_file(file_name)
    if not content:
        bot.send_message(user_id, f"❌ Không tìm thấy hoặc file rỗng: `{file_name}`", parse_mode="Markdown")
        return

    if not os.path.exists(image_name):
        bot.send_message(user_id, f"❌ Không tìm thấy ảnh: `{image_name}`", parse_mode="Markdown")
        return

    while chat_id in bot_states[bot.token].treo_list.get(user_id, []):
        try:
            with open(image_name, 'rb') as img:
                bot.send_photo(chat_id, img, caption=content)
            print(f"✅ Đã gửi ảnh `{image_name}` vào nhóm {chat_id}")
        except Exception as e:
            if "429" in str(e):
                retry_after = int(re.search(r"retry after (\d+)", str(e)).group(1))
                print(f"❌ Lỗi 429! Đợi {retry_after} giây.")
                time.sleep(retry_after)
            else:
                print(f"❌ Lỗi không xác định: {e}")
        time.sleep(delay)

def send_spam_messages(bot, chat_id, file_name, delay, user_id):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read().strip()

        while chat_id in bot_states[bot.token].treo_list.get(user_id, []):
            try:
                bot.send_message(chat_id, content)
                print(f"✅ Đã gửi tin nhắn vào nhóm {chat_id}")
            except Exception as e:
                if "429" in str(e):
                    retry_after = int(re.search(r"retry after (\d+)", str(e)).group(1))
                    print(f"❌ Lỗi 429! Đợi {retry_after} giây.")
                    time.sleep(retry_after)
                else:
                    print(f"❌ Lỗi không xác định: {e}")
            time.sleep(delay)

    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {file_name}")
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")

def setup_handlers(bot):
    @bot.message_handler(commands=['treo'])
    def treo_message(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        match = re.findall(r'(-?\d+)\s+(\S+)\s+(\d+)', message.text)
        if not match:
            return bot.reply_to(message, "⚠️ Sai cú pháp!\nVí dụ: `/treo -1001234567890 noidung.txt 5`", parse_mode="Markdown")

        chat_id, file_name, delay = match[0]
        delay = int(delay)

        if message.from_user.id not in bot_states[bot.token].treo_list:
            bot_states[bot.token].treo_list[message.from_user.id] = []

        if chat_id not in bot_states[bot.token].treo_list[message.from_user.id]:
            bot_states[bot.token].treo_list[message.from_user.id].append(chat_id)

        thread = threading.Thread(target=send_spam_messages, args=(bot, chat_id, file_name, delay, message.from_user.id))
        thread.daemon = True
        thread.start()

        bot_states[bot.token].treo_threads[chat_id] = thread
        bot.reply_to(message, f"✅ Đã bắt đầu gửi tin từ file `{file_name}` vào nhóm `{chat_id}`", parse_mode="Markdown")

    @bot.message_handler(commands=['stoptreo'])
    def stop_treo(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ Sai cú pháp!\nVí dụ: `/stoptreo -1001234567890`", parse_mode="Markdown")

        chat_id = args[1]

        if message.from_user.id in bot_states[bot.token].treo_list and chat_id in bot_states[bot.token].treo_list[message.from_user.id]:
            bot_states[bot.token].treo_list[message.from_user.id].remove(chat_id)
            bot.reply_to(message, f"✅ Đã dừng treo {chat_id}")
        else:
            bot.reply_to(message, "⚠️ Bạn không có tab treo nào với ID này!")

    @bot.message_handler(commands=['tabtreo'])
    def list_treo(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        if message.from_user.id not in bot_states[bot.token].treo_list or not bot_states[bot.token].treo_list[message.from_user.id]:
            return bot.reply_to(message, "📋 Bạn không có tab treo nào đang hoạt động.")

        treo_info = "\n".join(f"- {group}" for group in bot_states[bot.token].treo_list[message.from_user.id])
        bot.reply_to(message, f"📋 Danh sách tab treo của bạn:\n{treo_info}", parse_mode="Markdown")

    @bot.message_handler(commands=['id'])
    def send_user_id(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        if message.reply_to_message:
            user = message.reply_to_message.from_user
            bot.reply_to(message, f"🆔 ID của {user.first_name}: {user.id}", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"🆔 ID của bạn: {message.from_user.id}", parse_mode="Markdown")

    @bot.message_handler(commands=['idgroup'])
    def send_group_id(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        if message.chat.type in ['group', 'supergroup']:
            bot.reply_to(message, f"{message.chat.id}", parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ Lệnh này chỉ hoạt động trong nhóm!")

    @bot.message_handler(commands=['menu'])
    def show_menu(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        menu_text = """📜 Danh sách lệnh bot Dzi × Void:

/treo <idgroup> <file.txt> <delay> - Treo tin nhắn
/stoptreo <idgroup> - Dừng treo
/treoanh <idgroup> <file.txt> <delay> <anh.jpg> - Treo ngôn kèm ảnh
/stoptreoanh <idgroup> - Dừng treo ngôn ảnh
/tabtreo - Xem các tab treo
/id - Xem ID Telegram
/idgroup - Xem ID nhóm
/menu - Hiển thị danh sách lệnh
/add <id> - Thêm người dùng vào danh sách
/xoa <id> - Xóa người dùng khỏi danh sách
/list - Xem danh sách người dùng
/log <token> <idadmin> - Log thêm acc bot"""
        bot.reply_to(message, menu_text, parse_mode="Markdown")

    @bot.message_handler(commands=['add'])
    def add_user(message):
        if message.from_user.id != bot_states[bot.token].ADMIN_ID:
            return bot.reply_to(message, "❌ Bạn không phải admin!")

        try:
            user_id = int(message.text.split()[1])
            bot_states[bot.token].allowed_users.add(user_id)
            bot.reply_to(message, f"✅ Đã thêm {user_id} vào danh sách.")
        except (IndexError, ValueError):
            bot.reply_to(message, "⚠️ Vui lòng nhập ID hợp lệ.\nVí dụ: `/add 123456789`")

    @bot.message_handler(commands=['xoa'])
    def remove_user(message):
        if message.from_user.id != bot_states[bot.token].ADMIN_ID:
            return bot.reply_to(message, "❌ Bạn không phải admin!")

        try:
            user_id = int(message.text.split()[1])
            bot_states[bot.token].allowed_users.discard(user_id)
            bot.reply_to(message, f"✅ Đã xóa {user_id} khỏi danh sách.")
        except (IndexError, ValueError):
            bot.reply_to(message, "⚠️ Vui lòng nhập ID hợp lệ.\nVí dụ: `/xoa 123456789`")

    @bot.message_handler(commands=['list'])
    def list_users(message):
        if message.from_user.id != bot_states[bot.token].ADMIN_ID:
            return bot.reply_to(message, "❌ Bạn không phải admin!")

        if bot_states[bot.token].allowed_users:
            user_list = "\n".join(f"- {uid}" for uid in bot_states[bot.token].allowed_users)
            bot.reply_to(message, f"📋 Danh sách người dùng:\n{user_list}", parse_mode="Markdown")
        else:
            bot.reply_to(message, "📋 Không có ai trong danh sách.")

    @bot.message_handler(commands=['treoanh'])
    def treo_anh(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        match = re.findall(r'(-?\d+)\s+(\S+)\s+(\d+)\s+(\S+)', message.text)
        if not match:
            return bot.reply_to(message, "⚠️ Sai cú pháp!\nVí dụ: `/treoanh -1001234567890 noidung.txt 5 anh.jpg`", parse_mode="Markdown")

        chat_id, file_name, delay, image_name = match[0]
        delay = int(delay)

        if message.from_user.id not in bot_states[bot.token].treo_list:
            bot_states[bot.token].treo_list[message.from_user.id] = []

        if chat_id not in bot_states[bot.token].treo_list[message.from_user.id]:
            bot_states[bot.token].treo_list[message.from_user.id].append(chat_id)

        thread = threading.Thread(target=send_spam_image, args=(bot, chat_id, file_name, delay, image_name, message.from_user.id))
        thread.daemon = True
        thread.start()

        bot_states[bot.token].treo_threads[chat_id] = thread
        bot.reply_to(message, f"✅ Đã bắt đầu gửi `{file_name}` kèm ảnh `{image_name}` vào `{chat_id}`", parse_mode="Markdown")

    @bot.message_handler(commands=['stoptreoanh'])
    def stop_treo_anh(message):
        if not is_authorized(bot, message.from_user.id):
            return bot.reply_to(message, "❌ Bạn không có quyền sử dụng bot!")

        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ Sai cú pháp!\nVí dụ: `/stoptreoanh -1001234567890`", parse_mode="Markdown")

        chat_id = args[1]

        if message.from_user.id in bot_states[bot.token].treo_anh_list and chat_id in bot_states[bot.token].treo_anh_list[message.from_user.id]:
            bot_states[bot.token].treo_anh_list[message.from_user.id].remove(chat_id)
            bot.reply_to(message, f"✅ Đã dừng treo ảnh vào nhóm `{chat_id}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ Bạn không có tab treo ảnh nào với ID này!")

    @bot.message_handler(commands=['log'])
    def log_bot(message):
        if message.from_user.id != bot_states[bot.token].ADMIN_ID:
            return bot.reply_to(message, "❌ Bạn không phải admin!")

        args = message.text.split()
        if len(args) < 3:
            return bot.reply_to(message, "⚠️ Sai cú pháp!\nVí dụ: `/log <token> <admin_id>`", parse_mode="Markdown")

        token = args[1]
        try:
            admin_id = int(args[2])
        except ValueError:
            return bot.reply_to(message, "❌ ID Admin phải là số!")

        try:
            new_bot = telebot.TeleBot(token)
            bot_states[token] = BotState(admin_id)  # Tạo trạng thái mới cho bot
            threading.Thread(target=run_bot, args=(new_bot,)).start()
            bot.reply_to(message, f"✅ Bot mới với admin `{admin_id}` đã khởi chạy!", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi khi khởi chạy bot: {e}", parse_mode="Markdown")

def run_bot(bot):
    setup_handlers(bot)
    print(f"✅ Bot {bot.token[:10]}... đang chạy")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

# Khởi động các bot ban đầu
threads = [threading.Thread(target=run_bot, args=(bot,)) for bot in bots]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()