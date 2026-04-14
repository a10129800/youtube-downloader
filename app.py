from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import time

app = Flask(__name__)

def download_video(url):
    # 建立一個臨時資料夾來存影片
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # 用時間戳記當臨時檔名，避免多人同時下載時衝突
    timestamp = int(time.time())
    output_template = f'downloads/{timestamp}_%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # 取得下載後的實際完整檔案路徑
        file_path = ydl.prepare_filename(info)
        # 修正檔名（有些情況下 ydl 返回的路徑會跟實際存的不完全一樣）
        actual_path = file_path.replace('%(ext)s', info['ext'])
        return actual_path

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
