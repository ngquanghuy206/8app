
import requests, platform, random, time, sys

def get_os_info():
    return platform.system() + " " + platform.release()

def get_headers(referer, os_info):
    return {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': referer,
        'sec-ch-ua': f'"{os_info}";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': f'"{os_info}"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': f'Mozilla/5.0 ({os_info}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

def send_question(username, question, headers):
    data = {'username': username, 'question': question, 'deviceId': '6279391f-0ac5-417e-8274-5711f9adf80a'}
    response = requests.post('https://ngl.link/api/submit', headers=headers, data=data)
    return response.text

def read_questions_from_file(file_cauhoi):
    with open(file_cauhoi, 'r', encoding='utf-8') as file:
        questions = file.readlines()
    return [q.strip() for q in questions if q.strip()]

def read_full_content_from_file(file_cauhoi):
    with open(file_cauhoi, 'r', encoding='utf-8') as file:
        return file.read().strip()

while True:
    print("Tool Treo Nglink By Nguyễn Quang Huy")
    print("Chọn chức năng:")
    print("1. Treo Nhây")
    print("2. Treo Ngôn")
    print("Zalo: 0904562214")
    mode = input("Nhập lựa chọn (1 hoặc 2): ")

    username = input("Nhập Username: ")
    file_cauhoi = input("Nhập File Chứa Nội Dung: ")

    os_info = get_os_info()
    referer = f"https://ngl.link/{username}"
    headers = get_headers(referer, os_info)

    if mode == "1":
        list_of_questions = read_questions_from_file(file_cauhoi)
        random.shuffle(list_of_questions)
        
        while list_of_questions:
            so_lan_lap = int(input("Nhập Số Lần Bạn Muốn Lặp: "))
            for _ in range(so_lan_lap):
                if not list_of_questions:
                    print("Đã Nhây Thành Công")
                    sys.exit()
                question = list_of_questions.pop()
                response = send_question(username, question, headers)
                print(f"Đã gửi: '{question}' đến {username}.")
    elif mode == "2":
        full_content = read_full_content_from_file(file_cauhoi)
        so_lan_lap = int(input("Nhập Số Lần Bạn Muốn Lặp: "))
        for _ in range(so_lan_lap):
            response = send_question(username, full_content, headers)
            print(f"Đã treo nội dung trong file đến {username}.")
    else:
        print("Lựa chọn không hợp lệ! Vui lòng chọn 1 hoặc 2.")
        continue