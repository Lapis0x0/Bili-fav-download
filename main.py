import os
import json
from dotenv import load_dotenv
from src.getvideo import extract_media_id, get_fav_videos, save_videos_to_json
from src.remove_duplicates import remove_duplicates
from src.download import get_video_quality, get_download_type, download_video

def main():
    load_dotenv()
    
    # 检查downloads文件夹是否存在，如果不存在则创建
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        print("已创建downloads文件夹")
    else:
        print("downloads文件夹已存在")
    
    sessdata = os.getenv('SESSDATA')
    if not sessdata:
        print("错误: 未找到SESSDATA。请确保在.env文件中设置了SESSDATA。")
        return

    json_filename = 'fav_videos.json'
    output_dir = 'downloads'

    # 检查是否存在 JSON 文件
    if os.path.exists(json_filename):
        use_existing = input("检测到已存在的视频列表文件。是否继续上次的下载？(y/n): ").lower()
        if use_existing == 'y':
            with open(json_filename, 'r', encoding='utf-8') as f:
                videos_to_download = json.load(f)
            print("将继续上次的下载任务。")
        else:
            videos_to_download = None
    else:
        videos_to_download = None

    if videos_to_download is None:
        # 询问用户下载类型
        download_choice = input("请选择下载类型 (1: 单个视频, 2: 收藏夹): ")

        # 获取用户选择的下载类型（视频或音频）
        download_type = get_download_type()

        # 获取用户选择的视频质量
        quality = get_video_quality() if download_type == "1" else None

        if download_choice == "1":
            # 下载单个视频
            video_url = input("请输入视频链接: ")
            download_video(video_url, output_dir, sessdata, quality, download_type)
            print("视频下载完成")
            return
        elif download_choice == "2":
            # 下载收藏夹
            fav_url = input("请输入收藏夹链接: ")
            try:
                media_id = extract_media_id(fav_url)
                fav_videos = get_fav_videos(media_id, sessdata)
                save_videos_to_json(fav_videos, json_filename)
                print(f"视频信息已保存到 {json_filename}")
                remove_duplicates()
                print("已完成视频去重操作")
                with open(json_filename, 'r', encoding='utf-8') as f:
                    videos_to_download = json.load(f)
            except ValueError as e:
                print(f"错误: {e}")
                return
            except Exception as e:
                print(f"发生未知错误: {e}")
                import traceback
                traceback.print_exc()
                return
        else:
            print("无效的选择")
            return
    
    # 获取用户选择的下载类型（视频或音频）
    download_type = get_download_type()

    # 获取用户选择的视频质量
    quality = get_video_quality() if download_type == "1" else None

    if not videos_to_download:
        print("所有视频已下载，无需进行新的下载。")
        return

    # 下载视频
    for video in videos_to_download:
        download_video(video['link'], output_dir, sessdata, quality, download_type)
        
        # 从 JSON 文件中删除已下载的视频
        with open(json_filename, 'r', encoding='utf-8') as f:
            remaining_videos = json.load(f)
        
        remaining_videos = [v for v in remaining_videos if v['link'] != video['link']]
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(remaining_videos, f, ensure_ascii=False, indent=2)
        
        print(f"视频 {video['title']} 下载完成并已从 JSON 文件中删除")

    print("所有视频下载完成")

if __name__ == "__main__":
    main()
