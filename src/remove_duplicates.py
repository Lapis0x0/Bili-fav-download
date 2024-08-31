import json
import os

def remove_duplicates():
    # 清空 downloads 文件夹中的 .m4s 和 .jpg 文件
    downloads_dir = 'downloads'
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.m4s') or filename.endswith('.jpg'):
            file_path = os.path.join(downloads_dir, filename)
            os.remove(file_path)
    print("已清空 downloads 文件夹中的 .m4s 和 .jpg 文件")

    # 读取 fav_video.json 文件
    with open('fav_videos.json', 'r', encoding='utf-8') as f:
        fav_videos = json.load(f)
    
    # 获取 downloads 文件夹中的文件名列表
    downloaded_files = os.listdir(downloads_dir)
    
    # 创建一个新的列表来存储未下载的视频
    unique_videos = []
    
    for video in fav_videos:
        # 检查视频标题是否在已下载文件中
        if not any(video['title'] in file for file in downloaded_files):
            unique_videos.append(video)
    
    # 保存更新后的 json 文件
    with open('fav_videos.json', 'w', encoding='utf-8') as f:
        json.dump(unique_videos, f, ensure_ascii=False, indent=2)
    
    print(f"已从 {len(fav_videos)} 个视频中移除 {len(fav_videos) - len(unique_videos)} 个重复项。")

if __name__ == "__main__":
    remove_duplicates()