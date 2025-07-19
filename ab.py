import threading
import time
import re
import requests

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.id_user()
        self.fb_dtsg = None
        self.init_params()

    def id_user(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
        }
        try:
            response = requests.get('https://www.facebook.com', headers=headers)
            fb_dtsg_match = re.search(r'"token":"(.*?)"', response.text)
            if not fb_dtsg_match:
                response = requests.get('https://mbasic.facebook.com', headers=headers)
                fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
            if fb_dtsg_match:
                self.fb_dtsg = fb_dtsg_match.group(1)
            else:
                raise Exception("Không thể lấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi init: {str(e)}")

    def refresh_dtsg(self):
        try:
            self.init_params()
        except:
            pass

    def gui_tn(self, recipient_id, message):
        timestamp = int(time.time() * 1000)
        data = {
            'thread_fbid': recipient_id,
            'action_type': 'ma-type:user-generated-message',
            'body': message,
            'client': 'mercury',
            'author': f'fbid:{self.user_id}',
            'timestamp': timestamp,
            'source': 'source:chat:web',
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            '__user': self.user_id,
            '__a': '1',
            '__req': '1b',
            '__rev': '1015919737',
            'fb_dtsg': self.fb_dtsg
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'python-http/0.27.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'https://www.facebook.com/messages/t/{recipient_id}'
        }

        for attempt in range(3):
            try:
                res = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
                if res.status_code == 200:
                    return True
                else:
                    time.sleep(1)
                    self.refresh_dtsg()
                    data['fb_dtsg'] = self.fb_dtsg
            except:
                time.sleep(1)
                self.refresh_dtsg()
                data['fb_dtsg'] = self.fb_dtsg
        return False

def spam_thread(cookie, recipient_id, message, delay):
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        print(f"[!] Cookie lỗi: {e}")
        return
    while True:
        success = messenger.gui_tn(recipient_id, message)
        print(f"[{recipient_id}] {'Nikolai Gửi Thành Công' if success else '✗ Thất bại'} - {messenger.user_id}")
        time.sleep(delay)
        
def main():
    print(" TOOL MESSENGER SPAMMER - BY NG QUANG HUY")
    
    # Nhập đường dẫn file cookie
    print("=== Nhập đường dẫn file chứa cookie (mỗi dòng 1 cookie, ví dụ: cookies.txt) ===")
    cookie_file = input("File cookie: ").strip()
    cookies = []
    try:
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookies = [line.strip() for line in f if line.strip()]  # Đọc từng dòng, bỏ dòng trống
        if not cookies:
            print("[!] File cookie rỗng hoặc không hợp lệ")
            return
    except Exception as e:
        print(f"[!] Lỗi đọc file cookie: {e}")
        return

    print("\n=== Nhập ID Facebook (gõ 'done' để kết thúc) ===")
    ids = []
    while True:
        uid = input("ID: ").strip()
        if uid.lower() == "done":
            break
        if uid:
            ids.append(uid)

    # Nhập danh sách file tin nhắn
    print("\n=== Nhập đường dẫn file chứa tin nhắn (gõ 'done' để kết thúc, ví dụ: message1.txt) ===")
    message_files = []
    messages = []
    while True:
        path = input("File tin nhắn: ").strip()
        if path.lower() == "done":
            break
        if path:
            message_files.append(path)
    # Đọc nội dung từ các file tin nhắn
    for path in message_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                messages.append(f.read())
        except Exception as e:
            print(f"[!] Lỗi đọc file tin nhắn {path}: {e}")
            return
    if not messages:
        print("[!] Không có file tin nhắn nào hợp lệ")
        return

    try:
        delay = int(input("Delay (giây): ").strip())
    except ValueError:
        print("[!] Delay không hợp lệ")
        return

    print(f"\n➡️ Bắt đầu gửi... (tổng {len(cookies)} cookie x {len(ids)} id x {len(messages)} tin nhắn)")
    for i, cookie in enumerate(cookies):
        # Chọn nội dung tin nhắn theo thứ tự vòng tròn: cookie 1 -> file 1, cookie 2 -> file 2, cookie 3 -> file 1,...
        message = messages[i % len(messages)]
        for recipient_id in ids:
            threading.Thread(target=spam_thread, args=(cookie, recipient_id, message, delay), daemon=True).start()

    input("\nNhấn Enter để thoát...\n")

if __name__ == "__main__":
    main()