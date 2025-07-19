import requests
import re
import time
import os
import random
import pyfiglet
from colorama import Fore, init

os.system('cls' if os.name == 'nt' else 'clear')

banner = pyfiglet.figlet_format("OSUTSUKI", font="big")
print(banner)

COLORS = {
    "luc": "\033[1;32m",
    "trang": "\033[1;37m",
    "do": "\033[1;31m",
    "vang": "\033[0;93m",
    "hong": "\033[1;35m",
    "xduong": "\033[1;34m",
    "xnhac": "\033[1;36m",
}

init(autoreset=True)

a = " \033[1;97m[\033[1;31mNGQUANGHUY\033[1;97m] => "

def visual_delay(t):
    start_time = time.time()
    while time.time() - start_time < t:
        remaining_time = int(t - (time.time() - start_time))
        for step in ["LOADING ", "LOADING.", "LOADING..", "LOADING..."]:
            print(f"\r\033[1;31m[\033[1;33mTVK\033[1;31m] \033[1;92m ~> {step} \033[0;31m | {remaining_time} | \r", end='')
            time.sleep(0.00025)
    print("\r\033[1;95m    NgQuangHuy\033[1;97m                         \r", end='')

def check_login_facebook(cookie):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": cookie
        }
        response = requests.get("https://m.facebook.com/", headers=headers).text
        name_match = re.search(r'<title>(.*?)</title>', response)

        if name_match:
            name = name_match.group(1).replace(" | Facebook", "").strip()
            return name, None, None, "Unknown"
        else:
            print("Không tìm thấy thông tin tên người dùng.")
            return False
    except Exception as e:
        print(f"Error during login check: {e}")
        return False

def get_token(cookie):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.78", "Chromium";v="125.0.6422.78", "Not.A/Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'viewport-width': '868',
    }

    try:
        response = requests.get('https://business.facebook.com/content_management', headers=headers).text
        token = response.split('[{"accessToken":"')[1].split('","')[0]
        return token
    except Exception as e:
        print(f'\033[1;31mGet Token Thất Bại !')
        return None

def auto_cmt_moi_ne(access_token, idpost, mess, cookie):
    data = {
        "access_token": access_token,
        "message": mess
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A750GN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.106 Mobile Safari/537.36",
        "Cookie": cookie
    }

    response = requests.post(f"https://graph.facebook.com/{idpost}/comments", data=data, headers=headers)
    res = response.text

    if "An unknown error occurred" in res or '"fbtrace_id":' in res:
        return "1"

    result = response.json()

    if "error" in result:
        return {"status": "die", "msg": result["error"]["message"]}
    else:
        return result

def load_cookies(file_path):
    try:
        with open(file_path, 'r') as file:
            cookies = file.readlines()
            cookies = [cookie.strip() for cookie in cookies if cookie.strip()]
        return cookies
    except Exception as e:
        print(f"\033[1;92m An error occurred while reading the cookie file: {e}")
        return []

def get_random_line_and_count_from_file(file_path, empty_file_message):
    if not os.path.exists(file_path):
        return "Tệp không tồn tại.", 0
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    if not lines:
        return empty_file_message, 0
    return lines, len(lines)

file_path_comment = "chaychet.txt"

def main():
    comments, comment_count = get_random_line_and_count_from_file(file_path_comment, "Không có bình luận nào trong tệp.")
    cookies = load_cookies("cucki.txt")
    if not cookies:
        print("\033[1;92m No cookies loaded.")
        return
    print(f"{a}\033[1;92mSố lượng cookie đã tải: \033[1;33m{len(cookies)}")
    print(f"{a}\033[1;92mSố lượng comment đã tải: \033[1;33m{comment_count}")
    idpost = int(input(f"{a}\033[1;92mID Post:\033[1;33m "))
    dem = int(input(f"{a}\033[1;92mNhập Số Lần CMT:\033[1;33m "))
    delay_min = float(input(f"{a}\033[1;92mNhập Thời Gian Chờ Tối Thiểu (Giây):\033[1;33m "))
    delay_max = float(input(f"{a}\033[1;92mNhập Thời Gian Chờ Tối Đa (Giây):\033[1;33m "))
    tagbb = input(f"{a}\033[1;92mComment Tag (Y/N):\033[1;33m ").strip().upper()
    chongspam = input(f"{a}\033[1;92mKích Hoạt Chống Spam (Y/N):\033[1;33m ").strip().upper()
    switch_after = int(input(f"{a}\033[1;92mĐổi Cookie Sau Bao Nhiêu Lần CMT:\033[1;33m "))
    idbb = int(input(f"{a}\033[1;92mNhập ID Cần Tag:\033[1;33m ")) if tagbb == "Y" else None
    print("\n\033[1;31m══════════════════════\033[1;92mRunning\033[1;31m-\033[1;92mTools\033[1;31m══════════════════════\n")
    current_cookie_index = 0
    cookie_logged_in = False
    for i in range(dem):
        if i % switch_after == 0 and i != 0:
            current_cookie_index = (current_cookie_index + 1) % len(cookies)
            cookie_logged_in = False
            time.sleep(2)

        cookie = cookies[current_cookie_index] 
        try:
            if not cookie_logged_in:
                login_info = check_login_facebook(cookie) 
                if login_info:
                    name, fb_dtsg, jazoest, idacc = login_info
                    print("\033[1;31m─────────────────────────────────────────────────────────")
                    print(f"   \033[0;93mFaceBook: \033[1;35m{name} \033[0;93m</> Uid: \033[1;35m{idacc}")
                    print("\033[1;31m─────────────────────────────────────────────────────────")
                    cookie_logged_in = True
                else:
                    print(f" \033[1;97m[\033[1;31m+_+\033[1;97m] => \033[1;31mLogin thất bại với cookie {current_cookie_index + 1}. Chuyển sang cookie tiếp theo.")
                    continue

            comment_text = random.choice(comments)
            if comment_text is not None:
                noidung = f'{comment_text}'
                if idbb:
                    noidung += f' @[{idbb}:0]'
                access_token = get_token(cookie)
                if access_token:
                    response = auto_cmt_moi_ne(access_token, idpost, noidung, cookie)

                    if response == "1":
                        print("\033[1;31mĐã xảy ra lỗi khi đăng bình luận.")
                    else:
                        print(f"[{i+1}] {COLORS['luc']}Comment {COLORS['do']}| {COLORS['vang']}{response.get('id')} {COLORS['do']}| {COLORS['hong']}{noidung} | {COLORS['xnhac']}Thành Công")
                        delay = random.uniform(delay_min, delay_max)
                        visual_delay(delay)
                        if i + 1 == dem:
                            print("\033[1;31mĐã đạt được số lần cmt đã nhập. Dừng spam.")
                            break
                else:
                    print("Get token thất bại")
            else:
                print("\033[1;31mKhông thể phân tích bình luận.")
        except Exception as e:
            print(f"An error occurred: {e}")
            break

main()