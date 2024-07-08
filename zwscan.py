import json
import requests
import argparse
import hashlib

ascii_art = """
  _  ___              _______                   
 | |/ / |            |__   __|                  
 | ' /| |__   __ _ _ __ | | ___  __ _ _ __ ___  
 |  < | '_ \ / _` | '_ \| |/ _ \/ _` | '_ ` _ \ 
 | . \| | | | (_| | | | | |  __/ (_| | | | | | |
 |_|\_\_| |_|\__,_|_| |_|_|\___|\__,_|_| |_| |_|
                                                
                                                
"""

def load_fingerprints(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['fingerprint']

def calculate_icon_hash(content):
    # 这里是一个示例函数，你需要根据实际情况实现
    # 假设我们计算内容的MD5哈希值作为icon_hash
    hash_object = hashlib.md5(content.encode())
    return hash_object.hexdigest()

def check_fingerprint(url, fingerprint):
    cms = fingerprint['cms']
    method = fingerprint['method']
    location = fingerprint['location']
    keywords = fingerprint['keyword']

    try:
        response = requests.get(url)
        content = ""
        if location == 'body':
            content = response.text
        elif location == 'header':
            content = str(response.headers)
        elif location == 'title':
            if '<title>' in response.text and '</title>' in response.text:
                content = response.text.split('<title>')[1].split('</title>')[0]
            else:
                content = ""

        if method == 'keyword':
            for keyword in keywords:
                if keyword in content:
                    return f"{cms} 指纹匹配成功: {keyword}"
        elif method == 'icon_hash':
            # 计算icon_hash
            icon_hash = calculate_icon_hash(content)
            if icon_hash in keywords:
                return f"{cms} 指纹匹配成功: {icon_hash}"
        # 其他方法可以在这里添加
    except Exception as e:
        return f"Error: {e}"

    return None

def main():
    print(ascii_art)  # 打印ASCII艺术图标

    parser = argparse.ArgumentParser(description="指纹检测脚本")
    parser.add_argument('-u', '--url', required=True, help='目标URL')
    args = parser.parse_args()

    url = args.url

    # 加载指纹数据
    fingerprints = load_fingerprints('zw.json')

    # 检查所有指纹
    matched = False
    for fingerprint in fingerprints:
        result = check_fingerprint(url, fingerprint)
        if result:
            print(result)
            matched = True

    if not matched:
        print("未检测出指纹")

if __name__ == "__main__":
    main()
