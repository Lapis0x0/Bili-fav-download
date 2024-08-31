import subprocess
import os

def get_video_quality():
    quality_map = {
        "1": "127",  # 8K超高清
        "2": "120",  # 4K超清
        "3": "116",  # 1080P60
        "4": "80",   # 1080P
        "5": "64",   # 720P
        "6": "32",   # 480P
        "7": "16"    # 360P
    }
    while True:
        print("\n请选择视频质量:")
        print("1: 8K超高清")
        print("2: 4K超清")
        print("3: 1080P60")
        print("4: 1080P")
        print("5: 720P")
        print("6: 480P")
        print("7: 360P")
        choice = input("请输入选项编号 (1-7): ")
        if choice in quality_map:
            return quality_map[choice]
        print("无效的选择，请重新输入。")

def get_download_type():
    while True:
        print("\n请选择下载类型:")
        print("1: 下载视频")
        print("2: 仅下载音频")
        choice = input("请输入选项编号 (1-2): ")
        if choice in ["1", "2"]:
            return choice
        print("无效的选择，请重新输入。")

def download_video(url, output_dir, sessdata, quality, download_type):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "yutto",
        url,
        "-d", output_dir,
        "-c", sessdata,
        "--no-danmaku",
        "--no-subtitle",
        "--subpath-template", "{title}"
    ]
    
    if download_type == "1" and quality:
        cmd.extend(["--video-quality", quality])
    elif download_type == "2":
        cmd.append("--audio-only")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"{'音频' if download_type == '2' else '视频'} {url} 下载完成")
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {e}")

# 移除了 download_favorites 函数，因为在 main.py 中我们直接遍历视频列表调用 download_video

# 移除了 is_favorite_url 函数，因为在 main.py 中不再需要它

# 移除了 __main__ 部分，因为这个模块现在主要被 main.py 调用