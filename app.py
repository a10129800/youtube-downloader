from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import time

app = Flask(__name__)

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    timestamp = int(time.time())
    output_template = f'downloads/{timestamp}_%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'noplaylist': True,
        # --- 以下是強大的偽裝參數 ---
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'addheader': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        ],
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def start_download():
    video_url = request.form.get('url')
    if video_url:
        try:
            # 1. 下載到雲端主機的臨時空間
            file_path = download_video(video_url)
            
            # 2. 將檔案傳送給使用者（瀏覽器會跳出存檔視窗）
            response = send_file(file_path, as_attachment=True)
            
            # 注意：這裡有個小挑戰，下載完後通常要刪除臨時檔，
            # 雲端佈署時我們會再優化這部分。
            return response
            
        except Exception as e:
            return f"❌ 錯誤：{e}"
    return "網址無效！"

if __name__ == '__main__':
    # 讓 Render 自動決定連接埠 (Port)，並允許外部連線 (0.0.0.0)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
