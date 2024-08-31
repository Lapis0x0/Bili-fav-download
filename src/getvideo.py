import requests
import json
import re
import os
import time
from dotenv import load_dotenv

def get_fav_videos(media_id, sessdata):
    videos = []
    page = 1
    while True:
        url = 'https://api.bilibili.com/x/v3/fav/resource/list'
        params = {
            'media_id': media_id,
            'pn': page,
            'ps': 20,
            'platform': 'web'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'Cookie': f'SESSDATA={sessdata}'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            
            if 'data' not in response_json:
                error_msg = response_json.get('message', '未知错误')
                raise ValueError(f"API 返回错误: {error_msg}")
            
            data = response_json['data']
            
            if 'medias' not in data or not data['medias']:
                break
            
            for item in data['medias']:
                videos.append({
                    'bvid': item['bvid'],
                    'title': item['title'],
                    'link': f"https://www.bilibili.com/video/{item['bvid']}"
                })
            
            if not data.get('has_more', False):
                break
            
            page += 1
            time.sleep(1)  # 在每次请求之间添加1秒的延迟
        
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            print(f"响应内容: {response.text}")
            raise
    
    return videos

def save_videos_to_json(videos, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)

def extract_media_id(fav_url):
    pattern = r'fid=(\d+)'
    match = re.search(pattern, fav_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("无法从链接中提取media_id")

# 主程序
if __name__ == "__main__":
    load_dotenv()
    
    sessdata = os.getenv('SESSDATA')
    if not sessdata:
        print("错误: 未找到SESSDATA。请确保在.env文件中设置了SESSDATA。")
        exit(1)

    fav_url = input("请输入收藏夹链接: ")

    try:
        media_id = extract_media_id(fav_url)
        fav_videos = get_fav_videos(media_id, sessdata)

        if not fav_videos:
            print("警告: 未找到任何视频。请检查收藏夹链接是否正确,以及是否有权限访问该收藏夹。")
        else:
            json_filename = 'fav_videos.json'
            save_videos_to_json(fav_videos, json_filename)
            print(f"视频信息已保存到 {json_filename}")

    except ValueError as e:
        print(f"错误: {e}")
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
        import traceback
        traceback.print_exc()
