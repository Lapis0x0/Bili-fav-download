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

    # 询问用户下载类型
    download_choice = input("请选择下载类型 (1: 单个视频, 2: 收藏夹): ")

    # 获取用户选择的下载类型（视频或音频）
    download_type = get_download_type()

    # 获取用户选择的视频质量
    quality = get_video_quality() if download_type == "1" else None

    output_dir = 'downloads'

    if download_choice == "1":
        # 下载单个视频
        video_url = input("请输入视频链接: ")
        download_video(video_url, output_dir, sessdata, quality, download_type)
        print("视频下载完成")
    elif download_choice == "2":
        # 下载收藏夹
        fav_url = input("请输入收藏夹链接: ")
        try:
            media_id = extract_media_id(fav_url)
            fav_videos = get_fav_videos(media_id, sessdata)

            if not fav_videos:
                print("警告: 未找到任何视频。请检查收藏夹链接是否正确,以及是否有权限访问该收藏夹。")
                return

            json_filename = 'fav_videos.json'
            save_videos_to_json(fav_videos, json_filename)
            print(f"视频信息已保存到 {json_filename}")
            
            remove_duplicates()
            print("已完成视频去重操作")

            # 读取去重后的视频列表
            with open(json_filename, 'r', encoding='utf-8') as f:
                videos_to_download = json.load(f)

            if not videos_to_download:
                print("所有视频已下载,无需进行新的下载。")
                return

            # 下载视频
            for video in videos_to_download:
                download_video(video['link'], output_dir, sessdata, quality, download_type)

            print("所有视频下载完成")

        except ValueError as e:
            print(f"错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("无效的选择")

if __name__ == "__main__":
    main()
