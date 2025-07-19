import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def load_accounts():
    accounts = []
    with open("accounts.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                email, pw = line.strip().split("|")
                accounts.append((email.strip(), pw.strip()))
    return accounts

def load_random_line(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return random.choice(lines) if lines else "No Title"

def load_full_content(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_random_image(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    return os.path.join(folder, random.choice(files))

def send_email(email, app_pass, subject, body, to_email, image_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain", "utf-8"))

    if image_path:
        with open(image_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(image_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
            msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, app_pass)
            server.send_message(msg)
        print(f"[✅] Gửi thành công từ {email} đến {to_email}")
    except Exception as e:
        print(f"[❌] Lỗi khi gửi từ {email}: {e}")

def spam_loop(mode):
    accounts = load_accounts()
    if not accounts:
        print("Không tìm thấy tài khoản trong accounts.txt")
        return

    to_email = input("📨 Nhập email người nhận: ").strip()
    delay = float(input("⏱ Nhập delay giữa các lần gửi (giây): ").strip())

    index = 0  # bắt đầu từ dòng đầu

    while True:
        email, pw = accounts[index]
        subject = load_random_line("tieude.txt")

        if mode == "1":
            body = load_random_line("nhaychet.txt")
            send_email(email, pw, subject, body, to_email)

        elif mode == "2":
            body = load_full_content("moi.txt")
            send_email(email, pw, subject, body, to_email)

        elif mode == "3":
            body = load_full_content("moi.txt")
            img_path = load_random_image("ảnh")
            if not img_path:
                print("❌ Không tìm thấy ảnh trong thư mục 'ảnh'")
                return
            send_email(email, pw, subject, body, to_email, image_path=img_path)

        index = (index + 1) % len(accounts)  # chuyển sang acc kế tiếp, lặp lại
        time.sleep(delay)

def main():
    print("=== TOOL TREO GMAIL BY NGUYỄN QUANG HUY ===")
    print("1. Nhây Gmail (ngẫu nhiên từng dòng từ nhaychet.txt)")
    print("2. Treo Gmail (gửi toàn bộ nội dung từ noidung.txt)")
    print("3. Treo Ảnh Gmail (gửi nội dung + 1 ảnh ngẫu nhiên)")
    mode = input("👉 Nhập lựa chọn (1, 2 hoặc 3): ").strip()

    if mode not in ["1", "2", "3"]:
        print("❌ Lựa chọn không hợp lệ.")
        return

    try:
        spam_loop(mode)
    except KeyboardInterrupt:
        print("\n[🛑] Đã dừng spam.")

if __name__ == "__main__":
    main()