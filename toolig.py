import requests
import os
import time
import random
import threading
import logging
import datetime
from instagrapi import Client
from instagrapi.exceptions import RateLimitError, ClientError
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from colorama import Fore, Style
import pyfiglet

console = Console()

logging.basicConfig(
    filename='spam_tool_v5.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

stop_sending = False

def print_banner():
    ascii_banner = f"""{Fore.MAGENTA}
╭━╮╱╭╮╱╱╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮╱╭╮
┃┃╰╮┃┃╱╱╱┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃╱┃┃
┃╭╮╰╯┣━━╮┃┃╱┃┣╮╭┳━━┳━╮╭━━╮┃╰━╯┣╮╭┳╮╱╭╮
┃┃╰╮┃┃╭╮┃┃┃╱┃┃┃┃┃╭╮┃╭╮┫╭╮┃┃╭━╮┃┃┃┃┃╱┃┃
┃┃╱┃┃┃╰╯┃┃╰━╯┃╰╯┃╭╮┃┃┃┃╰╯┃┃┃╱┃┃╰╯┃╰━╯┃
╰╯╱╰━┻━╮┃╰━━╮┣━━┻╯╰┻╯╰┻━╮┃╰╯╱╰┻━━┻━╮╭╯
╱╱╱╱╱╭━╯┃╱╱╱╰╯╱╱╱╱╱╱╱╱╱╭━╯┃╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╰━━╯╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯╱╱╱╱╱╱╱╱╰━━╯
{Style.RESET_ALL}"""
    name_banner = pyfiglet.figlet_format("Ng Quang Huy")
    current_time = datetime.datetime.now().strftime("%I:%M %p, %d/%m/%Y")
    tool_info = (
        f"Tool v5 - Chế độ: Hoạt động\n"
        f"Admin: Facebook (https://www.facebook.com/profile.php?id=100077964955704), Zalo (0904562214)\n"
        f"Ngày update: 16/05/2025\n"
        f"Ngày giờ hiện tại: {current_time}"
    )
    banner_content = f"{ascii_banner}\n{name_banner}\n{tool_info}"
    console.print(Panel(
        banner_content,
        style="magenta",
        title="Tool Treo Instagram v5 - Ng Quang Huy",
        border_style="green",
        title_align="center"
    ))

def login_tool():
    max_attempts = 5
    attempts = 0
    correct_password = "nghuy2006"
    
    ascii_banner = f"""{Fore.MAGENTA}
╭━╮╱╭╮╱╱╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮╱╭╮
┃┃╰╮┃┃╱╱╱┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃╱┃┃
┃╭╮╰╯┣━━╮┃┃╱┃┣╮╭┳━━┳━╮╭━━╮┃╰━╯┣╮╭┳╮╱╭╮
┃┃╰╮┃┃╭╮┃┃┃╱┃┃┃┃┃╭╮┃╭╮┫╭╮┃┃╭━╮┃┃┃┃┃╱┃┃
┃┃╱┃┃┃╰╯┃┃╰━╯┃╰╯┃╭╮┃┃┃┃╰╯┃┃┃╱┃┃╰╯┃╰━╯┃
╰╯╱╰━┻━╮┃╰━━╮┣━━┻╯╰┻╯╰┻━╮┃╰╯╱╰┻━━┻━╮╭╯
╱╱╱╱╱╭━╯┃╱╱╱╰╯╱╱╱╱╱╱╱╱╱╭━╯┃╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╰━━╯╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯╱╱╱╱╱╱╱╱╰━━╯
{Style.RESET_ALL}"""
    name_banner = pyfiglet.figlet_format("Ng Quang Huy")
    current_time = datetime.datetime.now().strftime("%I:%M %p, %d/%m/%Y")
    tool_info = (
        f"Tool v5 - Chế độ: Hoạt động\n"
        f"Ngày update: 16/05/2025\n"
        f"Ngày giờ hiện tại: {current_time}"
    )
    banner_content = f"{ascii_banner}\n{name_banner}\n{tool_info}"
    
    console.print(Panel(
        banner_content,
        style="magenta",
        title="Đăng Nhập Tool v5 - Ng Quang Huy",
        border_style="green",
        title_align="center"
    ))
    
    admin_table = Table(title="Thông Tin Admin", style="cyan", title_style="bold magenta")
    admin_table.add_column("Kênh", style="green")
    admin_table.add_column("Thông Tin", style="white")
    admin_table.add_row("Facebook", "https://www.facebook.com/profile.php?id=100077964955704")
    admin_table.add_row("Zalo", "0904562214")
    console.print(admin_table)
    
    while attempts < max_attempts:
        password = Prompt.ask("[yellow]Nhập mật khẩu[/yellow]", password=True)
        attempts += 1
        if password == correct_password:
            console.print(Panel("Đăng nhập thành công!", style="green", title="Thông Báo"))
            logging.info("Đăng nhập tool thành công.")
            return True
        remaining = max_attempts - attempts
        console.print(Panel(f"Mật khẩu sai! Còn {remaining} lần thử.", style="red", title="Lỗi"))
        logging.warning(f"Đăng nhập sai. Lần thử {attempts}/{max_attempts}.")
    
    console.print(Panel("Đã hết số lần thử. Thoát tool.", style="red", title="Lỗi"))
    logging.error("Hết số lần thử đăng nhập. Thoát tool.")
    return False

def get_keys_from_anotepad():
    try:
        url = 'https://vi.anotepad.com/notes/xts83gw9'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            note_content = soup.find('div', {'class': 'plaintext'})
            if note_content:
                keys = [line.strip() for line in note_content.get_text().strip().split('\n') if line.strip()]
                console.print(Panel(f"Đã lấy {len(keys)} key từ anotepad.", style="green", title="Thông Báo"))
                logging.info(f"Lấy được {len(keys)} key từ anotepad.")
                return keys
            else:
                console.print(Panel("Không tìm thấy nội dung ghi chú.", style="red", title="Lỗi"))
                logging.error("Không tìm thấy nội dung ghi chú.")
                return []
        else:
            console.print(Panel(f"Yêu cầu thất bại với mã trạng thái: {response.status_code}", style="red", title="Lỗi"))
            logging.error(f"Yêu cầu thất bại với mã trạng thái: {response.status_code}")
            return []
    except Exception as e:
        console.print(Panel(f"Lỗi khi lấy key: {e}", style="red", title="Lỗi"))
        logging.error(f"Lỗi khi lấy key: {e}")
        return []

def load_messages(file_path):
    try:
        if not os.path.exists(file_path):
            console.print(Panel(f"Không tìm thấy file: {file_path}", style="red", title="Lỗi"))
            logging.error(f"Không tìm thấy file: {file_path}")
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            messages = ["\n".join([line.strip() for line in f if line.strip()])]
        if not messages or not messages[0]:
            console.print(Panel("File tin nhắn rỗng.", style="red", title="Lỗi"))
            logging.error("File tin nhắn rỗng.")
            return []
        console.print(Panel(f"Đã tải tin nhắn từ {file_path}.", style="green", title="Thông Báo"))
        logging.info(f"Đã tải tin nhắn từ {file_path}.")
        return messages
    except Exception as e:
        console.print(Panel(f"Lỗi khi đọc file tin nhắn: {e}", style="red", title="Lỗi"))
        logging.error(f"Lỗi khi đọc file tin nhắn: {e}")
        return []

def login_client(username, password, session_file):
    cl = Client()
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(username, password)
            console.print(Panel(f"Đã tải session cho {username}.", style="green", title="Thông Báo"))
            logging.info(f"Đã tải session cho {username}.")
        else:
            cl.login(username, password)
            cl.dump_settings(session_file)
            console.print(Panel(f"Đăng nhập và lưu session cho {username}.", style="green", title="Thông Báo"))
            logging.info(f"Đăng nhập và lưu session cho {username}.")
        return cl
    except Exception as e:
        console.print(Panel(f"Đăng nhập thất bại cho {username}: {e}", style="red", title="Lỗi"))
        logging.error(f"Đăng nhập thất bại cho {username}: {e}")
        return None

def send_message(cl, thread_id, message, username, attempt=1, max_attempts=5):
    try:
        cl.direct_send(message, [], thread_ids=[thread_id])
        console.print(Panel(f"[{username}] -> Đã gửi đến {thread_id}: {message[:30]}...", style="green", title="Thành Công"))
        logging.info(f"[{username}] Gửi tin nhắn đến {thread_id}: {message[:30]}...")
        return True
    except RateLimitError:
        if attempt < max_attempts:
            wait_time = (2 ** attempt) + random.uniform(0.5, 1.5)
            console.print(Panel(f"Giới hạn tốc độ cho {username}. Thử lại sau {wait_time:.2f} giây...", style="yellow", title="Cảnh Báo"))
            logging.warning(f"Giới hạn tốc độ cho {username}. Thử lại sau {wait_time:.2f} giây.")
            time.sleep(wait_time)
            return send_message(cl, thread_id, message, username, attempt + 1, max_attempts)
        else:
            console.print(Panel(f"Đã đạt số lần thử tối đa cho {username} trên nhóm {thread_id}.", style="red", title="Lỗi"))
            logging.error(f"Đã đạt số lần thử tối đa cho {username} trên nhóm {thread_id}.")
            return False
    except ClientError as e:
        console.print(Panel(f"Lỗi khi gửi tin nhắn từ {username} đến {thread_id}: {e}", style="red", title="Lỗi"))
        logging.error(f"Lỗi khi gửi tin nhắn từ {username} đến {thread_id}: {e}")
        return False

def listen_for_stop():
    global stop_sending
    console.print(Panel("Nhấn 'q' và Enter để dừng gửi tin nhắn...", style="yellow", title="Hướng Dẫn"))
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            stop_sending = True
            console.print(Panel("Đang dừng gửi tin nhắn...", style="red", title="Thông Báo"))
            logging.info("Người dùng yêu cầu dừng gửi tin nhắn.")
            break

def main_menu():
    options = [
        "Tool Treo Ngôn",
        "Thoát Tool"
    ]
    table = Table(title="Menu Tool v5 - Ng Quang Huy", style="cyan", title_style="bold magenta")
    table.add_column("Lựa Chọn", style="green", justify="center")
    table.add_column("Chức Năng", style="white")
    for idx, opt in enumerate(options, 1):
        table.add_row(str(idx), opt)
    console.print(table)
    return Prompt.ask("[bold cyan]Nhập lựa chọn[/bold cyan]", choices=["1", "2"], default="1")

def input_accounts():
    while True:
        try:
            num_accs = int(Prompt.ask("[yellow]Nhập số lượng tài khoản[/yellow]"))
            if num_accs <= 0:
                console.print(Panel("Số lượng tài khoản phải là số dương.", style="red", title="Lỗi"))
                continue
            break
        except ValueError:
            console.print(Panel("Vui lòng nhập số hợp lệ.", style="red", title="Lỗi"))
    
    console.print(Panel(f"Nhập {num_accs} tài khoản (định dạng: username|password, mỗi dòng 1 tài khoản).", style="yellow", title="Hướng Dẫn"))
    accs = []
    for i in range(num_accs):
        while True:
            line = Prompt.ask(f"Tài khoản {i+1}")
            if "|" in line:
                accs.append(tuple(line.strip().split("|")))
                break
            else:
                console.print(Panel("Định dạng không hợp lệ. Sử dụng username|password.", style="red", title="Lỗi"))
    return accs

def input_group_ids():
    console.print(Panel("Nhập danh sách ID nhóm, cách nhau bằng dấu phẩy (VD: id1,id2,id3).", style="yellow", title="Hướng Dẫn"))
    while True:
        group_ids_input = Prompt.ask("->")
        group_ids = [id.strip() for id in group_ids_input.split(",") if id.strip()]
        valid = True
        for group_id in group_ids:
            if not group_id.isdigit():
                console.print(Panel(f"ID nhóm '{group_id}' phải là số.", style="red", title="Lỗi"))
                valid = False
                break
        if valid and group_ids:
            return group_ids
        elif not group_ids:
            console.print(Panel("Danh sách ID nhóm không được rỗng.", style="red", title="Lỗi"))
        else:
            console.print(Panel("Vui lòng nhập lại danh sách ID hợp lệ.", style="red", title="Lỗi"))

def input_parameters():
    msg_file = Prompt.ask("[yellow]Nhập đường dẫn file .txt chứa tin nhắn[/yellow]")
    while True:
        try:
            delay = float(Prompt.ask("[yellow]Nhập thời gian delay (giây)[/yellow]", default="1.2"))
            if delay < 0:
                console.print(Panel("Delay không thể âm.", style="red", title="Lỗi"))
                continue
            break
        except ValueError:
            console.print(Panel("Vui lòng nhập số hợp lệ.", style="red", title="Lỗi"))
    return msg_file, delay

def check_network():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        console.print(Panel("Không có kết nối mạng. Vui lòng kiểm tra!", style="red", title="Lỗi"))
        logging.error("Không có kết nối mạng.")
        return False

def main():
    global stop_sending
    stop_sending = False
    print_banner()
    if not check_network():
        return
    keys = get_keys_from_anotepad()
    if not keys:
        console.print(Panel("Không lấy được key bảo mật. Thoát chương trình.", style="red", title="Lỗi"))
        logging.error("Không lấy được key bảo mật. Thoát chương trình.")
        return
    while True:
        choice = main_menu()
        logging.info(f"Người dùng chọn tùy chọn: {choice}")
        if choice == "2":
            console.print(Panel("Cảm ơn đã sử dụng Tool v5 - Ng Quang Huy!", style="green", title="Thông Báo"))
            logging.info("Người dùng thoát công cụ.")
            break
        accs = input_accounts()
        if not accs:
            console.print(Panel("Không có tài khoản nào được nhập. Quay lại menu.", style="red", title="Lỗi"))
            logging.error("Không có tài khoản nào được nhập.")
            continue
        group_ids = input_group_ids()
        if not group_ids:
            console.print(Panel("Không có ID nhóm nào được nhập. Quay lại menu.", style="red", title="Lỗi"))
            logging.error("Không có ID nhóm nào được nhập.")
            continue
        msg_file, delay = input_parameters()
        messages = load_messages(msg_file)
        if not messages:
            console.print(Panel("Không tải được tin nhắn. Quay lại menu.", style="red", title="Lỗi"))
            logging.error("Không tải được tin nhắn.")
            continue
        advertisement = "Coder By Ng Quang Huy"
        clients = []
        for username, password in track(accs, description="Đăng nhập tài khoản...", console=console):
            session_file = f"session_{username}.json"
            console.print(Panel(f"Đang đăng nhập: {username}", style="cyan", title="Đăng Nhập"))
            cl = login_client(username, password, session_file)
            if cl:
                clients.append((cl, username))
            else:
                console.print(Panel(f"Bỏ qua {username} do đăng nhập thất bại.", style="red", title="Lỗi"))
        if not clients:
            console.print(Panel("Không có tài khoản hợp lệ nào. Quay lại menu.", style="red", title="Lỗi"))
            logging.error("Không có tài khoản hợp lệ nào.")
            continue
        table = Table(title="Tài Khoản Đang Hoạt Động", style="cyan", title_style="bold magenta")
        table.add_column("Tên Tài Khoản", style="green")
        for _, username in clients:
            table.add_row(username)
        console.print(table)
        stop_thread = threading.Thread(target=listen_for_stop)
        stop_thread.daemon = True
        stop_thread.start()
        cycle_count = 0
        message_count = 0
        while not stop_sending:
            cycle_count += 1
            console.print(Panel(f"Bắt đầu chu kỳ {cycle_count}", style="blue", title="Thông Báo"))
            logging.info(f"Bắt đầu chu kỳ {cycle_count}")
            for cl, username in track(clients, description="Xử lý tài khoản...", console=console):
                if stop_sending:
                    break
                for thread_id in group_ids:
                    if stop_sending:
                        break
                    if send_message(cl, thread_id, advertisement, username):
                        message_count += 1
                        time.sleep(delay)
                for thread_id in group_ids:
                    if stop_sending:
                        break
                    for msg in messages:
                        if stop_sending:
                            break
                        if send_message(cl, thread_id, msg, username):
                            message_count += 1
                            time.sleep(delay)
                        else:
                            console.print(Panel(f"Bỏ qua tin nhắn tiếp theo cho {username} do lỗi.", style="yellow", title="Cảnh Báo"))
                            break
            console.print(Panel(f"Chu kỳ {cycle_count} hoàn tất. Tổng tin nhắn gửi: {message_count}", style="green", title="Thông Báo"))
            logging.info(f"Chu kỳ {cycle_count} hoàn tất. Tổng tin nhắn gửi: {message_count}")
        if stop_sending:
            console.print(Panel(f"Đã dừng chương trình. Tổng tin nhắn gửi: {message_count}. Cảm ơn bạn đã sử dụng!", style="green", title="Thông Báo"))
            logging.info(f"Đã dừng chương trình. Tổng tin nhắn gửi: {message_count}")
            break

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        if login_tool():
            main()
        else:
            console.print(Panel("Không thể đăng nhập. Thoát chương trình.", style="red", title="Lỗi"))
    except KeyboardInterrupt:
        console.print(Panel("Chương trình bị gián đoạn bởi người dùng.", style="red", title="Lỗi"))
        logging.info("Chương trình bị gián đoạn bởi người dùng.")
        stop_sending = True
        